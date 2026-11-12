"""步骤 2 验收脚本：把“做完的标准”变成可运行的检查。

用法：先确保 step02_micrograd_walkthrough.py 在同一目录，然后
    python3 step02_verify.py

检查项：
  1. 乘法偏导：手算 / micrograd / 有限差分 三方对照
  2. tanh 导数：手算 1-t² / micrograd / 有限差分 三方对照
  3. 梯度累加：e = a*a + a 在 a=3 处应为 2a+1 = 7（两条路径不能覆盖）
  4. 一次参数更新：w 从 0 到 1.6，loss 从 16 到 0.64
  5. 与 PyTorch 逐个参数对照：同一组权重、同一批样本，loss 和全部梯度一致
任何一项超出容差都会打印 FAIL 并以非零码退出。
"""
import math
import random
import sys

import step02_micrograd_walkthrough as mg

TOL = 1e-9          # micrograd（float64）内部对照容差
FD_TOL = 1e-6       # 有限差分容差，取中心差分 h=1e-6 时约 1e-10 误差
results = []        # (是否通过, 描述)


def check(label, ok, detail=""):
    results.append((ok, label))
    print(("  PASS  " if ok else "  FAIL  ") + label + (f"   {detail}" if detail else ""))


def fd(f, h=1e-6):
    """中心差分：比单侧差分精度高一阶。"""
    return (f(h) - f(-h)) / (2 * h)


print("=" * 68)
print("1. 乘法偏导 d = a*b+c：∂d/∂a=3, ∂d/∂b=2, ∂d/∂c=1")
print("=" * 68)
a, b, c = mg.Value(2), mg.Value(3), mg.Value(4)
d = a * b + c
d.backward()
check("d.data == 10", d.data == 10.0, f"实际 {d.data}")
check("∂d/∂a == 3", abs(a.grad - 3) < TOL, f"实际 {a.grad}")
check("∂d/∂b == 2", abs(b.grad - 2) < TOL, f"实际 {b.grad}")
check("∂d/∂c == 1", abs(c.grad - 1) < TOL, f"实际 {c.grad}")

# 有限差分独立再验一遍：只动一个输入，其他不动
for name, expected, f in [
    ("∂d/∂a", 3, lambda h: (2 + h) * 3 + 4),
    ("∂d/∂b", 2, lambda h: 2 * (3 + h) + 4),
    ("∂d/∂c", 1, lambda h: 2 * 3 + (4 + h)),
]:
    est = fd(f)
    check(f"{name} 与有限差分一致", abs(est - expected) < FD_TOL, f"差分={est:.9f}")

print()
print("=" * 68)
print("2. tanh 导数：手算 1-tanh(x)² / micrograd / 有限差分")
print("=" * 68)
print("     x       手算 1-t²      micrograd      有限差分     最大偏差")
for x in (-2.0, -0.5, 0.0, 0.5, 2.0):
    t = math.tanh(x)
    hand = 1 - t * t

    v = mg.Value(x)
    v.tanh().backward()
    auto = v.grad

    est = fd(lambda h: math.tanh(x + h))
    dev = max(abs(hand - auto), abs(hand - est))
    check(f"x={x:+.1f} 三方一致", dev < FD_TOL,
          f"手算={hand:.9f} 自动={auto:.9f} 差分={est:.9f} 偏差={dev:.2e}")

# 手算/自动应严格一致（同一公式），差分允许 1e-6 级误差
v = mg.Value(0.5)
v.tanh().backward()
check("手算与 micrograd 精确一致(<1e-12)",
      abs((1 - math.tanh(0.5) ** 2) - v.grad) < 1e-12, f"{v.grad:.15f}")

print()
print("=" * 68)
print("3. 梯度累加：e = a*a + a，a=3 时 de/da = 2a+1 = 7")
print("=" * 68)
a = mg.Value(3)
e = a * a + a          # a 同时是乘法的一个输入、加法的一个输入
e.backward()
check("e.data == 12", e.data == 12.0, f"实际 {e.data}")
check("de/da == 7（不是 6，也不是 1）", abs(a.grad - 7) < TOL, f"实际 {a.grad}")

# 单独再看 a+a 与 a*a，各用新建的 a，避免上一张图的 grad 混进来
a = mg.Value(3)
(a + a).backward()
check("a+a 的导数为 2", abs(a.grad - 2) < TOL, f"实际 {a.grad}")
a = mg.Value(3)
(a * a).backward()
check("a*a 的导数为 6", abs(a.grad - 6) < TOL, f"实际 {a.grad}")

