#!/usr/bin/env python3
"""Matrix digital rain for the terminal. Press q to quit.

Stdlib only. Meant to be left running as a terminal wallpaper: it ignores
every key except q / Q (and Ctrl-C), and restores the terminal on exit.
"""

import argparse
import curses
import locale
import random
import time

KATAKANA = (
    "ｦｧｨｩｪｫｬｭｮｯ"
    "ｱｲｳｴｵｶｷｸｹｺ"
    "ｻｼｽｾｿﾀﾁﾂﾃﾄ"
    "ﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎ"
    "ﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘ"
    "ﾙﾚﾛﾜﾝ"
    "0123456789"
)
ASCII_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*+=<>|/\\"

# Colour pair ids, brightest to dimmest.
P_HEAD, P_BRIGHT, P_MID, P_DIM = 1, 2, 3, 4


def pick_charset(stdscr):
    """Use katakana if the terminal can actually encode it, else ASCII."""
    try:
        stdscr.addstr(0, 0, KATAKANA[0])
        stdscr.erase()
        return KATAKANA
    except Exception:
        stdscr.erase()
        return ASCII_CHARS


def init_colors():
    curses.start_color()
    try:
        curses.use_default_colors()
        bg = -1
    except curses.error:
        bg = curses.COLOR_BLACK

    if curses.COLORS >= 256:
        curses.init_pair(P_HEAD, 231, bg)     # near-white
        curses.init_pair(P_BRIGHT, 48, bg)    # bright green
        curses.init_pair(P_MID, 40, bg)       # green
        curses.init_pair(P_DIM, 22, bg)       # dark green
    else:
        curses.init_pair(P_HEAD, curses.COLOR_WHITE, bg)
        curses.init_pair(P_BRIGHT, curses.COLOR_GREEN, bg)
        curses.init_pair(P_MID, curses.COLOR_GREEN, bg)
        curses.init_pair(P_DIM, curses.COLOR_GREEN, bg)


def attr_for(depth, length):
    """Colour attribute for a cell `depth` rows behind the head."""
    if depth == 0:
        return curses.color_pair(P_HEAD) | curses.A_BOLD
    if depth <= max(1, length // 6):
        return curses.color_pair(P_BRIGHT) | curses.A_BOLD
    if depth <= length // 2:
        return curses.color_pair(P_MID)
    return curses.color_pair(P_DIM) | curses.A_DIM


def new_drop(height, speed_mult, active):
    return {
        "active": active,
        "y": float(random.randint(-height, 0)),
        "last": -1,
        "speed": random.uniform(0.25, 0.9) * speed_mult,
        "length": random.randint(max(4, height // 6), max(6, height)),
    }


def build_state(height, width, speed_mult, density):
    grid = [[" "] * width for _ in range(height)]
    drops = [
        new_drop(height, speed_mult, random.random() < density)
        for _ in range(width)
    ]
    return grid, drops


def rain(stdscr, args):
    curses.curs_set(0)
    stdscr.nodelay(True)
    init_colors()
    charset = pick_charset(stdscr)

    height, width = stdscr.getmaxyx()
    grid, drops = build_state(height, width, args.speed, args.density)

    while True:
        key = stdscr.getch()
        if key in (ord("q"), ord("Q")):
            return
        if key == curses.KEY_RESIZE:
            height, width = stdscr.getmaxyx()
            grid, drops = build_state(height, width, args.speed, args.density)
            stdscr.erase()

        stdscr.erase()
        for x, drop in enumerate(drops):
            if not drop["active"]:
                continue

            head = int(drop["y"])
            # Stamp a fresh glyph into every row the head just passed through.
            for y in range(drop["last"] + 1, head + 1):
                if 0 <= y < height:
                    grid[y][x] = random.choice(charset)
            drop["last"] = head

            for depth in range(drop["length"]):
                y = head - depth
                if 0 <= y < height and grid[y][x] != " ":
                    try:
                        stdscr.addstr(y, x, grid[y][x], attr_for(depth, drop["length"]))
                    except curses.error:
                        pass  # bottom-right cell of the window

            drop["y"] += drop["speed"]
            if head - drop["length"] > height:
                drops[x] = new_drop(height, args.speed, random.random() < args.density)

        # A few glyphs flicker into something else each frame.
        for _ in range(max(1, width // 8)):
            y, x = random.randrange(height), random.randrange(width)
            if grid[y][x] != " ":
                grid[y][x] = random.choice(charset)

        stdscr.refresh()
        time.sleep(args.frame)


def main():
    parser = argparse.ArgumentParser(description="Matrix rain. Press q to quit.")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="fall speed multiplier (default: 1.0)")
    parser.add_argument("--density", type=float, default=0.7,
                        help="fraction of columns raining, 0-1 (default: 0.7)")
    parser.add_argument("--frame", type=float, default=0.05,
                        help="seconds between frames (default: 0.05)")
    args = parser.parse_args()
    args.density = min(max(args.density, 0.0), 1.0)

    locale.setlocale(locale.LC_ALL, "")
    try:
        curses.wrapper(rain, args)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
