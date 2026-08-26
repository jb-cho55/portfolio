from pathlib import Path
import unittest

from portfolio_sections import card


class PortfolioContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = Path("index.html").read_text(encoding="utf-8")
        cls.black_box_page = Path("artifacts/black-box/index.html").read_text(encoding="utf-8")
        cls.bootloader_page = Path("artifacts/bootloader/index.html").read_text(encoding="utf-8")

    def test_vehicle_embedded_sw_positioning(self):
        self.assertIn("Vehicle Embedded SW Portfolio", self.html)
        self.assertIn("Vehicle Embedded SW Engineer", self.html)
        self.assertIn("국민대학교 자동차IT융합학과와 HL만도·HL클레무브 부트캠프", self.html)
        self.assertIn("차량 HW·SW 전반의 전문지식", self.html)
        self.assertNotIn("Embedded SW QA Engineer", self.html)

    def test_featured_projects_are_limited_to_two_and_verification_is_first(self):
        self.assertEqual(self.html.count('class="project-card"'), 2)
        black_box = self.html.index("IVS Black Box Validation")
        bootloader = self.html.index("OTA를 위한 Bootloader 설계")
        self.assertLess(
            black_box, bootloader,
            "지원 직무가 차량 SW 검증이므로 검증 프로젝트가 먼저 와야 한다",
        )

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

    def test_project_artifact_sections_have_project_specific_evidence(self):
        self.assertEqual(self.html.count('class="artifact-section"'), 2)
        bootloader = card(self.html, "bootloader-project")
        for label in ["MEMORY MAP", "UDS SEQUENCE", "TEST RESULTS", "TRACE32 · RESTORE", "EVIDENCE"]:
            self.assertIn(f"<strong>{label}</strong>", bootloader)
        black_box = card(self.html, "black-box-project")
        for label in ["CODE", "TEST", "DOCUMENT", "DEMO", "EVIDENCE"]:
            self.assertIn(f"<strong>{label}</strong>", black_box)

    def test_private_project_repositories_are_not_exposed(self):
        self.assertIn("https://github.com/jb-cho55", self.html)
        self.assertNotIn("IVS-Black-Box-Validation", self.html)
        self.assertNotIn("IVS-Black-Box-Testing", self.html)
        self.assertNotIn("Bootloader_Design_For_OTA", self.html)

    def test_problem_solving_is_standardized(self):
        """대표 문제 해결은 두 산출물 페이지 모두 증상→원인→수정→재검증 순서를 지킨다."""
        for page, terms in [
            (self.black_box_page, ["<strong>증상</strong>", "<strong>원인 분석</strong>",
                                   "<strong>수정</strong>", "<strong>재검증</strong>"]),
            (self.bootloader_page, ["1. 증상", "6. 원인", "7. 수정·재검증"]),
        ]:
            self.assertIn('class="steps"', page)
            positions = [page.index(term) for term in terms]
            self.assertEqual(positions, sorted(positions))

    def test_bootloader_case_study_contains_implementation_and_validation_scope(self):
        expected = [
            "UDS 7개 서비스(0x10·0x27·0x31·0x34·0x36·0x37·0x11)",
            "Application Backup·Restore",
            "SHA-256 비교",
            "정상 다운로드",
            "전송 순서 오류",
            "무결성 불일치",
            "양방향 Flash Write",
        ]
        bootloader = card(self.html, "bootloader-project")
        for content in expected:
            self.assertIn(content, bootloader)

    def test_bootloader_alignment_story_follows_required_order(self):
        detail = self.bootloader_page[self.bootloader_page.index('id="alignment-root-cause"'):]
        expected = [
            "1. 증상",
            "FlsLoader_Write",
            "3. Source address 확인",
            "4. Alignment Trap 확인",
            "6. 원인",
            "7. 수정·재검증",
            "uint32",
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
        black_box = card(self.html, "black-box-project")
        card_level = ["Fault Detection·Recovery·Clear", "정적 결함 4건", "동적 결함 11건"]
        for content in card_level:
            self.assertIn(content, black_box)
        for content in [c for c in expected if c not in card_level]:
            self.assertIn(content, self.black_box_page)

    def test_black_box_fresh_frame_story_follows_required_order(self):
        detail = self.black_box_page[self.black_box_page.index("대표 문제 해결 — Fresh Frame 동기화"):]
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
            ref = "../../" + path
            self.assertIn(f'src="{ref}"', self.black_box_page)
            self.assertIn(f'href="{ref}"', self.black_box_page)
            self.assertIn(caption, self.black_box_page)

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

    def test_depth_lives_only_on_the_artifact_pages(self):
        """상세 내용은 산출물 페이지 한 곳에만 — 메인에 아코디언을 다시 만들지 않는다."""
        for gone in ["project-detail-toggle", "project-detail-region", "detail-block", "problem-flow"]:
            self.assertNotIn(gone, self.html, f"메인에 아코디언 잔재가 남음: {gone}")
        self.assertEqual(self.html.count('class="artifact-item"'), 13)
        self.assertNotIn("detail.hidden", self.html, "아코디언 JS가 남아 있음")

    def test_credentials_open_redacted_image_evidence(self):
        evidence = {
            "HL만도·HL클레무브 IVS 5기 수료증": "assets/evidence/fullsize/ivs_completion.png",
            "Black Box Testing 프로젝트 우수상": "assets/evidence/fullsize/black_box_award.png",
            "IVS 5기 모범상": "assets/evidence/fullsize/exemplary_award.png",
            "정보처리기사": "assets/evidence/fullsize/information_processing_engineer.png",
            "ISTQB CTFL": "assets/evidence/fullsize/istqb_ctfl.png",
        }
        for label, path in evidence.items():
            self.assertIn(label, self.html)
            self.assertIn(f'href="{path}"', self.html)
        self.assertEqual(self.html.count('class="credential-evidence-card"'), 5)

    def test_credential_evidence_is_labeled_as_redacted(self):
        self.assertIn("개인정보 보호를 위해 식별번호와 검증 코드를 마스킹했습니다.", self.html)
        self.assertEqual(self.html.count("확대 이미지 보기"), 5)
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
        # 증빙 썸네일 5장이 메인에 남은 유일한 이미지 — 전부 지연 로딩·대체텍스트를 가진다
        self.assertEqual(self.html.count("<img "), len(thumbnails))
        self.assertEqual(self.html.count('loading="lazy"'), len(thumbnails))
        self.assertEqual(self.html.count("alt="), len(thumbnails))

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
