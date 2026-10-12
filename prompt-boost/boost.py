#!/usr/bin/env python3
import json, os, re, subprocess, sys, time
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
HOME = Path.home() / '.claude'

DEFAULTS = {
    'model': 'sonnet',
    'deep_marker': '??',
    'bypass_prefix': ',',
    'replies': ['yes', 'no', 'ok', 'go', 'do it', 'continue', 'stop',
                'да', 'нет', 'ок', 'окей', 'ага', 'давай', 'делай', 'го', 'продолжай', 'стоп'],
    'language': 'English',
    'light': True,
    'show_brief': True,
    'timeout': 25,
    'profile': '',
    'memory_index': '',
    'context_command': '',
    'log': str(HOME / 'brief' / 'log.jsonl'),
}
TURNS = 6
CAP = 6000

SCHEMA = {
    'type': 'object',
    'properties': {
        'intent': {'type': 'string'},
        'task': {'type': 'string'},
        'done': {'type': 'string'},
        'nodes': {'type': 'array', 'items': {'type': 'string'}},
        'gaps': {'type': 'array', 'items': {
            'type': 'object',
            'properties': {
                'question': {'type': 'string'},
                'options': {'type': 'array', 'items': {'type': 'string'}, 'minItems': 2, 'maxItems': 4},
                'why': {'type': 'string'},
            },
            'required': ['question', 'options', 'why'],
        }},
        'risk': {'type': 'string', 'enum': ['none', 'outward']},
        'plan_needed': {'type': 'boolean'},
    },
    'required': ['intent', 'task', 'done', 'nodes', 'gaps', 'risk', 'plan_needed'],
}

FOR_CLAUDE = (
    'A separate model read the prompt first and produced the brief below. Read the listed memory notes before acting. '
    'Treat the gaps as candidates: settle every one you can from the conversation, memory, the code, git or a quick lookup, '
    'then ask only what is still genuinely open in one AskUserQuestion call with concrete options before doing the work. '
    'If plan_needed is true, agree a plan before long work. Outward actions need an explicit yes. '
    'Where the brief contradicts the literal prompt, the prompt wins.'
)

LIGHT = (
    'Before acting on this prompt, check it is clear enough to do well. If it is, proceed without comment. '
    'If it is vague, first resolve what you can from the conversation, memory, the code, git or a quick lookup; '
    'then ask only the decisions that are genuinely the user\'s in one AskUserQuestion call with concrete options. '
    'Know what done means before starting: built, verified by running it, reported. Long or multi-step work needs an agreed plan first.'
)

LABELS = {
    'English': ('Brief', 'Task', 'Done when', 'Read', 'Ask', 'Flags', 'plan first', 'outward action, needs your yes'),
    'Russian': ('Бриф', 'Задача', 'Готово, когда', 'Память', 'Вопрос', 'Флаги', 'нужен план', 'действие наружу, нужно твоё да'),
}


def load_config(cwd):
    cfg = dict(DEFAULTS)
    for path in (HOME / 'brief.json', Path(cwd or '.') / '.claude' / 'brief.json'):
        try:
            cfg.update(json.loads(path.read_text()))
        except Exception:
            pass
    for key in ('memory_index', 'log'):
        if cfg[key]:
            p = Path(os.path.expanduser(cfg[key]))
            cfg[key] = str(p if p.is_absolute() else Path(cwd or '.') / p)
    return cfg


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return ' '.join(b.get('text', '') for b in content if isinstance(b, dict) and b.get('type') == 'text')
    return ''


def turns(path, n=TURNS):
    out = []
    try:
        lines = Path(path).read_text().splitlines()
    except Exception:
        return out
    for line in reversed(lines):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get('type') not in ('user', 'assistant') or d.get('isMeta'):
            continue
        msg = d.get('message') or {}
        t = text_of(msg.get('content')).strip()
        if not t or t.startswith('<'):
            continue
        out.append((msg.get('role', d['type']), t))
        if len(out) >= n:
            break
    return list(reversed(out))


def last_assistant(history):
    for role, t in reversed(history):
        if role == 'assistant':
            return t
    return ''


def skip_reason(prompt, history, cfg):
    p = prompt.strip()
    if not p:
        return 'empty'
    if cfg['bypass_prefix'] and p.startswith(cfg['bypass_prefix']):
        return 'bypass'
    if is_deep(p, cfg):
        return None
    if p.startswith('/'):
        return 'command'
    if re.fullmatch(r'(\[Image[^\]]*\]\s*)+', p):
        return 'image'
    words = re.findall(r'\w+', p.lower())
    replies = {r.lower() for r in cfg['replies']}
    if len(words) <= 3 and (' '.join(words) in replies or set(words) & replies or '?' in last_assistant(history)[-400:]):
        return 'reply'
    return None


def is_deep(prompt, cfg):
    m = cfg['deep_marker']
    p = prompt.strip()
    return bool(m) and (p.endswith(m) or p.startswith(m))


