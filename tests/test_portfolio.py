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
        self.assertIn(
            "국민대학교 자동차IT융합학과에서 자동차·전자·소프트웨어를 학습하고, CANoe/CAPL 기반 차량 SW 테스트 설계와 자동화 검증을 수행했습니다.",
            self.html,
        )
        self.assertNotIn("융합 지식을 쌓고", self.html)
        self.assertNotIn("분석해 왔습니다", self.html)

    def test_project_is_prioritized_before_core_fit(self):
        self.assertLess(self.html.index('id="projects"'), self.html.index('id="core-fit"'))
        self.assertLess(self.html.index('href="#projects"'), self.html.index('href="#core-fit"'))

    def test_project_surfaces_scannable_results(self):
        self.assertIn('class="project-metrics"', self.html)
        for result in ["정적 결함 4건", "동적 동작 결함 검출", "CAPL 테스트 자동화", "프로젝트 우수상"]:
            self.assertIn(result, self.html)

    def test_sections_use_korean_first_hierarchy(self):
        self.assertIn("<h2>대표 프로젝트</h2>", self.html)
        self.assertIn("<h2>직무 역량</h2>", self.html)
        self.assertIn("<h2>학력 및 교육</h2>", self.html)
        self.assertNotIn("<h2>Embedded SW QA 직무 역량</h2>", self.html)

    def test_readability_tokens_are_professional(self):
        compact = self.html.replace(" ", "")
        self.assertIn("--max:1080px", compact)
        self.assertIn("line-height:1.7", compact)
        self.assertIn("@media(max-width:900px)", compact)

    def test_education_contains_ivs_hours(self):
        self.assertIn('id="education"', self.html)
        self.assertIn("812시간", self.html)

    def test_project_contains_required_fields(self):
        for label in ["프로젝트 목표", "담당 역할", "수행 내용", "주요 성과"]:
            self.assertIn(label, self.html)

    def test_public_links_do_not_expose_private_project_repositories(self):
        self.assertIn("https://github.com/jb-cho55", self.html)
        self.assertNotIn("IVS-Black-Box-Validation", self.html)
        self.assertNotIn("IVS-Black-Box-Testing", self.html)
        self.assertNotIn("Bootloader_Design_For_OTA", self.html)

    def test_two_project_cards_are_present_in_order(self):
        black_box = self.html.index("IVS Black Box Testing")
        bootloader = self.html.index("OTA를 위한 Bootloader 설계")
        self.assertLess(black_box, bootloader)
        self.assertGreaterEqual(self.html.count('class="project-card"'), 2)

    def test_project_detail_controls_are_accessible(self):
        self.assertEqual(self.html.count("프로젝트 상세 보기"), 2)
        for control_id in ["black-box-details", "bootloader-details"]:
            self.assertIn(f'aria-controls="{control_id}"', self.html)
            self.assertIn(f'id="{control_id}"', self.html)
        self.assertGreaterEqual(self.html.count('aria-expanded="false"'), 2)
        self.assertGreaterEqual(self.html.count("hidden"), 2)

    def test_black_box_detail_contains_qa_evidence(self):
        for content in [
            "요구사양 기반 시험",
            "정적 결함 4건",
            "동적 결함 11건",
            "IGN 50 Cycle",
            "Steering Timing",
            "기대 결과",
            "실제 결과",
        ]:
            self.assertIn(content, self.html)

    def test_black_box_detail_uses_neutral_scope_label(self):
        self.assertIn("수행 범위", self.html)
        self.assertNotIn("본인 수행 범위", self.html)
        self.assertNotIn(
            "원본 요구사양과 내부 자료는 제외하고, 직접 수행한 테스트 환경·결함 분석·개선 방향만 포트폴리오용으로 재구성했습니다.",
            self.html,
        )

    def test_black_box_gallery_contains_accessible_local_evidence(self):
        gallery = [
            ("assets/images/network_setup.svg", "CANoe Network 구성"),
            ("assets/images/automation_test_environment.svg", "CAPL 자동화 테스트 환경"),
            ("assets/images/panel_trace.svg", "Panel 및 Trace 화면"),
            ("assets/images/defect_batt_percent_15.svg", "Test Result 근거"),
        ]
        for path, caption in gallery:
            self.assertIn(f'src="{path}"', self.html)
            self.assertIn(caption, self.html)
        self.assertGreaterEqual(self.html.count('loading="lazy"'), 4)
        self.assertGreaterEqual(self.html.count("<figcaption>"), 4)
        self.assertGreaterEqual(self.html.count("alt="), 4)

    def test_bootloader_details_use_two_development_stages(self):
        self.assertIn("개발 단계 1 — 애플리케이션 보호 및 복구", self.html)
        self.assertIn("개발 단계 2 — SW Binary 무결성 검증", self.html)
        self.assertNotIn("정적 코드 리뷰", self.html)
        self.assertNotIn("검증 범위와 한계", self.html)
        self.assertNotIn("+0x05/-0x05", self.html)

    def test_memory_alignment_error_story_is_explicit(self):
        expected = [
            "Memory Alignment Error",
            "프로젝트 진행 중",
            "Trace32",
            "4바이트 정렬",
            "uint32",
            "Application → Backup",
            "Backup → Application",
        ]
        detail = self.html[self.html.index('id="bootloader-details"'):]
        positions = [detail.index(term) for term in expected]
        self.assertEqual(positions, sorted(positions))

    def test_project_detail_script_updates_accessibility_state(self):
        self.assertIn("aria-expanded", self.html)
        self.assertIn("상세 내용 접기", self.html)
        self.assertIn("detail.hidden", self.html)
        self.assertIn("button.textContent", self.html)


if __name__ == "__main__":
    unittest.main()
