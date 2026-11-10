"""助手编写的教学版：纯 Python 标量求导与四样本训练，不是官方源码。"""
import math  # 数学函数：tanh 与乘方
import random  # 随机数：初始化权重

# ── 核心一：Value 保存一个数字、它的梯度，以及它由谁算出来 ──
class Value:  # 定义 Value 类

    def __init__(self, data, parents=(), op=""):  # 构造方法
        self.data = float(data)  # 保存这个节点的数值
        self.grad = 0.0  # 梯度初始为 0
        self.parents = parents  # 记下产生它的上游节点
        self.op = op  # 记下用了哪种运算
        self._backward = lambda: None  # 局部反传函数，默认为空

    def __add__(self, other):  # 定义 + 运算
        other = other if isinstance(other, Value) else Value(other)  # 右边是普通数字时先包成 Value
        out = Value(self.data + other.data, (self, other), "+")  # 建输出节点，并记住两个父节点

        def backward():  # 定义加法的局部反传
            self.grad += out.grad  # x 的梯度累加 z 的梯度
            other.grad += out.grad  # y 的梯度累加 z 的梯度
        out._backward = backward  # 把反传函数挂到输出节点上
        return out  # 返回输出节点

    def __mul__(self, other):  # 定义 * 运算
        other = other if isinstance(other, Value) else Value(other)  # 数字先包成 Value
        out = Value(self.data * other.data, (self, other), "*")  # 建输出节点

        def backward():  # 定义乘法的局部反传
            self.grad += other.data * out.grad  # x 的梯度 += y × 下游梯度
            other.grad += self.data * out.grad  # y 的梯度 += x × 下游梯度
        out._backward = backward  # 挂上反传
        return out  # 返回输出节点

    def __pow__(self, exponent):  # 定义 ** 运算
        assert isinstance(exponent, (int, float))  # 只支持整数或浮点指数
        out = Value(self.data ** exponent, (self,), f"**{exponent}")  # 建输出节点

        def backward():  # 定义乘方的局部反传
            if exponent != 0:  # 指数为 0 时导数为 0，跳过
                self.grad += exponent * self.data ** (exponent - 1) * out.grad  # 梯度 += n·x^(n−1)·下游梯度
        out._backward = backward  # 挂上反传
        return out  # 返回输出节点

    def tanh(self):  # 定义 tanh
        t = math.tanh(self.data)  # 先算出 tanh 的值 t
        out = Value(t, (self,), "tanh")  # 建输出节点

        def backward():  # 定义 tanh 的局部反传
            self.grad += (1 - t * t) * out.grad  # 梯度 += (1−t²)·下游梯度
        out._backward = backward  # 挂上反传
        return out  # 返回输出节点

    def __neg__(self):  # 取负：-a
        return self * -1  # 等于乘 −1

    def __sub__(self, other):  # 减法：a-b
        return self + (-other)  # 等于加上 b 的相反数

    def __rsub__(self, other):  # 反向减法：数字 - a
        return other + (-self)  # 等于 other + (−a)

    def __truediv__(self, other):  # 除法：a/b
        return self * other ** -1  # 等于乘 b 的 −1 次方

    def __rtruediv__(self, other):  # 反向除法：数字 / a
        return other * self ** -1  # 等于 other × a⁻¹

    __radd__ = __add__  # 数字 + Value 也走加法
    __rmul__ = __mul__  # 数字 × Value 也走乘法

    def backward(self):  # 定义 backward
        order, visited = [], set()  # 拓扑序表与已访问集合

        def visit(node):  # 递归收集所有上游节点
            if node not in visited:  # 没访问过才处理
                visited.add(node)  # 标记为已访问
                for parent in node.parents:  # 遍历它的全部上游
                    visit(parent)  # 递归上游
                order.append(node)  # 上游都排完，再把自己放进序列
        visit(self)  # 从输出节点开始收集整张图
        self.grad = 1.0  # 输出对自己的梯度记为 1
        for node in reversed(order):  # 按逆拓扑序逐个执行
            node._backward()  # 调用该节点的局部反传

# ── 核心二：一个神经元 = 若干权重 + 一个偏置 + tanh ──
class Neuron:  # 定义 Neuron
    def __init__(self, input_count):  # 构造：输入个数
        self.w = [Value(random.uniform(-1, 1)) for _ in range(input_count)]  # 每个输入一个 −1 到 1 的随机权重
        self.b = Value(0)  # 偏置从 0 开始

    def __call__(self, x):  # 前向：被调用时
        return sum((w * xi for w, xi in zip(self.w, x)), self.b).tanh()  # 加权和 Σwᵢxᵢ + b，再过 tanh

    def parameters(self):  # 返回参数列表
        return self.w + [self.b]  # 权重加偏置

