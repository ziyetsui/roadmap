"""把“两个旋钮的地形”讲清楚：坐标是旋钮位置，颜色是损失，线是训练轨迹。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["PingFang HK", "Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, TEAL, ORANGE = "#18333d", "#087f8c", "#c66b24"

W1, W2 = np.meshgrid(np.linspace(-3, 3, 300), np.linspace(-3, 3, 300))
L = W1**2 + 3 * W2**2

fig, ax = plt.subplots(figsize=(9.6, 7.4))
cf = ax.contourf(W1, W2, L, levels=24, cmap="YlOrRd")
ax.contour(W1, W2, L, levels=[2, 6, 12, 20], colors="white", linewidths=0.7, alpha=0.7)

p = np.array([2.0, 1.6]); path = [p.copy()]
for _ in range(16):
    p = p - 0.18 * np.array([2 * p[0], 6 * p[1]])
    path.append(p.copy())
path = np.array(path)
ax.plot(path[:, 0], path[:, 1], "-o", color=INK, lw=2, ms=4, zorder=5)

# 标注
ax.annotate("起点：两个旋钮一开始拧在这里\n（颜色深红 = 损失很大）",
            xy=(path[0, 0], path[0, 1]), xytext=(0.55, 2.55),
            fontsize=11, color=INK,
            arrowprops=dict(arrowstyle="->", color="#555", lw=1.2))
ax.annotate("谷底：损失最小的地方\n（两个旋钮的最优值）",
            xy=(0.12, -0.12), xytext=(1.05, -1.15), fontsize=11, color=TEAL,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.4))
ax.annotate("", xy=(path[1, 0], path[1, 1]), xytext=(path[0, 0], path[0, 1]),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.6))
ax.text(1.02, 0.78, "一步：\n两个旋钮同时拧一点", fontsize=10, color=ORANGE)

ax.text(0.02, 0.975, "每个点 = 两个旋钮的一种组合\n颜色 = 这个组合算出来的损失（越浅越小）",
        transform=ax.transAxes, fontsize=10.5, color="#333", va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.85, edgecolor="#ddd"))

ax.set_xlabel("旋钮 1 的位置", fontsize=11)
ax.set_ylabel("旋钮 2 的位置", fontsize=11)
ax.set_title("从正上方看“两个旋钮”的地形", fontsize=15)
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
cb = fig.colorbar(cf, ax=ax, fraction=0.045, pad=0.02)
cb.set_label("损失", fontsize=10)
fig.tight_layout()
fig.savefig("dim2_map.png", dpi=150)
print("saved")
