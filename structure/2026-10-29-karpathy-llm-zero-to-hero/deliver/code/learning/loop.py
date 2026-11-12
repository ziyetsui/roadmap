"""把“分发”和“下山”接起来：一个循环，四个动作，跑一轮看数字。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
import numpy as np

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"

fig, (a, b) = plt.subplots(1, 2, figsize=(15.5, 6.4), gridspec_kw={"width_ratios": [1, 1.15]})
for ax in (a, b):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

def box(ax, x, y, txt, color=INK, w=0.34, h=0.16, fs=11):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02",
                                fc="white", ec=color, lw=1.9, zorder=3))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=color, zorder=4)

# ── 左：循环 ──
box(a, 0.50, 0.86, "① 前向：走一遍，算出损失", color=TEAL, w=0.62, h=0.13)
box(a, 0.82, 0.52, "② 反向：分发\n得到 41 个坡度", color=ORANGE, w=0.30, h=0.16, fs=10)
box(a, 0.50, 0.16, "③ 拧：每个旋钮\n按自己的坡度走一小步", color=INK, w=0.52, h=0.16, fs=10)
a.add_patch(FancyArrowPatch((0.72, 0.80), (0.80, 0.61), arrowstyle="-|>", mutation_scale=16, color=ORANGE, lw=2.2))
a.add_patch(FancyArrowPatch((0.72, 0.45), (0.66, 0.25), arrowstyle="-|>", mutation_scale=16, color=INK, lw=2.2))
a.add_patch(FancyArrowPatch((0.32, 0.22), (0.22, 0.78), arrowstyle="-|>", mutation_scale=16, color=TEAL, lw=2.2,
                            connectionstyle="arc3,rad=0.35"))
a.text(0.10, 0.50, "再量一次\n（损失应更小）", fontsize=9.5, color=TEAL, ha="center")
a.set_title("两个画面是同一件事的两半：一个量，一个走", fontsize=13.5)

# ── 右：跑一轮的真实数字 ──
steps = [
    ("开始", "w1=1.00  w2=2.00", "损失 64.0"),
    ("前向", "1×2 + 2×3 = 8", "存下 8 和 64"),
    ("反向", "16 分发：16×2=32\n16×3=48", "坡度 (32, 48)"),
    ("拧一步", "lr=0.01：w1=0.68\nw2=1.52", "损失 35.1"),
]
y = 0.90
for i, (name, mid, res) in enumerate(steps):
    b.add_patch(FancyBboxPatch((0.02, y - 0.095), 0.23, 0.19, boxstyle="round,pad=0.02",
                               fc="#f3f7f6", ec="#cfd8d6", lw=1.2))
    b.text(0.135, y, name, ha="center", va="center", fontsize=11, color=INK)
    b.text(0.34, y + 0.02, mid, fontsize=9.5, color=MUTED, va="center")
    b.text(0.66, y - 0.04, res, fontsize=11, color=TEAL if i in (3,) else INK, va="center")
    if i < 3:
        b.annotate("", xy=(0.13, y - 0.20), xytext=(0.13, y - 0.11),
                   arrowprops=dict(arrowstyle="-|>", color="#b9c4c2", lw=1.6))
    y -= 0.235
b.text(0.03, 0.03, "同一次反向里，16 只算一次；41 个旋钮就是 41 次乘法。拧完再跑前向，就是下一轮。",
       fontsize=9.5, color=MUTED)
b.set_title("同一个例子跑一轮：64 → 35", fontsize=13.5)

fig.suptitle("反向传播是“量坡度的仪器”，梯度下降是“按坡度走的那条腿”", fontsize=16, y=0.99)
fig.tight_layout()
fig.savefig("loop.png", dpi=150, facecolor="white")
print("saved")
