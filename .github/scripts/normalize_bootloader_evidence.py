from pathlib import Path
import re
import subprocess


def from_main(path: str) -> str:
    return subprocess.check_output(["git", "show", f"origin/main:{path}"], text=True)


def first(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"{label}: marker not found")
    return text.replace(old, new, 1)


index = from_main("index.html")
metadata_css = '''
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
'''
index = first(index, "    .project-summary {", metadata_css + "\n    .project-summary {", "metadata css")
responsive_css = '''
    @media (max-width: 900px) {
      .project-meta { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (max-width: 600px) {
      .project-meta {
        grid-template-columns: 1fr;
        padding-left: 21px;
        padding-right: 21px;
      }
    }
'''
index = first(index, "  </style>", responsive_css + "\n  </style>", "responsive css")

boot_marker = '<dl class="project-summary" aria-label="OTA Bootloader 5줄 요약">'
boot_meta = '''<dl class="project-meta" aria-label="OTA Bootloader 프로젝트 메타데이터">
            <div><dt>유형</dt><dd>개인 프로젝트</dd></div>
            <div><dt>수행 기간</dt><dd>2026.03.03–2026.03.24</dd></div>
            <div><dt>팀 규모</dt><dd>1명</dd></div>
            <div><dt>기여도</dt><dd>100%</dd></div>
            <div><dt>담당 범위</dt><dd>설계·구현·디버깅·검증 전담</dd></div>
          </dl>

          '''
index = first(index, boot_marker, boot_meta + boot_marker, "bootloader metadata")

black_marker = '<dl class="project-summary" aria-label="Black Box Validation 5줄 요약">'
black_meta = '''<dl class="project-meta" aria-label="Black Box Validation 프로젝트 메타데이터">
            <div><dt>유형</dt><dd>개인 프로젝트</dd></div>
            <div><dt>수행 기간</dt><dd>2026.03.19–2026.03.23</dd></div>
            <div><dt>팀 규모</dt><dd>1명</dd></div>
            <div><dt>기여도</dt><dd>100%</dd></div>
            <div><dt>담당 범위</dt><dd>요구분석·설계·자동화·결함 분석 전담</dd></div>
          </dl>

          '''
index = first(index, black_marker, black_meta + black_marker, "black box metadata")
index = first(index, '<span class="project-badge">프로젝트 우수상 · 검증 중심</span>', '<span class="project-badge">개인 프로젝트 · 검증 중심</span>', "black box badge")

prefix, projects = index.split('id="bootloader-project"', 1)
boot, suffix = projects.split('id="black-box-project"', 1)
changes = [
    ('href="#bootloader-implementation"', 'href="artifacts/bootloader/memory-map.html" target="_blank" rel="noreferrer"'),
    ('<strong>CODE</strong>', '<strong>MEMORY MAP</strong>'),
    ('UDS·Flash·Backup·Restore 핵심 구현 범위', '실제 주소 기반 PFlash·Backup·Valid Pattern 구조'),
    ('href="#bootloader-validation"', 'href="artifacts/bootloader/uds-sequence.html" target="_blank" rel="noreferrer"'),
    ('<strong>TEST</strong>', '<strong>UDS SEQUENCE</strong>'),
    ('정상·실패·복구 검증 시나리오', '정상 리프로그래밍과 무결성 실패·Restore 흐름'),
    ('href="#bootloader-flow"', 'href="artifacts/bootloader/test-results.html" target="_blank" rel="noreferrer"'),
    ('<strong>DOCUMENT</strong>', '<strong>TEST RESULTS</strong>'),
    ('시스템 구조와 리프로그래밍 절차', '테스트 케이스·실제 결과·근거 연결표'),
    ('href="#bootloader-debug"', 'href="artifacts/bootloader/trace32-restore.html" target="_blank" rel="noreferrer"'),
    ('<strong>DEMO</strong>', '<strong>TRACE32 · RESTORE</strong>'),
    ('Trace32 기반 Trap 분석 과정', 'Alignment Trap 분석과 양방향 복구 재검증'),
]
for old, new in changes:
    boot = first(boot, old, new, old)
index = prefix + 'id="bootloader-project"' + boot + 'id="black-box-project"' + suffix
Path("index.html").write_text(index, encoding="utf-8")

tests = from_main("tests/test_portfolio.py")
pattern = re.compile(r'    def test_artifacts_are_unified_by_five_categories\(self\):\n.*?(?=    def )', re.S)
replacement = '''    def test_project_artifact_sections_have_project_specific_evidence(self):
        self.assertEqual(self.html.count('class="artifact-section"'), 2)
        bootloader = self.html[self.html.index('id="bootloader-project"'):self.html.index('id="black-box-project"')]
        for label in ["MEMORY MAP", "UDS SEQUENCE", "TEST RESULTS", "TRACE32 · RESTORE", "EVIDENCE"]:
            self.assertIn(f"<strong>{label}</strong>", bootloader)
        black_box = self.html[self.html.index('id="black-box-project"'):]
        for label in ["CODE", "TEST", "DOCUMENT", "DEMO", "EVIDENCE"]:
            self.assertIn(f"<strong>{label}</strong>", black_box)

'''
tests, count = pattern.subn(replacement, tests, count=1)
if count != 1:
    raise SystemExit(f"portfolio artifact test: expected one match, found {count}")
Path("tests/test_portfolio.py").write_text(tests, encoding="utf-8")

for path in [
    "assets/site.css",
    ".github/workflows/normalize-bootloader-evidence.yml",
    ".github/workflows/normalize-bootloader-evidence-v2.yml",
    ".github/workflows/normalize-bootloader-evidence-v3.yml",
    ".github/workflows/normalize-bootloader-evidence-v4.yml",
    ".github/scripts/normalize_bootloader_evidence.py",
    "docs/.normalize-trigger",
    "docs/.normalize-trigger-2",
    "docs/.normalize-trigger-3",
]:
    Path(path).unlink(missing_ok=True)
