import streamlit as st
import matplotlib.pyplot as plt
import random
from geometric_enigmas import convex_hull, closest_pair, segments_intersect

st.set_page_config(page_title="Geometric Enigmas", layout="centered")
st.title("🧭 Geometric Enigmas Interactive Prototype")

# --- User Controls ---
st.sidebar.header("⚙️ Configuration")
num_points = st.sidebar.slider("Number of random points", 5, 30, 10)
show_segments = st.sidebar.checkbox("Show Line Segment Intersections", True)

# --- Generate Random Points ---
points = [(random.uniform(0, 5), random.uniform(0, 5)) for _ in range(num_points)]

# --- Run Algorithms ---
hull = convex_hull(points)
dist, pair = closest_pair(points)

# Example Segments (you can extend this)
segments = [((0, 0), (3, 3)), ((0, 3), (3, 0)), ((1, 0), (1, 4))]
intersections = []
if show_segments:
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            ok, ip = segments_intersect(segments[i][0], segments[i][1], segments[j][0], segments[j][1])
            if ok and ip is not None:
                intersections.append(ip)

# --- Visualization ---
fig, ax = plt.subplots(figsize=(6, 6))
xs, ys = zip(*points)
ax.scatter(xs, ys, s=40, color='blue', label='Points')

# Convex Hull
if len(hull) > 1:
    hx, hy = zip(*(hull + [hull[0]]))
    ax.plot(hx, hy, color='green', linewidth=1.5, label='Convex Hull')

# Closest Pair
if pair[0] and pair[1]:
    cx, cy = zip(*pair)
    ax.plot(cx, cy, 'r--', linewidth=2, label='Closest Pair')

# Segments + Intersections
if show_segments:
    for seg in segments:
        sx, sy = zip(*seg)
        ax.plot(sx, sy, color='purple', linewidth=1)
    for ip in intersections:
        ax.scatter([ip[0]], [ip[1]], color='red', s=60, marker='x', label='Intersections')

ax.set_aspect('equal', 'box')
ax.legend()
ax.set_title("Geometric Visualization")
st.pyplot(fig)

# --- Output Summary ---
st.subheader("🔍 Summary")
st.write("**Convex Hull Points:**", hull)
st.write("**Closest Pair:**", pair, " | **Distance:**", round(dist, 3))
if show_segments:
    st.write("**Intersections:**", intersections)
