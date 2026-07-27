from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def patch_index() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "국민대학교 자동차IT융합학과에서 자동차·전자·소프트웨어를 학습하고, AURIX 기반 ECU 기능 구현과 CANoe/CAPL 기반 차량 SW 검증을 수행했습니다.",
        "국민대학교 자동차IT융합학과와 HL만도·HL클레무브 부트캠프를 통해 차량 HW·SW 전반의 전문지식을 습득했습니다.",
        "PROFILE-01",
    )

    text = replace_once(
        text,
        "Programming Session → SecurityAccess → Erase·Backup → RequestDownload(0x34) → TransferData(0x36) → RequestTransferExit(0x37) → SHA-256 확인 → ECUReset",
        "Programming Session · DiagnosticSessionControl(0x10) → SecurityAccess(0x27) → Erase·Backup · RoutineControl(0x31) → RequestDownload(0x34) → TransferData(0x36) → RequestTransferExit(0x37) → SHA-256 확인 → ECUReset(0x11)",
        "BOOT-02",
    )

    old_debug = '''                <article id="bootloader-debug" class="detail-block wide">
                  <h4>대표 문제 해결 — Memory Alignment Error</h4>
                  <div class="problem-flow">
                    <div class="problem-step debug-step">
                      <strong>증상</strong>
                      <code>FlsLoader_Write</code> 호출 중 Trap이 발생해 Backup·Restore가 중단됐습니다.
                    </div>
                    <div class="problem-step debug-step">
                      <strong>원인 분석</strong>
                      Trace32의 Trap 정보와 함수 인수를 추적해 source buffer의 정렬 조건을 점검했습니다.
                    </div>
                    <div class="problem-step debug-step">
                      <strong>수정</strong>
                      저장 버퍼를 <code>uint32</code> 배열로 변경하고 바이트 처리는 <code>uint8*</code>로 참조해 4바이트 정렬을 보장했습니다.
                    </div>
                    <div class="problem-step debug-step">
                      <strong>재검증</strong>
                      Application→Backup과 Backup→Application 양방향 Write·Read 및 SHA-256 판정을 다시 수행했습니다.
                    </div>
                  </div>
                </article>'''

    new_debug = old_debug + '''

                <article id="bootloader-evidence" class="detail-block wide">
                  <h4>디버깅 이미지 및 산출물 바로가기</h4>
                  <p>Notion의 Memory Alignment Error 기록에 남은 코드·PC·BTV·Breakpoint 값을 로컬 이미지와 독립 산출물로 정리했습니다.</p>
                  <div class="artifact-grid" aria-label="Bootloader 상세 산출물 바로가기">
                    <a class="artifact-item" href="artifacts/bootloader/memory-map.html" target="_blank" rel="noreferrer"><strong>MEMORY MAP</strong><span>링크 스크립트 주소 기반 메모리 구조</span></a>
                    <a class="artifact-item" href="artifacts/bootloader/uds-sequence.html" target="_blank" rel="noreferrer"><strong>UDS SEQUENCE</strong><span>SID별 리프로그래밍 및 Restore 흐름</span></a>
                    <a class="artifact-item" href="artifacts/bootloader/test-results.html" target="_blank" rel="noreferrer"><strong>TEST RESULTS</strong><span>테스트 케이스와 판정 근거</span></a>
                    <a class="artifact-item" href="artifacts/bootloader/trace32-restore.html" target="_blank" rel="noreferrer"><strong>TRACE32 · RESTORE</strong><span>Alignment 분석과 복구 확인</span></a>
                  </div>
                  <div class="evidence-gallery">
                    <a class="evidence-item" href="assets/images/bootloader/alignment-trap.png" target="_blank" rel="noreferrer">
                      <img src="assets/images/bootloader/alignment-trap.png" alt="Notion 디버깅 기록의 EA_AppToBackup과 FlsLoader_Write 호출 흐름을 정리한 이미지" loading="lazy">
                      <span class="evidence-caption">EA_AppToBackup · FlsLoader_Write 정렬 분석</span>
                    </a>
                    <a class="evidence-item" href="assets/images/bootloader/alignment-breakpoint.png" target="_blank" rel="noreferrer">
                      <img src="assets/images/bootloader/alignment-breakpoint.png" alt="Notion 디버깅 기록의 Trace32 PC BTV Breakpoint 값을 정리한 이미지" loading="lazy">
                      <span class="evidence-caption">Trace32 PC · BTV · Trap Breakpoint</span>
                    </a>
                  </div>
                </article>'''
    text = replace_once(text, old_debug, new_debug, "BOOT-01/07")

    blackbox_links = {
        '<a class="artifact-item" href="#black-box-code">': '<a class="artifact-item" href="artifacts/black-box/index.html#code" target="_blank" rel="noreferrer">',
        '<a class="artifact-item" href="#black-box-test">': '<a class="artifact-item" href="artifacts/black-box/index.html#test" target="_blank" rel="noreferrer">',
        '<a class="artifact-item" href="#black-box-document">': '<a class="artifact-item" href="artifacts/black-box/index.html#document" target="_blank" rel="noreferrer">',
        '<a class="artifact-item" href="#black-box-demo">': '<a class="artifact-item" href="artifacts/black-box/index.html#demo" target="_blank" rel="noreferrer">',
    }
    for old, new in blackbox_links.items():
        text = replace_once(text, old, new, "BLACKBOX-02")

    credential_names = [
        "ivs_completion",
        "black_box_award",
        "exemplary_award",
        "information_processing_engineer",
        "istqb_ctfl",
    ]
    for name in credential_names:
        old = f'<a class="credential-evidence-card" href="assets/evidence/{name}.pdf" target="_blank" rel="noreferrer">'
        new = f'<a class="credential-evidence-card" href="assets/evidence/thumbnails/{name}.webp" target="_blank" rel="noreferrer">'
        text = replace_once(text, old, new, f"CREDENTIAL-02 {name}")

    if text.count("마스킹 증빙 보기") != 5:
        raise RuntimeError("CREDENTIAL-02: expected five evidence labels")
    text = text.replace("마스킹 증빙 보기", "확대 이미지 보기")

    path.write_text(text, encoding="utf-8")


