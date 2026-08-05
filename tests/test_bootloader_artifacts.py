from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "bootloader"
SECTIONS = ["memory-map", "uds", "test", "trace32"]


class BootloaderArtifactTests(unittest.TestCase):
    """부트로더 근거 자료는 블랙박스와 같은 모델 — 1페이지 + 앵커 4개."""

    @classmethod
    def setUpClass(cls):
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.page = (ARTIFACT_DIR / "index.html").read_text(encoding="utf-8")

    def test_evidence_is_one_page_with_four_anchors(self):
        self.assertEqual(
            sorted(q.name for q in ARTIFACT_DIR.glob("*.html")), ["index.html"],
            "부트로더 근거 자료는 index.html 한 개여야 한다",
        )
        for sid in SECTIONS:
            self.assertIn(f'<section id="{sid}" class="panel">', self.page)
            self.assertIn(f'<a href="#{sid}">', self.page)

    def test_main_page_links_to_each_section(self):
        for sid in SECTIONS:
            path = f"artifacts/bootloader/index.html#{sid}"
            pattern = rf'<a[^>]+href="{re.escape(path)}"'
            self.assertRegex(self.index, pattern)

    def test_no_dangling_internal_anchors(self):
        """페이지 안 #앵커가 전부 실재해야 한다 (통합 전 근거 보기 링크가 깨져 있었다)."""
        ids = set(re.findall(r'id="([^"]+)"', self.page))
        for anchor in set(re.findall(r'href="#([^"]+)"', self.page)):
            self.assertIn(anchor, ids, f"존재하지 않는 앵커: #{anchor}")

    def test_both_projects_publish_personal_project_metadata(self):
        self.assertEqual(self.index.count('class="project-meta"'), 2)
        for value in ["개인 프로젝트", "2026.03.03–2026.03.24", "2026.03.19–2026.03.23", "1명", "100%"]:
            self.assertIn(value, self.index)

    def test_memory_map_uses_exact_linker_addresses(self):
        for value in [
            "0x80000000–0x80025FFF", "0x80026000–0x80027FFF",
            "0x80100000–0x8017DFFF", "0x8017E000–0x8017FFDF",
            "0x8017FFE0–0x8017FFFF", "0x80180000–0x801FFFFF",
            "0xAF000000–0xAF01FFFF", "0xAF100000–0xAF103FFF",
            "0x80000020", "0x80027800",
        ]:
            self.assertIn(value, self.page)

    def test_uds_sequence_contains_services_and_restore_branch(self):
        for sid in ["0x10", "0x27", "0x31", "0x34", "0x36", "0x37", "0x11"]:
            self.assertIn(sid, self.page)
        for value in ["RID_EraseMemory", "RCOR_EraseMemory_App", "RID_CheckProgrammingDependencies",
                      "EA_AppToBackup()", "EA_AppRestore()", "SHA-256 불일치"]:
            self.assertIn(value, self.page)

    def test_test_report_uses_only_allowed_statuses(self):
        statuses = re.findall(r'data-status="([^"]+)"', self.page)
        self.assertGreaterEqual(len(statuses), 8)
        self.assertTrue(set(statuses) <= {"PASS", "FAIL", "Not executed", "Evidence unavailable"})
        self.assertIn("Evidence unavailable", statuses)
        self.assertIn("Not executed", statuses)

    def test_trace32_section_contains_actual_debug_values_and_code(self):
        for value in [
            # 실제 Trace32 Register view 캡처(trap-vector-breakpoint.png) 기준 값
            "PC = 0x80027840", "BTV = 0x80027800",
            "Break.Set 0x80027800++0xFF /Program /Onchip",
            "EA_AppToBackup()", "EA_AppRestore()", "FlsLoader_Write()",
            "static uint8 copyBuf[MEMORY_COPY_CHUNK_SIZE]", "uint32", "uint8*",
        ]:
            self.assertIn(value, self.page)

    def test_local_diagram_assets_exist(self):
        for path in ["assets/bootloader/memory-map.svg", "assets/bootloader/uds-sequence.svg"]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_artifacts_do_not_expose_expiring_or_private_urls(self):
        files = [ROOT / "index.html", *ARTIFACT_DIR.glob("*.html"), *Path(ROOT / "assets/bootloader").glob("*.svg")]
        text = chr(10).join(path.read_text(encoding="utf-8") for path in files if path.exists())
        for forbidden in ["prod-files-secure.s3", "X-Amz-", "notion.so", "app.notion.com", "Bootloader_Design_For_OTA"]:
            self.assertNotIn(forbidden, text)

    def test_page_is_accessible_and_returns_to_portfolio(self):
        self.assertIn('lang="ko"', self.page)
        self.assertIn('href="../../index.html#bootloader-project"', self.page)
        self.assertIn('href="../../assets/bootloader/shared.css"', self.page)
        self.assertIn('class="skip-link"', self.page)
        self.assertIn('id="main"', self.page)
        self.assertIn("<caption>", self.page)
        self.assertNotIn("<iframe", self.page)


if __name__ == "__main__":
    unittest.main()
