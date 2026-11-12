"""步长从哪来、怎么判断走对了：同一个碗，三种学习率。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti TC", "STHeiti", "Songti SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"

def run(lr, steps=12, w=0.3):
    ws = [w]
    for _ in range(steps):
        w = w - lr * 2 * (w - 2.0)     # L = (w-2)^2
        ws.append(w)
    return np.array(ws)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(14.5, 5.8), gridspec_kw={"width_ratios": [1.05, 1]})
for lr, c, name in [(0.02, "#9fb4d8", "lr=0.02：步子太小，慢慢挪"),
                    (0.45, TEAL, "lr=0.45：刚好，几步到底"),
                    (1.10, ORANGE, "lr=1.10：步子太大，越走越高")]:
    ws = run(lr)
    a1.plot(range(len(ws)), (ws - 2) ** 2, "o-", color=c, lw=2, ms=4, label=name)
a1.set_yscale("log"); a1.set_ylim(1e-8, 1e3)
a1.set_xlabel("走了几步"); a1.set_ylabel("损失（对数刻度）")
a1.set_title("看损失就能判断：降、稳、还是来回跳", fontsize=13)
a1.legend(fontsize=9)

w = np.linspace(-1.5, 5.5, 300)
a2.plot(w, (w - 2) ** 2, color=INK, lw=2)
for lr, c in [(0.45, TEAL), (0.90, ORANGE)]:
    ws = run(lr, steps=6)
    a2.plot(ws, (ws - 2) ** 2, "-o", color=c, lw=1.4, ms=7, zorder=5, label=f"lr={lr}")
a2.text(0.35, 10.5, "橙色：一脚跨过谷底，到另一边\n再跨回来，来回摆", fontsize=9.5, color=ORANGE)
a2.scatter([2], [0], marker="*", s=240, color=INK, zorder=6)
a2.set_xlabel("旋钮的位置"); a2.set_ylabel("损失")
a2.set_title("同一个碗：橙色在谷底两边来回跨", fontsize=13)
a2.legend(fontsize=9)

fig.suptitle("梯度给方向，学习率给每步走多远；走没走对，由损失说了算", fontsize=15, y=0.99)
fig.tight_layout()
fig.savefig("step_size.png", dpi=150)
print([round(float((run(l)[-1]-2)**2), 4) for l in (0.05, 0.45, 0.95)])