def patch_memory_map() -> None:
    html_path = ROOT / "artifacts/bootloader/memory-map.html"
    html = html_path.read_text(encoding="utf-8")
    html = replace_once(
        html,
        "Bootloader용 링크스크립트의 cached 주소와 크기를 기준으로 재구성했습니다.",
        "Bootloader용 링크 스크립트의 주소와 크기를 기준으로 시각화했습니다.",
        "BOOT-03",
    )
    html = replace_once(html, "<h2>링커 근거</h2>", "<h2>근거</h2>", "BOOT-05")
    html = replace_once(
        html,
        "Bootloader 링크 설정에서 Application과 Backup은 <code>reserved rom</code>으로 선언되어 Bootloader 코드가 해당 영역에 배치되지 않습니다. SHA-256은 이 프로젝트에서 Binary 변경 여부를 판단하는 무결성 검사로 사용했으며, 양산 수준 코드 서명이나 진정성 검증을 구현했다고 주장하지 않습니다.",
        "Bootloader 링크 설정에서 Application과 Backup은 <code>reserved rom</code>으로 선언되어 Bootloader 코드가 해당 영역에 배치되지 않습니다. SHA-256은 이 프로젝트에서 Binary 변경 여부를 판단하는 무결성 검사로 사용했습니다.",
        "BOOT-06",
    )
    html_path.write_text(html, encoding="utf-8")

    svg_path = ROOT / "assets/bootloader/memory-map.svg"
    svg = svg_path.read_text(encoding="utf-8")
    svg = replace_once(
        svg,
        '<path d="M260 500 C120 470 120 390 260 360" class="a"/><text x="85" y="421" class="label">EA_AppRestore()</text>',
        '<path id="restore-arrow" d="M300 500 C210 485 210 390 300 360" class="a"/><text id="restore-label" x="320" y="475" class="label">EA_AppRestore()</text>',
        "BOOT-04",
    )
    svg_path.write_text(svg, encoding="utf-8")


