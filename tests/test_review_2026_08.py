"""2026-08 채용담당자·직무담당자 관점 점검 반영분 회귀 테스트.

항목 ID는 점검 리스트(B-1, B-2, B-5)를 따른다.
"""

from pathlib import Path
import re
import unittest

from portfolio_sections import card


ROOT = Path(__file__).resolve().parents[1]


class Review202608Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.black_box = (ROOT / "artifacts/black-box/index.html").read_text(encoding="utf-8")
        cls.bootloader = (ROOT / "artifacts/bootloader/index.html").read_text(encoding="utf-8")

    def test_a01_reachable_contact_exists_in_hero_and_closing(self):
        """채용담당자가 연락할 수 있어야 한다 — 히어로와 클로징 양쪽에 mailto."""
        mailto = 'href="mailto:cho.jeongbin55@gmail.com"'
        self.assertEqual(self.index.count(mailto), 2)

        hero_actions = self.index[self.index.index('class="hero-actions"'):]
        hero_actions = hero_actions[:hero_actions.index("</div>")]
        self.assertIn(mailto, hero_actions)

        closing = self.index[self.index.index('class="contact"'):]
        self.assertIn("cho.jeongbin55@gmail.com</a>", closing)

    def test_b01_bootloader_states_cryptographic_scope_and_limit(self):
        """SHA-256 검사의 한계를 스스로 밝힌다 (HMAC·전자서명이 아님)."""
        bootloader = card(self.index, "bootloader-project")
        self.assertIn("<dt>범위·한계</dt>", bootloader)
        for phrase in [
            "고정 키를 접두어로 붙인 SHA-256",
            "HMAC이나 전자서명이 아니므로",
            "해시까지 다시 계산하는 공격자는 막지 못합니다",
        ]:
            self.assertIn(phrase, bootloader)

    def test_b02_capl_excerpt_is_verbatim_not_paraphrased(self):
        """CAPL 발췌는 실제 소스 그대로여야 한다. 지어낸 호출이 있으면 실패."""
        for invented in ["setTimer(detectionTimer", "waitBattReference();", "waitIGNReference();"]:
            self.assertNotIn(invented, self.black_box, f"지어낸 코드 발췌: {invented}")

        for actual in [
            "void waitBattReference(int timeoutMs , int data)",
            "TestWaitForMessage(BATT_01_10ms, timeoutMs)",
            "TestGetWaitEventMsgData(battRef_msg)",
            "setTimerCyclic(t_1ms ,1)",
            "TestStepFail",
        ]:
            self.assertIn(actual, self.black_box, f"원본 소스에 있는 표현 누락: {actual}")

    def test_b02_capl_excerpt_escapes_html_operators(self):
        """비교 연산자가 날것으로 들어가면 마크업이 깨진다."""
        self.assertIn("battPercent &lt;= 15", self.black_box)
        self.assertIn("i == 1 &amp;&amp; j == 1", self.black_box)
        self.assertNotIn("battPercent <= 15", self.black_box)

    def test_b05_uds_service_count_matches_listed_sids(self):
        """'7개 서비스' 배지와 본문 SID 나열이 일치해야 한다."""
        bootloader = card(self.index, "bootloader-project")
        self.assertIn("UDS 7개 서비스 흐름", bootloader)
        self.assertIn("UDS 7개 서비스(0x10·0x27·0x31·0x34·0x36·0x37·0x11)", bootloader)
        self.assertIn("EraseMemory·Backup과 CheckProgrammingDependencies 두 루틴", bootloader)

    def test_a05_university_period_is_stated(self):
        """국민대 카드만 기간이 비어 있으면 안 된다."""
        self.assertIn("2020.03–2026.02 · 졸업", self.index)

    def test_b03_static_code_review_findings_are_surfaced(self):
        """스스로 찾은 결함이 페이지에 드러나야 한다 — 근거 수준 단서와 함께."""
        self.assertIn('<section id="review" class="panel">', self.bootloader)
        for phrase in [
            "3,579바이트",
            "valid pattern을 기록합니다",
            "고정 Seed/Key",
            "ECU에서 검증한 결과가 아닙니다",
        ]:
            self.assertIn(phrase, self.bootloader)

    def test_b10_factor_defect_is_listed_as_representative(self):
        """CANdb Factor 미적용 결함(15mV)은 대표 결과에 있어야 한다."""
        self.assertIn("Factor 0.001 미적용으로 raw 15(15mV)", self.black_box)

    def test_c01_defect_result_captures_exist_and_are_linked(self):
        """공개 결정된 판정 화면 10장이 실제로 존재하고 페이지에 연결돼야 한다."""
        names = [
            "result_batt_percent_15_fail", "result_batt_percent_80_fail",
            "result_batt_voltage_invalid_precondition", "result_batt_voltage_recovery_fail",
            "result_battery_charging_invalid_precondition", "result_engine_fault_fail",
            "result_ign_49_cycle_fail", "result_ignition_fault_fail",
            "result_steering_invalid_condition_detected", "result_steering_timing_fail",
        ]
        for name in names:
            path = ROOT / f"assets/images/black-box/{name}.png"
            self.assertTrue(path.is_file(), f"캡처 누락: {path}")
            self.assertIn(f"../../assets/images/black-box/{name}.png", self.black_box)

    def test_c01_requirement_document_captures_stay_unpublished(self):
        """강사 요구사양 PDF 캡처는 공개 사이트에 들어오면 안 된다."""
        published = list((ROOT / "assets/images").rglob("*.png"))
        for path in published:
            self.assertFalse(
                path.name.startswith(("req_p", "static_req", "static_ref", "static_defect")),
                f"요구사양 문서 캡처가 공개 자산에 포함됨: {path.name}",
            )

    def test_a02_private_repository_policy_is_explained(self):
        """GitHub에 없는 이유를 페이지가 스스로 설명해야 한다."""
        self.assertIn("교육 자료 보호를 위해 비공개로 유지합니다", self.index)

    def test_a03_hero_states_what_he_does(self):
        """채용담당자가 첫 화면에서 직무를 판단할 수 있어야 한다."""
        self.assertIn("CANoe/CAPL 자동화로 시험하고, 결함의 원인까지 규명합니다", self.index)

    def test_a07_test_scale_has_a_denominator(self):
        """결함 건수만 있고 모수가 없으면 규모를 가늠할 수 없다."""
        self.assertIn("CAPL 스크립트 6종·테스트케이스 24개", self.black_box)
        self.assertIn("101 × Ignition 2 × Engine 2 = 404조합", self.black_box)

    def test_a08_og_image_is_declared_and_present(self):
        self.assertIn(
            '<meta property="og:image" content="https://jb-cho55.github.io/portfolio/assets/og-card.png">',
            self.index,
        )
        self.assertTrue((ROOT / "assets/og-card.png").is_file())

    def test_b04_evidence_level_is_stated_on_main_page(self):
        """저장소보다 페이지가 더 단정적이면 안 된다."""
        bootloader = card(self.index, "bootloader-project")
        self.assertIn("<dt>근거 수준</dt>", bootloader)
        for phrase in [
            "교육 당시 ECU에서 수행한 시나리오 시험 기록",
            "새 빌드나 하드웨어 재시험을 하지 않았고",
            "PASS · Not executed · Evidence unavailable",
        ]:
            self.assertIn(phrase, bootloader)

    def test_b06_capl_api_names_accompany_the_local_term(self):
        self.assertIn("<code>TestWaitForMessage</code>로 최신 수신 프레임을 확인", self.black_box)

    def test_b07_b08_b09_standards_and_techniques_are_named(self):
        for phrase in [
            "경계값 분석·동등분할·상태 전이 테스트로 Test Case 설계",
            "A-SPICE SWE.6 관점에서 요구사양–Test Case–판정 결과를 추적",
            "ISO 26262 기능안전, MISRA C 코딩 표준, Polyspace 정적 분석 (교육 이수)",
        ]:
            self.assertIn(phrase, self.index)

    def test_b11_provided_training_environment_is_disclosed(self):
        self.assertIn("제공된 AURIX·MCAL 교육 환경 위에서", self.index)

    def test_c02_skill_and_project_order_lead_with_verification(self):
        self.assertLess(
            self.index.index("PROJECT 01 · VEHICLE SW VERIFICATION"),
            self.index.index("PROJECT 02 · EMBEDDED SW DEVELOPMENT"),
        )

    def test_c04_other_projects_are_public_and_linked(self):
        for repo in [
            "IVS-CarMaker-ADAS",
            "Autonomous-Computing-Platform-FinalProject",
            "Capstone_DeepRacer_KOOKNET_2025",
        ]:
            self.assertIn(f"https://github.com/jb-cho55/{repo}", self.index)
        # 해커톤 주최측 스타터 저장소는 본인 산출물로 보이지 않으므로 링크하지 않는다
        self.assertNotIn("IVS_JETRACER", self.index)

    def test_fix04_main_page_has_no_unstyled_inline_code(self):
        """메인에는 <code>를 쓰지 않는다. 다시 넣으려면 스타일부터 정의해야 한다."""
        self.assertNotIn("<code>", self.index)
        shared = (ROOT / "assets/bootloader/shared.css").read_text(encoding="utf-8")
        self.assertIn("code{font-family:Consolas", shared)

    def test_fix05_other_projects_grid_is_not_five_columns(self):
        """.artifact-grid는 산출물 5개용 5열이라 3개짜리 기타 프로젝트에 그대로 쓰면 안 된다."""
        self.assertRegex(
            self.index,
            r"@media\s*\(min-width:\s*901px\)\s*\{\s*\.other-projects \.artifact-grid\s*\{[^}]*repeat\(3,",
        )

    def test_fix06_result_gallery_cards_do_not_stretch(self):
        self.assertIn(".result-gallery{align-items:start}", self.black_box)

    def test_ui01_artifact_links_open_in_same_tab(self):
        """산출물은 같은 사이트 안이므로 새 탭이 아니라 현재 창에서 이동한다."""
        for m in re.finditer(r'<a[^>]*href="artifacts/[^"]+"[^>]*>', self.index):
            self.assertNotIn("_blank", m.group(0), f"산출물 링크가 새 탭으로 열림: {m.group(0)[:90]}")

    def test_ui02_meta_row_fills_the_card_without_wrapping(self):
        """각 칸은 최소한 내용 폭을 갖고, 남는 폭은 균등 분배해 오른쪽에 빈 구간이 없어야 한다."""
        self.assertIn("grid-template-columns: repeat(5, minmax(max-content, 1fr));", self.index)
        shared = (ROOT / "assets/bootloader/shared.css").read_text(encoding="utf-8")
        self.assertIn("grid-template-columns:repeat(5,minmax(max-content,1fr))", shared)
        for css, label in [(self.index, "index.html"), (shared, "shared.css")]:
            self.assertIn("align-items:center" if css is shared else "align-items: center;", css, label)

    def test_ui03_implementation_line_has_no_lone_bold_token(self):
        """문장 안에서 0x31만 볼드로 튀지 않아야 한다."""
        self.assertIn("0x31은 EraseMemory·Backup과", self.index)
        self.assertNotIn("<code>0x31</code>", self.index)

    def test_ui04_resume_link_matches_file_presence(self):
        """resume.pdf가 있으면 노출, 없으면 hidden — 어긋나면 실패."""
        m = re.search(r'<p class="contact-resume"([^>]*)>', self.index)
        self.assertIsNotNone(m, "이력서 자리(.contact-resume)가 없음")
        is_hidden = "hidden" in m.group(1)
        has_file = (ROOT / "assets/resume.pdf").is_file()
        self.assertEqual(
            is_hidden, not has_file,
            "assets/resume.pdf 를 넣었다면 hidden 을 지우고, 지웠다면 hidden 을 다시 붙여야 한다",
        )
        self.assertIn('href="assets/resume.pdf"', self.index)

    def test_ui05b_meta_row_has_no_grey_gutters(self):
        """컨테이너를 회색으로 두면 좌우 padding이 '잘린 띠'처럼 보인다."""
        rule = re.search(r"\.project-meta \{(?P<body>[^}]*)\}", self.index)
        self.assertIsNotNone(rule)
        decl = "".join(rule.group("body").split())
        self.assertIn("background:#fff;", decl)
        self.assertNotIn("background:var(--line);", decl)
        self.assertNotIn("gap:1px;", decl)
        self.assertIn(".project-meta > div + div { border-left: 1px solid var(--line); }", self.index)

        shared = (ROOT / "assets/bootloader/shared.css").read_text(encoding="utf-8")
        self.assertIn(".meta-grid div+div{border-left:1px solid var(--line)}", shared)

    def test_ui11_each_card_has_a_clear_way_into_its_evidence_page(self):
        """아코디언을 없앤 자리에 깊이로 가는 진입점이 남아 있어야 한다."""
        for anchor, href in [("black-box-project", "artifacts/black-box/index.html"),
                             ("bootloader-project", "artifacts/bootloader/index.html")]:
            block = card(self.index, anchor)
            self.assertIn(f'<a class="project-more" href="{href}">', block)
        self.assertEqual(self.index.count('class="project-more"'), 2)

    def test_ui12_section_rail_lists_every_main_section(self):
        rail = self.index[self.index.index('class="section-rail"'):]
        rail = rail[:rail.index("</nav>")]
        for section in ["hero", "projects", "skills", "education", "credentials"]:
            self.assertIn(f'href="#{section}"', rail)
            self.assertIn(f'id="{section}"', self.index, f"레일이 가리키는 섹션 없음: {section}")
        self.assertIn("IntersectionObserver", self.index, "현재 위치 표시 로직 없음")
        self.assertIn("@media (min-width: 1400px) { .section-rail { display: grid; } }", self.index)

    def test_ui13_section_rail_is_readable_and_clears_the_content(self):
        """흐린 12px 글자로는 안 읽힌다 — 패널로 분리하고 대비를 준다."""
        rule = re.search(r"\.section-rail \{(?P<body>[^}]*)\}", self.index)
        self.assertIsNotNone(rule)
        panel = "".join(rule.group("body").split())
        self.assertIn("border:1pxsolidvar(--line);", panel)
        self.assertIn("background:rgba(255,255,255,.93);", panel)
        # 본문 폭(--max) 바깥으로 밀어내 카드와 겹치지 않게 한다
        self.assertIn("calc((100vw-var(--max))/2-152px)", panel)

        link = re.search(r"\.section-rail a \{(?P<body>[^}]*)\}", self.index)
        self.assertIsNotNone(link)
        decl = "".join(link.group("body").split())
        self.assertIn("font-size:13px;", decl)
        self.assertIn("color:#46536a;", decl)

    def test_private_repo_names_stay_unpublished(self):
        """저장소 비공개 방침 유지 — 이름이 새어나가면 실패."""
        for page in (self.index, self.black_box):
            self.assertNotIn("IVS-Black-Box-Testing", page)
            self.assertNotIn("Bootloader_Design_For_OTA", page)


if __name__ == "__main__":
    unittest.main()
