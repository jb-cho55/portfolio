# Portfolio Project Content Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refine both project detail panels so the Black Box project shows actual test evidence and the OTA project explains its two implementation stages and Memory Alignment Error debugging flow.

**Architecture:** Preserve the existing single-page HTML, CSS, and vanilla JavaScript accordion structure. Add four copied portfolio-safe PNG assets under `assets/images/`, render them as a responsive figure gallery inside the Black Box detail region, and replace the OTA review/limitation blocks with two development-stage cards plus one debugging narrative.

**Tech Stack:** Semantic HTML5, CSS Grid, vanilla JavaScript, Python `unittest`, GitHub Pages

## Global Constraints

- Keep Black Box Testing as Project 01 and OTA Bootloader as Project 02.
- Do not expose private repository links, original requirement documents, or education-internal materials.
- Replace `본인 수행 범위` with `수행 범위`.
- Remove the Black Box public-scope disclaimer sentence from the visible detail panel.
- Copy only `network_setup.png`, `automation_test_environment.png`, `panel_trace.png`, and `defect_batt_percent_15.png` into the public portfolio.
- Every project image must use a local path, descriptive `alt`, a visible caption, and `loading="lazy"`.
- Desktop image gallery uses two columns; widths at or below 900px use one column.
- Remove the OTA `정적 코드 리뷰` and `검증 범위와 한계` blocks.
- OTA details must use two purpose-based development stages rather than education project numbering.
- Describe the debug sequence as project-time discovery → Trace32 investigation → 4-byte alignment cause → `uint32` buffer correction.
- Do not describe the fixed-key hash as HMAC or a digital signature.
- Do not add OTA project 4 `+0x05/-0x05`, modals, routing, frameworks, or external image dependencies.

---

### Task 1: Define the revised portfolio requirements in tests

**Files:**
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: UTF-8 contents of `index.html`
- Produces: regression tests for removed copy, renamed labels, image accessibility, OTA stages, and debugging sequence

- [ ] **Step 1: Add failing tests for the revised content**

Add these methods to `PortfolioContentTests` and replace outdated assertions that require `정적 코드 리뷰` or `현재 ECU에서 재시험하지 않음`:

```python
    def test_black_box_detail_uses_neutral_scope_label(self):
        self.assertIn("수행 범위", self.html)
        self.assertNotIn("본인 수행 범위", self.html)
        self.assertNotIn(
            "원본 요구사양과 내부 자료는 제외하고, 직접 수행한 테스트 환경·결함 분석·개선 방향만 포트폴리오용으로 재구성했습니다.",
            self.html,
        )

    def test_black_box_gallery_contains_accessible_local_evidence(self):
        gallery = [
            ("assets/images/network_setup.png", "CANoe Network 구성"),
            ("assets/images/automation_test_environment.png", "CAPL 자동화 테스트 환경"),
            ("assets/images/panel_trace.png", "Panel 및 Trace 화면"),
            ("assets/images/defect_batt_percent_15.png", "Test Result 근거"),
        ]
        for path, caption in gallery:
            self.assertIn(f'src="{path}"', self.html)
            self.assertIn('loading="lazy"', self.html)
            self.assertIn(caption, self.html)
        self.assertGreaterEqual(self.html.count("<figcaption>"), 4)
        self.assertGreaterEqual(self.html.count("alt="), 4)

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
        positions = [self.html.index(term) for term in expected]
        self.assertEqual(positions, sorted(positions))
```

- [ ] **Step 2: Run the focused test file and verify expected failures**

Run:

```bash
python -m unittest tests/test_portfolio.py -v
```

Expected: failures for the old label, missing gallery, old OTA blocks, and missing development-stage/debugging copy.

- [ ] **Step 3: Commit the failing requirements**

```bash
git add tests/test_portfolio.py
git commit -m "test: define refined project detail requirements"
```

---

### Task 2: Add public test evidence and refine both detail panels

**Files:**
- Create: `assets/images/network_setup.png`
- Create: `assets/images/automation_test_environment.png`
- Create: `assets/images/panel_trace.png`
- Create: `assets/images/defect_batt_percent_15.png`
- Modify: `index.html`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: portfolio-safe images from `jb-cho55/IVS-Black-Box-Testing/assets/images/`
- Produces: `.evidence-gallery`, `.evidence-item`, two OTA development-stage blocks, and a Memory Alignment Error narrative