print()
print("=" * 68)
print("4. 一次参数更新：w=0, loss=(2w-4)², lr=0.1")
print("=" * 68)
w = mg.Value(0)
loss = (w * 2 - 4) ** 2
loss.backward()
check("初始 loss == 16", abs(loss.data - 16) < TOL, f"实际 {loss.data}")
check("w.grad == -16", abs(w.grad + 16) < TOL, f"实际 {w.grad}")
w.data -= 0.1 * w.grad
new_loss = (w * 2 - 4) ** 2
check("w 更新为 1.6", abs(w.data - 1.6) < TOL, f"实际 {w.data}")
check("更新后 loss == 0.64", abs(new_loss.data - 0.64) < TOL, f"实际 {new_loss.data}")
check("旧 loss 仍是 16（旧图不会自动重印）", abs(loss.data - 16) < TOL, f"实际 {loss.data}")

print()
print("=" * 68)
print("5. 与 PyTorch 同一计算图逐个参数对照")
print("=" * 68)
import torch

# ---- 5a. 标量图 d = a*b + c ----
ta = torch.tensor(2.0, dtype=torch.float64, requires_grad=True)
tb = torch.tensor(3.0, dtype=torch.float64, requires_grad=True)
tc = torch.tensor(4.0, dtype=torch.float64, requires_grad=True)
td = ta * tb + tc
td.backward()
check("torch: d == 10", abs(td.item() - 10) < TOL, f"实际 {td.item()}")
for name, ours, theirs in [
    ("∂d/∂a", 3, ta.grad), ("∂d/∂b", 2, tb.grad), ("∂d/∂c", 1, tc.grad)
]:
    check(f"torch 的 {name} == {theirs.item():g}", abs(theirs.item() - ours) < TOL)

# ---- 5b. 四样本 MLP：把 micrograd 的权重原样灌进 torch ----
random.seed(42)                       # 与教学脚本一致
model = mg.MLP(3, [4, 4, 1])
xs = [[2, 3, -1], [3, -1, 0.5], [0.5, 1, 1], [1, 1, -1]]
ys = [1, -1, -1, 1]

def m_loss():
    return sum((model(x) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)

loss = m_loss()
for p in model.parameters():
    p.grad = 0.0                      # 清梯度：上一轮贡献不能留到这一轮
loss.backward()
mg_grads = [p.grad for p in model.parameters()]
mg_params = model.parameters()

# 三个 Linear 对应三个 Layer；每个 Neuron 都是 w0,w1,w2,b 的顺序
lins = [torch.nn.Linear(3, 4, dtype=torch.float64),
        torch.nn.Linear(4, 4, dtype=torch.float64),
        torch.nn.Linear(4, 1, dtype=torch.float64)]
offset = 0
for lin in lins:
    n_out, n_in = lin.out_features, lin.in_features
    for i in range(n_out):
        for j in range(n_in):
            lin.weight.data[i][j] = mg_params[offset].data
            offset += 1
        lin.bias.data[i] = mg_params[offset].data
        offset += 1
assert offset == len(mg_params) == 41, offset

def t_forward(x):
    t = torch.tensor(x, dtype=torch.float64)
    for lin in lins:
        t = torch.tanh(lin(t))
    return t

t_loss = sum((t_forward(x) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
t_loss.backward()

check("参数量 41 与 PyTorch 对齐", offset == 41, f"{offset}")
check("初始 loss 逐位一致(<1e-12)", abs(t_loss.item() - loss.data) < 1e-12,
      f"micrograd={loss.data:.15f} torch={t_loss.item():.15f}")

# torch 的参数顺序是 weight 整个矩阵再 bias；这里换成 neuron-major 对齐
t_grads = []
for lin in lins:
    for i in range(lin.out_features):
        for j in range(lin.in_features):
            t_grads.append(lin.weight.grad[i][j].item())
        t_grads.append(lin.bias.grad[i].item())

worst = max(abs(g - t) for g, t in zip(mg_grads, t_grads))
check("41 个梯度逐个一致(<1e-9)", worst < 1e-9, f"最大偏差={worst:.2e}")

# 同一步 SGD 后，两边 loss 仍应一致：先让 torch 也沿同一梯度更新
k = 0
for lin in lins:
    for i in range(lin.out_features):
        for j in range(lin.in_features):
            lin.weight.data[i][j] -= 0.05 * t_grads[k]
            k += 1
        lin.bias.data[i] -= 0.05 * t_grads[k]
        k += 1
assert k == 41, k
for p, g in zip(mg_params, mg_grads):
    p.data -= 0.05 * g

with torch.no_grad():
    t_after = sum((t_forward(x) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
check("更新一步后 loss 仍一致(<1e-12)",
      abs(t_after.item() - m_loss().data) < 1e-12,
      f"micrograd={m_loss().data:.15f} torch={t_after.item():.15f}")

print()
print("=" * 68)
failed = [label for ok, label in results if not ok]
print(f"总计 {len(results)} 项，通过 {len(results) - len(failed)} 项")
if failed:
    print("未通过：")
    for label in failed:
        print("  -", label)
    sys.exit(1)
print("全部通过：可以据此说明梯度、累加与拓扑顺序都正确。")
