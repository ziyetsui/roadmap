"""高度不是坡度：loss 大不代表降得快。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"

sig = lambda x: 1 / (1 + np.exp(-x))
L = lambda w: 10 - 8 * sig(w - 3)
dL = lambda w: -8 * sig(w - 3) * (1 - sig(w - 3))

w = np.linspace(-2, 8, 400)
fig, ax = plt.subplots(figsize=(12.5, 6.6))
ax.plot(w, L(w), color=INK, lw=2.6)

for w0, name, col in [(1.0, "A", TEAL), (3.0, "B", ORANGE)]:
    y0, s = L(w0), dL(w0)
    xs = np.linspace(w0 - 1.0, w0 + 1.0, 2)
    ax.plot(xs, y0 + s * (xs - w0), color=col, lw=2, ls="--")
    ax.scatter([w0], [y0], s=110, color=col, zorder=5)
    # 一步的实际位移（学习率×坡度），画成箭头
    step = 0.9 * s
    ax.annotate("", xy=(w0 - step, L(w0) + s * (-step)), xytext=(w0, y0),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=3))
    ax.text(w0 + 0.12, y0 + 0.55, f"{name}\n损失 {y0:.1f}\n坡度 {s:+.2f}", fontsize=10.5, color=col)

ax.set_xlim(-2, 8); ax.set_ylim(0, 11)
ax.set_xlabel("旋钮的位置")
ax.set_ylabel("损失")
ax.set_title("A 站得高但很平，B 站得低但很陡：一步走多远，看的是坡度不是高度", fontsize=13.5)
fig.tight_layout()
fig.savefig("loss_vs_slope.png", dpi=150)
print("L(A)", round(L(1.0),2), "slope", round(dL(1.0),3), "| L(B)", round(L(3.0),2), "slope", round(dL(3.0),3))
