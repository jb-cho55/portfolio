# Bootloader Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add four public, independently accessible Bootloader evidence pages and consistent personal-project metadata for the Bootloader and Black Box case studies.

**Architecture:** Keep the portfolio as a dependency-free static site. The main `index.html` remains the entry point, while four focused HTML documents under `artifacts/bootloader/` share one stylesheet and repository-hosted SVG/PNG evidence assets. Python `unittest` tests enforce links, metadata, exact technical facts, evidence status policy, accessibility, and the absence of expiring Notion URLs.

**Tech Stack:** HTML5, CSS3, accessible SVG, static PNG assets, Python 3 `unittest`, GitHub Pages.

## Global Constraints

- Bootloader period: `2026.03.03–2026.03.24`.
- Black Box Validation period: `2026.03.19–2026.03.23`.
- Both projects are personal projects with team size `1명` and contribution `100%`.
- Publish actual memory addresses, actual function names, selected code, and Trace32 PC/BTV/breakpoint addresses.
- Do not add customer, production ECU, account, authentication, or private repository identifiers.
- Do not reference Notion signed URLs such as `prod-files-secure.s3`, `X-Amz-`, or `notion.so` from public HTML/CSS/SVG files.
- A test case may be marked `PASS` only when a screenshot, log, memory comparison, or explicit execution record is available.
- Unsupported results must use `Not executed` or `Evidence unavailable`; never infer a passing result.
- Describe SHA-256 as binary integrity/change detection, not production-grade code signing, secure boot, or authenticity verification.
- Use no JavaScript framework, CSS framework, Mermaid runtime, or new package dependency.
- All artifact pages must remain readable without JavaScript and include a link back to `../../index.html#bootloader-project`.
- All public images require specific `alt` text and visible captions.
- External/new-tab links use `target="_blank" rel="noreferrer"`.
- Retain the current Pretendard, Navy/Blue visual language, `1080px` maximum width, responsive layout, keyboard focus visibility, and `prefers-reduced-motion` behavior.

---

## File Structure

### Create

- `artifacts/bootloader/memory-map.html` — exact linker-based PFlash/DFlash map and transfer directions.
- `artifacts/bootloader/uds-sequence.html` — normal programming and integrity-failure/restore sequence.
- `artifacts/bootloader/test-results.html` — evidence-qualified test-case/result matrix.
- `artifacts/bootloader/trace32-restore.html` — alignment-trap debugging and restore case study.
- `assets/bootloader/shared.css` — shared artifact-page layout, metadata, tables, code, evidence cards, responsive behavior.
- `assets/bootloader/memory-map.svg` — accessible visual map of Bootloader, Application, valid pattern, and backup regions.
- `assets/bootloader/uds-sequence.svg` — accessible sequence visual for UDS services and restore branch.
- `assets/bootloader/trace32/routine-control-stop.png` — ECU response stop observed during RoutineControl.
- `assets/bootloader/trace32/app-to-backup-breakpoint.png` — `EA_AppToBackup()` breakpoint investigation.
- `assets/bootloader/trace32/trap-vector-breakpoint.png` — BTV-range breakpoint and trap investigation.
- `assets/bootloader/restore/app-to-backup-result.png` — Primary-to-Backup write/read evidence.
- `assets/bootloader/restore/backup-to-app-result.png` — Backup-to-Primary restore evidence.
- `assets/bootloader/tests/sha256-mismatch.png` — changed-binary SHA-256 mismatch evidence.
- `assets/bootloader/tests/reprogramming-log.png` — programming or restore execution-log evidence.
- `tests/test_bootloader_artifacts.py` — artifact file, content, link, status, and security regression tests.

### Modify

- `index.html` — project metadata blocks, four real Bootloader artifact links, Black Box personal-project badge.
- `tests/test_portfolio.py` — replace the obsolete shared five-category artifact assertion and retain existing portfolio regressions.
- `README.md` — document the artifact structure, public technical evidence, and test command.

---

### Task 1: Lock the Public Evidence Contract with Failing Tests

**Files:**
- Create: `tests/test_bootloader_artifacts.py`
- Modify: `tests/test_portfolio.py:45-49`

**Interfaces:**
- Consumes: current static site files from repository root.
- Produces: regression contract for all later tasks; no production files are changed in this task.

- [ ] **Step 1: Replace the obsolete unified artifact-category test**

Replace `test_artifacts_are_unified_by_five_categories` in `tests/test_portfolio.py` with:

