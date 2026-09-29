"""Gera os slides Reveal.js a partir de ../resumos/pygame.md."""

from __future__ import annotations

import html
import re
import shutil
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup, Tag


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "resumos" / "pygame.md"


def prepare_markdown(text: str) -> str:
    output: list[str] = []
    stack: list[int] = []
    names = {
        "exercise": "Exercício",
        "answer": "Resposta",
        "tip": "Dica",
        "warning": "Atenção",
        "info": "Informação",
        "note": "Nota",
        "question": "Questão",
    }
    for line in text.splitlines():
        indent = len(line) - len(line.lstrip(" "))
        if line.strip():
            while stack and indent <= stack[-1]:
                stack.pop()
        adjusted = line[4 * len(stack) :] if line.strip() else ""
        adjusted = re.sub(r"^(```[A-Za-z0-9_+-]+)\s+.*$", r"\1", adjusted)
        marker = re.match(r"^([!?]{3})\s+(\w+)(.*)$", adjusted)
        if marker:
            quoted = re.search(r'"([^"]+)"', marker.group(3))
            label = quoted.group(1) if quoted else names.get(marker.group(2), marker.group(2).title())
            output.extend(["", f"**{label}.**", ""])
            stack.append(indent)
        else:
            output.append(adjusted)
    document = "\n".join(output) + "\n"
    ids = re.findall(r'<a id="([^"]+)"', document)
    for fragment in set(re.findall(r"\]\(#([^)]+)\)", document)):
        if fragment in ids:
            continue
        matches = [anchor for anchor in ids if anchor.endswith("--" + fragment)]
        if len(matches) == 1:
            document = document.replace("](#" + fragment + ")", "](#" + matches[0] + ")")
    return document


def render_html(markdown: str) -> BeautifulSoup:
    proc = subprocess.run(
        ["pandoc", "-f", "markdown+raw_html+footnotes+tex_math_dollars", "-t", "html5", "--mathml"],
        input=markdown,
        text=True,
        capture_output=True,
        check=True,
    )
    return BeautifulSoup(proc.stdout, "html.parser")


def page_anchor(node: Tag) -> str | None:
    if node.name != "p":
        return None
    anchors = node.find_all("a", id=True, recursive=False)
    if len(anchors) == 1 and re.fullmatch(r"pygame-(?!grupo-)[a-z0-9-]+-md", anchors[0]["id"]):
        return anchors[0]["id"]
    return None


def extract_groups(soup: BeautifulSoup) -> list[dict]:
    groups: list[dict] = []
    active_group = None
    active_page = None
    in_index = False
    for node in list(soup.children):
        if not isinstance(node, Tag):
            continue
        if node.name == "h2":
            title = node.get_text(" ", strip=True)
            if title == "Índice":
                in_index = True
                continue
            in_index = False
            active_group = {"title": title, "pages": []}
            groups.append(active_group)
            active_page = None
            continue
        if in_index or active_group is None:
            continue
        anchor = page_anchor(node)
        if anchor:
            active_page = {"id": anchor, "title": "", "blocks": []}
            active_group["pages"].append(active_page)
            continue
        if active_page is None:
            if node.name == "h3":
                active_page = {"id": None, "title": node.get_text(" ", strip=True), "blocks": []}
                active_group["pages"].append(active_page)
            continue
        if node.name == "h3" and not active_page["title"]:
            active_page["title"] = node.get_text(" ", strip=True)
        elif active_group["title"] == "Slides das aulas" and node.name == "h3":
            active_page = {"id": None, "title": node.get_text(" ", strip=True), "blocks": []}
            active_group["pages"].append(active_page)
        else:
            active_page["blocks"].append(node)
    return groups


def chunks(blocks: list[Tag]) -> list[list[Tag]]:
    result: list[list[Tag]] = []
    current: list[Tag] = []
    weight = 0
    for block in blocks:
        if block.name == "p" and block.find("a", id=True) and not block.get_text(strip=True):
            current.append(block)
            continue
        heavy = bool(block.find(["pre", "img", "video", "table"])) or block.name in {"pre", "table", "div"}
        image_block = bool(block.find("img"))
        size = len(block.get_text(" ", strip=True))
        heading = block.name in {"h3", "h4", "h5", "h6"}
        short_caption = image_block and len(current) == 1 and weight <= 80 and current[0].name == "p"
        if current and not short_caption and (heading or heavy or weight + size > 1050 or len(current) >= 5):
            result.append(current)
            current = []
            weight = 0
        current.append(block)
        weight += size
        if heavy:
            result.append(current)
            current = []
            weight = 0
    if current:
        result.append(current)
    return result or [[]]


