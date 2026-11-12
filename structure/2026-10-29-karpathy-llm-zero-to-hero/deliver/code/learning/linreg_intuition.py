"""用最简单的线性回归看“梯度下降在干什么”：数据不动，线在动。

数据：x=1..4，y=2x（四个点正好排在 y=2x 这条线上）
模型：pred = w·x（只有一个旋钮 w，截距先设为 0）
损失：L(w) = mean((w·x - y)²)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["PingFang HK", "Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

xs = np.array([1.0, 2.0, 3.0, 4.0])
ys = 2.0 * xs

def loss(w):
    return float(np.mean((w * xs - ys) ** 2))

def grad(w):
    return float(np.mean(2 * (w * xs - ys) * xs))

w, lr = 0.5, 0.05
hist = [(w, loss(w))]
for _ in range(5):
    w = w - lr * grad(w)
    hist.append((w, loss(w)))

print("w path:", [round(h[0], 4) for h in hist])
print("loss path:", [round(h[1], 4) for h in hist])
print("target w = 2.0")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(13.5, 5.6))

a1.scatter(xs, ys, s=90, color="#c66b24", zorder=5, label="固定的数据点")
grid = np.linspace(0, 4.3, 10)
for i, (wv, lv) in enumerate(hist[:4]):
    a1.plot(grid, wv * grid, lw=1.8, alpha=0.9,
            color=plt.cm.Blues(0.35 + 0.17 * i),
            label=f"第 {i} 步  w={wv:.3f}  L={lv:.3f}")
a1.plot(grid, 2 * grid, "--", lw=1.4, color="#087f8c", label="目标线 y=2x（w=2）")
a1.set_xlim(0, 4.3); a1.set_ylim(0, 9)
a1.set_xlabel("x"); a1.set_ylabel("y")
a1.set_title("数据不动，线在动", fontsize=14)
a1.legend(fontsize=8.5, loc="upper left")

ws = np.linspace(0, 2.6, 200)
a2.plot(ws, 7.5 * (ws - 2) ** 2, color="#087f8c", lw=2)
a2.scatter([h[0] for h in hist], [h[1] for h in hist], s=70, color="#c66b24", zorder=5)
for i, (wv, lv) in enumerate(hist[:3]):
    a2.annotate(f"{i}", (wv, lv), textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=9, color="#c66b24")
a2.annotate("第 2 步之后，误差每步再缩到约 1/4", (1.55, 8.0), fontsize=9.5, color="#5b7079")
a2.set_xlabel("w（旋钮位置）"); a2.set_ylabel("L(w) 损失")
a2.set_title("损失是一条碗形曲线：w 一步步滑到谷底", fontsize=14)
a2.set_xlim(0, 2.7); a2.set_ylim(0, 17)

fig.suptitle("线性回归里的梯度下降：每步损失 16.875 → 1.055 → 0.066 → 0.004", fontsize=13)
fig.tight_layout()
fig.savefig("/Users/ziye/Documents/wiki/system/roadmap/structure/2026-10-29-karpathy-llm-zero-to-hero/deliver/code/learning/linreg_intuition.png", dpi=150)
print("saved")