# ── 核心三：一层 = 若干个神经元并排 ──
class Layer:  # 定义 Layer
    def __init__(self, input_count, output_count):  # 构造：输入维度、神经元个数
        self.neurons = [Neuron(input_count) for _ in range(output_count)]  # 建 output_count 个神经元

    def __call__(self, x):  # 前向
        return [neuron(x) for neuron in self.neurons]  # 每个神经元各算一个输出

    def parameters(self):  # 返回参数列表
        return [p for neuron in self.neurons for p in neuron.parameters()]  # 把各神经元参数摊平

# ── 核心四：多层感知机 = 若干层叠起来 ──
class MLP:  # 定义 MLP
    def __init__(self, input_count, widths):  # 构造：输入维度与各层宽度
        sizes = [input_count] + widths  # 尺寸表：输入 + 每层输出
        self.layers = [Layer(a, b) for a, b in zip(sizes, sizes[1:])]  # 相邻两项配对建层

    def __call__(self, x):  # 前向
        for layer in self.layers:  # 逐层往下传
            x = layer(x)  # 过一层
        return x[0] if len(x) == 1 else x  # 单输出时拆掉列表

    def parameters(self):  # 返回参数列表
        return [p for layer in self.layers for p in layer.parameters()]  # 各层参数汇总

# 五组对照：有限差分、计算图、重复节点、一次更新、四样本训练
def main():  # 定义 main
    print("1. 有限差分：目标导数为 8")  # 第 1 组标题：有限差分
    f = lambda x: 3 * x ** 2 - 4 * x + 5  # 被求导的函数 f(x)=3x²−4x+5
    for h in (0.1, 0.01, 0.001, 0.0001):  # 依次取四个步长 h
        print(h, (f(2 + h) - f(2)) / h)  # 打印差分估计 (f(2+h)−f(2))/h

    print("2. 计算图：d=2*3+4，梯度应为 3、2、1")  # 第 2 组标题：计算图
    a, b, c = Value(2), Value(3), Value(4)  # 三个输入节点
    d = a * b + c  # 先乘后加，得到输出 d
    d.backward()  # 从输出反传
    print(d.data, a.grad, b.grad, c.grad)  # 打印 d 与 a、b、c 的梯度（应为 10、3、2、1）

    print("3. 重复节点：a+a 和 a*a 分别建新图")  # 第 3 组标题：同一节点被用两次
    a = Value(3)  # 新建 a=3
    (a + a).backward()  # a+a 反传
    print("a+a:", a.grad)  # 应得 2
    a = Value(3)  # 重新新建 a=3
    (a * a).backward()  # a*a 反传
    print("a*a:", a.grad)  # 应得 2a=6

    print("4. 一个参数的一次更新")  # 第 4 组标题：一次参数更新
    w = Value(0)  # 参数 w 从 0 开始
    loss = (w * 2 - 4) ** 2  # 损失 (2w−4)²
    loss.backward()  # 反传
    before = loss.data  # 更新前的 loss
    w.data -= 0.1 * w.grad  # 沿负梯度走一步，学习率 0.1
    after = (w * 2 - 4) ** 2  # 更新后重新算 loss
    print("loss before/after:", before, after.data, "w:", w.data)  # 打印更新前后 loss 与 w

    print("5. 四样本小网络：200 次更新，打印重新计算的 loss")  # 第 5 组标题：四样本训练
    random.seed(42)  # 固定随机种子 42
    model = MLP(3, [4, 4, 1])  # 3 维输入，两个 4 宽隐层，1 个输出
    xs = [[2, 3, -1], [3, -1, 0.5], [0.5, 1, 1], [1, 1, -1]]  # 四组输入
    ys = [1, -1, -1, 1]  # 四个目标值

    def current_loss():  # 定义当前 loss
        return sum((model(x) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)  # 四组平方误差取平均

    print("parameters:", len(model.parameters()))  # 打印参数量
    print("step 0:", current_loss().data)  # 打印第 0 步 loss
    for step in range(200):  # 训练 200 轮
        loss = current_loss()  # 每轮重新前向，建新计算图
        for p in model.parameters():  # 遍历所有参数
            p.grad = 0.0  # 清掉上一轮梯度
        loss.backward()  # 反向传播
        for p in model.parameters():  # 再遍历所有参数
            p.data -= 0.05 * p.grad  # 沿负梯度更新，学习率 0.05
        if (step + 1) % 50 == 0:  # 每 50 轮
            print("step", step + 1, "loss:", current_loss().data)  # 打印这一轮的 loss
    print("predictions:", [round(model(x).data, 4) for x in xs])  # 打印四个预测值
    print("targets:", ys)  # 打印目标值

if __name__ == "__main__":  # 作为脚本直接运行时
    main()  # 执行 main
