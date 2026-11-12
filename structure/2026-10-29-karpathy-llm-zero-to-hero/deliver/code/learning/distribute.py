"""两个旋钮，把“分发”算给你看：16 只算一次，两条边各乘一次。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"
FWD, BWD = "#2f8f83", "#d97706"

def box(ax, x, y, txt, color=INK, w=0.26, h=0.15, fs=11.5):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02",
                                fc="white", ec=color, lw=1.8, zorder=3))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=color, zorder=4)

fig, axes = plt.subplots(1, 3, figsize=(16, 6.0))
for ax in axes:
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

# ① 前向
a = axes[0]
a.set_title("① 前向：算出 8 和 64，存下来", fontsize=13, color=FWD)
box(a, 0.20, 0.74, "w1×x1 = 1×2 = 2")
box(a, 0.20, 0.28, "w2×x2 = 2×3 = 6")
box(a, 0.56, 0.51, "8", color=FWD, w=0.12, h=0.12, fs=15)
box(a, 0.86, 0.51, "64", color=ORANGE, w=0.12, h=0.12, fs=15)
a.add_patch(FancyArrowPatch((0.33, 0.70), (0.49, 0.55), arrowstyle="-|>", mutation_scale=16, color=FWD, lw=2.2))
a.add_patch(FancyArrowPatch((0.33, 0.32), (0.49, 0.47), arrowstyle="-|>", mutation_scale=16, color=FWD, lw=2.2))
a.add_patch(FancyArrowPatch((0.62, 0.51), (0.80, 0.51), arrowstyle="-|>", mutation_scale=16, color=FWD, lw=2.2))
a.text(0.56, 0.36, "2 + 6", fontsize=9.5, color=MUTED, ha="center")
a.text(0.71, 0.57, "平方", fontsize=9.5, color=MUTED, ha="center")

# ② 反向
b = axes[1]
b.set_title("② 反向：16 只到站一次，两条边各乘一次", fontsize=13, color=BWD)
box(b, 0.19, 0.74, "w1 的梯度\n16 × 2 = 32", w=0.30, h=0.16, fs=10.5)
box(b, 0.19, 0.28, "w2 的梯度\n16 × 3 = 48", w=0.30, h=0.16, fs=10.5)
box(b, 0.57, 0.51, "16", color=BWD, w=0.13, h=0.13, fs=15)
box(b, 0.86, 0.51, "1", color=ORANGE, w=0.09, h=0.10, fs=13)
b.add_patch(FancyArrowPatch((0.81, 0.51), (0.64, 0.51), arrowstyle="-|>", mutation_scale=16, color=BWD, lw=2.4))
b.add_patch(FancyArrowPatch((0.52, 0.56), (0.33, 0.72), arrowstyle="-|>", mutation_scale=16, color=BWD, lw=2.4))
b.add_patch(FancyArrowPatch((0.52, 0.46), (0.33, 0.30), arrowstyle="-|>", mutation_scale=16, color=BWD, lw=2.4))
b.text(0.60, 0.70, "16 只算一次", fontsize=10.5, color=BWD, ha="center")

# ③ 笨办法
c = axes[2]
c.set_title("③ 笨办法：想得到一个，就重跑一遍", fontsize=13, color=MUTED)
for k, (yy, label) in enumerate([(0.72, "改 w1 → 整条重算 → 32"), (0.28, "改 w2 → 整条重算 → 48")]):
    for i in range(4):
        c.add_patch(FancyBboxPatch((0.08 + i*0.20, yy - 0.08), 0.15, 0.16, boxstyle="round,pad=0.012",
                                   fc="#f4f5f6", ec="#d3dade", lw=1.1))
    c.add_patch(FancyArrowPatch((0.25, yy), (0.86, yy), arrowstyle="-|>",
                                mutation_scale=13, color="#b8c2c0", lw=1.3))
    c.text(0.50, yy + 0.14, label, fontsize=10, color=MUTED, ha="center")
c.text(0.50, 0.10, "41 个旋钮 = 41 趟；答案一样，多跑 40 趟", fontsize=10, color=MUTED, ha="center")

fig.suptitle("“分发”就是：一个数走到岔路口，每条边拿它乘一下", fontsize=16, y=0.99)
fig.tight_layout()
fig.savefig("distribute.png", dpi=150, facecolor="white")
print("saved")
