from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tests.site_audit import heading_levels, parse_html, resolve_local_reference, site_documents


class AuditHelperTests(unittest.TestCase):
    def test_parser_preserves_duplicate_ids_and_heading_order(self):
        with TemporaryDirectory() as folder:
            page = Path(folder) / "index.html"
            page.write_text(
                '<!doctype html><html><head><title>Sample</title>'
                '<script type="application/ld+json">{"@type":"Person"}</script></head>'
                '<body><h1 id="same">A</h1><h2 id="same">B</h2><img src="x.png" alt="x"></body></html>',
                encoding="utf-8",
            )
            document = parse_html(page)
            self.assertEqual(document.ids, ["same", "same"])
            self.assertEqual(heading_levels(document), [1, 2])
            self.assertEqual(document.title, "Sample")
            self.assertEqual(document.json_ld[0]["@type"], "Person")

    def test_resolver_maps_project_root_and_fragment(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / "artifacts" / "black-box" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text("", encoding="utf-8")
            target, fragment = resolve_local_reference(
                root, page, "/portfolio/assets/a.png?v=1#result"
            )
            self.assertEqual(target, root / "assets" / "a.png")
            self.assertEqual(fragment, "result")

    def test_resolver_maps_fragment_only_reference_to_current_page(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / "artifacts" / "black-box" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text("", encoding="utf-8")
            target, fragment = resolve_local_reference(root, page, "#section")
            self.assertEqual(target, page)
            self.assertEqual(fragment, "section")

    def test_resolver_ignores_external_schemes(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / "index.html"
            for reference in ("mailto:a@example.com", "https://example.com", "data:image/png;base64,AA"):
                self.assertIsNone(resolve_local_reference(root, page, reference))

    def test_site_documents_returns_only_html_in_stable_order(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "b").mkdir()
            (root / "b" / "index.html").write_text("b", encoding="utf-8")
            (root / "index.html").write_text("a", encoding="utf-8")
            (root / "note.txt").write_text("x", encoding="utf-8")
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in site_documents(root)],
                ["b/index.html", "index.html"],
            )

    def test_parser_preserves_multiple_json_ld_blocks_in_dom_order(self):
        with TemporaryDirectory() as folder:
            page = Path(folder) / "index.html"
            page.write_text(
                '<script type="application/ld+json">{"@type":"Person"}</script>'
                '<script type="application/ld+json">{"@type":"WebSite"}</script>',
                encoding="utf-8",
            )
            document = parse_html(page)
            self.assertEqual(
                [item["@type"] for item in document.json_ld], ["Person", "WebSite"]
            )
