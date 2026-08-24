from collections import Counter
from pathlib import Path
import re
import unittest

from tests.site_audit import heading_levels, parse_html


class AccessibilityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = Path(__file__).parents[1] / "site" / "index.html"
        cls.stylesheet = cls.page.parent / "assets" / "css" / "site.css"
        cls.document = parse_html(cls.page)

    @classmethod
    def _rule_body(cls, selector: str) -> str:
        for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", cls.stylesheet.read_text(encoding="utf-8")):
            if selector in {item.strip() for item in selectors.split(",")}:
                return body
        raise AssertionError(f"No CSS rule found for {selector}")

    @classmethod
    def _resolved_color(cls, value: str) -> str:
        variable = re.fullmatch(r"var\((--[\w-]+)\)", value.strip())
        if not variable:
            return value.strip()
        declaration = re.search(
            rf"{re.escape(variable.group(1))}:\s*(#[0-9a-fA-F]{{6}})",
            cls._rule_body(":root"),
        )
        if not declaration:
            raise AssertionError(f"No color value found for {variable.group(1)}")
        return declaration.group(1)

    @staticmethod
    def _contrast_ratio(first: str, second: str) -> float:
        def luminance(color: str) -> float:
            channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
            linear = [
                channel / 12.92
                if channel <= 0.04045
                else ((channel + 0.055) / 1.055) ** 2.4
                for channel in channels
            ]
            return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

        lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
        return (lighter + 0.05) / (darker + 0.05)

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

    def test_default_palette_uses_only_approved_hex_literals(self):
        approved = {
            "#f6f5f2", "#171918", "#686b68", "#d7d8d3", "#888d88",
            "#ecece7", "#2f6662", "#202321", "#f3f2ed",
        }
        literals = set(re.findall(r"#[0-9a-fA-F]{3,8}\b", self.stylesheet.read_text(encoding="utf-8")))
        self.assertSetEqual({literal.lower() for literal in literals}, approved)

    def test_short_interactive_targets_have_44px_touch_boxes(self):
        for selector in (".identity", "nav a", ".text-link", ".detail-link", ".contact-links a"):
            with self.subTest(selector=selector):
                body = self._rule_body(selector)
                self.assertRegex(body, r"min-(?:inline-size|width):\s*44px")
                self.assertRegex(body, r"min-(?:block-size|height):\s*44px")

    def test_contact_focus_outline_meets_non_text_contrast(self):
        contact_background = re.search(
            r"background:\s*([^;]+)", self._rule_body(".contact-section")
        ).group(1)
        try:
            contact_focus = self._rule_body(".contact-section :focus-visible")
        except AssertionError:
            contact_focus = ""
        outline_color = re.search(r"outline-color:\s*([^;]+)", contact_focus)
        if outline_color:
            focus_color = outline_color.group(1)
        else:
            focus_color = re.search(
                r"outline:\s*\S+\s+\S+\s+([^;]+)",
                self._rule_body(":focus-visible"),
            ).group(1)

        ratio = self._contrast_ratio(
            self._resolved_color(focus_color),
            self._resolved_color(contact_background),
        )
        self.assertGreaterEqual(ratio, 3.0, f"focus contrast was only {ratio:.2f}:1")


if __name__ == "__main__":
    unittest.main()
