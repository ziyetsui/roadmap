"""前向一排、反向一排：同样的位置，反过来走一遍。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"

fig, ax = plt.subplots(figsize=(15, 9))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

def node(x, y, title, big, color=INK, w=0.105, h=0.105):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02",
                                fc="white", ec=color, lw=1.8, zorder=4))
    ax.text(x, y + 0.022, title, ha="center", va="center", fontsize=9.5, color=MUTED, zorder=5)
    ax.text(x, y - 0.022, big, ha="center", va="center", fontsize=15, color=color,
            fontweight="bold", zorder=5)

def arr(p, q, color, label="", off=(0, 0), fs=10):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=color, lw=2.2, zorder=3))
    if label:
        mx, my = (p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1]
        ax.text(mx, my, label, fontsize=fs, color=color, ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=1.0), zorder=6)

# ── 上排：前向 ──
ax.text(0.02, 0.975, "前向：只算数，把每个值写下来", fontsize=13.5, color=TEAL, va="top")
node(0.08, 0.86, "w1 的值", "1"); node(0.28, 0.86, "乘积 值", "2")
node(0.08, 0.60, "w2 的值", "2"); node(0.28, 0.60, "乘积 值", "6")
node(0.54, 0.73, "和 值", "8", color=TEAL); node(0.80, 0.73, "损失 值", "64", color=ORANGE)
arr((0.145, 0.86), (0.215, 0.86), TEAL, "×2 (x1)", (0, 0.05))
arr((0.145, 0.60), (0.215, 0.60), TEAL, "×3 (x2)", (0, 0.05))
arr((0.345, 0.84), (0.48, 0.76), TEAL, "+", (0.01, 0.05))
arr((0.345, 0.62), (0.48, 0.70), TEAL, "+", (0.01, -0.05))
arr((0.605, 0.73), (0.735, 0.73), TEAL, "平方", (0, 0.05))

# ── 下排：反向 ──
ax.text(0.02, 0.455, "反向：从损失出发，把信往回寄", fontsize=13.5, color=ORANGE, va="top")
node(0.08, 0.33, "w1 的信", "32", color=ORANGE); node(0.28, 0.33, "乘积 信", "16", color=ORANGE)
node(0.08, 0.09, "w2 的信", "48", color=ORANGE); node(0.28, 0.09, "乘积 信", "16", color=ORANGE)
node(0.54, 0.21, "和 的信", "16", color=ORANGE); node(0.80, 0.21, "损失 的信", "1", color=ORANGE)
arr((0.735, 0.21), (0.605, 0.21), ORANGE, "×16", (0, 0.05))
arr((0.48, 0.19), (0.345, 0.11), ORANGE, "原样", (0.01, -0.05))
arr((0.48, 0.23), (0.345, 0.31), ORANGE, "原样", (0.01, 0.05))
arr((0.215, 0.33), (0.145, 0.33), ORANGE, "×2", (0, 0.05))
arr((0.215, 0.09), (0.145, 0.09), ORANGE, "×3", (0, 0.05))

# 连接两排
ax.annotate("", xy=(0.80, 0.30), xytext=(0.80, 0.665),
            arrowprops=dict(arrowstyle="-|>", color="#b9a08a", lw=1.4, ls=":"))
ax.text(0.815, 0.52, "同一个节点：\n上面是它的值，\n下面是它收到的信", fontsize=9.5, color=MUTED)

fig.text(0.5, 0.95, "前向一排、反向一排：位置没变，方向反过来", fontsize=16, ha="center", color=INK)
fig.text(0.5, 0.03, "值越小越好；信是比值，和值的大小无关。信 = 这个盒子变 1，最终损失变几。",
         fontsize=11, ha="center", color=MUTED)
fig.savefig("one_step.png", dpi=150, facecolor="white")
print("saved")
