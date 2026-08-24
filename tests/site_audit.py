from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urlsplit


@dataclass
class ParsedDocument:
    tags: list[tuple[str, dict[str, str]]]
    ids: list[str]
    links: list[str]
    sources: list[str]
    text: str
    title: str
    json_ld: list[dict]


class _DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.ids: list[str] = []
        self.links: list[str] = []
        self.sources: list[str] = []
        self.text_parts: list[str] = []
        self.title_parts: list[str] = []
        self.json_ld_parts: list[str] = []
        self._ignored_tags: list[str] = []
        self._in_title = False
        self._in_json_ld = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        self.tags.append((tag, attributes))
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if "src" in attributes:
            self.sources.append(attributes["src"])
        if tag in {"script", "style"}:
            self._ignored_tags.append(tag)
        if tag == "title":
            self._in_title = True
        if tag == "script" and attributes.get("type", "").lower() == "application/ld+json":
            self._in_json_ld = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._ignored_tags:
            self._ignored_tags.pop()
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._in_json_ld = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._in_json_ld:
            self.json_ld_parts.append(data)
        if not self._ignored_tags:
            self.text_parts.append(data)


def parse_html(path: Path) -> ParsedDocument:
    parser = _DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    json_ld: list[dict] = []
    for block in parser.json_ld_parts:
        try:
            json_ld.append(json.loads(block))
        except json.JSONDecodeError as error:
            raise AssertionError(f"Invalid JSON-LD in {path}: {error}") from error
    return ParsedDocument(
        tags=parser.tags,
        ids=parser.ids,
        links=parser.links,
        sources=parser.sources,
        text="".join(parser.text_parts),
        title="".join(parser.title_parts),
        json_ld=json_ld,
    )


def site_documents(site_root: Path) -> list[Path]:
    return sorted(site_root.rglob("*.html"), key=lambda path: path.relative_to(site_root).as_posix())


def resolve_local_reference(
    site_root: Path, page: Path, reference: str
) -> tuple[Path, str | None] | None:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        return None
    root = site_root.resolve()
    relative_path = parsed.path
    if relative_path.startswith("/portfolio/"):
        target = root / relative_path.removeprefix("/portfolio/")
    elif relative_path.startswith("/"):
        target = root / relative_path.removeprefix("/")
    else:
        target = page.parent / relative_path
    target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return None
    return target, parsed.fragment or None


def heading_levels(document: ParsedDocument) -> list[int]:
    return [int(tag[1]) for tag, _ in document.tags if len(tag) == 2 and tag[0] == "h" and tag[1].isdigit()]
