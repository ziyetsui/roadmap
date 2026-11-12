"""41 维下坡：看不见地形时，靠什么决定往哪走。

左：2 个旋钮的地形（看得见）
中：41 个旋钮的坡度清单（41 个数）
右：只转一个旋钮的切片（一刀一刀看）
下：真跑 41 维，梯度下降 vs 随机瞎走
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["PingFang HK", "Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"

rng = np.random.default_rng(3)
D = 41
t = rng.normal(0, 1, D)                 # 最优点
a = rng.uniform(0.4, 3.0, D)            # 每个方向的陡峭程度
w0 = t + rng.uniform(-2.5, 2.5, D)      # 起点

def loss(w):  return float(np.sum(a * (w - t) ** 2))
def grad(w):  return 2 * a * (w - t)

lr = 0.22
w = w0.copy(); hist = [loss(w)]
for _ in range(80):
    w = w - lr * grad(w)
    hist.append(loss(w))

# 随机瞎走：步长与梯度下降每步位移相同，方向随机
steps = 80
rnd_curves = []
for seed in range(6):
    rg = np.random.default_rng(seed)
    ww = w0.copy(); cur = [loss(ww)]
    wg = w0.copy()
    for _ in range(steps):
        g = grad(wg)
        wg = wg - lr * g
        step = lr * np.linalg.norm(g)
        d = rg.normal(size=D); d /= np.linalg.norm(d)
        ww = ww + step * d
        cur.append(loss(ww))
    rnd_curves.append(cur)
rnd = np.mean(rnd_curves, axis=0)

fig = plt.figure(figsize=(16, 10.5))
gs = fig.add_gridspec(2, 3, height_ratios=[1, 0.95], hspace=0.34, wspace=0.26)

# ① 2 个旋钮的地形
ax = fig.add_subplot(gs[0, 0])
W1, W2 = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
L2 = W1**2 + 3 * W2**2
ax.contourf(W1, W2, L2, levels=18, cmap="YlOrRd")
p = np.array([2.0, 1.6]); path = [p.copy()]
for _ in range(14):
    p = p - 0.18 * np.array([2 * p[0], 6 * p[1]])
    path.append(p.copy())
path = np.array(path)
ax.plot(path[:, 0], path[:, 1], "-o", color=INK, ms=3, lw=1.6)
ax.scatter([0], [0], marker="*", s=200, color=TEAL, zorder=5)
ax.set_title("① 2 个旋钮的地形：看得见，也走得下去", fontsize=13)
ax.set_xlabel("旋钮 1"); ax.set_ylabel("旋钮 2")

# ② 41 个坡度
ax = fig.add_subplot(gs[0, 1])
g0 = grad(w0)
colors = [ORANGE if v > 0 else TEAL for v in g0]
ax.bar(range(1, D + 1), g0, color=colors, width=0.75)
ax.axhline(0, color="#555", lw=0.8)
ax.set_title("② 41 维的『坡度』= 41 个数，不是一张图", fontsize=13)
ax.set_xlabel("第几个旋钮"); ax.set_ylabel("往大拧，损失会变多少")
ax.set_xlabel("第几个旋钮（橙色＝该拧小，青色＝该拧大）")

# ③ 切片
ax = fig.add_subplot(gs[0, 2])
idx = [int(np.argmax(a)), int(np.argmin(a)), 17, 30]
for k, i in enumerate(idx):
    ws = np.linspace(t[i] - 3.5, t[i] + 3.5, 200)
    ax.plot(ws, a[i] * (ws - t[i]) ** 2, lw=1.8, label=f"第 {i+1} 个旋钮")
    ax.scatter([w0[i]], [a[i] * (w0[i] - t[i]) ** 2], s=45, zorder=5)
ax.axvline(0, color="#bbb", lw=0.8, ls=":")
ax.set_title("③ 固定其余 40 个，只转一个：又是一条坡", fontsize=13)
ax.set_xlabel("这个旋钮的位置"); ax.set_ylabel("损失")
ax.legend(fontsize=8.5, loc="upper right")

# ④ 下降曲线
ax = fig.add_subplot(gs[1, :])
ax.plot(hist, color=TEAL, lw=2.4, label="按 41 个坡度走（梯度下降）")
ax.plot(rnd, color=ORANGE, lw=2.0, ls="--", label="随机挑方向走（同样步长）")
ax.set_yscale("log")
ax.set_title("④ 真跑 41 维：看不见地形，损失照样往下掉；瞎走则原地打转", fontsize=13)
ax.annotate("起点 119.6", (0, hist[0]), xytext=(6, -28), textcoords="offset points", fontsize=9.5, color=TEAL)
ax.annotate("80 步后≈0", (steps, hist[-1]), xytext=(-62, 18), textcoords="offset points", fontsize=9.5, color=TEAL)
ax.annotate("瞎走：不降反升", (45, rnd[45]), xytext=(0, -18), textcoords="offset points", fontsize=9.5, color=ORANGE)
ax.set_xlabel("走了几步"); ax.set_ylabel("损失（对数刻度）")
ax.legend(fontsize=10)

fig.suptitle("41 个旋钮怎么下坡：你不需要看见山，只需要量出 41 个数", fontsize=17, y=0.965)
fig.savefig("dim41.png", dpi=140)
print("start loss", round(hist[0], 2), "end", round(hist[-1], 3), "random end", round(rnd[-1], 2))
