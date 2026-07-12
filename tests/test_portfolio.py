from pathlib import Path
import unittest


class PortfolioContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = Path("index.html").read_text(encoding="utf-8")

    def test_hero_contains_corporate_summary(self):
        self.assertIn("국민대학교 자동차IT융합학과 졸업", self.html)
        self.assertIn("ISTQB CTFL", self.html)
        self.assertIn("Black Box Testing 프로젝트 우수상", self.html)
        self.assertIn("직접 수행했습니다", self.html)
        self.assertNotIn("분석해 왔습니다", self.html)

    def test_education_contains_ivs_hours(self):
        self.assertIn('id="education"', self.html)
        self.assertIn("812시간", self.html)

    def test_project_contains_required_fields(self):
        for label in ["프로젝트 목표", "담당 역할", "수행 내용", "주요 성과"]:
            self.assertIn(label, self.html)

    def test_links_and_responsive_layout_exist(self):
        self.assertIn("https://github.com/jb-cho55", self.html)
        self.assertIn("https://github.com/jb-cho55/IVS-Black-Box-Validation", self.html)
        compact = self.html.replace(" ", "")
        self.assertIn("@media(max-width:900px)", compact)


if __name__ == "__main__":
    unittest.main()
