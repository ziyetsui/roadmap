"""分类的空间版：不写公式，只看东西被挪到哪里。

图 1：邮件是平面上的点 → 加一个方向 → 沿方向量出一根尺子 → b 挪零点
图 2：尺子弯成把握 → 答错罚多重 → 分界线怎么挪
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["PingFang HK", "Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

SPAM = "#c66b24"
OK = "#087f8c"
INK = "#18333d"

x1 = np.array([4.5, 5.0, 3.8, 4.2, 5.5, 1.0, 0.8, 2.0, 1.5, 2.5])
x2 = np.array([1.0, 1.5, 0.8, 1.8, 1.2, 3.0, 3.5, 2.8, 4.0, 3.2])
lab = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])   # 1=垃圾
col = np.where(lab == 1, SPAM, OK)

def score(x1, x2, b=0.5):
    return x1 - x2 + b

# ══════════════ 图 1 ══════════════
fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(16.5, 5.6))

a1.scatter(x1[lab == 1], x2[lab == 1], s=110, color=SPAM, label="垃圾邮件", zorder=5)
a1.scatter(x1[lab == 0], x2[lab == 0], s=110, color=OK, label="正常邮件", zorder=5)
a1.set_xlim(0, 6.4); a1.set_ylim(0, 4.6)
a1.set_xlabel("横轴：『免费』出现几次")
a1.set_ylabel("纵轴：链接几个")
a1.set_title("① 每封邮件 = 平面上的一个点", fontsize=13)
a1.legend(loc="upper right", fontsize=9)

u = np.array([1, -1]) / np.sqrt(2)
a2.scatter(x1[lab == 1], x2[lab == 1], s=110, color=SPAM, zorder=5)
a2.scatter(x1[lab == 0], x2[lab == 0], s=110, color=OK, zorder=5)
for xx, yy in zip(x1, x2):
    t = (np.array([xx, yy]) @ u)
    foot = t * u
    a2.plot([xx, foot[0]], [yy, foot[1]], ls=":", color="#aaa", lw=1)
    a2.scatter([foot[0]], [foot[1]], s=22, color="#555", zorder=4)
a2.annotate("", xy=(4.6 * u[0], 4.6 * u[1]), xytext=(-2.2 * u[0], -2.2 * u[1]),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2))
a2.text(3.1, -3.1, "w：往这个方向看", color=INK, fontsize=11, rotation=-35)
a2.set_xlim(-3, 6.4); a2.set_ylim(-4.2, 4.6)
a2.set_title("② 选一个方向，把每个点‘压’到这条线上", fontsize=13)
a2.set_xlabel("沿箭头量距离，就得到一个数")

s = score(x1, x2)
a3.axhline(0, color="#ddd", lw=1)
for v, c in zip(s, col):
    a3.plot([v, v], [-0.16, 0.16], color=c, lw=6, solid_capstyle="butt")
a3.axvline(0, color=SPAM, ls="--", lw=1.5)
a3.text(0.15, 0.55, "门槛 0：右边判垃圾，左边判正常", color=SPAM, fontsize=10.5)
a3.annotate("这根尺子的 0 点在哪，是 b 定的：\nb 调大，0 点就往下挪，判定更松",
            xy=(-0.05, -0.5), xytext=(-3.0, -0.95), fontsize=9.5, color="#555",
            arrowprops=dict(arrowstyle="->", color="#888"))
a3.set_xlim(-3.2, 5.2); a3.set_ylim(-1.2, 1.1)
a3.set_yticks([]); a3.set_xlabel("量出来的分数")
a3.set_title("③ 分数是一根尺子，判定只是看它落在 0 的哪边", fontsize=13)

fig.suptitle("空间版（一）：邮件先变成点，再被压成一根尺子", fontsize=16, y=0.99)
fig.tight_layout()
fig.savefig("classify_space_1.png", dpi=150)

# ══════════════ 图 2 ══════════════
fig, (b1, b2, b3) = plt.subplots(1, 3, figsize=(16.5, 5.6))

z = np.linspace(-8, 8, 400)
p = 1 / (1 + np.exp(-z))
b1.plot(z, p, color=OK, lw=2.6)
b1.axhline(0.5, color="#ccc", ls=":")
b1.axvline(0, color="#ccc", ls=":")
for zz, txt in [(-2, "12%"), (0, "50%"), (2, "88%")]:
    pp = 1 / (1 + np.exp(-zz))
    b1.scatter([zz], [pp], s=80, color=SPAM, zorder=5)
    b1.annotate(txt, (zz, pp), xytext=(9, 8), textcoords="offset points", fontsize=11, color=SPAM)
b1.set_xlabel("尺子上的分数")
b1.set_ylabel("说‘是垃圾’的把握")
b1.set_title("④ 把尺子弯一下：两头挤成 0% 和 100%", fontsize=13)
b1.set_ylim(-0.03, 1.03)

pp = np.linspace(0.01, 0.99, 300)
pen = -np.log(pp)
b2.plot(pp * 100, pen, color=SPAM, lw=2.6)
for ppp, txt in [(0.1, "答错还嘴硬\n罚 2.30"), (0.5, "半信半疑\n罚 0.69"), (0.9, "答对又自信\n罚 0.10")]:
    b2.scatter([ppp * 100], [-np.log(ppp)], s=80, color=INK, zorder=5)
    b2.annotate(txt, (ppp * 100, -np.log(ppp)), xytext=(10, 6), textcoords="offset points", fontsize=10, color=INK)
b2.set_xlabel("模型说‘是垃圾’的把握（%）")
b2.set_ylabel("罚多重")
b2.set_title("⑤ 罚分尺：越自信又越错，罚得越狠", fontsize=13)
b2.set_ylim(0, 4.8)

b3.scatter(x1[lab == 1], x2[lab == 1], s=100, color=SPAM, zorder=5)
b3.scatter(x1[lab == 0], x2[lab == 0], s=100, color=OK, zorder=5)
xx = np.linspace(0, 6.4, 50)
for i, (slope, b0, ls) in enumerate([(0.25, 3.2, ":"), (1.4, -0.2, "--"), (1.0, 0.5, "-")]):
    yy = slope * xx + b0
    pred = (x2 < slope * x1 + b0).astype(int)
    n_err = int(np.sum(pred != lab))
    b3.plot(xx, yy, ls=ls, color=INK if ls != "-" else SPAM, lw=2,
            label=f"第 {i+1} 次：错 {n_err} 个")
b3.set_xlim(0, 6.4); b3.set_ylim(0, 4.6)
b3.set_xlabel("横轴：『免费』次数")
b3.set_ylabel("纵轴：链接数")
b3.set_title("⑥ 训练 = 一次次挪线，直到两边都站对", fontsize=13)
b3.legend(loc="lower right", fontsize=8.5)

fig.suptitle("空间版（二）：弯尺子、量罚分、挪分界线", fontsize=16, y=0.99)
fig.tight_layout()
fig.savefig("classify_space_2.png", dpi=150)
print("saved")
