from pathlib import Path
import unittest

from tests.site_audit import parse_html, resolve_local_reference, site_documents


SITE_ROOT = Path(__file__).parents[1] / "site"


class RoutesAndLinksTests(unittest.TestCase):
    def _route_document(self, target: Path):
        if target.is_dir() or target.suffix == "":
            target = target / "index.html"
        self.assertTrue(target.is_file(), f"Missing local target: {target}")
        return target, parse_html(target) if target.suffix.lower() == ".html" else None

    def test_all_four_routes_exist(self):
        expected = {
            "index.html",
            "artifacts/black-box/index.html",
            "artifacts/carmaker/index.html",
            "artifacts/bootloader/index.html",
        }
        actual = {path.relative_to(SITE_ROOT).as_posix() for path in site_documents(SITE_ROOT)}
        self.assertTrue(expected.issubset(actual))

    def test_every_local_href_src_and_fragment_resolves(self):
        for page in site_documents(SITE_ROOT):
            document = parse_html(page)
            references = [
                attrs[name]
                for _, attrs in document.tags
                for name in ("href", "src")
                if attrs.get(name)
            ]
            for reference in references:
                with self.subTest(page=page.relative_to(SITE_ROOT), reference=reference):
                    resolved = resolve_local_reference(SITE_ROOT, page, reference)
                    if resolved is None:
                        continue
                    target, fragment = resolved
                    target, target_document = self._route_document(target)
                    if fragment:
                        self.assertIsNotNone(
                            target_document,
                            f"Fragment points to a non-HTML target: {reference}",
                        )
                        self.assertIn(fragment, target_document.ids)

    def test_home_preserves_legacy_project_fragments(self):
        document = parse_html(SITE_ROOT / "index.html")
        self.assertIn("black-box-project", document.ids)
        self.assertIn("bootloader-project", document.ids)

    def test_home_links_to_each_case_study(self):
        home = parse_html(SITE_ROOT / "index.html")
        expected = {
            "/portfolio/artifacts/black-box/",
            "/portfolio/artifacts/carmaker/",
            "/portfolio/artifacts/bootloader/",
        }
        self.assertTrue(expected.issubset(set(home.links)))


if __name__ == "__main__":
    unittest.main()