```python
    def test_project_artifact_sections_have_project_specific_evidence(self):
        self.assertEqual(self.html.count('class="artifact-section"'), 2)

        bootloader = self.html[
            self.html.index('id="bootloader-project"'):
            self.html.index('id="black-box-project"')
        ]
        for label in [
            "MEMORY MAP",
            "UDS SEQUENCE",
            "TEST RESULTS",
            "TRACE32 · RESTORE",
            "EVIDENCE",
        ]:
            self.assertIn(f"<strong>{label}</strong>", bootloader)

        black_box = self.html[self.html.index('id="black-box-project"'):]
        for label in ["CODE", "TEST", "DOCUMENT", "DEMO", "EVIDENCE"]:
            self.assertIn(f"<strong>{label}</strong>", black_box)
```

- [ ] **Step 2: Add the new artifact regression test module**

Create `tests/test_bootloader_artifacts.py` with:

```python
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "bootloader"


class BootloaderArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.pages = {
            name: (ARTIFACT_DIR / name).read_text(encoding="utf-8")
            for name in [
                "memory-map.html",
                "uds-sequence.html",
                "test-results.html",
                "trace32-restore.html",
            ]
        }

    def test_four_artifact_pages_exist(self):
        self.assertEqual(set(self.pages), {
            "memory-map.html",
            "uds-sequence.html",
            "test-results.html",
            "trace32-restore.html",
        })

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
        for value in [
            "개인 프로젝트",
            "2026.03.03–2026.03.24",
            "2026.03.19–2026.03.23",
            "1명",
            "100%",
        ]:
            self.assertIn(value, self.index)
        self.assertEqual(self.index.count('class="project-meta"'), 2)

    def test_memory_map_uses_exact_linker_addresses(self):
        page = self.pages["memory-map.html"]
        for value in [
            "0x80000000–0x80025FFF",
            "0x80026000–0x80027FFF",
            "0x80100000–0x8017DFFF",
            "0x8017E000–0x8017FFDF",
            "0x8017FFE0–0x8017FFFF",
            "0x80180000–0x801FFFFF",
            "0xAF000000–0xAF01FFFF",
            "0xAF100000–0xAF103FFF",
            "0x80000020",
            "0x80027800",
        ]:
            self.assertIn(value, page)

    def test_uds_sequence_contains_seven_services_and_restore_branch(self):
        page = self.pages["uds-sequence.html"]
        for sid in ["0x10", "0x27", "0x31", "0x34", "0x36", "0x37", "0x11"]:
            self.assertIn(sid, page)
        for value in [
            "RID_EraseMemory",
            "RCOR_EraseMemory_App",
            "RID_CheckProgrammingDependencies",
            "EA_AppToBackup()",
            "EA_AppRestore()",
            "SHA-256 불일치",
        ]:
            self.assertIn(value, page)

    def test_test_report_uses_only_allowed_statuses(self):
        page = self.pages["test-results.html"]
        statuses = re.findall(r'data-status="([^"]+)"', page)
        self.assertGreaterEqual(len(statuses), 8)
        self.assertTrue(set(statuses) <= {
            "PASS", "FAIL", "Not executed", "Evidence unavailable"
        })
        self.assertIn("Evidence unavailable", statuses)
        self.assertIn("Not executed", statuses)

    def test_trace32_page_contains_actual_debug_values_and_code(self):
        page = self.pages["trace32-restore.html"]
        for value in [
            "PC = 0x7000EC24",
            "BTV = 0x80027800",
            "Break.Set 0x80027800++0xFF /Program /Onchip",
            "EA_AppToBackup()",
            "EA_AppRestore()",
            "FlsLoader_Write()",
            "static uint8 copyBuf[MEMORY_COPY_CHUNK_SIZE]",
            "uint32",
            "uint8*",
        ]:
            self.assertIn(value, page)

    def test_local_evidence_assets_exist(self):
        paths = [
            "assets/bootloader/memory-map.svg",
            "assets/bootloader/uds-sequence.svg",
            "assets/bootloader/trace32/routine-control-stop.png",
            "assets/bootloader/trace32/app-to-backup-breakpoint.png",
            "assets/bootloader/trace32/trap-vector-breakpoint.png",
            "assets/bootloader/restore/app-to-backup-result.png",
            "assets/bootloader/restore/backup-to-app-result.png",
            "assets/bootloader/tests/sha256-mismatch.png",
            "assets/bootloader/tests/reprogramming-log.png",
        ]
        for path in paths:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_artifacts_do_not_expose_expiring_or_private_urls(self):
        public_text = self.index + "\n" + "\n".join(self.pages.values())
        for forbidden in [
            "prod-files-secure.s3",
            "X-Amz-",
            "notion.so",
            "app.notion.com",
            "Bootloader_Design_For_OTA",
        ]:
            self.assertNotIn(forbidden, public_text)

    def test_artifact_pages_are_accessible_and_return_to_portfolio(self):
        for page in self.pages.values():
            self.assertIn('lang="ko"', page)
            self.assertIn('href="../../index.html#bootloader-project"', page)
            self.assertIn('href="../../assets/bootloader/shared.css"', page)
            self.assertIn('class="skip-link"', page)
            self.assertIn('id="main"', page)
            self.assertIn("<caption>", page)
            self.assertNotIn("<iframe", page)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the new tests to verify the expected red state**

Run:

```bash
python -m unittest tests.test_bootloader_artifacts tests.test_portfolio -v
```

Expected: `test_bootloader_artifacts` fails because the four pages/assets and metadata blocks do not exist; existing unrelated portfolio tests continue to execute.

- [ ] **Step 4: Commit the failing contract tests**

```bash
git add tests/test_bootloader_artifacts.py tests/test_portfolio.py
git commit -m "test: define bootloader evidence contract"
```

---

### Task 2: Add Consistent Project Metadata and Real Artifact Links

**Files:**
- Modify: `index.html:295-371, 900px media rules, bootloader project, black-box project`
- Test: `tests/test_bootloader_artifacts.py`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: artifact paths fixed by Task 1.
- Produces: `.project-meta` component and public entry links used by all four artifact pages.

- [ ] **Step 1: Add metadata component styling**

Add after `.project-intro p`:

```css
.project-meta {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 1px;
  margin: 0;
  padding: 0 30px;
  background: var(--line);
  border-bottom: 1px solid var(--line);
}

