"""为什么要求导：高度不告诉你方向，坡度才告诉。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["PingFang HK", "Arial Unicode MS", "Heiti TC", "STHeiti", "DejaVu Sans"]
INK, TEAL, ORANGE, MUTED = "#18333d", "#087f8c", "#c66b24", "#5b7079"

fig, (a1, a2) = plt.subplots(1, 2, figsize=(14.5, 5.8), gridspec_kw={"width_ratios": [1.25, 1]})

# 左：山坡 + 切线
x = np.linspace(0.4, 4.0, 200)
y = 3 * x**2 - 4 * x + 5
a1.plot(x, y, color=TEAL, lw=2.6)
x0 = 2.0
y0 = 3 * x0**2 - 4 * x0 + 5
slope = 6 * x0 - 4
a1.plot([1.5, 2.5], [y0 - slope * 0.5, y0 + slope * 0.5], color=ORANGE, lw=2.4, ls="--")
a1.scatter([x0], [y0], s=120, color=ORANGE, zorder=5)
a1.annotate("站在这里：高度 9\n只知道『现在多高』", (x0, y0), xytext=(0.55, 21),
            fontsize=11, color=INK, arrowprops=dict(arrowstyle="->", color="#999"))
a1.annotate("", xy=(2.5, y0 + slope * 0.5), xytext=(2.0, y0),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=3))
a1.text(2.55, y0 + slope * 0.55, "往这边：越来越高", fontsize=10.5, color=ORANGE)
a1.annotate("", xy=(1.6, y0 - slope * 0.4), xytext=(2.0, y0),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=3))
a1.annotate("往这边：越来越低", xy=(1.55, y0 - slope * 0.44), xytext=(0.5, 1.2),
            fontsize=10.5, color=TEAL,
            arrowprops=dict(arrowstyle="-", color=TEAL, lw=0.9, ls=":"))
a1.set_xlim(0.4, 3.9); a1.set_ylim(0, 26)
a1.set_xlabel("旋钮的位置"); a1.set_ylabel("损失（越低越好）")
a1.set_title("高度只告诉你「多糟」，坡度告诉你「往哪走」", fontsize=13.5)

a2.set_xlim(0, 10); a2.set_ylim(0, 10); a2.axis("off")
rows = [("这个旋钮很陡", 8.2, ORANGE, "拧一格，损失变很多"),
        ("这个旋钮有点缓", 5.0, TEAL, "拧一格，损失变一点"),
        ("这个旋钮是平的", 1.8, MUTED, "拧一格，损失几乎不变")]
for name, yy, col, note in rows:
    a2.text(0.2, yy + 0.55, name, fontsize=12, color=col, fontweight="bold")
    a2.plot([0.3, 6.3], [yy, yy], color="#ddd", lw=1)
    a2.plot([0.3, 3.3], [yy, yy + (0.0 if col == MUTED else 0.9)], color=col, lw=3)
    a2.text(6.6, yy - 0.1, note, fontsize=10, color=MUTED)
a2.text(0.2, 0.5, "坡度的大小 = 这个旋钮的『杠杆』：越陡，动一点就越有效。", fontsize=10.5, color=INK)
a2.set_title("每个旋钮各有一根坡度；把它们列出来，就是梯度", fontsize=13.5)

fig.suptitle("为什么要求导：不是算数学题，是摸黑下山时脚下的感觉", fontsize=15, y=0.99)
fig.tight_layout()
fig.savefig("why_derivative.png", dpi=150)
print("saved")
