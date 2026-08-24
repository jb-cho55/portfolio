from pathlib import Path
import unittest

from tests.site_audit import parse_html


class HomeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = Path(__file__).parents[1] / "site" / "index.html"
        cls.document = parse_html(cls.page)

    def test_positioning_and_contact_are_immediately_available(self):
        self.assertIn("차량 소프트웨어를 검증 가능한 증거로 설명합니다.", self.document.text)
        self.assertIn("CANoe/CAPL 검증 자동화와 결함 원인 분석", self.document.text)
        self.assertIn("mailto:cho.jeongbin55@gmail.com", self.document.links)
        self.assertIn("https://github.com/jb-cho55", self.document.links)
        self.assertNotIn("resume.pdf", " ".join(self.document.links))

    def test_three_flagships_are_in_priority_order(self):
        page = self.page.read_text(encoding="utf-8")
        positions = [
            page.index(marker)
            for marker in (
                'id="black-box-project"',
                'id="carmaker-project"',
                'id="bootloader-project"',
            )
        ]
        self.assertEqual(positions, sorted(positions))

    def test_qualified_metrics_and_ownership_are_visible(self):
        for phrase in (
            "정적 4건 · 동적 11건",
            "6인 팀 최종 평가",
            "최대 오차 0.16 m",
            "7개 UDS 서비스",
            "개인 프로젝트",
            "팀장 · 주차 경로계획",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.document.text)


if __name__ == "__main__":
    unittest.main()