.project-meta > div {
  min-width: 0;
  padding: 15px 14px;
  background: #fff;
}

.project-meta dt {
  color: var(--muted);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .04em;
}

.project-meta dd {
  margin: 3px 0 0;
  color: var(--navy);
  font-size: 13px;
  font-weight: 750;
  line-height: 1.45;
}
```

Add responsive rules:

```css
@media(max-width:900px) {
  .project-meta { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media(max-width:600px) {
  .project-meta {
    grid-template-columns: 1fr;
    padding-left: 21px;
    padding-right: 21px;
  }
}
```

- [ ] **Step 2: Insert Bootloader metadata immediately after `.project-intro`**

```html
<dl class="project-meta" aria-label="OTA Bootloader 프로젝트 메타데이터">
  <div><dt>유형</dt><dd>개인 프로젝트</dd></div>
  <div><dt>수행 기간</dt><dd>2026.03.03–2026.03.24</dd></div>
  <div><dt>팀 규모</dt><dd>1명</dd></div>
  <div><dt>기여도</dt><dd>100%</dd></div>
  <div><dt>역할</dt><dd>설계·구현·디버깅·검증 전담</dd></div>
</dl>
```

- [ ] **Step 3: Insert Black Box metadata and make its badge explicitly personal**

Set the badge to:

```html
<span class="project-badge">개인 프로젝트 · 검증 중심</span>
```

Insert after its `.project-intro`:

```html
<dl class="project-meta" aria-label="Black Box Validation 프로젝트 메타데이터">
  <div><dt>유형</dt><dd>개인 프로젝트</dd></div>
  <div><dt>수행 기간</dt><dd>2026.03.19–2026.03.23</dd></div>
  <div><dt>팀 규모</dt><dd>1명</dd></div>
  <div><dt>기여도</dt><dd>100%</dd></div>
  <div><dt>역할</dt><dd>요구분석·설계·자동화·결함 분석 전담</dd></div>
</dl>
```

- [ ] **Step 4: Replace the four internal Bootloader artifact links**

Use exactly:

```html
<a class="artifact-item" href="artifacts/bootloader/memory-map.html" target="_blank" rel="noreferrer">
  <strong>MEMORY MAP</strong>
  <span>실제 주소 기반 PFlash·Backup·Valid Pattern 구조</span>
</a>
<a class="artifact-item" href="artifacts/bootloader/uds-sequence.html" target="_blank" rel="noreferrer">
  <strong>UDS SEQUENCE</strong>
  <span>정상 리프로그래밍과 무결성 실패·Restore 흐름</span>
</a>
<a class="artifact-item" href="artifacts/bootloader/test-results.html" target="_blank" rel="noreferrer">
  <strong>TEST RESULTS</strong>
  <span>테스트 케이스·실제 결과·근거 연결표</span>
</a>
<a class="artifact-item" href="artifacts/bootloader/trace32-restore.html" target="_blank" rel="noreferrer">
  <strong>TRACE32 · RESTORE</strong>
  <span>Alignment Trap 분석과 양방향 복구 재검증</span>
</a>
```

Retain the current IVS completion `EVIDENCE` item as the fifth card.

- [ ] **Step 5: Run focused tests**

```bash
python -m unittest \
  tests.test_bootloader_artifacts.BootloaderArtifactTests.test_main_page_links_to_real_artifacts \
  tests.test_bootloader_artifacts.BootloaderArtifactTests.test_both_projects_publish_personal_project_metadata \
  tests.test_portfolio.PortfolioContentTests.test_project_artifact_sections_have_project_specific_evidence \
  -v
```

Expected: metadata and main-link tests pass; artifact file tests still fail.

- [ ] **Step 6: Commit the main-page integration**

```bash
git add index.html
git commit -m "feat: add project metadata and evidence links"
```

---

### Task 3: Build the Shared Artifact Shell and Exact Memory Map

**Files:**
- Create: `assets/bootloader/shared.css`
- Create: `assets/bootloader/memory-map.svg`
- Create: `artifacts/bootloader/memory-map.html`
- Test: `tests/test_bootloader_artifacts.py`

**Interfaces:**
- Produces: shared `.artifact-page`, `.artifact-header`, `.meta-grid`, `.table-wrap`, `.evidence-grid`, `.status`, and code styles reused in Tasks 4–6.

- [ ] **Step 1: Create the shared stylesheet**

Implement these required selectors with the existing Navy/Blue variables:

```css
:root {
  --navy: #0b1f3a;
  --navy-deep: #071426;
  --blue: #216fe6;
  --blue-soft: #edf4ff;
  --ink: #172033;
  --muted: #5f6c7e;
  --line: #dbe2ea;
  --surface: #ffffff;
  --surface-soft: #f6f8fa;
  --max: 1080px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--surface-soft);
  font-family: "Pretendard", "Noto Sans KR", "Malgun Gothic", sans-serif;
  line-height: 1.7;
  word-break: keep-all;
}
a { color: inherit; }
img { max-width: 100%; }
.skip-link { position: absolute; left: -9999px; }
.skip-link:focus { left: 16px; top: 16px; z-index: 100; background: #fff; padding: 10px 14px; }
.artifact-page { width: min(var(--max), calc(100% - 40px)); margin: 0 auto; padding: 38px 0 72px; }
.artifact-header, .panel { background: #fff; border: 1px solid var(--line); border-radius: 12px; }
.artifact-header { padding: 28px; border-top: 5px solid var(--navy); }
.back-link { color: var(--blue); font-weight: 800; }
.eyebrow { color: var(--blue); font-size: 12px; font-weight: 800; letter-spacing: .08em; }
h1, h2, h3 { color: var(--navy); line-height: 1.3; }
.meta-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 1px; margin-top: 22px; background: var(--line); }
.meta-grid div { padding: 13px; background: #fff; }
.meta-grid dt { color: var(--muted); font-size: 11px; font-weight: 800; }
.meta-grid dd { margin: 3px 0 0; color: var(--navy); font-size: 13px; font-weight: 750; }
.panel { margin-top: 20px; padding: 24px; }
.figure { margin: 0; }
.figure img { display: block; width: 100%; border: 1px solid var(--line); border-radius: 10px; background: #fff; }
.figure figcaption { margin-top: 9px; color: var(--muted); font-size: 13px; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; min-width: 760px; }
caption { margin-bottom: 10px; color: var(--navy); font-weight: 800; text-align: left; }
th, td { padding: 12px; border: 1px solid var(--line); vertical-align: top; text-align: left; }
th { background: var(--blue-soft); color: var(--navy); }
pre { overflow-x: auto; padding: 16px; border-radius: 9px; background: var(--navy-deep); color: #e8f1fb; }
code { font-family: Consolas, "Courier New", monospace; }
.evidence-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.evidence-card { margin: 0; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; background: #fff; }
.evidence-card img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: contain; background: #eef2f7; }
.evidence-card figcaption { padding: 11px 13px; color: var(--muted); font-size: 13px; }
.status { display: inline-block; border-radius: 999px; padding: 3px 8px; font-size: 12px; font-weight: 800; }
.status-pass { color: #13653a; background: #eaf7ef; }
.status-neutral { color: #5a4a16; background: #fff6d8; }
:focus-visible { outline: 3px solid rgba(33, 111, 230, .35); outline-offset: 3px; }
@media(max-width:900px) { .meta-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media(max-width:600px) {
  .artifact-page { width: min(var(--max), calc(100% - 28px)); padding-top: 22px; }
  .artifact-header, .panel { padding: 19px; }
  .meta-grid, .evidence-grid { grid-template-columns: 1fr; }
}
@media(prefers-reduced-motion:reduce) { html { scroll-behavior: auto; } }
```

- [ ] **Step 2: Create an accessible Memory Map SVG**

The SVG must use `role="img"`, `aria-labelledby="memory-map-title memory-map-desc"`, and contain these exact labeled ranges:

```text
Bootloader User       0x80000000–0x80025FFF  152 KiB
INTTAB + TRAP          0x80026000–0x80027FFF    8 KiB
Application Primary   0x80100000–0x8017DFFF  504 KiB
Application INTTAB     0x8017E000–0x8017FFDF  8 KiB - 32 B
Valid Pattern          0x8017FFE0–0x8017FFFF   32 B
Application Backup    0x80180000–0x801FFFFF  512 KiB
DFlash Bank 0          0xAF000000–0xAF01FFFF  128 KiB
DFlash Bank 1          0xAF100000–0xAF103FFF   16 KiB
```

Show arrows labeled `EA_AppToBackup()` from Primary to Backup and `EA_AppRestore()` from Backup to Primary. Mark `RESET 0x80000020`, `INTTAB 0x80026000`, and `BTV 0x80027800`.

- [ ] **Step 3: Create `memory-map.html`**

Use the shared shell and include:

```html
<a class="skip-link" href="#main">본문 바로가기</a>
<main id="main" class="artifact-page">
  <header class="artifact-header">
    <a class="back-link" href="../../index.html#bootloader-project">← 포트폴리오로 돌아가기</a>
    <p class="eyebrow">BOOTLOADER EVIDENCE 01</p>
    <h1>Actual Memory Map</h1>
    <p>Bootloader 링크스크립트에 정의된 AURIX TC234LP의 PFlash·DFlash 구획과 Backup·Restore 데이터 이동을 실제 주소로 정리했습니다.</p>
    <!-- five-cell meta-grid -->
  </header>
</main>
```

Add the SVG figure and a semantic table with columns:

```text
영역 | 주소 범위 | 크기 | 목적 | 관련 함수·심볼 | 변경 시점
```

The table must explain that the Application and Backup areas are `reserved rom` in the Bootloader linker configuration, `pflash_app_valid` is a 32-byte completion/validity marker, and `SHA-256` is used for binary integrity detection rather than authenticity.

Add a source-code excerpt containing:

```c
#define INTTAB     0x80026000
#define RESET      0x80000020
#define IFXTRAPTAB (INTTAB + 0x1800)
```

- [ ] **Step 4: Run the Memory Map tests**

```bash
python -m unittest \
  tests.test_bootloader_artifacts.BootloaderArtifactTests.test_memory_map_uses_exact_linker_addresses \
  tests.test_bootloader_artifacts.BootloaderArtifactTests.test_artifact_pages_are_accessible_and_return_to_portfolio \
  -v
```

Expected: Memory Map assertions pass; tests for the other three missing pages still fail.

- [ ] **Step 5: Commit the shared shell and Memory Map**

```bash
git add assets/bootloader/shared.css assets/bootloader/memory-map.svg artifacts/bootloader/memory-map.html
git commit -m "feat: publish bootloader memory map"
```

---

### Task 4: Publish the UDS Programming and Restore Sequence

**Files:**
- Create: `assets/bootloader/uds-sequence.svg`
- Create: `artifacts/bootloader/uds-sequence.html`
- Test: `tests/test_bootloader_artifacts.py`

**Interfaces:**
- Consumes: `assets/bootloader/shared.css` and exact memory/function terminology from Task 3.
- Produces: a stable sequence page linked from the main portfolio and test report.

- [ ] **Step 1: Create the sequence SVG**

Use six lanes:

```text
Tester | BswCom | BswDcm | EcuAbsFls | FlsLoader | PFlash
```

Draw the normal flow in this exact order:

```text
0x10 DiagnosticSessionControl
0x27 SecurityAccess
0x31 RoutineControl: EA_AppToBackup()
0x31 RID_EraseMemory / RCOR_EraseMemory_App
0x34 RequestDownload
0x36 TransferData (Block Sequence validation)
0x37 RequestTransferExit
0x31 RID_CheckProgrammingDependencies
SHA-256 binary integrity comparison
0x11 ECUReset
```

Draw a separate failure branch:

```text
SHA-256 mismatch
→ do not mark Application valid
→ EA_AppRestore()
→ Backup to Application Primary
→ read-back / hash revalidation
→ 0x11 ECUReset only after recovery policy completes
```

Do not label this flow `Secure Boot`, `Code Signing`, or `Authenticity`.

- [ ] **Step 2: Create `uds-sequence.html`**

Include:

- The SVG with concrete alt text.
- A numbered semantic list matching the sequence.
- A RoutineControl request example:

```text
31 01 00 02 F0 01
SID | StartRoutine | RID_EraseMemory | RCOR_EraseMemory_App
```

- The actual RTE call chain:

```text
BswDcm
→ Rte_Call_BswDcm_rEcuAbsFls_erasePflashBlock()
→ REoiEcuAbs_pEcuAbsFls_erasePflashBlock()
→ EA_erasePflashBlock()
```

- A note that `RID_CheckProgrammingDependencies` was present in the training implementation, while the public page only claims checks demonstrated by the available record.

- [ ] **Step 3: Run the sequence test**

```bash
python -m unittest \
  tests.test_bootloader_artifacts.BootloaderArtifactTests.test_uds_sequence_contains_seven_services_and_restore_branch \
  -v
```

Expected: PASS.

- [ ] **Step 4: Commit the UDS sequence**

```bash
git add assets/bootloader/uds-sequence.svg artifacts/bootloader/uds-sequence.html
git commit -m "feat: publish bootloader uds sequence"
```

---

### Task 5: Publish Evidence-Qualified Test Cases and Results

**Files:**
- Create: `assets/bootloader/tests/sha256-mismatch.png`
- Create: `assets/bootloader/tests/reprogramming-log.png`
- Create: `artifacts/bootloader/test-results.html`
- Test: `tests/test_bootloader_artifacts.py`

**Interfaces:**
- Consumes: local evidence images, `memory-map.html`, `uds-sequence.html`, and status vocabulary from Task 1.
- Produces: stable anchors `tc-normal-download`, `tc-block-sequence`, `tc-transfer-length`, `tc-interruption`, `tc-sha-mismatch`, `tc-backup`, `tc-restore`, `tc-alignment` for cross-page evidence links.

- [ ] **Step 1: Export and normalize two Notion evidence images**

From the connected Notion Bootloader pages, download the current signed images only as source material and save stable repository copies:

```text
Project 02 · Secure Flash 1.0
→ assets/bootloader/tests/sha256-mismatch.png

Project 07 · Reprogramming Log Analysis
→ assets/bootloader/tests/reprogramming-log.png
```

Requirements:

- Preserve the actual Trace32/log content.
- Crop only empty window chrome when useful; do not alter result values.
- Do not retain query strings, signed URLs, EXIF location, account names, or workspace URLs.
- Use descriptive captions in HTML rather than drawing explanatory text into the screenshots.

- [ ] **Step 2: Create the test report with explicit result policy**

Add a table with columns:

```text
ID | 검증 목적 | 사전 조건 | 입력·절차 | 기대 결과 | 실제 결과 | 판정 | 증거
```

Use these rows and initial public statuses:

```text
BL-TC-01 정상 리프로그래밍                  PASS when reprogramming log is visible
BL-TC-02 Block Sequence 불일치              Evidence unavailable unless an execution log is located
BL-TC-03 TransferData 길이 초과             Not executed unless an execution record is located
BL-TC-04 전송 중단과 Valid Pattern          PASS only when the interruption/pattern record is visible
BL-TC-05 변경 Binary SHA-256 불일치         PASS with sha256-mismatch.png
BL-TC-06 Application Primary→Backup         PASS with app-to-backup evidence
BL-TC-07 무결성 실패 후 Backup Restore      PASS with backup-to-app evidence
BL-TC-08 Restore 후 실행 가능 상태 확인     Evidence unavailable unless reset/execute evidence is located
BL-TC-09 비정렬 버퍼 오류 재현              PASS with Trace32 stop/trap evidence
BL-TC-10 4바이트 정렬 수정 후 회귀 시험     PASS with bidirectional write/read evidence
```

Each `<tr>` must include `data-status="..."`. Use the exact status values from Task 1. For `Evidence unavailable` and `Not executed`, state what additional artifact would be required; do not soften the status.

- [ ] **Step 3: Link evidence cells to stable local assets or exact artifact anchors**

Examples:

```html
<a href="../../assets/bootloader/tests/sha256-mismatch.png" target="_blank" rel="noreferrer">SHA-256 mismatch 화면</a>
<a href="trace32-restore.html#alignment-root-cause">Alignment 원인 분석</a>
<a href="trace32-restore.html#restore-results">Restore 결과</a>
```

- [ ] **Step 4: Add an evidence gallery below the table**

Use two `.evidence-card` figures with specific `alt` values and visible captions. Include a short statement that source images are local static copies and the Notion signed URLs are not published.

- [ ] **Step 5: Run the status and asset tests**

```bash
python -m unittest \
  tests.test_bootloader_artifacts.BootloaderArtifactTests.test_test_report_uses_only_allowed_statuses \
  tests.test_bootloader_artifacts.BootloaderArtifactTests.test_artifacts_do_not_expose_expiring_or_private_urls \
  -v
```

Expected: PASS for the test-report assertions; local-asset existence remains red until Task 6 supplies all remaining images.

- [ ] **Step 6: Commit the test report**

```bash
git add assets/bootloader/tests artifacts/bootloader/test-results.html
git commit -m "feat: publish bootloader test evidence"
```

---

### Task 6: Publish Trace32 Alignment Debugging and Restore Evidence

**Files:**
- Create: `assets/bootloader/trace32/routine-control-stop.png`
- Create: `assets/bootloader/trace32/app-to-backup-breakpoint.png`
- Create: `assets/bootloader/trace32/trap-vector-breakpoint.png`
- Create: `assets/bootloader/restore/app-to-backup-result.png`
- Create: `assets/bootloader/restore/backup-to-app-result.png`
- Create: `artifacts/bootloader/trace32-restore.html`
- Test: `tests/test_bootloader_artifacts.py`

**Interfaces:**
- Consumes: local evidence conventions and shared stylesheet.
- Produces: anchors `symptom`, `breakpoint-analysis`, `alignment-root-cause`, `alignment-fix`, and `restore-results` used by the test report.

- [ ] **Step 1: Export five stable evidence images from Notion**

Use these source selections:

```text
참고 · Aligned Memory Access Error
- initial RoutineControl/CAN response stop → routine-control-stop.png
- Break.Set EA_AppToBackup investigation → app-to-backup-breakpoint.png
- BTV-range breakpoint investigation → trap-vector-breakpoint.png

프로젝트 01 · Logical Memory Redundancy and restore records
- Application Primary to Backup result → app-to-backup-result.png
- Backup to Application Primary result → backup-to-app-result.png
```

Apply the same integrity/privacy rules as Task 5. Confirm the saved files open as PNG before committing.

- [ ] **Step 2: Build the debugging narrative in `trace32-restore.html`**

Use sections in this order:

```text
1. 증상
2. 가설과 함수 Breakpoint
3. PC/BTV 관찰
4. Trap Vector 범위 Breakpoint
5. 정렬 조건 원인
6. 코드 수정
7. Application→Backup→Application 재검증
```

Include these exact values:

```text
PC = 0x7000EC24
BTV = 0x80027800
Break.Set EA_AppToBackup
Break.Set 0x80027800++0xFF /Program /Onchip
```

Include the original code excerpt:

```c
static uint8 copyBuf[MEMORY_COPY_CHUNK_SIZE];

memcpy(copyBuf,
       (const void *)(MEMORY_ADDRESS_APPLICATION + offset),
       copySize);

*errorResult = (uint8)FlsLoader_Write(
    MEMORY_ADDRESS_BACKUP + offset,
    copySize,
    copyBuf);
```

Explain the fix with code that makes the alignment intent explicit:

```c
static uint32 copyBufAligned[
    MEMORY_COPY_CHUNK_SIZE / sizeof(uint32)
];
uint8 *copyBuf = (uint8 *)copyBufAligned;
```

State that the `uint32` backing storage provides 4-byte alignment while the `uint8*` view preserves byte-wise copying. Do not claim that changing the pointer type alone creates alignment.

- [ ] **Step 3: Show both actual restore directions**

Under `id="restore-results"`, provide two evidence cards and a verification table:

```text
Application Primary → Backup
- erase Secondary
- chunked memcpy to aligned RAM buffer
- FlsLoader_Write to MEMORY_ADDRESS_BACKUP + offset
- read-back comparison

Backup → Application Primary
- erase Primary
- chunked copy from MEMORY_ADDRESS_BACKUP
- FlsLoader_Write to MEMORY_ADDRESS_APPLICATION + offset
- read-back and SHA-256 revalidation
```

- [ ] **Step 4: Run Trace32 and local-asset tests**

```bash
python -m unittest \
  tests.test_bootloader_artifacts.BootloaderArtifactTests.test_trace32_page_contains_actual_debug_values_and_code \
  tests.test_bootloader_artifacts.BootloaderArtifactTests.test_local_evidence_assets_exist \
  -v
```

Expected: PASS.

- [ ] **Step 5: Commit the debugging case study**

```bash
git add assets/bootloader/trace32 assets/bootloader/restore artifacts/bootloader/trace32-restore.html
git commit -m "feat: publish trace32 restore evidence"
```

---

### Task 7: Update Documentation and Run Full Verification

**Files:**
- Modify: `README.md`
- Modify only if verification exposes a defect: `index.html`, `artifacts/bootloader/*.html`, `assets/bootloader/shared.css`, `tests/*.py`

**Interfaces:**
- Consumes: all prior tasks.
- Produces: documented repository layout and verified Draft PR-ready branch.

- [ ] **Step 1: Update README title and evidence description**

Change the title to:

```markdown
# Vehicle Embedded SW Portfolio
```

Add under major contents:

```markdown
- **Bootloader 공개 기술 산출물**  
  실제 주소 기반 Memory Map, UDS Sequence Diagram, 증거 수준을 구분한 Test Results, Trace32 Alignment Trap·Restore 분석
```

Update the repository tree to:

```text
.
├── index.html
├── artifacts/bootloader/          # Bootloader 독립 기술 산출물 4개
├── assets/bootloader/             # Memory Map, UDS Diagram, Trace32·Restore·Test 증거
├── assets/images/black-box/       # Black Box Testing 실제 화면
├── assets/evidence/               # 개인정보 마스킹 자격·수상 PDF와 썸네일
├── tests/test_portfolio.py
└── tests/test_bootloader_artifacts.py
```

Update the public-scope paragraph to state that selected educational-project addresses, function names, code excerpts, and debugging screens are public, while private repositories and expiring Notion URLs remain unpublished.

- [ ] **Step 2: Run the complete unit-test suite**

```bash
python -m unittest discover -s tests -v
```

Expected: all tests pass with zero failures and zero errors.

- [ ] **Step 3: Scan public files for forbidden URLs and overclaims**

Run:

```bash
python - <<'PY'
from pathlib import Path

files = [Path("index.html"), *Path("artifacts/bootloader").glob("*.html"),
         *Path("assets/bootloader").glob("*.css"),
         *Path("assets/bootloader").glob("*.svg")]
text = "\n".join(path.read_text(encoding="utf-8") for path in files)

forbidden = [
    "prod-files-secure.s3",
    "X-Amz-",
    "notion.so",
    "app.notion.com",
    "Bootloader_Design_For_OTA",
    "production-grade secure boot",
    "코드 서명 구현",
]

found = [term for term in forbidden if term in text]
if found:
    raise SystemExit(f"Forbidden public content: {found}")
print(f"Scanned {len(files)} public text files: OK")
PY
```

Expected: `Scanned <N> public text files: OK`.

- [ ] **Step 4: Verify every local reference resolves**

Run:

```bash
python - <<'PY'
from html.parser import HTMLParser
from pathlib import Path

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "a" and data.get("href"):
            self.refs.append(data["href"])
        if tag in {"img", "script"} and data.get("src"):
            self.refs.append(data["src"])
        if tag == "link" and data.get("href"):
            self.refs.append(data["href"])

html_files = [Path("index.html"), *Path("artifacts/bootloader").glob("*.html")]
missing = []
for html_file in html_files:
    parser = Links()
    parser.feed(html_file.read_text(encoding="utf-8"))
    for ref in parser.refs:
        if ref.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = (html_file.parent / ref.split("#", 1)[0]).resolve()
        if not target.exists():
            missing.append((str(html_file), ref))
if missing:
    raise SystemExit(f"Missing local references: {missing}")
print(f"Checked local references in {len(html_files)} HTML files: OK")
PY
```

Expected: `Checked local references in 5 HTML files: OK`.

- [ ] **Step 5: Perform a browser smoke test**

Run:

```bash
python -m http.server 8000
```

Check:

```text
http://localhost:8000/
http://localhost:8000/artifacts/bootloader/memory-map.html
http://localhost:8000/artifacts/bootloader/uds-sequence.html
http://localhost:8000/artifacts/bootloader/test-results.html
http://localhost:8000/artifacts/bootloader/trace32-restore.html
```

Verify desktop and narrow/mobile widths, keyboard focus, image loading, horizontal table scrolling, back links, and new-tab artifact links.

- [ ] **Step 6: Commit documentation and any verified corrections**

```bash
git add README.md index.html artifacts assets/bootloader tests
git commit -m "docs: document bootloader evidence artifacts"
```

- [ ] **Step 7: Compare the branch to `main` and open a Draft PR**

The Draft PR body must list:

```markdown
## What changed
- Added four public Bootloader evidence pages.
- Added actual linker addresses, UDS sequence, evidence-qualified test results, and Trace32/Restore records.
- Added consistent personal-project metadata for both featured projects.

## Evidence policy
- PASS is used only with public execution evidence.
- Missing evidence is explicitly marked Not executed or Evidence unavailable.
- Expiring Notion URLs and private repository identifiers are not published.

## Validation
- `python -m unittest discover -s tests -v`
- forbidden-public-content scan
- local-reference scan
- browser smoke test
```

Open as Draft against `main` from `agent/bootloader-evidence`.

---

## Self-Review Record

### Spec coverage

- Four independently clickable Bootloader artifacts: Tasks 2–6.
- Actual memory addresses and function names: Tasks 3, 4, and 6.
- UDS normal/failure/restore sequence: Task 4.
- Test case/result table with evidence policy: Task 5.
- Trace32 and Restore evidence: Task 6.
- Personal-project metadata for both projects: Task 2.
- Responsive design, keyboard access, alt text, captions, reduced motion: Tasks 2–6.
- Stable repository assets without signed Notion URLs: Tasks 5–7.
- README and complete verification: Task 7.

### Placeholder scan

The plan contains no `TBD`, `TODO`, `implement later`, generic error-handling instruction, or undefined “similar to” step. Every production task identifies exact files, required text, tests, commands, and commit boundaries.

### Interface consistency

- Main-page hrefs exactly match the four files created in Tasks 3–6.
- All artifact pages use `../../assets/bootloader/shared.css` and return to `../../index.html#bootloader-project`.
- Test-report evidence links target local assets or anchors created by Tasks 4 and 6.
- Status values exactly match the allowed set enforced by Task 1.
- Technical addresses match the linker ranges and Trace32 values fixed in the approved design.
