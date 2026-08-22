from __future__ import annotations

import html
import re
import shutil
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import markdown
import yaml


ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
BLOG_DIR = CONTENT_DIR / "blog"
TEMPLATE_PATH = ROOT / "template.html"
OUTPUT_DIR = ROOT / "public"
MARKDOWN_SUFFIXES = {".md", ".markdown"}

FRONT_MATTER_RE = re.compile(
    r"\A---\s*\n(?P<metadata>.*?)\n---\s*(?:\n|\Z)",
    re.DOTALL,
)


class FrontMatterLoader(yaml.SafeLoader):
    """Keep YAML timestamps as strings so their original formatting is preserved."""


for first_character, resolvers in list(
    FrontMatterLoader.yaml_implicit_resolvers.items()
):
    FrontMatterLoader.yaml_implicit_resolvers[first_character] = [
        (tag, pattern)
        for tag, pattern in resolvers
        if tag != "tag:yaml.org,2002:timestamp"
    ]


def parse_front_matter(source: str) -> tuple[dict, str]:
    """Parse YAML front matter and return metadata plus the Markdown body."""
    match = FRONT_MATTER_RE.match(source)
    if not match:
        return {}, source

    metadata = yaml.load(match.group("metadata"), Loader=FrontMatterLoader) or {}
    if not isinstance(metadata, dict):
        raise ValueError("Front matter must contain a YAML mapping")

    return metadata, source[match.end() :]


def render_markdown(source: str) -> str:
    return markdown.markdown(
        source,
        extensions=[
            "pymdownx.highlight",
            "pymdownx.superfences",
            "tables",
            "toc",
        ],
        output_format="html",
    )


def render_template(
    template: str, title: str, content: str, date_text: str = ""
) -> str:
    required_placeholders = ("{{title}}", "{{content}}", "{{date}}")
    if any(placeholder not in template for placeholder in required_placeholders):
        raise ValueError(
            "Template must contain {{title}}, {{date}}, and {{content}} placeholders"
        )

    return (
        template.replace("{{title}}", html.escape(title))
        .replace("{{date}}", html.escape(date_text))
        .replace("{{content}}", content)
    )


def is_draft(metadata: dict) -> bool:
    return metadata.get("draft") is True


def format_article_date(metadata: dict) -> str:
    date_text = str(metadata.get("date") or "")
    lastmod = metadata.get("lastmod")
    if lastmod:
        date_text += f" (updated on: {lastmod})"
    return date_text


def markdown_output_path(relative_path: Path) -> Path:
    """Return the public HTML path for a Markdown file."""
    if relative_path.stem == "index":
        return relative_path.with_suffix(".html")
    return relative_path.parent / relative_path.stem / "index.html"


def generate_markdown_page(
    source_path: Path, destination_path: Path, template: str
) -> None:
    source = source_path.read_text(encoding="utf-8")
    metadata, markdown_source = parse_front_matter(source)
    if is_draft(metadata):
        return

    title = str(metadata.get("title") or source_path.stem)
    date_text = format_article_date(metadata)
    content = render_markdown(markdown_source)
    page = render_template(template, title, content, date_text)

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(page, encoding="utf-8")


@dataclass(frozen=True)
class BlogArticle:
    title: str
    date: date
    href: str


def parse_article_date(value: object, source_path: Path) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            pass

    raise ValueError(f"Blog article has no valid date: {source_path}")


def collect_blog_articles() -> list[BlogArticle]:
    articles = []

    for source_path in BLOG_DIR.rglob("*"):
        if not source_path.is_file():
            continue
        if source_path.suffix.lower() not in MARKDOWN_SUFFIXES:
            continue

        source = source_path.read_text(encoding="utf-8")
        metadata, _ = parse_front_matter(source)
        if is_draft(metadata):
            continue

        article_date = parse_article_date(metadata.get("date"), source_path)
        relative_path = markdown_output_path(
            source_path.relative_to(CONTENT_DIR)
        )

        articles.append(
            BlogArticle(
                title=str(metadata.get("title") or source_path.stem),
                date=article_date,
                href=relative_path.as_posix(),
            )
        )

    return sorted(articles, key=lambda article: article.date, reverse=True)


def render_blog_index(articles: list[BlogArticle]) -> str:
    years: dict[int, list[BlogArticle]] = {}
    for article in articles:
        years.setdefault(article.date.year, []).append(article)

    lines = [
        "<p>Things worth sharing.</p>",
        "<ul>"
    ]

    for year in sorted(years, reverse=True):
        lines.append(f"  <li>{year}")
        lines.append("    <ul>")
        for article in years[year]:
            title = html.escape(article.title)
            href = html.escape(article.href, quote=True)
            lines.append(f'      <li><a href="{href}">{title}</a></li>')
        lines.append("    </ul>")
        lines.append("  </li>")
    lines.append("</ul>")
    return "\n".join(lines)


def write_blog_index(template: str) -> None:
    content = render_blog_index(collect_blog_articles())
    page = render_template(template, "Blog", content)
    (OUTPUT_DIR / "index.html").write_text(page, encoding="utf-8")


def main() -> None:
    if not CONTENT_DIR.is_dir():
        raise SystemExit(f"Content directory does not exist: {CONTENT_DIR}")
    if not TEMPLATE_PATH.is_file():
        raise SystemExit(f"Template file does not exist: {TEMPLATE_PATH}")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    for source_path in CONTENT_DIR.rglob("*"):
        if not source_path.is_file():
            continue

        relative_path = source_path.relative_to(CONTENT_DIR)
        destination_path = OUTPUT_DIR / relative_path

        if source_path.suffix.lower() in MARKDOWN_SUFFIXES:
            generate_markdown_page(
                source_path,
                OUTPUT_DIR / markdown_output_path(relative_path),
                template,
            )
        else:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)

    write_blog_index(template)


if __name__ == "__main__":
    main()
