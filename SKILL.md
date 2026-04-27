---
name: terminal-plot
description: Render simple charts (bar, horizontal bar, line, multi-line, sparkline, histogram) inline in the terminal as native unicode text. Use when the user wants to visualize numeric data without leaving the CLI, or when you need to summarize tabular data with a quick chart in chat.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/plot.py *)
---

## terminal-plot

A CLI that draws charts as native terminal text — no images, no GUI. Output is ANSI-free by default so it survives logs, transcripts, and pipes. Pass `--color` on supported subcommands to opt into ANSI color.

Backed by [`termgraph`](https://github.com/mkaz/termgraph) (bar/hist), [`asciichartpy`](https://github.com/kroitor/asciichart) (line), and [`plotext`](https://github.com/piccolomo/plotext) (horizontal bar). Runs via `uv run --script` with PEP 723 inline metadata, so no venv setup is required other than having `uv` installed.

### When to use

- The user pastes or generates numeric data and wants a quick visualization.
- You want to summarize a tabular result (e.g. benchmark output, log aggregation, file sizes) with a chart.
- The user asks for a "pie chart" — render `hbar` instead and note that true pies render poorly in terminal.

### Subcommands

```bash
${CLAUDE_SKILL_DIR}/plot.py bar       --labels "A,B,C" --values "1,2,3" [--title "..."] [--width N] [--color]
${CLAUDE_SKILL_DIR}/plot.py hbar      --labels "A,B,C" --values "1,2,3" [--title "..."] [--width N] [--color]
${CLAUDE_SKILL_DIR}/plot.py line      --values "1,2,3,..."              [--title "..."] [--height N]
${CLAUDE_SKILL_DIR}/plot.py multiline --series "[[1,2,3],[4,5,6]]"      [--title "..."] [--height N]
${CLAUDE_SKILL_DIR}/plot.py sparkline --values "1,2,3,..."              [--title "..."]
${CLAUDE_SKILL_DIR}/plot.py hist      --values "1,2,3,..." [--bins N]   [--title "..."] [--width N] [--color]
```

### Choosing the right chart

| Want                                  | Use         |
|---------------------------------------|-------------|
| Compare a few categories              | `bar`       |
| Show share-of-total (pie substitute)  | `hbar`      |
| Show a single trend over time         | `line`      |
| Compare two or more trends            | `multiline` |
| Inline one-line trend in a sentence   | `sparkline` |
| Show distribution of many values      | `hist`      |

### Tips

- **Width**: the script auto-fits to `$COLUMNS`. Override with `--width` only if you have a reason.
- **Color**: omitted by default. Add `--color` only when you know the output is going to a real terminal (not a transcript, log, or piped consumer).
- **Pies**: do not attempt. `hbar` is the standard terminal substitute and is what users actually want.
- **Numeric input**: comma-separated list of floats. For `multiline`, pass a JSON array of arrays.
