# 课程代码与有界检查

7个官方仓库按固定commit保留，见本目录SOURCES.json；目录中保留原LICENSE。它们是课程原代码快照，check_labs.py为助手另写的有界检查，不是作者原提示词。

## 打开哪些文件

- micrograd：nn-zero-to-hero/lectures/micrograd/ 下两个笔记本，micrograd/micrograd/engine.py 作源码对照。
- makemore 1–5：nn-zero-to-hero/lectures/makemore/makemore_part1_bigrams.ipynb 至 makemore_part5_cnn1.ipynb。names.txt 已放在同目录。启动Jupyter前切到此目录，避免相对路径指错。
- 字符GPT：ng-video-lecture/bigram.py、gpt.py；同目录已有input.txt。默认gpt.py会跑较大配置，先在自己的副本修改参数。
- BPE：minbpe/minbpe/basic.py、regex.py、gpt4.py，与exercise.md。
- GPT-2：build-nanogpt/train_gpt2.py、fineweb.py、hellaswag.py。不要import train_gpt2.py来取GPT类，它的顶层会启动训练。

## 运行局部检查

在自己的Python环境安装torch、matplotlib、regex、tiktoken后，在code目录执行：

```bash
MPLBACKEND=Agg python check_labs.py > lab-checks.json
```

它会检查micrograd的重复节点累加、作者第5课笔记本的原子/合并反传、BPE多语种往返，以及从作者GPT-2文件抽取的缩小网络（2层、32宽、10次更新）。不下载GPT-2权重、不下载FineWeb，不执行完整124M训练。

本次CPU/PyTorch2.8.0局部检查通过；因果差值0、缩小模型loss约3.488降至1.296。不能把此结果称为完整课程试用或124M质量复现。

## 平台限制

原fineweb.py采用顶层multiprocessing Pool，按课程Linux环境使用；macOS默认spawn须先加main guard并验证，或在Linux准备数据。不直接运行原脚本在macOS下下载大数据。云GPU费用和预算未确认，本次没有启动付费训练。

7个快照的日期/commit保留在仓库清单，运行自己的学习副本后记录变更；不要把视频录制时版本与当前快照混为一谈。

## 步骤2逐项教学脚本

`learning/step02_micrograd_walkthrough.py` 是助手编写的纯Python教学实现，含有限差分、Value自动求导、重复节点梯度、单参数更新与四样本MLP训练。运行 `python3 learning/step02_micrograd_walkthrough.py`，无需第三方依赖；逐段说明已放入手册步骤2。它不是官方源码，也不代表完整语言模型训练。