- [ ] **Step 1: Copy the four approved PNG files into the portfolio repository**

Use the exact source-to-target mapping:

```text
IVS-Black-Box-Testing/assets/images/network_setup.png
→ portfolio/assets/images/network_setup.png

IVS-Black-Box-Testing/assets/images/automation_test_environment.png
→ portfolio/assets/images/automation_test_environment.png

IVS-Black-Box-Testing/assets/images/panel_trace.png
→ portfolio/assets/images/panel_trace.png

IVS-Black-Box-Testing/assets/images/defect_batt_percent_15.png
→ portfolio/assets/images/defect_batt_percent_15.png
```

- [ ] **Step 2: Add responsive gallery styles**

Insert the following styles next to the existing project-detail styles:

```css
.evidence-gallery {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.evidence-item {
  overflow: hidden;
  margin: 0;
  border: 1px solid var(--line);
  border-radius: 9px;
  background: #fff;
}
.evidence-item img {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: contain;
  background: #eef2f7;
}
.evidence-item figcaption {
  padding: 10px 12px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 750;
}
.stage-list {
  display: grid;
  gap: 9px;
  margin: 12px 0 0;
  padding-left: 18px;
  color: var(--muted);
  font-size: 14px;
}
.debug-flow {
  display: grid;
  gap: 10px;
  margin-top: 12px;
}
.debug-step {
  padding: 12px 14px;
  border-left: 3px solid var(--blue);
  background: var(--blue-soft);
  color: #394962;
  font-size: 14px;
}
```

Add this rule inside `@media(max-width:900px)`:

```css
.evidence-gallery { grid-template-columns: 1fr; }
```

- [ ] **Step 3: Refine the Black Box detail region**

- Change `<h4>본인 수행 범위</h4>` to `<h4>수행 범위</h4>`.
- Keep the test-flow and representative-defect blocks.
- Delete the sentence beginning `원본 요구사양과 내부 자료는 제외하고`.
- Add a full-width detail block containing this gallery:

```html
<article class="detail-block wide">
  <h4>실제 수행 화면 및 Test Result</h4>
  <div class="evidence-gallery">
    <figure class="evidence-item">
      <img src="assets/images/network_setup.png" alt="CANoe에서 IVS와 주변 ECU Network Node를 구성한 화면" loading="lazy">
      <figcaption>CANoe Network 구성</figcaption>
    </figure>
    <figure class="evidence-item">
      <img src="assets/images/automation_test_environment.png" alt="CAPL 기반 자동화 테스트 실행 환경 화면" loading="lazy">
      <figcaption>CAPL 자동화 테스트 환경</figcaption>
    </figure>
    <figure class="evidence-item">
      <img src="assets/images/panel_trace.png" alt="Panel 입력 제어와 CAN Trace 확인 화면" loading="lazy">
      <figcaption>Panel 및 Trace 화면</figcaption>
    </figure>
    <figure class="evidence-item">
      <img src="assets/images/defect_batt_percent_15.png" alt="Batt Percent 15퍼센트 경계값 결함을 확인한 Test Result 화면" loading="lazy">
      <figcaption>Test Result 근거 — Batt Percent 15% 경계값</figcaption>
    </figure>
  </div>
</article>
```

- [ ] **Step 4: Replace the OTA detail blocks**

Keep the system/reprogramming flow, then replace `정적 코드 리뷰` and `검증 범위와 한계` with:

