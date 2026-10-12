<p align="center">
  <img src="../docs/clawds.png" width="460" alt="Five Clawds dancing">
</p>

<h1 align="center">grill</h1>

<p align="center">Claude interviews you about a task before building it.<br>One question at a time, each with ready answers, until the plan is yours too.</p>

<p align="center">
  <img src="docs/hero.gif" width="860" alt="Claude reads the code, then asks one question at a time with a recommended answer, and sums up the plan">
</p>

## How it goes

<table>
<tr>
<td align="center" width="33%"><img src="docs/reading.png" width="110"><br><b>Reads first</b><br><sub>code, git, docs</sub></td>
<td align="center" width="33%"><img src="docs/asking.png" width="110"><br><b>Asks one thing</b><br><sub>with a recommendation</sub></td>
<td align="center" width="33%"><img src="docs/happy.png" width="110"><br><b>Sums up</b><br><sub>then waits for your yes</sub></td>
</tr>
<tr>
<td valign="top">Anything the code, the history or the docs already answer is never asked.</td>
<td valign="top">Each question comes as a form with two to four options and the one Claude would pick first. Every answer shapes the next question.</td>
<td valign="top">A short spec: the goal, every decision and default, what is out of scope, and how done will be checked. No code is written before you agree.</td>
</tr>
</table>

## One question at a time

<p align="center">
  <img src="docs/question.png" width="860" alt="A question about how existing endpoints should behave once login exists, with three options and a recommendation">
</p>

## The plan you agree on

<p align="center">
  <img src="docs/summary.png" width="860" alt="The summary with decisions, defaults taken, out of scope and done-when checks">
</p>

## When to use it

Run `/grill` with the task, for example `/grill add login to the api`, or just say "grill me" before a large or vague piece of work. It pairs with [prompt-boost](../prompt-boost), which improves every prompt automatically; grill is the deep, deliberate version for the tasks worth a real conversation first.

## Install

```
/plugin marketplace add Mhitaryan-Tigran/claude-plugins
/plugin install grill@tigran-macintosh
```

Restart Claude Code and run `/grill`. For updates on their own, open `/plugin` → **Marketplaces** → `tigran-macintosh` → **Enable auto-update**.

<sub>MIT · Tigran Macintosh</sub>
