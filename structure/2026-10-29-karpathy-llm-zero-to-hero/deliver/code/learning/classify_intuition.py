"""分类的三个零件：分数轴、sigmoid、分界线。

例子：判断邮件是不是垃圾邮件
特征：x1 = 「免费」出现次数，x2 = 链接个数
分数：z = 1*x1 - 2*x2 + 0.5
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["PingFang HK", "Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(16, 5.4))

# ── 左：分数轴 ──────────────────────────────────────────────
zs = np.linspace(-4, 4, 400)
a1.axhline(0, color="#bbb", lw=1)
for z, lab, col, dy in [(-2.5, "免费 1 次、链接 2 个", "#087f8c", 22),
                        (-0.5, "免费 3 次、链接 2 个", "#c66b24", -34),
                        (3.5, "免费 5 次、链接 1 个", "#087f8c", 22)]:
    a1.scatter([z], [0], s=90, color=col, zorder=5)
    a1.annotate(lab, (z, 0), xytext=(0, dy), textcoords="offset points",
                ha="center", fontsize=9, color=col)
a1.axvline(0, color="#c66b24", ls="--", lw=1.4)
a1.text(0.08, 0.9, "门槛：分数 > 0 判为垃圾", fontsize=10, color="#c66b24")
a1.set_xlim(-4.2, 4.4); a1.set_ylim(-0.8, 1.0)
a1.set_yticks([]); a1.set_xlabel("分数  z = w·x + b")
a1.set_title("第一步：先算一个分数", fontsize=13)

# ── 中：sigmoid ────────────────────────────────────────────
z = np.linspace(-8, 8, 400)
s = 1 / (1 + np.exp(-z))
a2.plot(z, s, color="#087f8c", lw=2.4)
a2.axhline(0.5, color="#ccc", lw=1, ls=":")
a2.axvline(0, color="#ccc", lw=1, ls=":")
for zz, txt in [(-2, "12%"), (0, "50%"), (2, "88%")]:
    p = 1 / (1 + np.exp(-zz))
    a2.scatter([zz], [p], s=70, color="#c66b24", zorder=5)
    a2.annotate(txt, (zz, p), xytext=(8, 8), textcoords="offset points", fontsize=10, color="#c66b24")
a2.set_xlabel("分数 z"); a2.set_ylabel("“是垃圾邮件”的把握")
a2.set_title("第二步：把分数压成 0–100%", fontsize=13)
a2.set_ylim(-0.03, 1.03)

# ── 右：b 让分界线平移 ─────────────────────────────────────
rng = np.random.default_rng(7)
x1_spam = rng.uniform(3, 5, 6); x2_spam = rng.uniform(0.5, 2.0, 6)
x1_ok = rng.uniform(0.5, 3.0, 6); x2_ok = rng.uniform(2.2, 4.2, 6)
a3.scatter(x1_spam, x2_spam, color="#c66b24", s=55, label="垃圾邮件")
a3.scatter(x1_ok, x2_ok, color="#087f8c", s=55, label="正常邮件")
xx = np.linspace(0, 6, 100)
a3.plot(xx, (xx + 0.5) / 2, color="#c66b24", lw=2, label="b = 0.5")
a3.plot(xx, (xx + 2.5) / 2, color="#c66b24", lw=2, ls="--", label="b = 2.5（线整体左下移）")
a3.set_xlim(0, 6); a3.set_ylim(0, 5)
a3.set_xlabel("x1：「免费」出现次数"); a3.set_ylabel("x2：链接个数")
a3.set_title("b 是什么：把整条线挪一挪", fontsize=13)
a3.legend(fontsize=8.5, loc="upper right")

fig.suptitle("分类就三件事：算分数 → 变概率 → 挪分界线", fontsize=15, y=0.99)
fig.tight_layout()
out = "/Users/ziye/Documents/wiki/system/roadmap/structure/2026-10-29-karpathy-llm-zero-to-hero/deliver/code/learning/classify_intuition.png"
fig.savefig(out, dpi=150)
print("saved", out)