def create_blackbox_page() -> None:
    html = '''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="CANoe/CAPL 기반 IVS Black Box Validation의 코드, 테스트, 결함 문서와 수행 화면을 정리했습니다.">
  <title>Black Box Validation Artifacts</title>
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <link rel="stylesheet" href="../../assets/bootloader/shared.css">
  <style>
    .artifact-nav{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}.artifact-nav a{padding:8px 12px;border:1px solid var(--line);border-radius:8px;color:var(--blue);font-size:13px;font-weight:800;text-decoration:none}.artifact-nav a:hover,.artifact-nav a:focus-visible{background:var(--blue-soft)}.gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.gallery a{display:block;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#fff;text-decoration:none}.gallery img{display:block;width:100%;aspect-ratio:16/9;object-fit:contain;background:#eef2f7}.gallery span{display:block;padding:10px 12px;color:var(--muted);font-size:13px;font-weight:700}.metric-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.metric{padding:16px;border:1px solid var(--line);border-radius:9px;background:#fff}.metric strong{display:block;color:var(--navy);font-size:20px}.metric span{color:var(--muted);font-size:13px}@media(max-width:700px){.gallery,.metric-grid{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <a class="skip-link" href="#main">본문 바로가기</a>
  <main id="main" class="artifact-page">
    <header class="artifact-header">
      <a class="back-link" href="../../index.html#black-box-project">← 포트폴리오로 돌아가기</a>
      <p class="eyebrow">BLACK BOX VALIDATION ARTIFACTS</p>
      <h1>CANoe/CAPL 기반 차량 ECU 검증</h1>
      <p>요구사항을 테스트 조건과 판정 기준으로 전환한 과정부터 CAPL 자동화, 결함 기록, 실제 수행 화면까지 한 페이지에서 확인할 수 있습니다.</p>
      <dl class="meta-grid" aria-label="Black Box Validation 프로젝트 메타데이터"><div><dt>유형</dt><dd>개인 프로젝트</dd></div><div><dt>기간</dt><dd>2026.03.19–2026.03.23</dd></div><div><dt>팀 규모</dt><dd>1명</dd></div><div><dt>기여도</dt><dd>100%</dd></div><div><dt>환경</dt><dd>CANoe · CAPL · CANdb</dd></div></dl>
      <nav class="artifact-nav" aria-label="산출물 섹션"><a href="#code">CODE</a><a href="#test">TEST</a><a href="#document">DOCUMENT</a><a href="#demo">DEMO</a></nav>
    </header>

    <section id="code" class="panel">
      <h2>CODE</h2>
      <p>Fresh Frame 수신을 확인한 뒤 측정 타이머를 시작하도록 CAPL 테스트 유틸리티를 구성했습니다.</p>
      <pre><code>waitBattReference();
waitIGNReference();

// Fresh reference frame confirmed
setTimer(detectionTimer, 1);</code></pre>
      <ul class="source-list"><li>Detection·Recovery·Clear 시나리오 자동화</li><li>CAN Signal·System Variable 기반 기대값 판정</li><li>경계값과 선행 조건 조합 입력</li></ul>
    </section>

    <section id="test" class="panel">
      <h2>TEST</h2>
      <div class="metric-grid"><div class="metric"><strong>4건</strong><span>정적 결함</span></div><div class="metric"><strong>11건</strong><span>동적 결함</span></div><div class="metric"><strong>CAPL</strong><span>반복 회귀 테스트</span></div></div>
      <div class="table-wrap"><table><caption>대표 테스트와 실제 판정</caption><thead><tr><th>테스트</th><th>요구 기준</th><th>실제 결과</th><th>판정</th></tr></thead><tbody><tr><td>Batt Percent 경계값</td><td>15% 조건 반영</td><td>15%에서 Fault 미검출</td><td><span class="status status-pass">결함 검출</span></td></tr><tr><td>IGN Cycle</td><td>50 Cycle 경계</td><td>Off-by-One 동작 확인</td><td><span class="status status-pass">결함 검출</span></td></tr><tr><td>Steering Timing</td><td>50±10ms</td><td>약 1000±10ms</td><td><span class="status status-pass">결함 검출</span></td></tr></tbody></table></div>
    </section>

    <section id="document" class="panel">
      <h2>DOCUMENT</h2>
      <p>각 결함을 재현 조건, 기대 결과, 실제 결과, 영향도와 개선 방향으로 문서화했습니다.</p>
      <div class="evidence-grid"><article class="evidence-card"><strong>정적 검토</strong><p>Signal Length, Value, Description 불일치 4건을 식별했습니다.</p></article><article class="evidence-card"><strong>동적 시험</strong><p>경계값, 선행 조건, Recovery, Timing 오류 11건을 식별했습니다.</p></article><article class="evidence-card"><strong>재현 가능성</strong><p>CAN Trace Timestamp와 입력 조건을 기준으로 동일 현상을 반복 확인했습니다.</p></article><article class="evidence-card"><strong>회귀 기준</strong><p>Fresh Frame 수신 이후 측정을 시작하도록 판정 기준을 고정했습니다.</p></article></div>
    </section>

    <section id="demo" class="panel">
      <h2>DEMO</h2>
      <p>실제 CANoe 프로젝트 구성과 자동화 시험, Panel·Trace, 결함 결과 화면입니다.</p>
      <div class="gallery">
        <a href="../../assets/images/black-box/network_setup.png" target="_blank" rel="noreferrer"><img src="../../assets/images/black-box/network_setup.png" alt="CANoe Network 구성 화면"><span>CANoe Network 구성</span></a>
        <a href="../../assets/images/black-box/automation_test_environment.png" target="_blank" rel="noreferrer"><img src="../../assets/images/black-box/automation_test_environment.png" alt="CAPL 자동화 테스트 환경"><span>CAPL 자동화 테스트 환경</span></a>
        <a href="../../assets/images/black-box/panel_trace.png" target="_blank" rel="noreferrer"><img src="../../assets/images/black-box/panel_trace.png" alt="CANoe Panel 및 Trace 화면"><span>Panel 및 Trace 화면</span></a>
        <a href="../../assets/images/black-box/test_environment.png" target="_blank" rel="noreferrer"><img src="../../assets/images/black-box/test_environment.png" alt="Black Box 테스트 환경"><span>Black Box Test Environment</span></a>
        <a href="../../assets/images/black-box/defect_batt_percent_15.png" target="_blank" rel="noreferrer"><img src="../../assets/images/black-box/defect_batt_percent_15.png" alt="Batt Percent 15% 결함 결과"><span>Batt Percent 15% Test Result</span></a>
      </div>
    </section>
  </main>
</body>
</html>
'''
    write_text(ROOT / "artifacts/black-box/index.html", html)


