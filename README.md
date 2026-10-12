<p align="center">
  <img src="docs/clawds.png" width="573" alt="Five Clawds dancing">
</p>

<h1 align="center">Claude Code plugins</h1>

<p align="center">Small plugins for Claude Code by Tigran Macintosh.<br>One marketplace, add it once and install what you need.</p>

## Plugins

<table>
<tr>
<td width="45%"><a href="prompt-boost"><img src="prompt-boost/docs/hero.gif" alt="prompt-boost"></a></td>
<td valign="top">
<h3><a href="prompt-boost">prompt-boost</a></h3>
Improves every prompt automatically. Vague prompts get settled from the code first and only your real decisions are asked, through the question form. End a prompt with <code>??</code> for a full brief from a second model: intent, task, done bar and open questions.
<br><br>
<code>/plugin install prompt-boost@tigran-macintosh</code>
</td>
</tr>
<tr>
<td width="45%"><a href="grill"><img src="grill/docs/hero.gif" alt="grill"></a></td>
<td valign="top">
<h3><a href="grill">grill</a></h3>
Interviews you about a task before building it. Claude reads the code first, then asks one question at a time with a recommended answer, and sums up the plan before writing anything.
<br><br>
<code>/plugin install grill@tigran-macintosh</code>
</td>
</tr>
</table>

## Install

```
/plugin marketplace add Mhitaryan-Tigran/claude-plugins
/plugin install prompt-boost@tigran-macintosh
/plugin install grill@tigran-macintosh
```

Restart Claude Code after installing. To get new versions on their own, open `/plugin`, go to **Marketplaces**, pick `tigran-macintosh` and choose **Enable auto-update**; Claude Code then checks at every start. `/plugin` also lists what is installed and updates it by hand.

<sub>MIT · Tigran Macintosh</sub>
