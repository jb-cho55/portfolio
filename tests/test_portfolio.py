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
            "국민대학교 자동차IT융합학과에서 자동차·전자·소프트웨어를 학습하고, AURIX 기반 Embedded SW 구현과 CANoe/CAPL 기반 차량 SW 검증을 수행했습니다.",
            self.html,
        )
        self.assertNotIn("융합 지식을 쌓고", self.html)
        self.assertNotIn("분석해 왔습니다", self.html)

    def test_vehicle_embedded_sw_positioning_and_competencies(self):
        self.assertIn("Vehicle Embedded SW Portfolio", self.html)
        self.assertIn("Vehicle Embedded SW Engineer", self.html)
        self.assertNotIn("Embedded SW QA Portfolio", self.html)
        self.assertNotIn("Embedded SW QA Engineer", self.html)
        expected = [
            "차량 SW 개발과 검증 프로젝트에서 수행한 설계·구현·테스트·문제 해결 역량을 중심으로 정리했습니다.",
            "EMBEDDED IMPLEMENTATION",
            "Embedded C 기반 ECU 기능 구현",
            "AURIX 환경에서 UDS Bootloader, Flash Backup·Restore, SHA-256 무결성 검사 기능을 구현했습니다.",
            "VEHICLE COMMUNICATION",
            "차량 통신 및 진단 프로토콜 활용",
            "CAN·ISO-TP·UDS 통신 흐름을 이해하고 진단 서비스와 ECU 리프로그래밍 절차에 적용했습니다.",
            "TEST ENGINEERING",
            "요구사양 기반 테스트 설계·자동화",
            "요구사양을 테스트 조건과 판정 기준으로 구조화하고 CANoe/CAPL로 반복 시험을 자동화했습니다.",
            "DEBUGGING &amp; ANALYSIS",
            "디버깅 및 결함 원인 분석",
            "CAN Trace와 Trace32를 활용해 통신 동작과 Memory Alignment 오류의 재현 조건과 원인을 분석했습니다.",
        ]
        for content in expected:
            self.assertIn(content, self.html)

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
        self.assertNotIn("포트폴리오 재구성", self.html)
        self.assertNotIn("assets/images/network_setup.svg", self.html)
        self.assertGreaterEqual(self.html.count('loading="lazy"'), 10)
        self.assertGreaterEqual(self.html.count("alt="), 10)

    def test_credentials_include_original_pdf_evidence(self):
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
        self.assertGreaterEqual(self.html.count("원본 PDF 보기"), 5)
        self.assertGreaterEqual(self.html.count('target="_blank"'), 11)
        self.assertGreaterEqual(self.html.count('rel="noreferrer"'), 11)

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
        self.assertIn('class="credential-evidence-grid"', self.html)

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

    def test_typography_and_readability_requirements(self):
        compact = self.html.replace(" ", "")
        self.assertIn("pretendard/dist/web/static/pretendard.css", self.html)
        self.assertIn('font-family:"Pretendard","NotoSansKR","MalgunGothic"', compact)
        self.assertIn("font-size:13px", compact)
        self.assertGreaterEqual(compact.count("max-width:48rem"), 2)
        self.assertIn("color:#667085", compact)
        self.assertNotIn("font-weight:850", compact)


if __name__ == "__main__":
    unittest.main()
