from collections import Counter
from pathlib import Path
import unittest

from tests.site_audit import heading_levels, parse_html


class AccessibilityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = Path(__file__).parents[1] / "site" / "index.html"
        cls.document = parse_html(cls.page)

    def test_page_has_one_main_and_one_h1(self):
        tags = [tag for tag, _ in self.document.tags]
        self.assertEqual(tags.count("main"), 1)
        self.assertEqual(tags.count("h1"), 1)

    def test_skip_link_targets_main(self):
        skip_links = [
            attrs
            for tag, attrs in self.document.tags
            if tag == "a" and "skip-link" in attrs.get("class", "").split()
        ]
        self.assertEqual(len(skip_links), 1)
        target = skip_links[0].get("href", "").removeprefix("#")
        self.assertTrue(target)
        self.assertIn(target, self.document.ids)
        self.assertTrue(
            any(tag == "main" and attrs.get("id") == target for tag, attrs in self.document.tags)
        )

    def test_ids_are_unique(self):
        duplicates = [name for name, count in Counter(self.document.ids).items() if count > 1]
        self.assertEqual(duplicates, [])

    def test_heading_levels_do_not_skip(self):
        levels = heading_levels(self.document)
        self.assertTrue(levels)
        self.assertEqual(levels[0], 1)
        for current, following in zip(levels, levels[1:]):
            with self.subTest(current=current, following=following):
                self.assertLessEqual(following - current, 1)

    def test_images_have_accessible_text_and_raster_dimensions(self):
        images = [attrs for tag, attrs in self.document.tags if tag == "img"]
        self.assertTrue(images)
        for attrs in images:
            with self.subTest(src=attrs.get("src")):
                self.assertTrue(attrs.get("alt", "").strip())
                if attrs.get("src", "").lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    self.assertGreater(int(attrs.get("width", "0")), 0)
                    self.assertGreater(int(attrs.get("height", "0")), 0)

    def test_new_tab_links_are_safe(self):
        for tag, attrs in self.document.tags:
            if tag == "a" and attrs.get("target") == "_blank":
                with self.subTest(href=attrs.get("href")):
                    self.assertIn("noreferrer", attrs.get("rel", "").split())


if __name__ == "__main__":
    unittest.main()
