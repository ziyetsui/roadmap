#!/usr/bin/env python3
"""Build GitHub Pages from the committed delivery files, without raw sources."""
import html
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
STATUS = {'delivered': '已交付', 'needs-qc': '待最终验收', 'needs-review': '待内容评审'}

def main():
    catalog = json.loads((ROOT / 'structure/catalog.json').read_text())
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / '.nojekyll').touch()
    rows = []
    for item in catalog:
        slug = item['slug']
        src = ROOT / 'structure' / item['episode'] / 'deliver'
        dst = OUT / slug
        shutil.copytree(src, dst)
        shutil.copy2(dst / item['html'], dst / 'index.html')
        title = html.escape(item['title'])
        status = html.escape(STATUS.get(item['status'], item['status']))
        links = f'<a href="{slug}/">在线阅读</a> · <a href="{slug}/{item["pdf"]}">PDF</a> · <a href="{slug}/{item["md"]}">Markdown</a>'
        rows.append(f'<article><h2><a href="{slug}/">{title}</a></h2><p>{status}</p><nav>{links}</nav></article>')
    (OUT / 'index.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>实战手册 · Roadmap</title><style>body{max-width:900px;margin:48px auto;padding:0 22px;background:#fffdf8;color:#203137;font:16px/1.8 system-ui,sans-serif}h1{line-height:1.3}a{color:#1c655c}article{margin:24px 0;padding:22px;border:1px solid #cbd9d9;border-radius:12px;background:white}h2{font-size:21px;margin:0}p{color:#52646a}footer{margin:40px 0}</style><h1>实战手册 · Roadmap</h1><p>从材料到可以照着做的手册。提供在线阅读、PDF、Markdown 和配套模板。各册保留当前评审状态；发布不代表已完成真实试用。</p>''' + '\n'.join(rows) + '<footer><a href="https://github.com/ziyetsui/roadmap">GitHub 仓库</a></footer></html>')
    print(f'Built {len(catalog)} manuals in {OUT}')

if __name__ == '__main__':
    main()
