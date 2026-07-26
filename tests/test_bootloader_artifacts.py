from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "bootloader"

class BootloaderArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")

    def _page(self, name):
        return (ARTIFACT_DIR / name).read_text(encoding="utf-8")

    def test_four_artifact_pages_exist(self):
        for name in ["memory-map.html", "uds-sequence.html", "test-results.html", "trace32-restore.html"]:
            self.assertTrue((ARTIFACT_DIR / name).is_file(), name)

    def test_main_page_links_to_real_artifacts(self):
        for path in [
            "artifacts/bootloader/memory-map.html",
            "artifacts/bootloader/uds-sequence.html",
            "artifacts/bootloader/test-results.html",
            "artifacts/bootloader/trace32-restore.html",
        ]:
            pattern = rf'<a[^>]+href="{re.escape(path)}"[^>]+target="_blank"[^>]+rel="noreferrer"'
            self.assertRegex(self.index, pattern)

    def test_both_projects_publish_personal_project_metadata(self):
        self.assertEqual(self.index.count('class="project-meta"'), 2)
        for value in ["개인 프로젝트", "2026.03.03–2026.03.24", "2026.03.19–2026.03.23", "1명", "100%"]:
            self.assertIn(value, self.index)

    def test_memory_map_uses_exact_linker_addresses(self):
        page = self._page("memory-map.html")
        for value in [
            "0x80000000–0x80025FFF", "0x80026000–0x80027FFF",
            "0x80100000–0x8017DFFF", "0x8017E000–0x8017FFDF",
            "0x8017FFE0–0x8017FFFF", "0x80180000–0x801FFFFF",
            "0xAF000000–0xAF01FFFF", "0xAF100000–0xAF103FFF",
            "0x80000020", "0x80027800",
        ]:
            self.assertIn(value, page)

    def test_uds_sequence_contains_services_and_restore_branch(self):
        page = self._page("uds-sequence.html")
        for sid in ["0x10", "0x27", "0x31", "0x34", "0x36", "0x37", "0x11"]:
            self.assertIn(sid, page)
        for value in ["RID_EraseMemory", "RCOR_EraseMemory_App", "RID_CheckProgrammingDependencies", "EA_AppToBackup()", "EA_AppRestore()", "SHA-256 불일치"]:
            self.assertIn(value, page)

    def test_test_report_uses_only_allowed_statuses(self):
        page = self._page("test-results.html")
        statuses = re.findall(r'data-status="([^"]+)"', page)
        self.assertGreaterEqual(len(statuses), 8)
        self.assertTrue(set(statuses) <= {"PASS", "FAIL", "Not executed", "Evidence unavailable"})
        self.assertIn("Evidence unavailable", statuses)
        self.assertIn("Not executed", statuses)

    def test_trace32_page_contains_actual_debug_values_and_code(self):
        page = self._page("trace32-restore.html")
        for value in [
            "PC = 0x7000EC24", "BTV = 0x80027800",
            "Break.Set 0x80027800++0xFF /Program /Onchip",
            "EA_AppToBackup()", "EA_AppRestore()", "FlsLoader_Write()",
            "static uint8 copyBuf[MEMORY_COPY_CHUNK_SIZE]", "uint32", "uint8*",
        ]:
            self.assertIn(value, page)

    def test_local_diagram_assets_exist(self):
        for path in ["assets/bootloader/memory-map.svg", "assets/bootloader/uds-sequence.svg"]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_artifacts_do_not_expose_expiring_or_private_urls(self):
        files = [ROOT / "index.html", *ARTIFACT_DIR.glob("*.html"), *Path(ROOT / "assets/bootloader").glob("*.svg")]
        text = "\n".join(path.read_text(encoding="utf-8") for path in files if path.exists())
        for forbidden in ["prod-files-secure.s3", "X-Amz-", "notion.so", "app.notion.com", "Bootloader_Design_For_OTA"]:
            self.assertNotIn(forbidden, text)

    def test_artifact_pages_are_accessible_and_return_to_portfolio(self):
        for name in ["memory-map.html", "uds-sequence.html", "test-results.html", "trace32-restore.html"]:
            page = self._page(name)
            self.assertIn('lang="ko"', page)
            self.assertIn('href="../../index.html#bootloader-project"', page)
            self.assertIn('href="../../assets/bootloader/shared.css"', page)
            self.assertIn('class="skip-link"', page)
            self.assertIn('id="main"', page)
            self.assertIn("<caption>", page)
            self.assertNotIn("<iframe", page)

if __name__ == "__main__":
    unittest.main()