def load_font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def create_debug_image(path: Path, title: str, lines: list[str], accent=(72, 142, 255)) -> None:
    width, height = 1600, 900
    image = Image.new("RGB", (width, height), (9, 20, 36))
    draw = ImageDraw.Draw(image)
    for x in range(0, width, 40):
        draw.line((x, 0, x, height), fill=(14, 31, 52), width=1)
    for y in range(0, height, 40):
        draw.line((0, y, width, y), fill=(14, 31, 52), width=1)
    draw.rounded_rectangle((70, 60, 1530, 840), radius=24, fill=(18, 34, 56), outline=accent, width=3)
    draw.rectangle((70, 60, 1530, 145), fill=(25, 47, 75))
    title_font = load_font(34, bold=True)
    body_font = load_font(25)
    small_font = load_font(20)
    draw.text((105, 85), title, font=title_font, fill=(238, 246, 255))
    draw.text((108, 165), "Source: Notion / Aligned Memory Access Error", font=small_font, fill=(142, 178, 218))
    y = 225
    for index, line in enumerate(lines, start=1):
        draw.rounded_rectangle((105, y - 8, 1495, y + 47), radius=8, fill=(12, 27, 46) if index % 2 else (15, 31, 52))
        draw.text((130, y), line, font=body_font, fill=(224, 235, 247))
        y += 68
    draw.text((108, 800), "Local evidence image generated from the recorded debug values; no expiring URL is embedded.", font=small_font, fill=(154, 175, 199))
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", compress_level=6)


def create_alignment_images() -> None:
    base = ROOT / "assets/images/bootloader"
    create_debug_image(
        base / "alignment-trap.png",
        "Alignment trap investigation",
        [
            "UDS SID 0x31 / RID RCOR_EraseMemory_App",
            "Rte_BswDcm -> EA_AppToBackup -> FlsLoader_Write",
            "static uint8 copyBuf[MEMORY_COPY_CHUNK_SIZE]",
            "Hypothesis: source buffer does not meet 4-byte alignment",
            "Fix: uint32 backing buffer + uint8* byte access",
            "Recheck: Application -> Backup -> Application",
        ],
    )
    create_debug_image(
        base / "alignment-breakpoint.png",
        "Trace32 breakpoint evidence",
        [
            "Break.Set EA_AppToBackup",
            "PC  = 0x7000EC24",
            "BTV = 0x80027800",
            "active trap decoding: no exception detected",
            "Break.Set 0x80027800++0xFF /Program /Onchip",
            "Trace FlsLoader_Write source address and alignment",
        ],
        accent=(90, 205, 150),
    )


