"""一次前向 + 一次反向，怎么得到 41 个梯度：三联画。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

plt.rcParams["font.sans-serif"] = ["PingFang HK", "Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"
FWD, BWD = "#2f8f83", "#d97706"

def node(ax, xy, txt, color=TEAL, r=0.045):
    ax.add_patch(Circle(xy, r, facecolor="white", edgecolor=color, lw=2.4, zorder=4))
    ax.text(xy[0], xy[1] - 0.09, txt, ha="center", fontsize=10, color=color)

fig = plt.figure(figsize=(16.5, 6.4))
gs = fig.add_gridspec(1, 3, wspace=0.12)
for i in range(3):
    ax = fig.add_subplot(gs[0, i])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

# ── ① 前向 ──
ax = fig.axes[0]
xs = [0.10, 0.35, 0.60, 0.86]
for x in xs:
    node(ax, (x, 0.5), "数")
for a, b in zip(xs, xs[1:]):
    ax.add_patch(FancyArrowPatch((a + 0.05, 0.5), (b - 0.05, 0.5),
                                 arrowstyle="-|>", mutation_scale=18, color=FWD, lw=2.4))
ax.text(0.5, 0.82, "① 前向：从左到右走一遍", ha="center", fontsize=14, color=FWD)
ax.text(0.5, 0.28, "每站算出一个数，顺手存下来", ha="center", fontsize=11, color=MUTED)
ax.text(0.5, 0.16, "代价：走 1 遍", ha="center", fontsize=11, color=INK)

# ── ② 反向 ──
ax = fig.axes[1]
for k, x in enumerate(xs):
    node(ax, (x, 0.5), "1" if x == xs[3] else "信")
for a, b in zip(xs[::-1], xs[::-1][1:]):
    ax.add_patch(FancyArrowPatch((a - 0.05, 0.5), (b + 0.05, 0.5),
                                 arrowstyle="-|>", mutation_scale=18, color=BWD, lw=2.4))
ax.text(0.5, 0.82, "② 反向：从右到左再走一遍", ha="center", fontsize=14, color=BWD)
ax.text(0.5, 0.28, "每站把『下游有多敏感』乘上本地斜率", ha="center", fontsize=11, color=MUTED)
ax.text(0.5, 0.16, "代价：走 1 遍", ha="center", fontsize=11, color=INK)

# ── ③ 41 根边同时拿到 ──
ax = fig.axes[2]
cx, cy = 0.5, 0.52
node(ax, (cx, cy), "中间量", r=0.05)
n = 41
ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
for k, th in enumerate(ang):
    x, y = cx + 0.34 * np.cos(th), cy + 0.34 * np.sin(th)
    ax.annotate("", xy=(x, y), xytext=(cx + 0.06 * np.cos(th), cy + 0.06 * np.sin(th)),
                arrowprops=dict(arrowstyle="-|>", color=BWD, lw=0.9, alpha=0.65,
                                shrinkA=0, shrinkB=0))
    ax.scatter([x], [y], s=12, color=ORANGE, zorder=5)
ax.text(0.5, 0.90, "③ 一封信到站，41 根线各自领走一份", ha="center", fontsize=14, color=BWD)
ax.text(0.5, 0.06, "每根线只做一次乘法，不用重跑整条链", ha="center", fontsize=11, color=MUTED)

fig.text(0.5, 0.955, "一次前向 + 一次反向 = 41 个梯度：不是跑 41 遍，而是同一遍路上顺手分了 41 份",
         ha="center", fontsize=16, color=INK)
fig.savefig("backprop_once.png", dpi=150, facecolor="white")
print("saved")
