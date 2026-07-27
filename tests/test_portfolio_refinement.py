from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PortfolioRefinementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.memory_map = (ROOT / "artifacts/bootloader/memory-map.html").read_text(encoding="utf-8")
        cls.memory_svg = (ROOT / "assets/bootloader/memory-map.svg").read_text(encoding="utf-8")

    def test_profile_01_mentions_both_education_sources_and_vehicle_hw_sw(self):
        expected = (
            "국민대학교 자동차IT융합학과와 HL만도·HL클레무브 부트캠프를 통해 "
            "차량 HW·SW 전반의 전문지식을 습득했습니다."
        )
        self.assertIn(expected, self.index)

    def test_boot_01_detail_has_capture_gallery_and_artifact_shortcuts(self):
        detail = self.index[
            self.index.index('id="bootloader-details"'):
            self.index.index('id="black-box-project"')
        ]
        for path in [
            "artifacts/bootloader/memory-map.html",
            "artifacts/bootloader/uds-sequence.html",
            "artifacts/bootloader/test-results.html",
            "artifacts/bootloader/trace32-restore.html",
            "assets/images/bootloader/alignment-trap.png",
            "assets/images/bootloader/alignment-breakpoint.png",
        ]:
            self.assertIn(path, detail)
            self.assertTrue((ROOT / path).is_file(), path)

    def test_boot_02_reprogramming_flow_names_uds_services_and_sids(self):
        flow = self.index[
            self.index.index('id="bootloader-flow"'):
            self.index.index('id="bootloader-implementation"')
        ]
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
            self.memory_map,
        )
        self.assertIn("<h2>근거</h2>", self.memory_map)
        self.assertNotIn("<h2>링커 근거</h2>", self.memory_map)
        self.assertIn(
            "Bootloader 링크 설정에서 Application과 Backup은 <code>reserved rom</code>으로 선언되어 "
            "Bootloader 코드가 해당 영역에 배치되지 않습니다. SHA-256은 이 프로젝트에서 Binary 변경 여부를 "
            "판단하는 무결성 검사로 사용했습니다.",
            self.memory_map,
        )
        self.assertNotIn("양산 수준 코드 서명", self.memory_map)

    def test_boot_04_restore_label_has_dedicated_non_overlapping_position(self):
        self.assertIn('id="restore-label"', self.memory_svg)
        self.assertIn('id="restore-arrow"', self.memory_svg)
        self.assertRegex(
            self.memory_svg,
            r'id="restore-label"[^>]*x="3[0-9]{2}"[^>]*y="4[6-9][0-9]"',
        )

    def test_boot_07_alignment_images_are_local_and_expiring_urls_are_absent(self):
        for name in ["alignment-trap.png", "alignment-breakpoint.png"]:
            path = ROOT / "assets/images/bootloader" / name
            self.assertTrue(path.is_file(), str(path))
            self.assertGreater(path.stat().st_size, 10_000)

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
            pattern = rf'<a class="artifact-item" href="{re.escape(href)}" target="_blank" rel="noreferrer">\s*<strong>{label}</strong>'
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
            image = ROOT / f"assets/evidence/thumbnails/{name}.webp"
            pdf = ROOT / f"assets/evidence/{name}.pdf"
            self.assertTrue(image.is_file(), str(image))
            self.assertTrue(pdf.is_file(), str(pdf))
            self.assertGreater(image.stat().st_size, 10_000)
            self.assertIn(f'href="assets/evidence/thumbnails/{name}.webp"', self.index)
        credentials = self.index[self.index.index('id="credentials"'):]
        self.assertNotRegex(credentials, r'class="credential-evidence-card" href="[^"]+\.pdf"')
        self.assertEqual(credentials.count("확대 이미지 보기"), 5)

    def test_cleanup_02_keeps_only_current_superpowers_documents(self):
        plans = sorted(p.name for p in (ROOT / "docs/superpowers/plans").glob("*.md"))
        specs = sorted(p.name for p in (ROOT / "docs/superpowers/specs").glob("*.md"))
        self.assertEqual(plans, ["2026-07-27-portfolio-evidence-refinement.md"])
        self.assertEqual(specs, ["2026-07-27-portfolio-evidence-refinement-design.md"])

    def test_verify_02_has_id_based_verification_record(self):
        path = ROOT / "docs/verification/2026-07-27-portfolio-refinement.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for requirement_id in [
            "PROFILE-01", "BOOT-01", "BOOT-02", "BOOT-03", "BOOT-04", "BOOT-05", "BOOT-06", "BOOT-07",
            "BLACKBOX-01", "BLACKBOX-02", "CREDENTIAL-01", "CREDENTIAL-02",
            "CLEANUP-01", "CLEANUP-02", "CLEANUP-03", "CLEANUP-04", "VERIFY-01", "VERIFY-02",
        ]:
            self.assertRegex(text, rf"\| {re.escape(requirement_id)} \| .* \| PASS \|")


if __name__ == "__main__":
    unittest.main()
