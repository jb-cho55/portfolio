from pathlib import Path
import struct
import unittest
from urllib.parse import urlsplit
from xml.etree import ElementTree

from tests.site_audit import parse_html


REPO_ROOT = Path(__file__).parents[1]
SITE_ROOT = REPO_ROOT / "site"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "pages.yml"
OG_IMAGE_URL = "https://jb-cho55.github.io/portfolio/assets/og-card.png"
CANONICALS = {
    "index.html": "https://jb-cho55.github.io/portfolio/",
    "artifacts/black-box/index.html": (
        "https://jb-cho55.github.io/portfolio/artifacts/black-box/"
    ),
    "artifacts/carmaker/index.html": (
        "https://jb-cho55.github.io/portfolio/artifacts/carmaker/"
    ),
    "artifacts/bootloader/index.html": (
        "https://jb-cho55.github.io/portfolio/artifacts/bootloader/"
    ),
}


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.documents = {
            route: parse_html(SITE_ROOT / route) for route in CANONICALS
        }

    def test_pages_have_unique_titles_and_descriptions(self):
        titles = []
        descriptions = []
        for route, document in self.documents.items():
            with self.subTest(route=route):
                description_tags = [
                    attrs
                    for tag, attrs in document.tags
                    if tag == "meta" and attrs.get("name") == "description"
                ]
                self.assertTrue(document.title.strip())
                self.assertEqual(len(description_tags), 1)
                self.assertTrue(description_tags[0].get("content", "").strip())
                titles.append(document.title.strip())
                descriptions.append(description_tags[0]["content"].strip())
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_each_page_has_matching_canonical_and_open_graph_urls(self):
        for route, expected_url in CANONICALS.items():
            document = self.documents[route]
            with self.subTest(route=route):
                canonical = [
                    attrs.get("href")
                    for tag, attrs in document.tags
                    if tag == "link" and attrs.get("rel") == "canonical"
                ]
                og_url = [
                    attrs.get("content")
                    for tag, attrs in document.tags
                    if tag == "meta" and attrs.get("property") == "og:url"
                ]
                og_image = [
                    attrs.get("content")
                    for tag, attrs in document.tags
                    if tag == "meta" and attrs.get("property") == "og:image"
                ]
                self.assertEqual(canonical, [expected_url])
                self.assertEqual(og_url, [expected_url])
                self.assertEqual(og_image, [OG_IMAGE_URL])
                self.assertEqual(urlsplit(og_image[0]).scheme, "https")

    def test_json_ld_describes_person_and_authored_case_studies(self):
        home = self.documents["index.html"]
        self.assertEqual(len(home.json_ld), 1)
        self.assertEqual(home.json_ld[0].get("@type"), "Person")
        self.assertEqual(home.json_ld[0].get("name"), "조정빈")
        self.assertEqual(home.json_ld[0].get("url"), CANONICALS["index.html"])

        for route, canonical in CANONICALS.items():
            if route == "index.html":
                continue
            document = self.documents[route]
            with self.subTest(route=route):
                self.assertEqual(len(document.json_ld), 1)
                article = document.json_ld[0]
                self.assertEqual(article.get("@type"), "TechArticle")
                self.assertEqual(article.get("url"), canonical)
                self.assertEqual(
                    article.get("author"),
                    {"@type": "Person", "name": "조정빈"},
                )

    def test_discovery_files_publish_exactly_the_four_canonical_routes(self):
        sitemap = SITE_ROOT / "sitemap.xml"
        root = ElementTree.parse(sitemap).getroot()
        namespace = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = {
            node.text for node in root.findall("sitemap:url/sitemap:loc", namespace)
        }
        self.assertEqual(locations, set(CANONICALS.values()))

        robots = (SITE_ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *", robots)
        self.assertIn("Allow: /portfolio/", robots)
        self.assertIn(
            "Sitemap: https://jb-cho55.github.io/portfolio/sitemap.xml",
            robots,
        )
        self.assertTrue((SITE_ROOT / ".nojekyll").is_file())

    def test_open_graph_png_is_1200_by_630(self):
        image = SITE_ROOT / "assets" / "og-card.png"
        data = image.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(data[12:16], b"IHDR")
        self.assertEqual(struct.unpack(">II", data[16:24]), (1200, 630))


class DeploymentWorkflowTests(unittest.TestCase):
    def test_workflow_gates_site_only_deployment_on_main_push(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for action in (
            "actions/checkout@v7",
            "actions/setup-python@v7",
            "actions/configure-pages@v6",
            "actions/upload-pages-artifact@v5",
            "actions/deploy-pages@v5",
        ):
            self.assertIn(action, workflow)
        self.assertIn("python -B -m unittest discover -s tests -v", workflow)
        self.assertIn("needs: test", workflow)
        self.assertIn("path: site/", workflow)
        self.assertIn("github.ref == 'refs/heads/main'", workflow)

    def test_workflow_uses_least_privilege_permissions(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn(
            "permissions:\n      pages: write\n      id-token: write",
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
