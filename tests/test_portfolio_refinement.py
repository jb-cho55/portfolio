from pathlib import Path
import re
import struct
import unittest

from portfolio_sections import card


ROOT = Path(__file__).resolve().parents[1]


class PortfolioRefinementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.evidence = (ROOT / "artifacts/bootloader/index.html").read_text(encoding="utf-8")
        cls.black_box_page = (ROOT / "artifacts/black-box/index.html").read_text(encoding="utf-8")
        cls.memory_svg = (ROOT / "assets/bootloader/memory-map.svg").read_text(encoding="utf-8")

    def test_profile_01_mentions_both_education_sources_and_vehicle_hw_sw(self):
        expected = (
            "국민대학교 자동차IT융합학과와 HL만도·HL클레무브 부트캠프를 통해 "
            "차량 HW·SW 전반의 전문지식을 습득했습니다."
        )
        self.assertIn(expected, self.index)

    def test_boot_01_trace32_captures_live_on_the_evidence_page(self):
        """디버깅 캡처는 산출물 페이지 한 곳에만 (메인의 사본 2장은 동일 해시라 삭제)."""
        for name in ["uds-routinecontrol-trace", "alignment-address-trace",
                     "alignment-trap-dmi", "trap-vector-breakpoint"]:
            path = f"assets/images/bootloader/{name}.png"
            self.assertTrue((ROOT / path).is_file(), path)
            self.assertIn(f"../../{path}", self.evidence)
        for removed in ["alignment-trap.png", "alignment-breakpoint.png"]:
            self.assertFalse((ROOT / "assets/images/bootloader" / removed).exists(), removed)

    def test_boot_01b_artifact_links_appear_exactly_once(self):
        """같은 곳으로 가는 링크 그리드가 카드 안에서 두 번 반복되면 안 된다."""
        bootloader = card(self.index, "bootloader-project")
        for sid in ["memory-map", "uds", "test", "trace32"]:
            self.assertEqual(
                bootloader.count(f'href="artifacts/bootloader/index.html#{sid}"'), 1,
                f"#{sid} 링크가 카드 안에서 중복됨",
            )

    def test_boot_02_reprogramming_flow_names_uds_services_and_sids(self):
        flow = self.evidence[self.evidence.index('id="overview"'):]
        for item in [
            "DiagnosticSessionControl(0x10)",
            "SecurityAccess(0x27)",
            "RoutineControl(0x31)",
            "RequestDownload(0x34)",
            "TransferData(0x36)",
            "RequestTransferExit(0x37)",
            "ECUReset(0x11)",
        ]:
            self.assertIn(item, flow)

    def test_boot_03_05_06_memory_map_copy_matches_request(self):
        self.assertIn(
            "Bootloader용 링크 스크립트의 주소와 크기를 기준으로 시각화했습니다.",
            self.evidence,
        )
        self.assertIn("<h3>근거</h3>", self.evidence)
        self.assertNotIn("링커 근거", self.evidence)
        self.assertIn(
            "Bootloader 링크 설정에서 Application과 Backup은 <code>reserved rom</code>으로 선언되어 "
            "Bootloader 코드가 해당 영역에 배치되지 않습니다. SHA-256은 이 프로젝트에서 Binary 변경 여부를 "
            "판단하는 무결성 검사로 사용했습니다.",
            self.evidence,
        )
        self.assertNotIn("양산 수준 코드 서명", self.evidence)

    def test_boot_04_restore_label_has_dedicated_non_overlapping_position(self):
        self.assertIn('id="restore-label"', self.memory_svg)
        self.assertIn('id="restore-arrow"', self.memory_svg)
        self.assertRegex(
            self.memory_svg,
            r'id="restore-label"[^>]*x="3[0-9]{2}"[^>]*y="4[6-9][0-9]"',
        )

    def test_boot_07_real_trace32_images_and_analysis_are_present(self):
        names = [
            "uds-routinecontrol-trace.png",
            "alignment-address-trace.png",
            "alignment-trap-dmi.png",
            "trap-vector-breakpoint.png",
        ]
        for name in names:
            path = ROOT / "assets/images/bootloader" / name
            self.assertTrue(path.is_file(), str(path))
            self.assertGreater(path.stat().st_size, 10_000)
            self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

        trace_page = self.evidence
        for item in [
            "uds-routinecontrol-trace.png",
            "alignment-address-trace.png",
            "alignment-trap-dmi.png",
            "trap-vector-breakpoint.png",
            "0x7000240D",
            "ALN Error",
            "BTV = 0x80027800",
            "PC = 0x80027840",
        ]:
            self.assertIn(item, trace_page)

        public_files = [ROOT / "index.html"]
        for directory in [ROOT / "artifacts", ROOT / "assets", ROOT / "docs/verification"]:
            public_files.extend(path for path in directory.rglob("*") if path.is_file())
        forbidden = ("prod-files-" + "secure.s3", "X-" + "Amz-")
        for path in public_files:
            if path.suffix.lower() in {".html", ".css", ".svg", ".md"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
                for marker in forbidden:
                    self.assertNotIn(marker, text, str(path))

    def test_blackbox_01_integrated_page_has_four_sections(self):
        page = ROOT / "artifacts/black-box/index.html"
        self.assertTrue(page.is_file())
        html = page.read_text(encoding="utf-8")
        for section_id, title in [
            ("code", "CODE"),
            ("test", "TEST"),
            ("document", "DOCUMENT"),
            ("demo", "DEMO"),
        ]:
            self.assertIn(f'id="{section_id}"', html)
            self.assertIn(f">{title}<", html)
        for path in [
            "../../assets/images/black-box/network_setup.png",
            "../../assets/images/black-box/automation_test_environment.png",
            "../../assets/images/black-box/panel_trace.png",
            "../../assets/images/black-box/test_environment.png",
            "../../assets/images/black-box/defect_batt_percent_15.png",
        ]:
            self.assertIn(path, html)

    def test_blackbox_02_main_buttons_open_integrated_page_sections(self):
        expected = {
            "CODE": "artifacts/black-box/index.html#code",
            "TEST": "artifacts/black-box/index.html#test",
            "DOCUMENT": "artifacts/black-box/index.html#document",
            "DEMO": "artifacts/black-box/index.html#demo",
        }
        for label, href in expected.items():
            pattern = rf'<a class="artifact-item" href="{re.escape(href)}">\s*<strong>{label}</strong>'
            self.assertRegex(self.index, pattern)

    def test_credential_01_02_cards_open_existing_images_and_keep_pdf_sources(self):
        names = [
            "ivs_completion",
            "black_box_award",
            "exemplary_award",
            "information_processing_engineer",
            "istqb_ctfl",
        ]
        for name in names:
            image = ROOT / f"assets/evidence/fullsize/{name}.png"
            pdf = ROOT / f"assets/evidence/{name}.pdf"
            self.assertTrue(image.is_file(), str(image))
            self.assertTrue(pdf.is_file(), str(pdf))
            self.assertGreater(image.stat().st_size, 20_000)
            data = image.read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", data[16:24])
            self.assertGreaterEqual(min(width, height), 1100)
            self.assertGreaterEqual(max(width, height), 1600)
            self.assertIn(f'href="assets/evidence/fullsize/{name}.png"', self.index)
        credentials = self.index[self.index.index('id="credentials"'):]
        self.assertNotRegex(credentials, r'class="credential-evidence-card" href="[^"]+\.pdf"')
        self.assertEqual(credentials.count("확대 이미지 보기"), 5)

    def test_cleanup_02_removes_superpowers_working_documents(self):
        superpowers = ROOT / "docs/superpowers"
        self.assertFalse(superpowers.exists(), str(superpowers))

    def test_verify_02_has_id_based_verification_record(self):
        path = ROOT / "docs/verification/2026-07-27-portfolio-refinement.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        expected = {
            "PROFILE-01": "PASS", "BOOT-01": "PASS", "BOOT-02": "PASS", "BOOT-03": "PASS",
            "BOOT-04": "PASS", "BOOT-05": "PASS", "BOOT-06": "PASS", "BOOT-07": "PASS",
            "BLACKBOX-01": "PASS", "BLACKBOX-02": "PASS", "CREDENTIAL-01": "PASS", "CREDENTIAL-02": "PASS",
            "CLEANUP-01": "PASS", "CLEANUP-02": "PASS", "CLEANUP-03": "PASS", "CLEANUP-04": "PASS",
            "VERIFY-01": "PASS", "VERIFY-02": "PASS",
        }
        for requirement_id, status in expected.items():
            self.assertRegex(text, rf"\| {re.escape(requirement_id)} \| .* \| {status} \|")


if __name__ == "__main__":
    unittest.main()
