# Claudecraft Primer

The 2009 *Tradecraft Primer*, adapted into an explicitly invoked skill for Claude Code and Codex. A small experiment in using intelligence-analysis techniques to review evidence, compare explanations, and communicate uncertainty.

Based on **US Government, *A Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis*, March 2009**. [Original publication](https://www.cia.gov/resources/csi/books-monographs/a-tradecraft-primer) · [Original PDF](https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf)

## Install

The repository itself is the skill folder. Installation needs Git; using the skill requires no additional packages, API keys, or MCP servers. Choose the client you use, or install into both separate directories.

### Claude Code

```sh
skill_destination="$HOME/.claude/skills/claudecraft-primer"
if [ -e "$skill_destination" ] || [ -L "$skill_destination" ]; then
  echo "Destination already exists; leaving it unchanged."
else
  mkdir -p "$(dirname "$skill_destination")" &&
    git clone https://github.com/btgaskin/claudecraft-primer.git "$skill_destination"
fi
```

Start a fresh Claude Code session and invoke:

```text
/claudecraft-primer Review this claim at light depth: …
```

### Codex

```sh
skill_destination="$HOME/.agents/skills/claudecraft-primer"
if [ -e "$skill_destination" ] || [ -L "$skill_destination" ]; then
  echo "Destination already exists; leaving it unchanged."
else
  mkdir -p "$(dirname "$skill_destination")" &&
    git clone https://github.com/btgaskin/claudecraft-primer.git "$skill_destination"
fi
```

Start a fresh Codex session and invoke:

```text
$claudecraft-primer Compare these explanations at standard depth: …
```

These commands leave existing directories and symlinks unchanged. If you already have a copy, use the update instructions below. Install only one copy per client scope to avoid duplicate names.

These are local skill installations, following [Claude Code's skill documentation](https://code.claude.com/docs/en/skills) and [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills). Claude's frontmatter and Codex's `agents/openai.yaml` each configure explicit-only invocation.

### Install in a project

From an existing clone of this repository, export the committed files into a new project skill directory. Choose `.claude/skills` for Claude Code or `.agents/skills` for Codex:

```sh
# Set this to your project's intended skill directory.
skill_destination="/absolute/path/to/project/.claude/skills/claudecraft-primer"
if [ -e "$skill_destination" ] || [ -L "$skill_destination" ]; then
  echo "Destination already exists; leaving it unchanged."
else
  mkdir -p "$skill_destination" && git archive HEAD | tar -x -C "$skill_destination"
fi
```

This creates a copy without a nested Git repository, suitable for committing with your project. To update a project copy, export a newer revision into a separate directory and review the diff before replacing it. ZIP users can similarly copy the extracted repository contents into a new folder named `claudecraft-primer`, with `SKILL.md` directly inside it.

## Use

- **Light:** “Check the main assumptions in this explanation. Keep it brief.”
- **Standard:** “Compare these accounts, including source dependencies and what would distinguish them.”
- **Deep:** “Assess this proposal using the supplied evidence. Include a source table and test the conclusion against plausible alternatives.”

Specify the intensity or let the skill infer it. Request a concise answer, supporting tables, or a fuller document independently of depth. The default is a clear assessment with decisive evidence, material uncertainty, and what would change the conclusion.

The skill covers all twelve techniques: assumptions and information checks, indicators, competing hypotheses, Devil's Advocacy, Team A/Team B, high-impact/low-probability analysis, What If analysis, brainstorming, outside-in thinking, actor perspectives, and alternative futures.

## How it adapts the primer

The procedures use original summaries with page references. They select methods proportionately, preserve source dependence, and compare explanations without automatic inconsistency scores. Constructed perspectives and hypothetical scenarios are labeled.

Research on ACH has found mixed or absent benefits in particular tasks, including problems with judgment coherence and evidence presentation. Those findings inform this adaptation and are included in [Sources, evidence, and adaptation](references/evidence.md). This skill is an experiment; its analytical effectiveness has not been established by those human studies.

## Update or remove

For a personal Git installation, inspect local changes first, then update with a fast-forward pull. Substitute the Codex path if appropriate:

```sh
git -C "$HOME/.claude/skills/claudecraft-primer" status --short
# Continue only if the checkout is clean; preserve local edits first.
git -C "$HOME/.claude/skills/claudecraft-primer" pull --ff-only
```

To remove the skill, move its `claudecraft-primer` folder out of the client's skills directory, then start a fresh session. This preserves local edits and requires no changes to global client configuration. A project installation can be removed through the project's normal version-control workflow.

## Checks

Run the package checks with Python 3:

```sh
python3 -m unittest discover -s tests -v
```

They exercise portable installation, reference resolution, invocation metadata, preservation of existing destinations, and removal. [Behavioral cases](tests/cases.md) provide small exercises for reviewing the analytical output. These checks assess packaging and specific behaviors, not general accuracy gains.

The common skill metadata also works with the Codex skill-creator validator after excluding the documented Claude-only `disable-model-invocation` field in a temporary validation copy. Keep that field in the distributed skill.

## Attribution and license

An independent adaptation by Ben Gaskin. No affiliation with or endorsement by the US Government, Anthropic, or OpenAI is implied. Original repository contributions are licensed under [MIT](LICENSE). Cited works retain their own status and attribution; this repository links to the primer rather than redistributing its PDF or third-party quotations.
