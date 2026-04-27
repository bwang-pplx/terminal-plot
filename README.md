# terminal-plot

A [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills) that renders simple charts inline in the terminal as **native unicode text** — no images, no GUIs, survives logs and transcripts.

When you ask Claude to visualize numeric data, it picks one of six chart types and shells out to a tiny Python CLI. Output is ANSI-free by default; pass `--color` to opt in.

## What it looks like

### Bar (`bar`)

```
# GitHub stars (k)

Python: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 62.00
Rust  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 48.00
Go    : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 35.00
TS    : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 51.00
Zig   : ▇▇▇▇ 12.00
```

### Horizontal bar / pie substitute (`hbar`)

```
─────────────────────────────── Cost split (%) ───────────────────────────────
Compute ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 55.00
Storage ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 25.00
Network ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 15.00
Other   ▇▇▇▇▇▇ 5.00
```

### Line (`line`)

```
Hourly temperature (C)
   38.00  ┤           ╭─╮
   35.64  ┤         ╭─╯ ╰╮
   33.27  ┤       ╭─╯    ╰╮
   30.91  ┤      ╭╯       ╰╮
   28.55  ┤      │         ╰╮
   26.18  ┤     ╭╯          ╰╮
   23.82  ┤     │            │
   21.45  ┤    ╭╯            ╰╮
   19.09  ┤   ╭╯              ╰─╮
   16.73  ┤  ╭╯                 ╰╮
   14.36  ┼──╯                   ╰
   12.00  ┤
```

### Multi-line (`multiline`)

```
rising vs falling
   10.00  ┤
    9.18  ┤╮       ╭
    8.36  ┤╰╮     ╭╯
    7.55  ┤ ╰╮   ╭╯
    6.73  ┤  ╰╮ ╭╯
    5.91  ┤   ╰╮╯
    5.09  ┤   ╭╰╮
    4.27  ┤   │ │
    3.45  ┤  ╭╯ ╰╮
    2.64  ┤ ╭╯   ╰╮
    1.82  ┤╭╯     ╰╮
    1.00  ┼╯       ╰
```

### Sparkline (`sparkline`)

```
weekly trend: ▁▂▄▇▄▂▁▁▃▅█▆▄▂
```

### Histogram (`hist`)

```
# value distribution

1.0-2.0: ▇▇▇▇▇▇▇▇▇▇▇▇ 1.00
2.0-3.0: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 2.00
3.0-4.0: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 3.00
4.0-5.0: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 4.00
5.0-6.0: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 5.00
6.0-7.0: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 4.00
7.0-8.0: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 3.00
8.0-9.0: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 3.00
```

## Install

Requires [`uv`](https://docs.astral.sh/uv/) (used to run the script with isolated dependencies via PEP 723).

```bash
git clone https://github.com/bwang-pplx/terminal-plot.git ~/.claude/skills/terminal-plot
```

That's it. Restart Claude Code (or start a new session) and the skill is auto-discovered. First run takes ~2 seconds while `uv` resolves and caches `termgraph` / `asciichartpy` / `plotext`; subsequent runs are instant.

## Usage from Claude

Just ask for a chart in natural language:

> *Plot a bar chart of these benchmark results: A=120ms, B=85ms, C=210ms*

> *Show a sparkline for the weekly request counts: 120, 145, 180, 220, 195, 160, 175*

> *Visualize the cost split: compute 55%, storage 25%, network 15%, other 5%*

Claude will pick the right subcommand and call it.

## Direct CLI usage

```bash
~/.claude/skills/terminal-plot/plot.py bar       --labels "A,B,C" --values "1,2,3" --title "demo"
~/.claude/skills/terminal-plot/plot.py hbar      --labels "A,B,C" --values "1,2,3"
~/.claude/skills/terminal-plot/plot.py line      --values "1,2,3,5,4,7"
~/.claude/skills/terminal-plot/plot.py multiline --series "[[1,2,3],[3,2,1]]"
~/.claude/skills/terminal-plot/plot.py sparkline --values "1,3,5,8,5,3,1,9"
~/.claude/skills/terminal-plot/plot.py hist      --values "1,2,2,3,3,3,4,4,4,4,5"
```

Add `--color` to `bar`, `hbar`, or `hist` for ANSI color in real terminals.

## Why no pie chart?

True pie charts render badly in terminals because cells aren't square (typically ~2:1 height:width), so circles come out as squashed eggs. The `hbar` subcommand is the standard terminal substitute for "share of total" data and is what users actually want once they see it.

## Credits

Built on:
- [`termgraph`](https://github.com/mkaz/termgraph) — bar charts and histograms
- [`asciichartpy`](https://github.com/kroitor/asciichart) — line charts
- [`plotext`](https://github.com/piccolomo/plotext) — horizontal bars

## License

MIT — see [LICENSE](./LICENSE).
