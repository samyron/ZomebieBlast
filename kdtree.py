from point import Point
from dataclasses import dataclass
from math import inf, sqrt


@dataclass
class KDNode:
    point: Point
    left: 'KDNode' = None
    right: 'KDNode' = None


def distance(p: Point, q: Point):
    return sqrt(((q.x - p.x) ** 2) + ((q.y - p.y) ** 2))


def insert0(node: KDNode, point: Point, depth: int):
    if not node:
        return KDNode(point)

    cd = depth % 2
    if point[cd] < node.point[cd]:
        node.left = insert0(node.left, point, depth+1)
    else:
        node.right = insert0(node.right, point, depth+1)

    return node


def contains0(node: KDNode, point: Point, depth: int):
    if not node:
        return False

    if node.point == point:
        return True

    cd = depth % 2

    if point[cd] < node.point[cd]:
        return contains0(node.left, point, depth+1)
    else:
        return contains0(node.right, point, depth+1)


# NN Source: https://courses.cs.washington.edu/courses/cse373/02au/lectures/lecture22l.pdf

class KDTree(object):
    def __init__(self):
        self.root = None

    def insert(self, point: Point):
        self.root = insert0(self.root, point, 0)

    def contains(self, point: Point):
        return contains0(self.root, point, 0)

    def nearest_neighbor(self, query: Point, minimax=0.0):
        def nn(node: KDNode, point: Point, w: float, depth: int):
            if not node:
                return point, w

            d = distance(query, node.point)
            if d < w:
                w = d
                point = node.point

            if w <= minimax:
                # print(f"quit early! w={w}, minimax={minimax}")
                return point, w

            if node.left is None and node.right is None:
                return point, w

            cd = depth % 2

            q_cd = query[cd]
            np_cd = node.point[cd]

            if q_cd < np_cd:
                point, w = nn(node.left, point, w, depth+1)
                if w <= minimax:
                    # print(f"quit early 2! w={w}, minimax={minimax}")
                    return point, w
                if q_cd + w >= np_cd:
                    # print(f"Left query={query} node.point={node.point} (depth: {depth}): w={w}, q_cd={q_cd}, np_cd={np_cd}, (q_cd + w)={q_cd + w}")
                    point, w = nn(node.right, point, w, depth+1)
                # else:
                #     print("Skip going right!")
            else:
                point, w = nn(node.right, point, w, depth+1)
                if w <= minimax:
                    # print(f"quit early 3! w={w}, minimax={minimax}")
                    return point, w
                if q_cd - w <= np_cd:
                    # print(
                    #     f"Right query={query} node.point={node.point} (depth: {depth}): w={w}, q_cd={q_cd}, np_cd={np_cd}, (q_cd - w)={q_cd - w}")
                    point, w = nn(node.left, point, w, depth + 1)
                # else:
                #     print("Skip going left!")

            return point, w

        return nn(self.root, None, inf, 0)