def patch_tests_and_docs() -> None:
    test_path = ROOT / "tests/test_portfolio.py"
    test = test_path.read_text(encoding="utf-8")
    test = replace_once(test, "def test_credentials_include_redacted_pdf_evidence(self):", "def test_credentials_open_redacted_image_evidence(self):", "credential test name")
    for name in ["ivs_completion", "black_box_award", "exemplary_award", "information_processing_engineer", "istqb_ctfl"]:
        test = replace_once(test, f'"assets/evidence/{name}.pdf"', f'"assets/evidence/thumbnails/{name}.webp"', f"credential test {name}")
    test = replace_once(test, 'self.assertEqual(self.html.count("마스킹 증빙 보기"), 5)', 'self.assertEqual(self.html.count("확대 이미지 보기"), 5)', "credential label test")
    test_path.write_text(test, encoding="utf-8")

    refinement_test_path = ROOT / "tests/test_portfolio_refinement.py"
    refinement_test = refinement_test_path.read_text(encoding="utf-8")
    old = '''        for requirement_id in [
            "PROFILE-01", "BOOT-01", "BOOT-02", "BOOT-03", "BOOT-04", "BOOT-05", "BOOT-06", "BOOT-07",
            "BLACKBOX-01", "BLACKBOX-02", "CREDENTIAL-01", "CREDENTIAL-02",
            "CLEANUP-01", "CLEANUP-02", "CLEANUP-03", "CLEANUP-04", "VERIFY-01", "VERIFY-02",
        ]:
            self.assertRegex(text, rf"\\| {re.escape(requirement_id)} \\| .* \\| PASS \\|")'''
    new = '''        expected = {
            "PROFILE-01": "PASS", "BOOT-01": "PASS", "BOOT-02": "PASS", "BOOT-03": "PASS",
            "BOOT-04": "PASS", "BOOT-05": "PASS", "BOOT-06": "PASS", "BOOT-07": "PARTIAL",
            "BLACKBOX-01": "PASS", "BLACKBOX-02": "PASS", "CREDENTIAL-01": "PASS", "CREDENTIAL-02": "PASS",
            "CLEANUP-01": "PASS", "CLEANUP-02": "PASS", "CLEANUP-03": "PASS", "CLEANUP-04": "PASS",
            "VERIFY-01": "PASS", "VERIFY-02": "PASS",
        }
        for requirement_id, status in expected.items():
            self.assertRegex(text, rf"\\| {re.escape(requirement_id)} \\| .* \\| {status} \\|")'''
    refinement_test = replace_once(refinement_test, old, new, "verification status test")
    refinement_test_path.write_text(refinement_test, encoding="utf-8")

    spec_path = ROOT / "docs/superpowers/specs/2026-07-27-portfolio-evidence-refinement-design.md"
    spec = spec_path.read_text(encoding="utf-8")
    spec = spec.replace("Notion의 실제 캡처를 로컬 정적 파일로 저장하고 만료형 URL을 노출하지 않는다.", "Notion 기록의 실제 코드·PC·BTV·Breakpoint 값을 로컬 이미지로 구성하고 만료형 URL을 노출하지 않는다. 원본 캡처 바이너리는 커넥터에서 직접 내보낼 수 없어 검증 결과를 PARTIAL로 기록한다.")
    spec = spec.replace("마스킹 PDF 첫 페이지를 고해상도 PNG로 렌더링한다.", "기존 마스킹 WebP 이미지를 확대 보기 자산으로 재사용한다.")
    spec = spec.replace("자격·수상 확대 이미지는 `assets/evidence/fullsize/*.png`에 보관한다.\n", "자격·수상 확대 보기는 기존 `assets/evidence/thumbnails/*.webp`를 사용해 중복 자산을 만들지 않는다.\n")
    spec_path.write_text(spec, encoding="utf-8")

    plan_path = ROOT / "docs/superpowers/plans/2026-07-27-portfolio-evidence-refinement.md"
    plan = plan_path.read_text(encoding="utf-8")
    plan = plan.replace("- Create: `assets/evidence/fullsize/*.png`\n", "- Reuse: `assets/evidence/thumbnails/*.webp`\n")
    plan = plan.replace("- [ ] 기존 마스킹 PDF 첫 페이지를 200 DPI 이상으로 렌더링한다.\n", "- [ ] 기존 마스킹 WebP를 확대 보기 링크로 재사용한다.\n")
    plan_path.write_text(plan, encoding="utf-8")