```html
<article class="detail-block">
  <h4>개발 단계 1 — 애플리케이션 보호 및 복구</h4>
  <p>OTA 업데이트 중 전송 중단이나 Flash 쓰기 실패가 발생해도 기존 애플리케이션을 보호할 수 있도록 Backup·Erase·Restore 흐름을 구현했습니다.</p>
  <ul class="stage-list">
    <li>Application Primary를 Backup 영역으로 복사</li>
    <li>Primary 영역 Erase 후 신규 SW Binary 기록</li>
    <li>부팅 시 valid pattern으로 애플리케이션 유효성 확인</li>
    <li>유효하지 않으면 Backup을 Primary로 복구</li>
  </ul>
</article>
<article class="detail-block">
  <h4>개발 단계 2 — SW Binary 무결성 검증</h4>
  <p>Application 데이터의 SHA-256 계산값과 서명 영역의 32바이트 저장값을 비교해 Binary 변경 여부를 확인했습니다. 이후 교육용 고정 키와 Application 데이터를 결합한 SHA-256 검사 흐름으로 확장했습니다.</p>
  <ul class="stage-list">
    <li>Application Binary의 SHA-256 계산</li>
    <li>계산값과 32바이트 저장값 비교</li>
    <li>교육용 고정 키와 Application 데이터를 결합한 검사</li>
    <li>검사 결과에 따라 실행 또는 복구 경로 분기</li>
  </ul>
</article>
<article class="detail-block wide">
  <h4>대표 문제 해결 — Memory Alignment Error</h4>
  <p>프로젝트 진행 중 Backup·Restore 기능을 구현하면서 Flash 쓰기 경로에서 Memory Alignment Error로 인한 Trap을 발견해 디버깅했습니다.</p>
  <div class="debug-flow">
    <div class="debug-step"><strong>문제 발생</strong> — `FlsLoader_Write` 호출 과정에서 Backup·Restore가 중단되는 Trap 발생</div>
    <div class="debug-step"><strong>원인 추적</strong> — Trace32의 Trap 관련 레지스터와 Flash Loader 인수를 확인</div>
    <div class="debug-step"><strong>원인 확인</strong> — `uint8` source buffer가 Flash Loader의 4바이트 정렬 조건을 보장하지 않음</div>
    <div class="debug-step"><strong>수정</strong> — 저장 버퍼를 `uint32` 배열로 변경하고 바이트 처리는 `uint8*`로 참조</div>
    <div class="debug-step"><strong>적용 범위</strong> — Application → Backup과 Backup → Application 경로에 동일하게 적용</div>
  </div>
</article>
```

- [ ] **Step 5: Run the focused tests**

Run:

```bash
python -m unittest tests/test_portfolio.py -v
```

Expected: all portfolio tests pass.

- [ ] **Step 6: Commit the project detail refinement**

```bash
git add index.html assets/images tests/test_portfolio.py
git commit -m "feat: refine project evidence and bootloader story"
```

---

### Task 3: Update documentation and verify the final branch

**Files:**
- Modify: `README.md`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: final visible portfolio content
- Produces: repository documentation matching the evidence gallery and two-stage OTA explanation

- [ ] **Step 1: Update README feature bullets**

Add or revise bullets so `주요 구성` includes:

```markdown
- CANoe·CAPL·Panel·Trace·Test Result 화면을 제공하는 Black Box Testing 상세 갤러리
- 애플리케이션 보호·복구와 SW Binary 무결성 검증의 2단계 OTA Bootloader 설명
- Memory Alignment Error를 Trace32로 분석하고 4바이트 정렬 버퍼로 개선한 문제 해결 사례
```

- [ ] **Step 2: Run all tests**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: all discovered tests pass.

- [ ] **Step 3: Verify local image references and removed content**

Run:

```bash
python - <<'PY'
from pathlib import Path
html = Path("index.html").read_text(encoding="utf-8")
for path in [
    "assets/images/network_setup.png",
    "assets/images/automation_test_environment.png",
    "assets/images/panel_trace.png",
    "assets/images/defect_batt_percent_15.png",
]:
    assert Path(path).is_file(), path
    assert f'src="{path}"' in html, path
for removed in ["본인 수행 범위", "정적 코드 리뷰", "검증 범위와 한계", "+0x05/-0x05"]:
    assert removed not in html, removed
print("portfolio refinement checks passed")
PY
```

Expected: `portfolio refinement checks passed`.

- [ ] **Step 4: Commit documentation**

```bash
git add README.md
git commit -m "docs: describe evidence gallery and OTA stages"
```

- [ ] **Step 5: Final verification**

Run:

```bash
python -m unittest discover -s tests -v
git diff --check main...HEAD
git status --short
```

Expected: all tests pass, no whitespace errors, and a clean working tree.
