# 实战手册 · Roadmap

把课程、帖子和项目材料整理成可以照着做的实战手册。

- [在线目录](https://ziyetsui.github.io/roadmap/)
- [人大同等学力申硕（计算机）](https://ziyetsui.github.io/roadmap/ruc-cs-equivalent-master/)
- [人大手册 PDF](https://ziyetsui.github.io/roadmap/ruc-cs-equivalent-master/manual.pdf)

公开仓库保存各集 `deliver/` 中的 Markdown、离线网页、PDF、图片及配套模板。原始材料、证据快照和本地工作记录不上传。发布页显示各册现有评审状态；上线不代表最终验收或真实试用完成。

## 陈天老师 AI 编程实战手册

- [w1 实战手册：用 AI 从需求到交付项目管理工具](https://ziyetsui.github.io/roadmap/w1-project-alpha/)
- [数据库查询工具实战手册：从 Spec Kit 到 PostgreSQL 与 MySQL](https://ziyetsui.github.io/roadmap/w2-db-query/)
- [RaFlow 实战手册：用 Claude Code 构建语音输入 App](https://ziyetsui.github.io/roadmap/w3-raflow/)
- [GenSlides 实战手册：从产品规划到 AI 图片幻灯片](https://ziyetsui.github.io/roadmap/w7-genslides/)

每本提供在线阅读、PDF、Markdown、课程自动转写稿与配套模板。W7 包含新增的竞品与技术可行性调研模板。

## 更新与发布

```sh
python3 scripts/build-pages.py
```

构建输出 `_site/`。合并到 `main` 后，GitHub Actions 自动构建并部署 GitHub Pages。目录元数据保存在 `structure/catalog.json`；各册内容来自 `structure/<episode>/deliver/`。
