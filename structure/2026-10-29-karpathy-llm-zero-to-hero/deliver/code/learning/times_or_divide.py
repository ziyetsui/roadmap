"""乘回去 vs 除回去：一个算梯度，一个只是还原输入。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"

fig, ax = plt.subplots(figsize=(12.5, 7.6))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

def box(x, y, t, c, w=0.11, h=0.12, fs=19):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02",
                                fc="white", ec=c, lw=2.2))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, color=c, fontweight="bold")

def arrow(x1, x2, y, label, c, above=True):
    ax.add_patch(FancyArrowPatch((x1, y), (x2, y), arrowstyle="-|>", mutation_scale=17, color=c, lw=2.4))
    ax.text((x1 + x2) / 2, y + (0.055 if above else -0.075), label, fontsize=14, color=c, ha="center")

xs = [0.16, 0.46, 0.80]
ax.text(0.02, 0.95, "① 前向（值）：1 被 ×2、×4 放大成 8", fontsize=12.5, color=TEAL)
for x, t in zip(xs, ["1", "2", "8"]):
    box(x, 0.80, t, INK)
arrow(xs[0] + 0.06, xs[1] - 0.06, 0.80, "×2", TEAL)
arrow(xs[1] + 0.06, xs[2] - 0.06, 0.80, "×4", TEAL)

ax.text(0.02, 0.62, "② 反向（信）：从 8 出发，倒着把倍数乘回去", fontsize=12.5, color=ORANGE)
for x, t in zip(xs, ["信 8", "信 4", "信 1"]):
    box(x, 0.46, t, ORANGE, fs=13)
arrow(xs[1] - 0.06, xs[0] + 0.06, 0.46, "×2", ORANGE)
arrow(xs[2] - 0.06, xs[1] + 0.06, 0.46, "×4", ORANGE)
ax.text(0.5, 0.345, "2 × 4 = 8：这就是梯度（1 变 1，最后变 8）", fontsize=11.5, color=ORANGE, ha="center")

ax.text(0.02, 0.245, "③ 如果改成“除回去”，会发生什么", fontsize=12.5, color="#9aa7a5")
for x, t in zip(xs, ["8", "2", "1"]):
    box(x, 0.15, t, "#9aa7a5")
arrow(xs[1] - 0.06, xs[0] + 0.06, 0.15, "÷4", "#9aa7a5")
arrow(xs[2] - 0.06, xs[1] + 0.06, 0.15, "÷2", "#9aa7a5")
ax.text(0.5, 0.045, "8 ÷ 4 ÷ 2 = 1：这只是把输入还原出来，你早就知道它是 1；它不告诉你该往哪下山",
        fontsize=10.5, color="#9aa7a5", ha="center")

fig.text(0.5, 0.975, "反向传播问的是「倍数」，不是「原来的输入」", fontsize=16, ha="center", color=INK)
fig.savefig("times_or_divide.png", dpi=150, facecolor="white")
print("saved")
