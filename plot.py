#!/usr/bin/env -S -u UV_EXCLUDE_NEWER uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "termgraph>=0.7.6",
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


def cmd_bar(args: argparse.Namespace) -> None:
    from termgraph.module import Args as TgArgs, BarChart, Data

    labels = _parse_strs(args.labels)
    values = _parse_floats(args.values)
    if len(labels) != len(values):
        sys.exit(f"labels ({len(labels)}) and values ({len(values)}) length mismatch")

    label_w = max(len(label) for label in labels)
    width = args.width or max(10, _term_cols() - label_w - 12)
    data = Data([[v] for v in values], labels)
    tg_kwargs = {"title": args.title or "", "space_between": False, "width": width}
    if args.color:
        tg_kwargs["colors"] = [94]
    with _strip_ansi_stdout(strip=not args.color):
        BarChart(data, TgArgs(**tg_kwargs)).draw()


def cmd_hbar(args: argparse.Namespace) -> None:
    import plotext as plt

    labels = _parse_strs(args.labels)
    values = _parse_floats(args.values)
    if len(labels) != len(values):
        sys.exit(f"labels ({len(labels)}) and values ({len(values)}) length mismatch")

    width = args.width or _term_cols() - 2
    plt.simple_bar(labels, values, width=width, title=args.title or "")
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
    from termgraph.module import Args as TgArgs, BarChart, Data

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

    label_w = max(len(label) for label in labels)
    width = args.width or max(10, _term_cols() - label_w - 12)
    data = Data([[c] for c in counts], labels)
    tg_kwargs = {"title": args.title or "", "space_between": False, "width": width}
    if args.color:
        tg_kwargs["colors"] = [94]
    with _strip_ansi_stdout(strip=not args.color):
        BarChart(data, TgArgs(**tg_kwargs)).draw()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="plot", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    pb = sub.add_parser("bar", help="vertical-style bar chart (termgraph)")
    pb.add_argument("--labels", required=True, help="comma-separated category labels")
    pb.add_argument("--values", required=True, help="comma-separated numeric values")
    pb.add_argument("--title", default="")
    pb.add_argument("--width", type=int, help="max bar width in chars (auto-fit by default)")
    pb.add_argument("--color", action="store_true", help="enable ANSI colors")
    pb.set_defaults(fn=cmd_bar)

    ph = sub.add_parser("hbar", help="horizontal bar chart (plotext simple_bar)")
    ph.add_argument("--labels", required=True)
    ph.add_argument("--values", required=True)
    ph.add_argument("--title", default="")
    ph.add_argument("--width", type=int)
    ph.add_argument("--color", action="store_true", help="enable ANSI colors")
    ph.set_defaults(fn=cmd_hbar)

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

    ps = sub.add_parser("sparkline", help="one-line trend in unicode block chars")
    ps.add_argument("--values", required=True)
    ps.add_argument("--title", default="")
    ps.set_defaults(fn=cmd_sparkline)

    pi = sub.add_parser("hist", help="histogram, auto-binned (via termgraph)")
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
