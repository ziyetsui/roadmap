# 就地提示词模板汇总

助手抽象模板；替换〔〕后使用。完整原文与边界以手册对应位置为准。

## 可套用模板｜P1

```text
构建一个用于〔用户场景〕、管理〔核心对象〕的工具。数据库采用〔数据库〕，后端采用〔后端栈〕，前端采用〔前端栈〕；用户与认证范围为〔范围〕。
用户需要：〔对象生命周期操作〕、〔分类关联操作〕、按〔分类字段〕查看列表、按〔检索字段〕搜索。
先生成详细需求和设计文档，说明数据模型、接口、交互、错误与验收，保存到〔规格文件路径〕，以〔输出语言〕撰写。
```

## 可套用模板｜P2

```text
按照〔需求与设计文件路径〕生成详细实现计划，保存到〔计划文件路径〕，输出为〔语言〕。
将任务按依赖划分阶段，逐阶段列出范围、相关文件与可执行验收；本轮只生成计划。
```

## 可套用模板｜P3

```text
先阅读〔需求文档〕、〔实现计划〕和〔任务文件〕，核对〔本轮阶段〕的前置条件。
只完成该阶段列出的全部任务，代码写入〔项目目录〕；提供实际改动、执行的验证、失败与未测项，再更新任务状态。
```

## 可套用模板｜P4

```text
为〔项目及数据库〕生成〔种子文件路径〕，包含〔对象数量〕条有业务意义的〔核心对象〕与〔分类数量〕条〔分类对象〕。
分类覆盖〔分类维度及示例〕，对象与分类关联合理，兼顾〔验收场景〕；确保文件可由〔数据库客户端〕执行。
说明执行前提、重复执行行为及验证条数的方法。
```

## 可套用模板｜P5

```text
参照〔设计参考网站或截图〕优化〔项目页面〕的UI与UX。
先指出〔布局/层次/间距/反馈〕的具体问题，按〔改动优先级〕实施，保持〔既有业务行为〕，并检查〔典型交互与页面状态〕。
```

## 可套用模板｜P6

```text
阅读〔风格规范文件〕，学习〔参考项目目录〕中的设计token定义，优化〔目标项目〕整体UI与UX。
将颜色、字体、间距、组件状态映射到已有token，检查〔目标页面与交互〕的一致性；原输入归属未核不代表课堂已执行。
```

## 可套用模板｜P7

```text
请调整〔项目〕的侧栏，集中展示全部〔资源类型〕并提供添加、删除与当前选中状态。
遵循〔设计规则/token文件〕；主页默认展示〔默认资源选择规则〕对应的〔信息区〕和〔操作区〕，减少进入详情的步骤。
检查添加、切换、删除当前项及无资源时的行为，记录布局与交互结果。
```

## 可套用模板｜P8

```text
依据〔真实参考截图及区域标记〕调整〔结构侧栏〕：〔资源名〕与〔刷新控件〕组成顶部栏，使用〔主题token〕。
结构树占满顶部栏之外的可用高度，明确滚动区域；〔指标区〕与〔主编辑区〕放入同一容器，按〔空间分配要求〕收紧尺寸。
检查〔目标窗口尺寸〕下的高度、溢出、刷新与编辑行为；缺少截图时先确认区域，不猜附件内容。
```

## 可套用模板｜N1

```text
Help me discover papers and recent progress about 〔research topic〕 during 〔time window〕.
Return sources relevant to 〔research question〕, with publication dates and links for verification.
```

## 可套用模板｜N2

```text
Help me discover recent progress about 〔research topic〕 during 〔time window〕, limited to 〔video platform/source type〕.
Check that each result matches the requested source type; list mismatches separately.
```

## 可套用模板｜N3

```text
Help me discover papers and recent progress about 〔research topic〕 during 〔time window〕, limited to 〔paper repository/domain〕.
For each result, record the date, link and relevance to 〔research question〕.
```

## 可套用模板｜N4

```text
基于当前选中的〔来源范围〕，说明〔研究领域〕未来的主要方向。
分别回答〔关键能力或目标〕是否可能实现，以及〔关键指标〕可能如何发展；逐项给出来源依据，并区分已知事实、预测和缺乏证据的判断。
```

## 可套用模板｜N5

```text
Help me analyze the market for 〔product category〕 serving 〔target users〕 with 〔core use case〕.
Identify existing products, usage evidence, user sentiment and improvement opportunities. Link each claim to its source and separate verified findings from assumptions.
```

## 可套用模板｜N6

```text
Help me analyze the market for 〔product category〕 serving 〔target users〕 with 〔core use case〕.
Compare existing products, usage evidence, user sentiment and improvements. Search 〔video platform〕 during 〔time window〕; check dates and relevance rather than treating broad market results as product evidence.
```

## 可套用模板｜N7

```text
笔记标题：我对〔主题〕的个人看法
这是个人推断：我认为〔能力或指标〕可能在〔时间条件〕达到〔预期范围〕，从而影响〔应用场景〕。
依据：〔已有观察或待验证依据〕；需验证：〔不确定条件〕。此模板是笔记骨架，不能把个人预测当外部研究结论。
```

## 可套用模板｜N8

```text
基于〔当前选择的资料〕，〔目标能力或指标〕未来可能达到什么范围？
请注明各结论的来源与时间，区分个人笔记、外部研究和模型推断；来源不能支持的预测写明不确定。
```

## 可套用模板｜R1

```text
根据〔项目API契约与实际路由〕，使用〔REST客户端格式〕编写〔测试文件路径〕，覆盖全部已支持API。
核对地址前缀、请求字段及资源依赖，包含成功与错误请求；区分已编写的用例和已执行的结果。
```

## 可套用模板｜R2

```text
先阅读〔需求文档〕、〔实现计划〕和〔任务文件〕，核对〔本轮阶段〕的前置条件。
只完成该阶段列出的全部任务，代码写入〔项目目录〕；提供实际改动、执行的验证、失败与未测项，再更新任务状态。
```

## 可套用模板｜R2

```text
先阅读〔需求文档〕、〔实现计划〕和〔任务文件〕，核对〔本轮阶段〕的前置条件。
只完成该阶段列出的全部任务，代码写入〔项目目录〕；提供实际改动、执行的验证、失败与未测项，再更新任务状态。
```

## 可套用模板｜R2

```text
先阅读〔需求文档〕、〔实现计划〕和〔任务文件〕，核对〔本轮阶段〕的前置条件。
只完成该阶段列出的全部任务，代码写入〔项目目录〕；提供实际改动、执行的验证、失败与未测项，再更新任务状态。
```

## 可套用模板｜R3

```text
请在〔构建脚本路径〕删除已不需要的〔目标列表〕，并修复〔失效目标〕。
先检查目标依赖、启动进程与停止方式，保持〔仍需保留的命令行为〕；执行相关命令验证，记录退出码和残留进程情况。
```

## 可套用模板｜建议问题

```text
针对〔研究主题〕，〔新架构或方法〕如何解决〔挑战一〕与〔挑战二〕？
请按挑战、机制、适用条件与证据组织回答，引用〔所选来源〕并指出尚未验证的限制。此模板抽象自产品建议问题，不改写其作者归属。
```
