from pathlib import Path
import unittest


class PortfolioContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = Path("index.html").read_text(encoding="utf-8")

    def test_vehicle_embedded_sw_positioning(self):
        self.assertIn("Vehicle Embedded SW Portfolio", self.html)
        self.assertIn("Vehicle Embedded SW Engineer", self.html)
        self.assertIn("AURIX 기반 ECU 기능 구현", self.html)
        self.assertIn("CANoe/CAPL 기반 차량 SW 검증", self.html)
        self.assertNotIn("Embedded SW QA Engineer", self.html)

    def test_featured_projects_are_limited_to_two_and_bootloader_is_first(self):
        self.assertEqual(self.html.count('class="project-card"'), 2)
        bootloader = self.html.index("OTA를 위한 Bootloader 설계")
        black_box = self.html.index("IVS Black Box Validation")
        self.assertLess(bootloader, black_box)

    def test_each_project_has_five_line_summary(self):
        self.assertEqual(self.html.count('class="project-summary"'), 2)
        for label in ["<dt>목표</dt>", "<dt>역할</dt>", "<dt>구현</dt>", "<dt>검증</dt>", "<dt>결과</dt>"]:
            self.assertEqual(self.html.count(label), 2)

    def test_each_project_has_key_results_box(self):
        self.assertEqual(self.html.count('class="key-results"'), 2)
        self.assertEqual(self.html.count("<h4>KEY RESULTS</h4>"), 2)
        for result in [
            "UDS 7개 서비스 흐름",
            "Backup·Restore",
            "SHA-256",
            "Trap 원인 해결",
            "정적 결함 4건",
            "동적 결함 11건",
            "CAPL 회귀 테스트",
            "프로젝트 우수상",
        ]:
            self.assertIn(result, self.html)

    def test_artifacts_are_unified_by_five_categories(self):
        self.assertEqual(self.html.count('class="artifact-section"'), 2)
        for category in ["CODE", "TEST", "DOCUMENT", "DEMO", "EVIDENCE"]:
            self.assertEqual(self.html.count(f"<strong>{category}</strong>"), 2)

    def test_private_project_repositories_are_not_exposed(self):
        self.assertIn("https://github.com/jb-cho55", self.html)
        self.assertNotIn("IVS-Black-Box-Validation", self.html)
        self.assertNotIn("IVS-Black-Box-Testing", self.html)
        self.assertNotIn("Bootloader_Design_For_OTA", self.html)

    def test_problem_solving_is_standardized(self):
        self.assertEqual(self.html.count('class="problem-flow"'), 2)
        for label in ["<strong>증상</strong>", "<strong>원인 분석</strong>", "<strong>수정</strong>", "<strong>재검증</strong>"]:
            self.assertEqual(self.html.count(label), 2)

    def test_bootloader_case_study_contains_implementation_and_validation_scope(self):
        expected = [
            "UDS 0x10·0x27·0x34·0x36·0x37",
            "Application Backup·Restore",
            "SHA-256 비교",
            "정상 다운로드",
            "전송 순서 오류",
            "무결성 불일치",
            "양방향 Flash Write",
        ]
        bootloader = self.html[self.html.index('id="bootloader-project"'):self.html.index('id="black-box-project"')]
        for content in expected:
            self.assertIn(content, bootloader)

    def test_bootloader_alignment_story_follows_required_order(self):
        detail = self.html[self.html.index('id="bootloader-debug"'):self.html.index('id="black-box-project"')]
        expected = [
            "증상",
            "FlsLoader_Write",
            "원인 분석",
            "Trace32",
            "수정",
            "uint32",
            "재검증",
            "Application→Backup",
        ]
        positions = [detail.index(term) for term in expected]
        self.assertEqual(positions, sorted(positions))

    def test_black_box_case_study_contains_test_evidence(self):
        expected = [
            "Fault Detection·Recovery·Clear",
            "정적 결함 4건",
            "동적 결함 11건",
            "IGN 50 Cycle",
            "Steering Timing",
            "기대 결과",
            "실제 결과",
            "영향도",
        ]
        black_box = self.html[self.html.index('id="black-box-project"'):]
        for content in expected:
            self.assertIn(content, black_box)

    def test_black_box_fresh_frame_story_follows_required_order(self):
        detail = self.html[self.html.index("대표 문제 해결 — Fresh Frame 동기화"):]
        expected = [
            "증상",
            "이전 프레임",
            "원인 분석",
            "CAN Trace Timestamp",
            "수정",
            "waitBattReference",
            "재검증",
            "CAPL 회귀 테스트",
        ]
        positions = [detail.index(term) for term in expected]
        self.assertEqual(positions, sorted(positions))

    def test_black_box_gallery_uses_actual_project_pngs(self):
        gallery = [
            ("assets/images/black-box/network_setup.png", "CANoe Network 구성"),
            ("assets/images/black-box/automation_test_environment.png", "CAPL 자동화 테스트 환경"),
            ("assets/images/black-box/panel_trace.png", "Panel 및 Trace 화면"),
            ("assets/images/black-box/test_environment.png", "Black Box Test Environment"),
            ("assets/images/black-box/defect_batt_percent_15.png", "Batt Percent 15% Test Result"),
        ]
        for path, caption in gallery:
            self.assertIn(f'src="{path}"', self.html)
            self.assertIn(f'href="{path}"', self.html)
            self.assertIn(caption, self.html)

    def test_skill_section_describes_applied_experience_levels(self):
        self.assertIn('id="skills"', self.html)
        self.assertIn("<h2>기술 경험 수준</h2>", self.html)
        for level in ["프로젝트 적용", "프로토콜 적용", "자동화 구현", "원인 분석", "교육·실습 적용", "자격·프로젝트 적용"]:
            self.assertIn(level, self.html)
        for evidence in [
            "UDS Bootloader",
            "Trace와 System Variable",
            "Trap 레지스터",
            "EB tresos",
            "ISTQB CTFL 기반",
        ]:
            self.assertIn(evidence, self.html)

    def test_skill_section_is_not_a_plain_tool_list(self):
        self.assertNotIn("<h2>기술 스택</h2>", self.html)
        self.assertGreaterEqual(self.html.count('class="skill-card"'), 6)
        self.assertEqual(self.html.count('class="skill-level"'), 6)

    def test_project_detail_controls_are_accessible(self):
        self.assertEqual(self.html.count(">프로젝트 상세 보기</button>"), 2)
        for control_id in ["bootloader-details", "black-box-details"]:
            self.assertIn(f'aria-controls="{control_id}"', self.html)
            self.assertIn(f'id="{control_id}"', self.html)
        self.assertGreaterEqual(self.html.count('aria-expanded="false"'), 3)
        self.assertGreaterEqual(self.html.count("hidden"), 2)
        self.assertIn("detail.hidden", self.html)
        self.assertIn("button.textContent", self.html)

    def test_credentials_include_redacted_pdf_evidence(self):
        evidence = {
            "HL만도·HL클레무브 IVS 5기 수료증": "assets/evidence/ivs_completion.pdf",
            "Black Box Testing 프로젝트 우수상": "assets/evidence/black_box_award.pdf",
            "IVS 5기 모범상": "assets/evidence/exemplary_award.pdf",
            "정보처리기사": "assets/evidence/information_processing_engineer.pdf",
            "ISTQB CTFL": "assets/evidence/istqb_ctfl.pdf",
        }
        for label, path in evidence.items():
            self.assertIn(label, self.html)
            self.assertIn(f'href="{path}"', self.html)
        self.assertEqual(self.html.count('class="credential-evidence-card"'), 5)

    def test_credential_evidence_is_labeled_as_redacted(self):
        self.assertIn("개인정보 보호를 위해 식별번호와 검증 코드를 마스킹했습니다.", self.html)
        self.assertEqual(self.html.count("마스킹 증빙 보기"), 5)
        self.assertNotIn("원본 PDF 보기", self.html)

    def test_credential_thumbnails_are_accessible(self):
        thumbnails = [
            "assets/evidence/thumbnails/ivs_completion.webp",
            "assets/evidence/thumbnails/black_box_award.webp",
            "assets/evidence/thumbnails/exemplary_award.webp",
            "assets/evidence/thumbnails/information_processing_engineer.webp",
            "assets/evidence/thumbnails/istqb_ctfl.webp",
        ]
        for path in thumbnails:
            self.assertIn(f'src="{path}"', self.html)
        self.assertGreaterEqual(self.html.count('loading="lazy"'), 10)
        self.assertGreaterEqual(self.html.count("alt="), 10)

    def test_education_contains_ivs_hours(self):
        self.assertIn('id="education"', self.html)
        self.assertIn("812시간", self.html)

    def test_readability_tokens_and_responsive_layout(self):
        compact = self.html.replace(" ", "")
        self.assertIn("--max:1080px", compact)
        self.assertIn("line-height:1.7", compact)
        self.assertIn("@media(max-width:900px)", compact)
        self.assertIn("@media(max-width:600px)", compact)
        self.assertIn("pretendard/dist/web/static/pretendard.css", self.html)
        self.assertNotIn("font-weight:850", compact)

    def test_sections_prioritize_projects_before_skills(self):
        self.assertLess(self.html.index('id="projects"'), self.html.index('id="skills"'))
        self.assertLess(self.html.index('href="#projects"'), self.html.index('href="#skills"'))


if __name__ == "__main__":
    unittest.main()
