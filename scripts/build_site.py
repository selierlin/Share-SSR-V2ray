#!/usr/bin/env python3
"""Build GitHub Pages content from the repository's Markdown sources."""

from __future__ import annotations

import argparse
import html
import re
import shutil
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


@dataclass(frozen=True)
class Guide:
    slug: str
    source: str
    title: str
    platform: str
    summary: str


GUIDES = (
    Guide("clash-party-windows", "Clash/Clash_Windows.md", "Clash Party Windows", "Windows", "导入 Clash / Mihomo 订阅、选择节点并开启系统代理。"),
    Guide("clash-party-macos", "Clash/Clash_Mac.md", "Clash Party macOS", "macOS", "在 Mac 上导入订阅、选择节点并配置系统代理。"),
    Guide("clash-meta-android", "Clash/Clash_Android.md", "Clash Meta for Android", "Android", "导入 Clash / Mihomo 订阅并建立 Android VPN 连接。"),
    Guide("v2rayn-windows", "V2ray/V2rayN_Windows.md", "v2rayN Windows", "Windows", "在 Windows 上导入订阅、更新节点并配置代理模式。"),
    Guide("v2rayng-android", "V2ray/V2ray_Android.md", "v2rayNG Android", "Android", "在 Android 上导入订阅、更新节点并开启 VPN。"),
)


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
    anchor = "low-cost" if title.startswith("免费") else "recommended"
    return f"""<section class="service-group" id="{anchor}">
  <div class="section-heading">
    <p class="eyebrow">{len(services)} 个选项</p>
    <h2>{html.escape(title)}</h2>
    {description_html}
  </div>
  <div class="service-grid">
{cards}
  </div>
</section>"""


def guide_cards(base: str = "") -> str:
    return "\n".join(
        f"""<article class="guide-card">
  <p class="platform">{html.escape(guide.platform)}</p>
  <h3>{html.escape(guide.title)}</h3>
  <p>{html.escape(guide.summary)}</p>
  <a class="text-link" href="{base}guides/{guide.slug}/">查看教程 →</a>
</article>"""
        for guide in GUIDES
    )


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
        <a href="guides/">客户端教程</a>
        <a href="{REPO_URL}" target="_blank" rel="noopener">GitHub ↗</a>
      </div>
    </nav>
    <div class="hero-content shell">
      <p class="eyebrow">订阅服务信息整理</p>
      <h1>机场推荐与代理订阅注册入口</h1>
      <p class="lead">快速比较价格、流量和试用信息，直接进入服务商注册页面。</p>
      <div class="hero-actions">
        <a class="primary-button" href="#recommended">查看精选推荐 <span aria-hidden="true">↓</span></a>
        <a class="secondary-button" href="guides/">查看客户端教程</a>
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
    <section class="next-steps" id="guides">
      <p class="eyebrow">注册后使用</p>
      <h2>选择你的客户端教程</h2>
      <p>注册并获取订阅地址后，按设备选择客户端，导入订阅并完成基础配置。</p>
      <div class="guide-grid compact-guide-grid">
        {guide_cards()}
      </div>
      <div class="link-row">
        <a class="text-link" href="guides/">查看全部客户端教程 →</a>
        <a class="text-link" href="{SOURCE_URL}" target="_blank" rel="noopener">查看完整注册资料 ↗</a>
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