def decorate(blocks: list[Tag]) -> str:
    fragment = BeautifulSoup("".join(str(block) for block in blocks), "html.parser")
    for pre in list(fragment.find_all("pre")):
        wrapper_target = pre.parent if pre.parent and "sourceCode" in pre.parent.get("class", []) else pre
        box = fragment.new_tag("div", attrs={"class": "code-box"})
        wrapper_target.wrap(box)
        button = fragment.new_tag("button", attrs={"type": "button", "class": "copy-code", "aria-label": "Copiar código"})
        button.string = "Copiar código  ·  Alt+C"
        box.insert(0, button)
    return str(fragment)


def safe_id(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def build(groups: list[dict]) -> tuple[str, list[tuple[str, str]], int]:
    stacks = []
    menu = []
    slide_count = 0
    for group_index, group in enumerate(groups, 1):
        gid = "modulo-" + safe_id(group["title"])
        menu.append((gid, group["title"]))
        sections = [
            f'<section class="module-title" id="{gid}" data-section="{html.escape(group["title"])}">'
            f'<div class="eyebrow">Pygame · {group_index:02d}</div>'
            f'<h2>{html.escape(group["title"])}</h2>'
            f'<p>{len(group["pages"])} {"tópico" if len(group["pages"]) == 1 else "tópicos"} · pressione ↓ para continuar</p>'
            "</section>"
        ]
        slide_count += 1
        for page in group["pages"]:
            page_title = page["title"] or group["title"]
            for part_index, part in enumerate(chunks(page["blocks"]), 1):
                sid = f' id="{page["id"]}"' if part_index == 1 and page["id"] else ""
                content = decorate(part)
                sections.append(
                    f'<section class="content-slide"{sid} data-section="{html.escape(group["title"])}">'
                    f'<div class="slide-kicker">{html.escape(group["title"])} <span>›</span> {html.escape(page_title)}</div>'
                    f'<h2>{html.escape(page_title)}{f" <small>· {part_index}</small>" if part_index > 1 else ""}</h2>'
                    f'<div class="slide-body">{content}</div>'
                    "</section>"
                )
                slide_count += 1
        stacks.append("<section>" + "".join(sections) + "</section>")
    return "".join(stacks), menu, slide_count


def main() -> None:
    markdown = prepare_markdown(SOURCE.read_text())
    groups = extract_groups(render_html(markdown))
    content, menu, count = build(groups)
    shutil.copytree(ROOT / "resumos" / "imagens", HERE / "imagens", dirs_exist_ok=True)
    menu_html = "".join(f'<a href="#{target}" data-jump="{target}">{html.escape(title)}</a>' for target, title in menu)
    page = f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pygame · Apresentação completa</title>
  <link rel="stylesheet" href="vendor/reveal/reset.css">
  <link rel="stylesheet" href="vendor/reveal/reveal.css">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <button id="menu-button" aria-label="Abrir índice" aria-expanded="false">Índice <kbd>M</kbd></button>
  <nav id="module-menu" aria-label="Índice dos módulos"><h2>Conteúdo</h2>{menu_html}</nav>
  <div class="reveal"><div class="slides">
    <section class="cover" data-section="Início">
      <div class="eyebrow">Developer Life · Jogos em Python</div>
      <h1>Pygame</h1>
      <p>Da primeira janela ao projeto de jogo</p>
      <div class="cover-guide">→ módulos &nbsp; ↓ tópicos &nbsp; M índice &nbsp; Alt+C copiar código</div>
    </section>
    {content}
  </div></div>
  <div id="section-label" aria-hidden="true"></div>
  <div id="copy-status" role="status" aria-live="polite"></div>
  <script src="vendor/reveal/reveal.js"></script>
  <script src="app.js"></script>
</body>
</html>'''
    (HERE / "index.html").write_text(page)
    (HERE / "README.md").write_text(
        "# Apresentação Pygame\n\n"
        "Abra `index.html` no navegador, ou sirva esta pasta com `python -m http.server`. "
        "Use ←/→ para mudar de módulo, ↑/↓ para percorrer o conteúdo, M para abrir o índice "
        "e Alt+C (Option+C no macOS) para copiar o primeiro código do slide. "
        "Cada bloco de código também tem um botão de cópia.\n\n"
        "Para atualizar a apresentação após editar `../resumos/pygame.md`, execute `python gerar.py`. "
        "A geração requer `pandoc` e `beautifulsoup4`.\n"
    )
    print(f"{count + 1} slides em {len(groups)} módulos")


if __name__ == "__main__":
    main()
