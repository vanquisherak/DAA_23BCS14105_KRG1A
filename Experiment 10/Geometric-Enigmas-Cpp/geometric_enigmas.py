import math
from typing import List, Tuple, Optional

Point = Tuple[float, float]
Segment = Tuple[Point, Point]

# -------------------------
# Geometry helpers
# -------------------------
def dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])

def orientation(a: Point, b: Point, c: Point) -> int:
    val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
    if abs(val) < 1e-12:
        return 0
    return 1 if val > 0 else 2

def on_segment(a: Point, b: Point, c: Point) -> bool:
    return (min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and
            min(a[1], c[1]) <= b[1] <= max(a[1], c[1]))

# -------------------------
# Line intersection
# -------------------------
def line_intersection_point(p1: Point, p2: Point, p3: Point, p4: Point) -> Optional[Point]:
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(denom) < 1e-12:
        return None
    px = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / denom
    return (px, py)

def segments_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> Tuple[bool, Optional[Point]]:
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True, line_intersection_point(p1, q1, p2, q2)

    if o1 == 0 and on_segment(p1, p2, q1): return True, p2
    if o2 == 0 and on_segment(p1, q2, q1): return True, q2
    if o3 == 0 and on_segment(p2, p1, q2): return True, p1
    if o4 == 0 and on_segment(p2, q1, q2): return True, q1

    return False, None

# -------------------------
# Convex Hull (Graham Scan)
# -------------------------
def convex_hull(points: List[Point]) -> List[Point]:
    pts = sorted(points)
    if len(pts) <= 1:
        return pts

    def cross(o: Point, a: Point, b: Point) -> float:
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

# -------------------------
# Closest Pair (Divide & Conquer)
# -------------------------
def closest_pair(points: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    pts = sorted(points, key=lambda x: x[0])
    def _closest(px, py):
        n = len(px)
        if n <= 3:
            best = float('inf')
            pair = (None, None)
            for i in range(n):
                for j in range(i+1, n):
                    d = dist(px[i], px[j])
                    if d < best:
                        best, pair = d, (px[i], px[j])
            return best, pair

        mid = n // 2
        midx = px[mid][0]
        Qx, Rx = px[:mid], px[mid:]
        Qset = set(Qx)
        Qy = [p for p in py if p in Qset]
        Ry = [p for p in py if p not in Qset]

        dl, pl = _closest(Qx, Qy)
        dr, pr = _closest(Rx, Ry)
        d, pair = (dl, pl) if dl < dr else (dr, pr)

        strip = [p for p in py if abs(p[0] - midx) < d]
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j][1] - strip[i][1]) < d:
                dj = dist(strip[i], strip[j])
                if dj < d:
                    d, pair = dj, (strip[i], strip[j])
                j += 1
        return d, pair

    py = sorted(pts, key=lambda p: p[1])
    return _closest(pts, py)