def normalize_setext_headings(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    normalized: list[str] = []
    index = 0
    while index < len(lines):
        if index + 1 < len(lines) and lines[index].strip() and re.fullmatch(r"=+|-+", lines[index + 1].strip()):
            level = "#" if lines[index + 1].strip().startswith("=") else "##"
            normalized.append(f"{level} {lines[index].strip()}")
            index += 2
            continue
        normalized.append(lines[index])
        index += 1
    return normalized


def render_inline(value: str, asset_paths: dict[str, str]) -> str:
    escaped = html.escape(value, quote=False)

    def image_repl(match: re.Match[str]) -> str:
        alt, source = html.unescape(match.group(1)), html.unescape(match.group(2))
        target = asset_paths.get(source, source)
        return f'<img src="{html.escape(target, quote=True)}" alt="{html.escape(alt, quote=True)}" loading="lazy">'

    def link_repl(match: re.Match[str]) -> str:
        label, url = match.group(1), html.unescape(match.group(2))
        return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{label} ↗</a>'

    escaped = re.sub(r"!\[([^]]*)\]\(([^)]+)\)", image_repl, escaped)
    escaped = re.sub(r"(?<!!)\[([^]]+)\]\(([^)]+)\)", link_repl, escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def render_markdown(markdown: str, asset_paths: dict[str, str]) -> tuple[str, str]:
    lines = normalize_setext_headings(markdown)
    title = ""
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    list_type = ""
    quote_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{render_inline(' '.join(part.strip() for part in paragraph), asset_paths)}</p>")
            paragraph.clear()

    def flush_list() -> None:
        nonlocal list_type
        if list_items:
            output.append(f"<{list_type}>" + "".join(f"<li>{render_inline(item, asset_paths)}</li>" for item in list_items) + f"</{list_type}>")
            list_items.clear()
        list_type = ""

    def flush_quote() -> None:
        if quote_lines:
            output.append(f"<blockquote><p>{render_inline(' '.join(quote_lines), asset_paths)}</p></blockquote>")
            quote_lines.clear()

    for raw_line in lines:
        line = raw_line.rstrip()
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        image_only = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", line.strip())
        quote = re.match(r"^>\s?(.*)$", line)
        unordered = re.match(r"^\s*[-*]\s+(.+)$", line)
        ordered = re.match(r"^\s*\d+\.\s+(.+)$", line)

        if heading:
            flush_paragraph(); flush_list(); flush_quote()
            level, text = len(heading.group(1)), heading.group(2)
            if level == 1 and not title:
                title = re.sub(r"<[^>]+>", "", render_inline(text, asset_paths))
                continue
            level = min(max(level, 2), 4)
            output.append(f"<h{level}>{render_inline(text, asset_paths)}</h{level}>")
        elif not line.strip():
            flush_paragraph(); flush_list(); flush_quote()
        elif quote:
            flush_paragraph(); flush_list()
            quote_lines.append(quote.group(1).strip())
        elif image_only:
            flush_paragraph(); flush_list(); flush_quote()
            output.append(f'<figure>{render_inline(line.strip(), asset_paths)}</figure>')
        elif unordered or ordered:
            flush_paragraph(); flush_quote()
            current_type = "ul" if unordered else "ol"
            if list_type and list_type != current_type:
                flush_list()
            list_type = current_type
            list_items.append((unordered or ordered).group(1))
        else:
            flush_list(); flush_quote()
            paragraph.append(line)

    flush_paragraph(); flush_list(); flush_quote()
    return title, "\n".join(output)


def copy_guide_assets(source: Path, output: Path) -> dict[str, str]:
    asset_paths: dict[str, str] = {}
    for match in re.finditer(r"!\[[^]]*\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
        markdown_path = match.group(1)
        image = (source.parent / markdown_path).resolve()
        if not image.is_file():
            raise SystemExit(f"教程图片不存在：{source}: {markdown_path}")
        destination = output / "assets" / "images" / image.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(image, destination)
        asset_paths[markdown_path] = f"../../assets/images/{image.name}"
    return asset_paths


def render_guide_page(guide: Guide, title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(guide.summary, quote=True)}">
  <meta name="theme-color" content="#f7f8fc">
  <title>{html.escape(title)}｜Share SSR V2ray</title>
  <link rel="stylesheet" href="../../style.css">
</head>
<body>
  <nav class="nav shell" aria-label="主导航">
    <a class="brand" href="../../">Share SSR V2ray</a>
    <div class="nav-links">
      <a href="../../">注册推荐</a>
      <a href="../">客户端教程</a>
      <a href="{REPO_URL}" target="_blank" rel="noopener">GitHub ↗</a>
    </div>
  </nav>
  <main class="shell guide-layout">
    <a class="back-link" href="../">← 返回客户端教程</a>
    <article class="guide-article">
      <header class="guide-header">
        <p class="eyebrow">{html.escape(guide.platform)} 客户端</p>
        <h1>{html.escape(title)}</h1>
        <p class="lead">{html.escape(guide.summary)}</p>
      </header>
      <div class="guide-content">
{body}
      </div>
      <footer class="guide-source">内容源自 <a href="{REPO_URL}/blob/master/{guide.source}" target="_blank" rel="noopener">仓库 Markdown 文档 ↗</a>，修改仓库后会自动更新本页。</footer>
    </article>
  </main>
  <footer class="footer shell"><span>Share SSR V2ray</span><span>教程信息请以客户端官方页面为准</span></footer>
</body>
</html>
"""


def render_guides_index() -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Clash Party、Clash Meta for Android、v2rayN 与 v2rayNG 的订阅导入和基础配置教程。">
  <meta name="theme-color" content="#f7f8fc">
  <title>客户端使用教程｜Share SSR V2ray</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <nav class="nav shell" aria-label="主导航">
    <a class="brand" href="../">Share SSR V2ray</a>
    <div class="nav-links"><a href="../">注册推荐</a><a href="{REPO_URL}" target="_blank" rel="noopener">GitHub ↗</a></div>
  </nav>
  <main class="shell guide-index">
    <header class="guide-index-header">
      <p class="eyebrow">主推客户端</p>
      <h1>客户端使用教程</h1>
      <p class="lead">注册并获取订阅地址后，选择你的设备和客户端，按教程完成导入与连接。</p>
    </header>
    <section class="guide-grid">
      {guide_cards(base="../")}
    </section>
    <div class="notice"><strong>提示</strong><span>订阅地址通常相当于账号凭证，请勿公开分享；客户端请优先从官方发布页下载。</span></div>
  </main>
  <footer class="footer shell"><span>Share SSR V2ray</span><span>历史客户端资料仍保留在 GitHub 仓库</span></footer>
</body>
</html>
"""


def build_guides(output: Path) -> None:
    (output / "guides").mkdir(parents=True, exist_ok=True)
    for guide in GUIDES:
        source = Path(guide.source)
        assets = copy_guide_assets(source, output)
        title, body = render_markdown(source.read_text(encoding="utf-8"), assets)
        if not title:
            title = guide.title + " 使用教程"
        destination = output / "guides" / guide.slug
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "index.html").write_text(render_guide_page(guide, title, body), encoding="utf-8")
    (output / "guides" / "index.html").write_text(render_guides_index(), encoding="utf-8")


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
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output / "index.html").write_text(render_page(normal, low_cost), encoding="utf-8")
    (output / "style.css").write_text(Path("site/style.css").read_text(encoding="utf-8"), encoding="utf-8")
    build_guides(output)
    print(f"Generated {output}: {len(normal)} registered + {len(low_cost)} low-cost services + {len(GUIDES)} guides")


if __name__ == "__main__":
    main()
