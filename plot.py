#!/usr/bin/env -S -u UV_EXCLUDE_NEWER uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "asciichartpy>=1.5.25",
#     "plotext>=5.3.2",
# ]
# ///
"""terminal-plot: render bar / line / sparkline / histogram charts in the terminal.

Defaults to ANSI-free output so it survives logs, transcripts, and pipes.
Pass --color on subcommands that support it to opt into color.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import shutil
import sys

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


@contextlib.contextmanager
def _strip_ansi_stdout(strip: bool):
    if not strip:
        yield
        return
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        yield
    sys.stdout.write(_ANSI_RE.sub("", buf.getvalue()))


def _term_cols(default: int = 80) -> int:
    return shutil.get_terminal_size((default, 20)).columns


def _parse_floats(s: str) -> list[float]:
    return [float(x.strip()) for x in s.split(",") if x.strip()]


def _parse_strs(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def _draw_simple_bar(labels: list[str], values: list[float], title: str,
                     width: int | None, color: bool) -> None:
    import plotext as plt

    width = width or _term_cols() - 2
    plt.simple_bar(labels, values, width=width, title=title or "")
    with _strip_ansi_stdout(strip=not color):
        plt.show()
    plt.clear_figure()


def cmd_bar(args: argparse.Namespace) -> None:
    labels = _parse_strs(args.labels)
    values = _parse_floats(args.values)
    if len(labels) != len(values):
        sys.exit(f"labels ({len(labels)}) and values ({len(values)}) length mismatch")
    _draw_simple_bar(labels, values, args.title, args.width, args.color)


def cmd_hbar(args: argparse.Namespace) -> None:
    cmd_bar(args)


def _parse_series(s: str) -> list[list[float]]:
    series = json.loads(s)
    if not isinstance(series, list) or not all(isinstance(x, list) for x in series):
        sys.exit("expected JSON array of arrays, e.g. [[1,2,3],[4,5,6]]")
    return [[float(v) for v in row] for row in series]


def cmd_stacked(args: argparse.Namespace) -> None:
    import plotext as plt

    labels = _parse_strs(args.labels)
    series = _parse_series(args.series)
    names = _parse_strs(args.names) if args.names else None

    width = args.width or _term_cols() - 2
    kwargs: dict = {"width": width, "title": args.title or ""}
    if names:
        kwargs["labels"] = names
    plt.simple_stacked_bar(labels, series, **kwargs)
    with _strip_ansi_stdout(strip=not args.color):
        plt.show()
    plt.clear_figure()


def cmd_grouped(args: argparse.Namespace) -> None:
    import plotext as plt

    labels = _parse_strs(args.labels)
    series = _parse_series(args.series)
    names = _parse_strs(args.names) if args.names else None

    width = args.width or _term_cols() - 2
    kwargs: dict = {"width": width, "title": args.title or ""}
    if names:
        kwargs["labels"] = names
    plt.simple_multiple_bar(labels, series, **kwargs)
    with _strip_ansi_stdout(strip=not args.color):
        plt.show()
    plt.clear_figure()


def cmd_gauge(args: argparse.Namespace) -> None:
    pct = max(0.0, min(1.0, args.value / args.max))
    width = args.width
    filled = int(round(pct * width))
    bar = "█" * filled + "░" * (width - filled)
    pct_str = f"{pct * 100:.1f}%"
    if args.label:
        print(f"{args.label} [{bar}] {pct_str}")
    else:
        print(f"[{bar}] {pct_str}")


def cmd_box(args: argparse.Namespace) -> None:
    import plotext as plt

    labels = _parse_strs(args.labels)
    datasets = _parse_series(args.datasets)
    if len(labels) != len(datasets):
        sys.exit(f"labels ({len(labels)}) and datasets ({len(datasets)}) length mismatch")

    plt.theme("clear")
    plt.box(labels, datasets)
    if args.title:
        plt.title(args.title)
    plt.plotsize(args.width or _term_cols() - 2, args.height)
    with _strip_ansi_stdout(strip=not args.color):
        plt.show()
    plt.clear_figure()


def cmd_line(args: argparse.Namespace) -> None:
    import asciichartpy

    values = _parse_floats(args.values)
    if args.title:
        print(args.title)
    print(asciichartpy.plot(values, {"height": args.height}))


def cmd_multiline(args: argparse.Namespace) -> None:
    import asciichartpy

    series = json.loads(args.series)
    if not isinstance(series, list) or not all(isinstance(s, list) for s in series):
        sys.exit("--series must be a JSON array of arrays, e.g. [[1,2,3],[4,5,6]]")
    if args.title:
        print(args.title)
    print(asciichartpy.plot(series, {"height": args.height}))


def cmd_scatter(args: argparse.Namespace) -> None:
    import plotext as plt

    x = _parse_floats(args.x)
    y = _parse_floats(args.y)
    if len(x) != len(y):
        sys.exit(f"x ({len(x)}) and y ({len(y)}) length mismatch")

    plt.theme("clear")
    plt.scatter(x, y, marker="braille")
    if args.title:
        plt.title(args.title)
    if args.xlabel:
        plt.xlabel(args.xlabel)
    if args.ylabel:
        plt.ylabel(args.ylabel)
    plt.plotsize(args.width or _term_cols() - 2, args.height)
    with _strip_ansi_stdout(strip=not args.color):
        plt.show()
    plt.clear_figure()


def cmd_sparkline(args: argparse.Namespace) -> None:
    values = _parse_floats(args.values)
    if not values:
        sys.exit("--values is empty")
    ramp = "▁▂▃▄▅▆▇█"
    lo, hi = min(values), max(values)
    span = hi - lo if hi > lo else 1.0
    out = "".join(ramp[min(7, int((v - lo) / span * 7))] for v in values)
    print(f"{args.title}: {out}" if args.title else out)


def cmd_hist(args: argparse.Namespace) -> None:
    values = _parse_floats(args.values)
    if not values:
        sys.exit("--values is empty")

    bins = args.bins
    lo, hi = min(values), max(values)
    span = hi - lo if hi > lo else 1.0
    counts = [0] * bins
    for v in values:
        idx = min(bins - 1, int((v - lo) / span * bins))
        counts[idx] += 1
    edges = [lo + i * span / bins for i in range(bins + 1)]
    labels = [f"{edges[i]:.1f}-{edges[i + 1]:.1f}" for i in range(bins)]
    _draw_simple_bar(labels, [float(c) for c in counts], args.title, args.width, args.color)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="plot", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_bar_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--labels", required=True, help="comma-separated category labels")
        parser.add_argument("--values", required=True, help="comma-separated numeric values")
        parser.add_argument("--title", default="")
        parser.add_argument("--width", type=int, help="max bar width in chars (auto-fit by default)")
        parser.add_argument("--color", action="store_true", help="enable ANSI colors")

    pb = sub.add_parser("bar", help="bar chart (plotext simple_bar)")
    add_bar_args(pb)
    pb.set_defaults(fn=cmd_bar)

    ph = sub.add_parser("hbar", help="alias for bar (kept for natural-language flexibility)")
    add_bar_args(ph)
    ph.set_defaults(fn=cmd_hbar)

    pst = sub.add_parser("stacked", help="stacked bar chart (plotext simple_stacked_bar)")
    pst.add_argument("--labels", required=True, help="comma-separated category labels")
    pst.add_argument("--series", required=True, help="JSON array of arrays, one per stacked series")
    pst.add_argument("--names", default="", help="comma-separated series names (optional)")
    pst.add_argument("--title", default="")
    pst.add_argument("--width", type=int)
    pst.add_argument("--color", action="store_true")
    pst.set_defaults(fn=cmd_stacked)

    pg = sub.add_parser("grouped", help="grouped/multi bar chart (plotext simple_multiple_bar)")
    pg.add_argument("--labels", required=True)
    pg.add_argument("--series", required=True, help="JSON array of arrays, one per group series")
    pg.add_argument("--names", default="", help="comma-separated series names (optional)")
    pg.add_argument("--title", default="")
    pg.add_argument("--width", type=int)
    pg.add_argument("--color", action="store_true")
    pg.set_defaults(fn=cmd_grouped)

    pgg = sub.add_parser("gauge", help="single-value progress bar")
    pgg.add_argument("--value", type=float, required=True)
    pgg.add_argument("--max", type=float, default=100.0)
    pgg.add_argument("--label", default="")
    pgg.add_argument("--width", type=int, default=30)
    pgg.set_defaults(fn=cmd_gauge)

    pbox = sub.add_parser("box", help="box plot (plotext, canvas mode)")
    pbox.add_argument("--labels", required=True)
    pbox.add_argument("--datasets", required=True, help="JSON array of arrays, one per box")
    pbox.add_argument("--title", default="")
    pbox.add_argument("--width", type=int)
    pbox.add_argument("--height", type=int, default=18)
    pbox.add_argument("--color", action="store_true")
    pbox.set_defaults(fn=cmd_box)

    pl = sub.add_parser("line", help="line chart (asciichart)")
    pl.add_argument("--values", required=True)
    pl.add_argument("--title", default="")
    pl.add_argument("--height", type=int, default=10)
    pl.set_defaults(fn=cmd_line)

    pm = sub.add_parser("multiline", help="multi-series line chart (asciichart)")
    pm.add_argument("--series", required=True, help='JSON array of arrays: [[1,2,3],[4,5,6]]')
    pm.add_argument("--title", default="")
    pm.add_argument("--height", type=int, default=10)
    pm.set_defaults(fn=cmd_multiline)

    pt = sub.add_parser("scatter", help="scatter plot, braille markers (plotext, canvas mode)")
    pt.add_argument("--x", required=True, help="comma-separated x values")
    pt.add_argument("--y", required=True, help="comma-separated y values")
    pt.add_argument("--title", default="")
    pt.add_argument("--xlabel", default="")
    pt.add_argument("--ylabel", default="")
    pt.add_argument("--width", type=int)
    pt.add_argument("--height", type=int, default=18)
    pt.add_argument("--color", action="store_true", help="enable ANSI colors")
    pt.set_defaults(fn=cmd_scatter)

    ps = sub.add_parser("sparkline", help="one-line trend in unicode block chars")
    ps.add_argument("--values", required=True)
    ps.add_argument("--title", default="")
    ps.set_defaults(fn=cmd_sparkline)

    pi = sub.add_parser("hist", help="histogram, auto-binned (plotext simple_bar)")
    pi.add_argument("--values", required=True)
    pi.add_argument("--bins", type=int, default=10)
    pi.add_argument("--title", default="")
    pi.add_argument("--width", type=int)
    pi.add_argument("--color", action="store_true")
    pi.set_defaults(fn=cmd_hist)

    return p


def main() -> None:
    args = build_parser().parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
