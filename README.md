# terminal-plot

A [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills) that renders simple charts inline in the terminal as **native unicode text** — no images, no GUIs, survives logs and transcripts.

When you ask Claude to visualize numeric data, it picks one of twelve chart types and shells out to a tiny Python CLI. Output is ANSI-free by default; pass `--color` to opt in.

## What it looks like

### Bar (`bar` / `hbar`)

```
────────────────────────────── GitHub stars (k) ──────────────────────────────
Python ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 62.00
Rust   ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 48.00
Go     ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 35.00
TS     ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 51.00
Zig    ▇▇▇▇▇▇▇▇▇▇▇▇▇ 12.00
```

For "share of total":

```
─────────────────────────────── Cost split (%) ───────────────────────────────
Compute ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 55.00
Storage ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 25.00
Network ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 15.00
Other   ▇▇▇▇▇▇ 5.00
```

(`bar` and `hbar` are the same renderer — both names are kept for natural-language flexibility.)

### Stacked bar (`stacked`)

```
────────────────────────── Revenue by quarter ($M) ───────────────────────────
Q1 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 23.00
Q2 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 28.00
Q3 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 34.00
Q4 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 42.00
─────────────────────────── ▇▇▇ US ▇▇▇ EU ▇▇▇ APAC ───────────────────────────
```

Pass `--color` for distinct ANSI colors per series — without it, segments share the same glyph and only stacked totals are visually meaningful.

### Grouped bar (`grouped`)

```
────────────────────────────── YoY revenue ($M) ──────────────────────────────
Q1 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 10.00
   ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 12.00

Q2 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 12.00
   ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 14.00

Q3 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 15.00
   ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 17.00

Q4 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 18.00
   ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 20.00
───────────────────────────── ▇▇▇ 2024 ▇▇▇ 2025 ──────────────────────────────
```

### Gauge (`gauge`)

```
Disk usage [████████████████████░░░░░░░░░░] 67.0%
```

### Calendar heatmap (`calendar`)

```
commits over 20 weeks
▂▂▁ ▄▄▃▁▄▁▄▁▁▄▇▆▁▂▇
▂▂▁▂ ▄▄▂▆▅▇▃▃▃▂▄▃▃▃▅
▂▃▃▄▄ ▄▄▄ ▄▄▅▁▆▄▆ ▅▄
▄▃▅▄ ▄▃▂▄▃▁▁▃▄▃  ▃ ▆
▂▅▃▂ ▁▄█▆▃▁▂▃▃▂▄▂ ▂▄
 ▁▁▁ ▁▁ ▁   ▁▂ ▁▂▁▁▁
▁▁▁▁ ▁   ▁▂ ▂▁▁  ▁▂
```

Rows are days (default 7 = days of week), columns are weeks; values map to a 9-step block ramp.

### Box plot (`box`)

```
score distributions
    ┌────────────────────────────────────────────────────────────────────────┐
10.0┤                                    │                                   │
    │          │                         │                                   │
 8.5┤          │                         │                                   │
    │          │                         │                        │          │
 7.0┤█████████████████████    ██████████████████████              │          │
    │█████████████████████    ██████████████████████              │          │
 5.5┤█████████████████████    ──────────────────────    █████████████████████│
    │─────────────────────    ██████████████████████    ─────────────────────│
    │█████████████████████               │              █████████████████████│
 4.0┤█████████████████████               │              █████████████████████│
    │█████████████████████               │              █████████████████████│
 2.5┤          │                                                  │          │
    │          │                                                  │          │
 1.0┤          │                                                             │
    └──────────┬─────────────────────────┬────────────────────────┬──────────┘
               A                         B                        C
```

Like `scatter`, `box` uses **canvas mode** (boxed) since each group's distribution needs its own y-axis range.

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

### Scatter (`scatter`)

```
scatter test
    ┌──────────────────────────────────────────────────────┐
13.0┤                                                ⢀    ⠈│
11.2┤                                            ⠂         │
    │                                       ⠄              │
 9.4┤                                  ⠄                   │
 7.6┤                             ⠂                        │
    │                        ⠐                             │
 5.7┤                   ⠠                                  │
 3.9┤         ⢀    ⠐                                       │
    │     ⠄                                                │
 2.1┤⡀                                                     │
    └┬────────────┬─────────────┬────────────┬────────────┬┘
    1.0          3.8           6.5          9.2        12.0
```

Note: scatter is the one chart type that needs **canvas mode** (since x and y are both coordinates), so it has a `┌─┐` box around it. Braille markers give ~4× density vs block chars.

### Sparkline (`sparkline`)

```
weekly trend: ▁▂▄▇▄▂▁▁▃▅█▆▄▂
```

### Histogram (`hist`)

```
───────────────────────────── value distribution ─────────────────────────────
1.0-2.0 ▇▇▇▇▇▇▇▇▇▇▇▇▇ 1.00
2.0-3.0 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 2.00
3.0-4.0 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 3.00
4.0-5.0 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 4.00
5.0-6.0 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 5.00
6.0-7.0 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 4.00
7.0-8.0 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 3.00
8.0-9.0 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 3.00
```

## Install

Requires [`uv`](https://docs.astral.sh/uv/) (used to run the script with isolated dependencies via PEP 723).

```bash
git clone https://github.com/bwang-pplx/terminal-plot.git ~/.claude/skills/terminal-plot
```

That's it. Restart Claude Code (or start a new session) and the skill is auto-discovered. First run takes ~2 seconds while `uv` resolves and caches `asciichartpy` / `plotext`; subsequent runs are instant.

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
~/.claude/skills/terminal-plot/plot.py stacked   --labels "Q1,Q2" --series "[[10,12],[8,9]]" --names "US,EU"
~/.claude/skills/terminal-plot/plot.py grouped   --labels "Q1,Q2" --series "[[10,12],[12,14]]" --names "2024,2025"
~/.claude/skills/terminal-plot/plot.py line      --values "1,2,3,5,4,7"
~/.claude/skills/terminal-plot/plot.py multiline --series "[[1,2,3],[3,2,1]]"
~/.claude/skills/terminal-plot/plot.py scatter   --x "1,2,3,4,5" --y "2,4,3,6,5"
~/.claude/skills/terminal-plot/plot.py sparkline --values "1,3,5,8,5,3,1,9"
~/.claude/skills/terminal-plot/plot.py gauge     --value 67 --label "Disk usage"
~/.claude/skills/terminal-plot/plot.py calendar  --values "1,2,0,5,3,1,0,4,2,1,0,3,5,2"
~/.claude/skills/terminal-plot/plot.py hist      --values "1,2,2,3,3,3,4,4,4,4,5"
~/.claude/skills/terminal-plot/plot.py box       --labels "A,B,C" --datasets "[[1,2,3,4,5],[3,4,5,6,7],[2,3,4,5,6]]"
```

Add `--color` to `bar`, `hbar`, `stacked`, `grouped`, `hist`, `scatter`, or `box` for ANSI color in real terminals.

## Credits

Built on:
- [`plotext`](https://github.com/piccolomo/plotext) — `simple_bar` for bar / hbar / hist
- [`asciichartpy`](https://github.com/kroitor/asciichart) — line and multi-line charts

## License

MIT — see [LICENSE](./LICENSE).
