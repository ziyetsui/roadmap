"""两台机器：1 → ×2 → 2 → ×3 → 6。倍数乘起来就行。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"

fig, ax = plt.subplots(figsize=(12, 6.4))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

def box(x, y, t, c=INK, w=0.12, h=0.13, fs=20):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02",
                                fc="white", ec=c, lw=2.2))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, color=c, fontweight="bold")

xs = [0.14, 0.46, 0.80]
top, bot = 0.72, 0.26
for x, t in zip(xs, ["1", "2", "6"]):
    box(x, top, t)
for x, t in zip(xs, ["6", "3", "1"]):
    box(x, bot, t, ORANGE)

for i in range(2):
    ax.add_patch(FancyArrowPatch((xs[i] + 0.065, top), (xs[i+1] - 0.065, top),
                                 arrowstyle="-|>", mutation_scale=18, color=TEAL, lw=2.6))
    ax.add_patch(FancyArrowPatch((xs[i+1] - 0.065, bot), (xs[i] + 0.065, bot),
                                 arrowstyle="-|>", mutation_scale=18, color=ORANGE, lw=2.6))

ax.text((xs[0]+xs[1])/2, top + 0.09, "×2", fontsize=18, color=TEAL, ha="center")
ax.text((xs[1]+xs[2])/2, top + 0.09, "×3", fontsize=18, color=TEAL, ha="center")
ax.text((xs[0]+xs[1])/2, bot - 0.10, "×2", fontsize=18, color=ORANGE, ha="center")
ax.text((xs[1]+xs[2])/2, bot - 0.10, "×3", fontsize=18, color=ORANGE, ha="center")

ax.text(0.02, 0.92, "上排：前向。1 被 ×2 变成 2，再被 ×3 变成 6。", fontsize=12, color=TEAL)
ax.text(0.02, 0.06, "下排：反向。同一个 ×3、×2，倒着乘回去：1 → 3 → 6。", fontsize=12, color=ORANGE)
ax.text(0.5, 0.985, "两台机器串起来，倍数乘一乘就完事", fontsize=16, ha="center", color=INK)

fig.tight_layout()
fig.savefig("two_machines.png", dpi=150, facecolor="white")
print("saved")