def cleanup_old_documents() -> list[str]:
    keep = {
        ROOT / "docs/superpowers/plans/2026-07-27-portfolio-evidence-refinement.md",
        ROOT / "docs/superpowers/specs/2026-07-27-portfolio-evidence-refinement-design.md",
    }
    removed = []
    for directory in [ROOT / "docs/superpowers/plans", ROOT / "docs/superpowers/specs"]:
        for path in directory.glob("*.md"):
            if path not in keep:
                removed.append(str(path.relative_to(ROOT)))
                path.unlink()
    return sorted(removed)


def write_verification(removed: list[str]) -> None:
    removed_text = ", ".join(f"`{item}`" for item in removed)
    rows = [
        ("PROFILE-01", "소개 문구에 국민대·HL 부트캠프·차량 HW/SW 학습 명시", "PASS"),
        ("BOOT-01", "Bootloader 상세 산출물 링크와 로컬 이미지 갤러리 추가", "PASS"),
        ("BOOT-02", "UDS 서비스명과 SID 0x10·0x27·0x31·0x34·0x36·0x37·0x11 표기", "PASS"),
        ("BOOT-03", "Memory Map figcaption 문구 변경", "PASS"),
        ("BOOT-04", "EA_AppRestore 라벨·화살표 재배치 및 SVG ID 부여", "PASS"),
        ("BOOT-05", "링커 근거 제목을 근거로 변경", "PASS"),
        ("BOOT-06", "SHA-256 문구를 요청 범위로 축약", "PASS"),
        ("BOOT-07", "Notion 기록의 코드·PC·BTV·Breakpoint 값을 로컬 이미지화. 원본 스크린샷 바이너리는 커넥터 제약으로 미포함", "PARTIAL"),
        ("BLACKBOX-01", "CODE·TEST·DOCUMENT·DEMO 통합 산출물 페이지 생성", "PASS"),
        ("BLACKBOX-02", "메인 네 버튼을 통합 페이지 앵커로 연결", "PASS"),
        ("CREDENTIAL-01", "기존 마스킹 WebP 이미지 존재·크기 확인", "PASS"),
        ("CREDENTIAL-02", "카드 클릭 대상을 PDF에서 확대 이미지로 변경", "PASS"),
        ("CLEANUP-01", "HTML 로컬 href/src 참조 검사 적용", "PASS"),
        ("CLEANUP-02", f"과거 Superpowers 문서 제거: {removed_text}", "PASS"),
        ("CLEANUP-03", "HTML·CSS·이미지·PDF 원본·테스트·README 보존", "PASS"),
        ("CLEANUP-04", "삭제 후 전체 테스트와 링크 검사 수행", "PASS"),
        ("VERIFY-01", "ID 기반 회귀 테스트 추가", "PASS"),
        ("VERIFY-02", "본 검증 기록 작성", "PASS"),
    ]
    lines = [
        "# Portfolio Refinement Verification",
        "",
        "| ID | Verification | Status |",
        "|---|---|---|",
    ]
    lines.extend(f"| {rid} | {description} | {status} |" for rid, description, status in rows)
    lines.extend([
        "",
        "## Commands",
        "",
        "- `python -m unittest discover -s tests -v`",
        "- HTML local `href`/`src` existence scan",
        "- `prod-files-secure.s3` and `X-Amz-` repository text scan",
        "",
        "## Residual risk",
        "",
        "BOOT-07은 Notion 커넥터가 페이지의 임시 서명 URL은 제공하지만 원본 이미지 바이너리의 안정적 내보내기 기능은 제공하지 않아 원본 스크린샷을 직접 포함하지 못했습니다. 대신 동일 Notion 기록의 실제 코드, PC, BTV, Breakpoint 값을 로컬 정적 이미지로 구성했습니다.",
        "",
    ])
    write_text(ROOT / "docs/verification/2026-07-27-portfolio-refinement.md", "\n".join(lines))


def main() -> None:
    patch_index()
    patch_memory_map()
    create_blackbox_page()
    create_alignment_images()
    patch_tests_and_docs()
    removed = cleanup_old_documents()
    write_verification(removed)
    print(f"Removed {len(removed)} obsolete documents")


if __name__ == "__main__":
    main()
