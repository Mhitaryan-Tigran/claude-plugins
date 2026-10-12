import importlib.machinery, importlib.util, json, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
loader = importlib.machinery.SourceFileLoader('brief', str(HERE / 'brief.py'))
spec = importlib.util.spec_from_loader('brief', loader)
brief = importlib.util.module_from_spec(spec)
loader.exec_module(brief)

cfg = dict(brief.DEFAULTS)
asked = [('user', 'обнови skywall'), ('assistant', 'Делаю так?')]
told = [('user', 'обнови skywall'), ('assistant', 'Готово, релиз вышел.')]

assert brief.skip_reason('давай', told, cfg) == 'reply'
assert brief.skip_reason('выруби', asked, cfg) == 'reply'
assert brief.skip_reason('обнови skywall', told, cfg) is None
assert brief.skip_reason(', просто привет', told, cfg) == 'bypass'
assert brief.skip_reason('/plan', told, cfg) == 'command'
assert brief.skip_reason('[Image #3] [Image #4]', told, cfg) == 'image'
assert brief.skip_reason('?? обнови skywall', asked, cfg) is None
assert brief.skip_reason('сделай сайт для кофейни с меню и формой брони', asked, cfg) is None

lines = [
    {'type': 'user', 'message': {'role': 'user', 'content': 'первый'}},
    {'type': 'user', 'isMeta': True, 'message': {'role': 'user', 'content': 'meta'}},
    {'type': 'assistant', 'message': {'role': 'assistant', 'content': [{'type': 'thinking', 'thinking': 'x'}, {'type': 'text', 'text': 'ответ'}]}},
    {'type': 'user', 'message': {'role': 'user', 'content': [{'type': 'tool_result', 'content': 'r'}]}},
    {'type': 'user', 'message': {'role': 'user', 'content': '<command-name>/x</command-name>'}},
    {'type': 'attachment'},
]
with tempfile.NamedTemporaryFile('w', suffix='.jsonl', delete=False) as f:
    f.write('\n'.join(json.dumps(l) for l in lines) + '\nnot json\n')
assert brief.turns(f.name) == [('user', 'первый'), ('assistant', 'ответ')]
assert brief.turns('/nonexistent') == []

b = brief.clean({'intent': 'i', 'task': 't', 'done': 'd', 'nodes': ['skywall', 'ghost'],
                 'gaps': [{'question': 'q', 'options': ['a', 'b'], 'why': 'w'}, {'question': 'bad', 'options': ['only'], 'why': 'w'}],
                 'risk': 'outward', 'plan_needed': True}, brief.known_nodes('- [S](skywall.md)\n- [T](tigran.md)'))
assert b['nodes'] == ['skywall'] and len(b['gaps']) == 1
out = brief.output(b, {**cfg, 'language': 'Russian'})
assert out['hookSpecificOutput']['hookEventName'] == 'UserPromptSubmit'
assert 'AskUserQuestion' in out['hookSpecificOutput']['additionalContext']
assert 'Вопрос: q [a / b]' in out['systemMessage'] and 'нужен план' in out['systemMessage']
assert 'systemMessage' not in brief.output(b, {**cfg, 'show_brief': False})
assert brief.skip_reason('давай', told, {**cfg, 'replies': []}) is None
assert '{profile}' not in brief.system_prompt({**cfg, 'profile': 'dev'}) and 'dev' in brief.system_prompt({**cfg, 'profile': 'dev'})
with tempfile.TemporaryDirectory() as d:
    Path(d, '.claude').mkdir()
    Path(d, '.claude', 'brief.json').write_text('{"model": "haiku", "memory_index": "memory/MEMORY.md"}')
    c = brief.load_config(d)
    assert c['model'] == 'haiku' and c['memory_index'] == str(Path(d, 'memory', 'MEMORY.md'))
assert 'AskUserQuestion' in brief.light()['hookSpecificOutput']['additionalContext']
assert 'candidates' in brief.FOR_CLAUDE
print('ok')
