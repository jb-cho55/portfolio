from pathlib import Path
import subprocess
import unittest
from urllib.parse import unquote, urljoin, urlsplit

from tests.site_audit import parse_html, resolve_local_reference, site_documents


SITE_ROOT = Path(__file__).parents[1] / "site"
REPO_ROOT = SITE_ROOT.parent


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

    def test_references_resolve_at_root_and_github_pages_mounts(self):
        deployments = (
            ("root", "http://localhost:8000/"),
            ("github-pages", "https://jb-cho55.github.io/portfolio/"),
        )
        missing = []
        invalid_fragments = []
        for deployment, base_url in deployments:
            base = urlsplit(base_url)
            for page in site_documents(SITE_ROOT):
                if deployment == "root" and page == SITE_ROOT / "404.html":
                    # Python's root-mounted development server does not inject
                    # the Pages custom 404 at a retained nested request URL.
                    # Task 4 verifies that production-only contract separately.
                    continue
                route = page.relative_to(SITE_ROOT).as_posix()
                if route == "index.html":
                    route = ""
                elif route.endswith("/index.html"):
                    route = route.removesuffix("index.html")
                page_url = urljoin(base_url, route)
                document = parse_html(page)
                references = [
                    attrs[name]
                    for _, attrs in document.tags
                    for name in ("href", "src")
                    if attrs.get(name)
                ]
                for reference in references:
                    absolute = urlsplit(urljoin(page_url, reference))
                    if (absolute.scheme, absolute.netloc) != (base.scheme, base.netloc):
                        continue
                    if not absolute.path.startswith(base.path):
                        missing.append((deployment, page.name, reference, "outside mount"))
                        continue
                    relative = unquote(absolute.path.removeprefix(base.path))
                    target = SITE_ROOT / relative
                    if not relative or relative.endswith("/"):
                        target /= "index.html"
                    if not target.is_file():
                        missing.append((deployment, page.name, reference, target.as_posix()))
                        continue
                    if absolute.fragment and target.suffix.lower() == ".html":
                        if absolute.fragment not in parse_html(target).ids:
                            invalid_fragments.append(
                                (deployment, page.name, reference, absolute.fragment)
                            )
        self.assertEqual(missing, [])
        self.assertEqual(invalid_fragments, [])

    def test_pdfs_are_treated_as_binary_by_git(self):
        result = subprocess.run(
            [
                "git",
                "check-attr",
                "text",
                "diff",
                "--",
                "site/assets/evidence/black_box_award.pdf",
            ],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn(": text: unset", result.stdout)
        self.assertIn(": diff: unset", result.stdout)

    def test_home_preserves_legacy_project_fragments(self):
        document = parse_html(SITE_ROOT / "index.html")
        self.assertIn("black-box-project", document.ids)
        self.assertIn("bootloader-project", document.ids)

    def test_home_links_to_each_case_study(self):
        home = parse_html(SITE_ROOT / "index.html")
        expected = {
            "artifacts/black-box/",
            "artifacts/carmaker/",
            "artifacts/bootloader/",
        }
        self.assertTrue(expected.issubset(set(home.links)))


if __name__ == "__main__":
    unittest.main()
