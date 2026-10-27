# 实战手册 · Roadmap

把课程、帖子和项目材料整理成可以照着做的实战手册。

- [在线目录](https://ziyetsui.github.io/roadmap/)
- [人大同等学力申硕（计算机）](https://ziyetsui.github.io/roadmap/ruc-cs-equivalent-master/)
- [人大手册 PDF](https://ziyetsui.github.io/roadmap/ruc-cs-equivalent-master/manual.pdf)

公开仓库保存各集 `deliver/` 中的 Markdown、离线网页、PDF、图片及配套模板。原始材料、证据快照和本地工作记录不上传。发布页显示各册现有评审状态；上线不代表最终验收或真实试用完成。

## 更新与发布

```sh
python3 scripts/build-pages.py
```

构建输出 `_site/`。合并到 `main` 后，GitHub Actions 自动构建并部署 GitHub Pages。目录元数据保存在 `structure/catalog.json`；各册内容来自 `structure/<episode>/deliver/`。
