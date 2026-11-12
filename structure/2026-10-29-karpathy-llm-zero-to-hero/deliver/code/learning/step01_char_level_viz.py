"""字符级 bigram 的“空间转换”可视化：把一个名字拆成珠子，再一路变成矩阵与概率。

运行：
    python3 step01_char_level_viz.py

产出两张图（与脚本同目录）：
    01_string_to_onehot.png  字符串 → 编号 (6,) → one-hot (6,27)
    02_onehot_to_sample.png  计数矩阵 27×27 → 一行概率 → 逐个字符抽样

所有数字都来自 ../makemore/names.txt 的真实统计，不是编的。
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

plt.rcParams["font.sans-serif"] = [
    "PingFang HK", "PingFang SC", "Arial Unicode MS",
    "Heiti TC", "STHeiti", "Songti SC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False

HERE = Path(__file__).resolve().parent
NAMES = HERE.parent / "makemore" / "names.txt"
OUT = HERE

# ── 1. 读名字，建 27 格词表 ─────────────────────────────────────────
words = NAMES.read_text().split()
chars = sorted(set("".join(words)))          # a..z 共 26 个
ITOS = ["."] + chars                         # 点号放 0 号位
STOI = {c: i for i, c in enumerate(ITOS)}
V = len(ITOS)                                # 27

# ── 2. 数 bigram：每个名字前后补点号，数相邻两字符 ──────────────────
N = np.zeros((V, V), dtype=np.int64)
for w in words:
    seq = ["."] + list(w) + ["."]
    for c1, c2 in zip(seq, seq[1:]):
        N[STOI[c1], STOI[c2]] += 1

name = "emma"
beads = ["."] + list(name) + ["."]           # . e m m a .
ids = [STOI[c] for c in beads]

print(f"词表 {V} 格：{''.join(ITOS)}")
print(f"{name!r} → 珠子 {beads} → 编号 {ids}")
print(f"p(e|.) = {N[0, STOI['e']] / N[0].sum():.4f}")

TITLE_COLOR = "#1a1a1a"
MUTED = "#666666"

# ══════════════════════════════════════════════════════════════════
# 图 1：字符串 → 编号 → one-hot
# ══════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(13.5, 9.8))
gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.3], height_ratios=[0.95, 1.0],
                      left=0.045, right=0.97, top=0.875, bottom=0.105,
                      hspace=0.40, wspace=0.14)

fig.text(0.5, 0.975, "一个名字的两次空间转换：字符串 → 编号 → one-hot 矩阵",
         ha="center", fontsize=20, fontweight="bold", color=TITLE_COLOR)
fig.text(0.5, 0.938, "同一个东西换了三件衣服；每次转换，数据的形状都变一次",
         ha="center", fontsize=11.5, color="#555555")

# ── 面板 ①：珠子 ───────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 0])
ax.set_xlim(-0.75, len(beads) - 0.25)
ax.set_ylim(-1.45, 0.95)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("① 名字不是整体，是 6 颗珠子", fontsize=13.5, loc="left", pad=10)

ax.plot([-0.35, len(beads) - 0.65], [0, 0], color="#c4c4c4", lw=3, zorder=0)
for i, ch in enumerate(beads):
    edge = ch == "."
    ax.add_patch(Circle((i, 0), 0.31, facecolor="#ffe9d6" if edge else "#dce9ff",
                        edgecolor="#e07a2f" if edge else "#3b6fd4", lw=2, zorder=2))
    ax.text(i, 0, ch, ha="center", va="center", fontsize=18,
            fontweight="bold", color="#a3410a" if edge else "#123a8a", zorder=3)

ax.text(0, -0.62, "开场", ha="center", fontsize=9, color="#a3410a")
ax.text(len(beads) - 1, -0.62, "收尾", ha="center", fontsize=9, color="#a3410a")
ax.text(-0.7, -1.05, "点号不是字母，只是两个路标：一个说“开始猜”，\n一个说“到这里停”。",
        fontsize=9.5, color=MUTED, va="top")

# ── 面板 ②：27 格货架 ──────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 1])
ax.set_xlim(0, 9)
ax.set_ylim(0, 4.0)
ax.axis("off")
ax.set_title("② 货架只有 27 格：26 个字母 + 1 个点号", fontsize=13.5, loc="left", pad=10)

for idx, ch in enumerate(ITOS):
    r, c = divmod(idx, 9)
    y = 3.30 - r * 1.03
    used = ch in beads
    ax.add_patch(plt.Rectangle((c + 0.07, y - 0.40), 0.86, 0.80,
                               facecolor="#ffe0c2" if used else "#f3f5f8",
                               edgecolor="#e07a2f" if used else "#cfd6df",
                               lw=1.9 if used else 1.0))
    ax.text(c + 0.5, y + 0.09, ch, ha="center", va="center",
            fontsize=13, fontweight="bold" if used else "normal",
            color="#a3410a" if used else "#5b6672")
    ax.text(c + 0.5, y - 0.24, str(idx), ha="center", va="center",
            fontsize=7.5, color="#b4551a" if used else "#98a2ad")

ax.text(0, 0.10, "橙色 = emma 用到的 4 格；格子角上的小数字就是编号，顺序固定",
        fontsize=9.5, color=MUTED)

# ── 面板 ③：编号向量 ───────────────────────────────────────────────
ax = fig.add_subplot(gs[1, 0])
ax.set_xlim(-0.75, len(ids) - 0.25)
ax.set_ylim(-1.05, 1.05)
ax.axis("off")
ax.set_title("③ 查表得到编号向量，形状 (6,)", fontsize=13.5, loc="left", pad=10)

for i, (ch, k) in enumerate(zip(beads, ids)):
    ax.add_patch(plt.Rectangle((i - 0.34, -0.34), 0.68, 0.56,
                               facecolor="#dce9ff", edgecolor="#3b6fd4", lw=1.6))
    ax.text(i, -0.06, str(k), ha="center", va="center", fontsize=16,
            fontweight="bold", color="#123a8a")
    ax.text(i, 0.42, ch, ha="center", fontsize=11, color="#666")
    ax.annotate("", xy=(i, 0.21), xytext=(i, 0.34),
                arrowprops=dict(arrowstyle="->", color="#9fb4d8", lw=1.0))

ax.text(-0.7, -0.72, "编号本身没有大小含义：m 是 13 号、a 是 1 号，\n"
                     "只表示它放在第几格，不代表 m 比 a “大”。",
        fontsize=9.5, color=MUTED, va="top")

# ── 面板 ④：one-hot 矩阵 ───────────────────────────────────────────
ax = fig.add_subplot(gs[1, 1])
oh = np.zeros((len(ids), V))
for r, k in enumerate(ids):
    oh[r, k] = 1
ax.imshow(oh, aspect="auto", cmap="Blues", vmin=0, vmax=1.4)
ax.set_xticks(range(V))
ax.set_xticklabels(ITOS, fontsize=7.5)
ax.set_yticks(range(len(ids)))
ax.set_yticklabels([f"{c} → {k}" for c, k in zip(beads, ids)], fontsize=9)
ax.set_title("④ 编号摊成 one-hot 矩阵，形状 (6, 27)", fontsize=13.5, loc="left", pad=10)
ax.set_xlabel("每一行只有 1 个格子是 1，其余 26 个都是 0", fontsize=9.5, color="#555")
ax.tick_params(length=0)
for r, k in enumerate(ids):
    ax.text(k, r, "1", ha="center", va="center", fontsize=8.5,
            color="white", fontweight="bold")
for s in ax.spines.values():
    s.set_color("#cccccc")

fig.text(0.5, 0.030,
         'str "emma"  →  list[int] (6,)  →  one-hot (6, 27)  →  '
         '× W (27, 27)  =  logits (6, 27)  →  softmax  →  概率 (6, 27)',
         ha="center", fontsize=9.6, color="#333")
fig.savefig(OUT / "01_string_to_onehot.png", dpi=160)
plt.close(fig)

# ══════════════════════════════════════════════════════════════════
# 图 2：计数矩阵 → 一行概率 → 逐个字符抽样
# ══════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(13.5, 10.6))
gs = fig.add_gridspec(2, 2, width_ratios=[1.12, 1.0], height_ratios=[1.0, 0.92],
                      left=0.05, right=0.965, top=0.875, bottom=0.055,
                      hspace=0.44, wspace=0.20)

fig.text(0.5, 0.975, "从一张 27×27 的计数表，到把名字一个字一个字抽出来",
         ha="center", fontsize=20, fontweight="bold", color=TITLE_COLOR)
fig.text(0.5, 0.938,
         f"统计自 {len(words):,} 个名字：每个名字补上点号，数相邻两个字符一起出现过多少次",
         ha="center", fontsize=11.5, color="#555555")

# ── 面板 ⑤：27×27 计数热力图 ──────────────────────────────────────
ax = fig.add_subplot(gs[0, 0])
im = ax.imshow(np.log1p(N), aspect="auto", cmap="YlOrRd")
ax.set_xticks(range(V))
ax.set_xticklabels(ITOS, fontsize=6.8)
ax.set_yticks(range(V))
ax.set_yticklabels(ITOS, fontsize=6.8)
ax.set_xlabel("后一个字符（第 0 列的点号也充当 END）", fontsize=10, labelpad=6)
ax.set_ylabel("当前字符", fontsize=10, labelpad=6)
ax.set_title("⑤ 计数矩阵 N：第 i 行第 j 列 = “i 后面跟 j”出现过几次",
             fontsize=12.5, loc="left", pad=10)
ax.tick_params(length=0)
ax.add_patch(plt.Rectangle((-0.5, -0.5), V, 1, fill=False, edgecolor="#1b6ec2", lw=2.4))
ax.add_patch(plt.Rectangle((-0.5, -0.5), 1, V, fill=False, edgecolor="#1b6ec2",
                           lw=2.4, linestyle=":"))
ax.text(-1.4, 0, "START", fontsize=7.5, color="#1b6ec2", ha="right", va="center",
        clip_on=False)
cb = fig.colorbar(im, ax=ax, fraction=0.036, pad=0.02)
cb.set_label("log(1+次数)", fontsize=8.5)
cb.ax.tick_params(labelsize=7.5)

# ── 面板 ⑥：一行 one-hot 乘 N = 取出一行 ──────────────────────────
ax = fig.add_subplot(gs[1, 0])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("⑥ 一行 one-hot 乘 N，等于把那一行“取”出来", fontsize=12.5,
             loc="left", pad=10)

ax.text(0.0, 0.87, "one-hot 行  [1, 0, 0, …, 0]   ×   N (27×27)   =   N 的第 0 行",
        fontsize=12, color="#333")
ax.text(0.0, 0.70,
        "0 乘任何数都是 0，只有 1 所在的位置活下来：\n"
        "所以这一步的“矩阵乘法”只是查表 —— 选出“点号后面跟什么”的 27 个计数。",
        fontsize=10, color="#444", va="top")

row = N[0]
p = row / row.sum()
order = np.argsort(p)[::-1]
ax.text(0.0, 0.30, "点号这一行的前 6 名（计数）：", fontsize=9.5, color=MUTED)
ax.text(0.0, 0.17, "   ".join(f"{ITOS[j]} {row[j]}" for j in order[:6]),
        fontsize=12, color="#333")

# ── 面板 ⑦：归一化成概率条 ────────────────────────────────────────
ax = fig.add_subplot(gs[0, 1])
colors = ["#d9dde3"] * V
colors[STOI["e"]] = "#e07a2f"
ax.bar(range(V), p * 100, color=colors, width=0.78)
ax.set_xticks(range(V))
ax.set_xticklabels(ITOS, fontsize=6.8)
ax.set_ylabel("概率 %", fontsize=10)
ax.set_title("⑦ 除以总和，变成“下一个字符是谁”的概率", fontsize=12.5, loc="left", pad=10)
ax.tick_params(length=0)
ax.set_ylim(0, max(p) * 100 * 1.42)
for j in order[:4]:
    ax.text(j, p[j] * 100 + 0.5, f"{p[j]*100:.1f}%", ha="center", fontsize=7.5, color="#333")
ax.annotate(f"e 只有 {p[STOI['e']]*100:.2f}%\n但这次偏偏抽中它",
            xy=(STOI["e"] + 0.45, p[STOI["e"]] * 100 + 0.3),
            xytext=(2.0, max(p) * 100 * 0.75),
            fontsize=9, color="#a3410a",
            arrowprops=dict(arrowstyle="->", color="#a3410a", lw=1.2))
ax.text(0.02, 0.92, "这一整行加起来 = 100%", transform=ax.transAxes,
        fontsize=9, color=MUTED)

# ── 面板 ⑧：六次抽签 ──────────────────────────────────────────────
ax = fig.add_subplot(gs[1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("⑧ 一个名字 = 五次抽签，每次只看前一个字符", fontsize=12.5,
             loc="left", pad=10)

rows = [("START", "e"), ("e", "m"), ("m", "m"), ("m", "a"), ("a", "END")]
ax.text(0.02, 0.94, "当前上下文", fontsize=8.5, color="#999")
ax.text(0.34, 0.94, "抽到", fontsize=8.5, color="#999")
ax.text(0.52, 0.94, "这一步概率", fontsize=8.5, color="#999")

y = 0.84
probs = []
for cur, nxt in rows:
    tgt = "." if nxt == "END" else nxt
    k = 0 if cur == "START" else STOI[cur[0]]
    prob = N[k, STOI[tgt]] / N[k].sum()
    probs.append(prob)
    ax.plot([0.02, 0.88], [y + 0.055, y + 0.055], color="#ececec", lw=0.8, zorder=0)
    ax.text(0.02, y, f'"{cur}"', fontsize=11, color="#333")
    ax.text(0.34, y, f'{tgt if tgt != "." else "·"}', fontsize=12,
            color="#a3410a", fontweight="bold")
    ax.text(0.52, y, f"{prob*100:.2f}%", fontsize=10.5, color="#333")
    y -= 0.135

total = math.prod(probs)
ax.plot([0.02, 0.88], [y + 0.02, y + 0.02], color="#bbb", lw=1.2)
ax.text(0.02, y - 0.10,
        f'p(".emma.") = {" × ".join(f"{q*100:.1f}%" for q in probs)} '
        f'≈ {total:.2e}',
        fontsize=9.2, color="#1b6ec2")
ax.text(0.02, y - 0.26,
        f'取负对数：−log p = {-math.log(total):.2f}  （这就是这个名字的“惊讶程度”）',
        fontsize=9.2, color="#1b6ec2")
ax.text(0.02, y - 0.46,
        "训练时，27×27 这 729 个数会被调来调去：\n"
        "真实名字的这条路概率变大，乱拼出来的名字概率变小。",
        fontsize=9.2, color=MUTED, va="top")

fig.savefig(OUT / "02_onehot_to_sample.png", dpi=160)
plt.close(fig)

print("已写出：", OUT / "01_string_to_onehot.png")
print("已写出：", OUT / "02_onehot_to_sample.png")