def strip_marker(prompt, cfg):
    p, m = prompt.strip(), cfg['deep_marker']
    return (p[len(m):] if p.startswith(m) else p[:-len(m)] if p.endswith(m) else p).strip()


def read(path):
    try:
        return Path(path).read_text() if path else ''
    except Exception:
        return ''


def known_nodes(index_text):
    return set(re.findall(r'\]\(([\w./-]+?)\.md\)', index_text))


def run(command):
    if not command:
        return ''
    try:
        return subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        return ''


def context(prompt, history, cwd, cfg):
    convo = '\n\n'.join(f'{r.upper()}: {t}' for r, t in history if t != prompt)[-CAP:]
    parts = [('conversation', convo), ('memory_index', read(cfg['memory_index'])),
             ('extra_context', run(cfg['context_command'])), ('cwd', cwd), ('message', prompt)]
    return '\n\n'.join(f'<{k}>\n{v}\n</{k}>' for k, v in parts if v)


def system_prompt(cfg):
    profile = cfg['profile']
    if profile and Path(os.path.expanduser(profile)).is_file():
        profile = read(os.path.expanduser(profile))
    return (read(HERE / 'prompt.md')
            .replace('{language}', cfg['language'])
            .replace('{profile}', profile.strip() or 'No profile given.'))


def ask_model(payload, cfg):
    env = dict(os.environ, CLAUDE_BRIEF_CHILD='1')
    env.pop('CLAUDECODE', None)
    r = subprocess.run(
        ['claude', '-p', '--model', cfg['model'], '--setting-sources', '', '--strict-mcp-config', '--tools', '',
         '--no-session-persistence', '--output-format', 'json', '--json-schema', json.dumps(SCHEMA),
         '--system-prompt', system_prompt(cfg)],
        input=payload, capture_output=True, text=True, timeout=cfg['timeout'], cwd='/tmp', env=env)
    d = json.loads(r.stdout)
    if d.get('is_error') or not isinstance(d.get('structured_output'), dict):
        raise RuntimeError(str(d.get('result'))[:200])
    return d['structured_output']


def clean(brief, known):
    brief['nodes'] = [n for n in brief.get('nodes', []) if n in known]
    brief['gaps'] = [g for g in brief.get('gaps', []) if g.get('question') and 2 <= len(g.get('options', [])) <= 4][:4]
    return brief


def for_user(b, language):
    L = LABELS.get(language, LABELS['English'])
    lines = [f'{L[0]} · {b["intent"]}', f'{L[1]}: {b["task"]}', f'{L[2]}: {b["done"]}']
    if b['nodes']:
        lines.append(f'{L[3]}: ' + ', '.join(b['nodes']))
    for g in b['gaps']:
        lines.append(f'{L[4]}: {g["question"]} [{" / ".join(g["options"])}]')
    flags = [f for f, on in ((L[6], b['plan_needed']), (L[7], b['risk'] == 'outward')) if on]
    if flags:
        lines.append(f'{L[5]}: ' + ', '.join(flags))
    return '\n'.join(lines)


def output(b, cfg):
    out = {'hookSpecificOutput': {
        'hookEventName': 'UserPromptSubmit',
        'additionalContext': FOR_CLAUDE + '\n<brief>\n' + json.dumps(b, ensure_ascii=False, indent=1) + '\n</brief>',
    }}
    if cfg['show_brief']:
        out['systemMessage'] = for_user(b, cfg['language'])
    return out


def light():
    return {'hookSpecificOutput': {'hookEventName': 'UserPromptSubmit', 'additionalContext': LIGHT}}


def log(cfg, entry):
    if not cfg['log']:
        return
    try:
        Path(cfg['log']).parent.mkdir(parents=True, exist_ok=True)
        with open(cfg['log'], 'a') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    except Exception:
        pass


def main():
    if os.environ.get('CLAUDE_BRIEF_CHILD'):
        return
    start = time.time()
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    cwd = data.get('cwd', '')
    cfg = load_config(cwd)
    prompt = data.get('prompt', '')
    history = turns(data.get('transcript_path', ''))
    reason = skip_reason(prompt, history, cfg)
    entry = {'time': time.strftime('%Y-%m-%d %H:%M:%S'), 'cwd': cwd, 'prompt': prompt}
    if reason:
        log(cfg, {**entry, 'skipped': reason})
        return
    if not is_deep(prompt, cfg):
        if cfg['light']:
            log(cfg, {**entry, 'light': True})
            print(json.dumps(light(), ensure_ascii=False))
        return
    prompt = strip_marker(prompt, cfg)
    try:
        brief = clean(ask_model(context(prompt, history, cwd, cfg), cfg), known_nodes(read(cfg['memory_index'])))
    except Exception as e:
        log(cfg, {**entry, 'error': f'{type(e).__name__}: {e}'[:300], 'ms': int((time.time() - start) * 1000)})
        return
    log(cfg, {**entry, 'brief': brief, 'ms': int((time.time() - start) * 1000)})
    print(json.dumps(output(brief, cfg), ensure_ascii=False))


if __name__ == '__main__':
    main()
