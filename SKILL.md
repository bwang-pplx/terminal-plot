---
name: terminal-plot
description: Render charts (bar, horizontal bar, stacked bar, grouped bar, line, multi-line, scatter, sparkline, gauge, calendar heatmap, histogram, box plot) inline in the terminal as native unicode text. Use when the user wants to visualize numeric data without leaving the CLI, or when you need to summarize tabular data with a quick chart in chat.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/plot.py *)
---

## terminal-plot

A CLI that draws charts as native terminal text — no images, no GUI. Output is ANSI-free by default so it survives logs, transcripts, and pipes. Pass `--color` on supported subcommands to opt into ANSI color.

Backed by [`plotext`](https://github.com/piccolomo/plotext) (`simple_bar` for bar/hbar/hist) and [`asciichartpy`](https://github.com/kroitor/asciichart) (line/multiline). Runs via `uv run --script` with PEP 723 inline metadata, so no venv setup is required other than having `uv` installed.

### When to use

- The user pastes or generates numeric data and wants a quick visualization.
- You want to summarize a tabular result (e.g. benchmark output, log aggregation, file sizes) with a chart.
- The user asks for a "pie chart" — render `hbar` instead and note that true pies render poorly in terminal.

### Subcommands

```bash
${CLAUDE_SKILL_DIR}/plot.py bar       --labels "A,B,C" --values "1,2,3"               [--title "..."] [--width N] [--color]
${CLAUDE_SKILL_DIR}/plot.py hbar      --labels "A,B,C" --values "1,2,3"               [--title "..."] [--width N] [--color]
${CLAUDE_SKILL_DIR}/plot.py stacked   --labels "A,B,C" --series "[[1,2,3],[4,5,6]]"   [--names "s1,s2"] [--title "..."] [--width N] [--color]
${CLAUDE_SKILL_DIR}/plot.py grouped   --labels "A,B,C" --series "[[1,2,3],[4,5,6]]"   [--names "s1,s2"] [--title "..."] [--width N] [--color]
${CLAUDE_SKILL_DIR}/plot.py line      --values "1,2,3,..."                            [--title "..."] [--height N]
${CLAUDE_SKILL_DIR}/plot.py multiline --series "[[1,2,3],[4,5,6]]"                    [--title "..."] [--height N]
${CLAUDE_SKILL_DIR}/plot.py scatter   --x "1,2,3" --y "4,5,6"                         [--title "..."] [--xlabel ...] [--ylabel ...] [--width N] [--height N] [--color]
${CLAUDE_SKILL_DIR}/plot.py sparkline --values "1,2,3,..."                            [--title "..."]
${CLAUDE_SKILL_DIR}/plot.py gauge     --value 67 [--max 100]                          [--label "..."] [--width N]
${CLAUDE_SKILL_DIR}/plot.py calendar  --values "1,2,0,5,..."                          [--rows 7] [--title "..."]
${CLAUDE_SKILL_DIR}/plot.py hist      --values "1,2,3,..." [--bins N]                 [--title "..."] [--width N] [--color]
${CLAUDE_SKILL_DIR}/plot.py box       --labels "A,B,C" --datasets "[[1,2,3],[4,5,6]]" [--title "..."] [--width N] [--height N] [--color]
```

### Choosing the right chart

| Want                                            | Use         |
|-------------------------------------------------|-------------|
| Compare a few categories                        | `bar`       |
| Show share-of-total (pie substitute)            | `hbar`      |
| Compare composition across categories           | `stacked`   |
| Compare two series side-by-side per category    | `grouped`   |
| Show a single trend over time                   | `line`      |
| Compare two or more trends                      | `multiline` |
| Show 2D point cloud / correlation               | `scatter`   |
| Inline one-line trend in a sentence             | `sparkline` |
| Single value vs. a max (progress / utilization) | `gauge`     |
| Activity over days (GitHub-style heatmap)       | `calendar`  |
| Show distribution of many values                | `hist`      |
| Compare distributions across groups             | `box`       |

### Tips

- **Width**: the script auto-fits to `$COLUMNS`. Override with `--width` only if you have a reason.
- **Color**: omitted by default. Add `--color` only when you know the output is going to a real terminal (not a transcript, log, or piped consumer).
- **Pies**: do not attempt. `hbar` is the standard terminal substitute and is what users actually want.
- **Numeric input**: comma-separated list of floats. For `multiline`, pass a JSON array of arrays.
