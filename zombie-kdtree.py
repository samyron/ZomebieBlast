from datetime import datetime, timedelta
import math
import os
import sys
from kdtree import KDTree, distance
from point import Point
import random


def main():
    if len(sys.argv) != 2:
        print(f"Usage: #{sys.argv[0]} <filename>", file=sys.stderr)
        return 1

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"The file '{input_file}' does not exist.", file=sys.stderr)
        return 1

    mines = []
    zombies = []

    with open(input_file, 'r') as f:
        num_puzzles = int(f.readline())
        print(f"Number of puzzles in file: {num_puzzles}")
        dims = f.readline()
        cols,  rows = [int(i) for i in dims.split(sep=' ', maxsplit=1)]

        print(f"rows={rows}, cols={cols}")

        for i in range(0, rows):
            row = f.readline().strip()
            for j, c in enumerate(row):
                if c == 'M':
                    mines.append(Point(i, j))
                elif c == 'Z':
                    zombies.append(Point(i, j))

    print(f"Mines: {len(mines)}")
    print(f"Zombies: {len(zombies)}")

    start = datetime.now()

    random.shuffle(mines)

    z_len = len(zombies)
    early_tests = [zombies[0], zombies[int(z_len / 2)], zombies[int(z_len / 4)], zombies[int(z_len / 8)], zombies[-1]]

    random.shuffle(zombies)
    random.shuffle(zombies)
    print(f"Shuffle time: {datetime.now() - start}")

    tree = KDTree()

    for m in mines:
        tree.insert(m)

    print(f"Build KDTree: {datetime.now() - start}")

    best_w = 0
    best_point = None
    simple_skipped = 0

    for z in early_tests:
        if best_point:
            d = distance(z, best_point)
            if d < best_w:
                continue
        p, w = tree.nearest_neighbor(z, best_w)
        if w > best_w:
            best_w = w
            best_point = p

    print(f"Early tests: best_point={best_point}, best_w={best_w}")

    for z in zombies:
        if best_point:
            d = distance(z, best_point)
            if d < best_w:
                simple_skipped += 1
                continue
        p, w = tree.nearest_neighbor(z, best_w)
        if w > best_w:
            best_w = w
            best_point = p

    result = best_w

    end = datetime.now()
    duration = end - start

    print(f"Zombies skipped: {simple_skipped}")
    print(f"Result: {result:.7f}")
    print(f"Duration: {duration}")

    return 0


if __name__ == '__main__':
    sys.exit(main())

