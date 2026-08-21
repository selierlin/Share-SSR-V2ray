#!/usr/bin/env python3
"""Build the public registration landing page from the Markdown source table."""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


REPO_URL = "https://github.com/selierlin/Share-SSR-V2ray"
SOURCE_URL = f"{REPO_URL}/blob/master/1-share-ssr-v2ray.md"


@dataclass
class Service:
    name: str
    url: str
    price: str
    traffic: str
    trial: str
    proxy: str
    note: str


def clean_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def parse_link(value: str) -> tuple[str, str]:
    match = re.fullmatch(r"\[([^]]+)\]\(([^)]+)\)", value.strip())
    if not match:
        return value.strip(), "#"
    return clean_cell(match.group(1)), match.group(2).strip()


def parse_table(lines: list[str], start: int) -> tuple[list[Service], int]:
    rows: list[Service] = []
    index = start
    while index < len(lines):
        line = lines[index].strip()
        if not line.startswith("|"):
            break
        cells = [clean_cell(cell) for cell in line.strip("|").split("|")]
        if len(cells) != 6:
            index += 1
            continue
        if index == start or all(set(cell) <= {"-", ":", " "} for cell in cells):
            index += 1
            continue
        name, url = parse_link(cells[0])
        rows.append(Service(name, url, *cells[1:]))
        index += 1
    return rows, index


def parse_source(source: str) -> tuple[list[Service], list[Service]]:
    lines = source.splitlines()
    normal: list[Service] = []
    low_cost: list[Service] = []
    current: list[Service] | None = None
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if line == "## 注册站点":
            current = normal
        elif line == "## 免费与低价机场":
            current = low_cost
        elif line.startswith("## "):
            current = None
        if current is not None and line.startswith("| 机场 |"):
            rows, index = parse_table(lines, index)
            current.extend(rows)
            continue
        index += 1
    return normal, low_cost


def render_card(service: Service) -> str:
    details = [
        ("价格参考", service.price),
        ("流量 / 套餐", service.traffic),
        ("试用 / 赠送", service.trial),
        ("需要代理", service.proxy),
    ]
    detail_html = "".join(
        f'<div class="detail"><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>'
        for label, value in details
    )
    note = "" if service.note == "—" else f'<p class="note">{html.escape(service.note)}</p>'
    safe_url = html.escape(service.url, quote=True)
    return f"""<article class="service-card">
  <div class="card-heading">
    <h3>{html.escape(service.name)}</h3>
    <a class="register-button" href="{safe_url}" target="_blank" rel="nofollow sponsored noopener">立即注册<span aria-hidden="true"> ↗</span></a>
  </div>
  <div class="details">{detail_html}</div>
  {note}
</article>"""


def render_group(title: str, services: list[Service], description: str = "") -> str:
    description_html = f'<p class="group-description">{html.escape(description)}</p>' if description else ""
    cards = "\n".join(render_card(service) for service in services)
    return f"""<section class="service-group" id="{'low-cost' if title.startswith('免费') else 'recommended'}">
  <div class="section-heading">
    <p class="eyebrow">{len(services)} 个选项</p>
    <h2>{html.escape(title)}</h2>
    {description_html}
  </div>
  <div class="service-grid">
{cards}
  </div>
</section>"""


def render_page(normal: list[Service], low_cost: list[Service]) -> str:
    generated = date.today().isoformat()
    normal_group = render_group("注册站点", normal, "适合希望直接注册并自行选择套餐的用户。")
    low_group = render_group("免费与低价机场", low_cost, "适合轻度使用或临时备用；购买前请先核对服务商当前规则。")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="整理机场与代理订阅注册信息，以及 Clash Party、v2rayN 和 v2rayNG 客户端配置教程入口。">
  <meta name="theme-color" content="#f7f8fc">
  <title>机场推荐与代理订阅注册入口</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="hero">
    <nav class="nav shell" aria-label="主导航">
      <a class="brand" href="./">Share SSR V2ray</a>
      <div class="nav-links">
        <a href="#recommended">注册推荐</a>
        <a href="#low-cost">免费 / 低价</a>
        <a href="{REPO_URL}" target="_blank" rel="noopener">GitHub ↗</a>
      </div>
    </nav>
    <div class="hero-content shell">
      <p class="eyebrow">订阅服务信息整理</p>
      <h1>机场推荐与代理订阅注册入口</h1>
      <p class="lead">快速比较价格、流量和试用信息，直接进入服务商注册页面。</p>
      <div class="hero-actions">
        <a class="primary-button" href="#recommended">查看精选推荐 <span aria-hidden="true">↓</span></a>
        <a class="secondary-button" href="{REPO_URL}" target="_blank" rel="noopener">查看完整教程</a>
      </div>
      <p class="trust-note">页面内容来自仓库中的 Markdown 表格；套餐、域名和可用性请以服务商官网实时信息为准。</p>
    </div>
  </header>

  <main class="shell main-content">
    <div class="notice">
      <strong>先看这里</strong>
      <span>部分链接可能包含邀请码或推广参数。项目不提供代理服务，也不保证第三方服务的可用性。</span>
    </div>
    {normal_group}
    {low_group}
    <section class="next-steps">
      <p class="eyebrow">继续了解</p>
      <h2>注册后如何使用？</h2>
      <p>选择服务商并注册后，可回到项目仓库查看客户端安装、订阅导入和节点选择教程。</p>
      <div class="link-row">
        <a class="text-link" href="{SOURCE_URL}" target="_blank" rel="noopener">查看完整注册资料 ↗</a>
        <a class="text-link" href="{REPO_URL}/blob/master/tools.md" target="_blank" rel="noopener">查看客户端推荐 ↗</a>
        <a class="text-link" href="{REPO_URL}" target="_blank" rel="noopener">访问 GitHub 仓库 ↗</a>
      </div>
    </section>
  </main>

  <footer class="footer shell">
    <span>Share SSR V2ray</span>
    <span>页面生成于 {generated} · 信息请以服务商官网为准</span>
  </footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="1-share-ssr-v2ray.md")
    parser.add_argument("--output", default="site-dist")
    args = parser.parse_args()

    source = Path(args.source).read_text(encoding="utf-8")
    normal, low_cost = parse_source(source)
    if not normal or not low_cost:
        raise SystemExit("未找到完整的注册站点表格，停止生成以避免发布空页面。")

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_text(render_page(normal, low_cost), encoding="utf-8")
    (output / "style.css").write_text(Path("site/style.css").read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Generated {output / 'index.html'}: {len(normal)} registered + {len(low_cost)} low-cost services")


if __name__ == "__main__":
    main()
