# Portfolio Project Details Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace inaccessible private project repository links with accessible in-page project details and add the OTA Bootloader as a second portfolio project.

**Architecture:** Keep the existing single-file portfolio architecture. `index.html` will own both project summaries, collapsible detail regions, component styling, and a small button controller that updates `hidden`, `aria-expanded`, and button copy. `tests/test_portfolio.py` will verify content, private-link removal, accessibility attributes, and interaction source; `README.md` will describe the two-project portfolio.

**Tech Stack:** Semantic HTML5, CSS, vanilla JavaScript, Python `unittest`, GitHub Pages

## Global Constraints

- Preserve the existing white, navy, and blue corporate visual language.
- Keep Black Box Testing as Project 01 and OTA Bootloader as Project 02.
- Do not expose private repository links or unpublished source material.
- Both project summaries must remain useful when JavaScript is unavailable.
- Detail buttons must use `aria-expanded` and `aria-controls` and update both state and visible copy.
- Initial detail state is collapsed.
- At widths of 900px or below, all project detail layouts become single-column.
- Do not add frameworks, routing, modals, or external image dependencies.
- Do not claim current ECU re-execution or build reproducibility for the OTA project.

---

### Task 1: Define portfolio project-detail requirements in tests

**Files:**
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: UTF-8 contents of `index.html`
- Produces: regression tests for project ordering, private-link removal, accordion accessibility, OTA content, and interaction source

- [ ] **Step 1: Replace the outdated project-link test and add failing detail tests**

Add the following methods to `PortfolioContentTests`, replacing the existing `test_links_exist` method:

```python
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

    def test_bootloader_project_contains_embedded_qa_evidence(self):
        for content in [
            "Infineon AURIX TC234LP",
            "UDS 리프로그래밍",
            "Backup·Restore",
            "SHA-256",
            "Trace32",
            "4바이트 정렬",
            "정적 코드 리뷰",
            "현재 ECU에서 재시험하지 않음",
        ]:
            self.assertIn(content, self.html)

    def test_project_detail_script_updates_accessibility_state(self):
        self.assertIn("aria-expanded", self.html)
        self.assertIn("상세 내용 접기", self.html)
        self.assertIn("detail.hidden", self.html)
        self.assertIn("button.textContent", self.html)
```

- [ ] **Step 2: Run the focused test file and verify failure**

Run:

```bash
python -m unittest tests/test_portfolio.py -v
```

Expected: failures for missing OTA content, missing detail controls, and the still-present private Black Box project link.

- [ ] **Step 3: Commit the failing requirements**

```bash
git add tests/test_portfolio.py
git commit -m "test: define project detail portfolio requirements"
```

---

### Task 2: Add in-card project details and OTA Bootloader project

**Files:**
- Modify: `index.html`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: Existing `.project-card`, `.project-header`, `.project-metrics`, `.project-details`, `.project-footer`, and responsive breakpoints
- Produces: Two independent controls targeting `#black-box-details` and `#bootloader-details`

- [ ] **Step 1: Add reusable detail styles to the existing `<style>` block**

Insert these rules after `.project-footer` and before `.tag-list`:

```css
.projects-stack {
  display: grid;
  gap: 28px;
}
.project-detail-toggle {
  padding: 0;
  border: 0;
  color: var(--blue);
  background: transparent;
  font-weight: 850;
  cursor: pointer;
  white-space: nowrap;
}
.project-detail-toggle::after {
  content: " +";
}
.project-detail-toggle[aria-expanded="true"]::after {
  content: " −";
}
.project-detail-region {
  border-top: 1px solid var(--line);
  background: var(--surface-soft);
}
.project-detail-region[hidden] {
  display: none;
}
.project-detail-inner {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  padding: 26px 30px 30px;
}
.detail-block {
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 9px;
  background: #fff;
}
.detail-block.wide {
  grid-column: 1 / -1;
}
.detail-block h4 {
  margin: 0 0 8px;
  color: var(--navy);
  font-size: 15px;
}
.detail-block p,
.detail-block ul {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
}
.detail-block ul {
  padding-left: 18px;
}
.flow-line {
  color: #31425a;
  font-size: 13px;
  font-weight: 750;
  line-height: 1.9;
}
.project-note {
  color: var(--muted);
  font-size: 12px;
}
```

Extend the existing `@media(max-width:900px)` block with:

```css
.project-detail-inner { grid-template-columns: 1fr; }
.detail-block.wide { grid-column: auto; }
```

Extend the existing `@media(max-width:600px)` block with:

```css
.project-detail-inner { padding-left: 21px; padding-right: 21px; }
```

- [ ] **Step 2: Wrap project cards in a vertical stack**

Change the projects section body from a single direct `.project-card` to:

```html
<div class="projects-stack">
  <!-- Project 01 card -->
  <!-- Project 02 card -->
</div>
```

Keep the current Black Box card as the first child.

- [ ] **Step 3: Replace the Black Box private link with a detail button**

In the first card footer, retain the technology tags and replace the external repository anchor with:

```html
<button
  class="project-detail-toggle"
  type="button"
  aria-expanded="false"
  aria-controls="black-box-details"
>
  프로젝트 상세 보기
</button>
```

Immediately before the closing tag of the first `.project-card`, add:

```html
<div id="black-box-details" class="project-detail-region" hidden>
  <div class="project-detail-inner">
    <article class="detail-block wide">
      <h4>테스트 수행 흐름</h4>
      <p class="flow-line">요구사양 분석 → CANoe·CANdb·Panel 환경 구성 → 수동 시험·CAPL 자동화 시험 → 정적·동적 시험 → 결함 분석 및 개선 방향 제시</p>
    </article>
    <article class="detail-block">
      <h4>본인 수행 범위</h4>
      <ul>
        <li>CAN·UDS 요구사양과 Fault 상태 전이 조건 분석</li>
        <li>CANdb 작성 및 CANoe Network Node 구성</li>
        <li>CAPL 테스트 작성, Panel 입력 제어, Trace 분석</li>
        <li>기대 결과·실제 결과·재현 조건·영향도 문서화</li>
      </ul>
    </article>
    <article class="detail-block">
      <h4>대표 검출 결과</h4>
      <ul>
        <li>정적 결함 4건: Signal Length, Value, Description 불일치</li>
        <li>동적 결함 11건: 경계값, 선행 조건, Recovery, Timing 오류</li>
        <li>Batt Percent 15% 경계값과 IGN 50 Cycle Off-by-One 확인</li>
        <li>Steering Timing 요구사양 50±10ms 대비 약 1000±10ms 검출</li>
      </ul>
    </article>
    <article class="detail-block wide">
      <h4>QA 관점과 공개 범위</h4>
      <p>요구사양 기반 시험에서 단순 Pass/Fail을 넘어 결함 근거와 영향도를 구조화했습니다. 원본 요구사양과 내부 자료는 제외하고, 직접 수행한 테스트 환경·결함 분석·개선 방향만 포트폴리오용으로 재구성했습니다.</p>
    </article>
  </div>
</div>
```

Ensure the visible first-card summary also contains the exact phrase `요구사양 기반 시험`.

- [ ] **Step 4: Add the OTA Bootloader summary card**

Add this card after the Black Box card inside `.projects-stack`:

```html
<article class="project-card">
  <header class="project-header">
    <div>
      <p class="project-label">PROJECT 02 · EMBEDDED PLATFORM</p>
      <h3>OTA를 위한 Bootloader 설계 및 SW Binary 위변조 감지</h3>
    </div>
    <span class="project-award">개인 프로젝트</span>
  </header>
  <div class="project-intro">
    <p>Infineon AURIX TC234LP 기반 ECU에서 OTA 업데이트 실패나 Binary 변경이 발생했을 때 기존 애플리케이션을 보호하고 복구할 수 있도록 UDS 리프로그래밍과 무결성 검사 흐름을 설계했습니다.</p>
  </div>
  <div class="project-metrics" aria-label="OTA Bootloader 프로젝트 핵심 결과">
    <div class="project-metric"><strong>UDS 리프로그래밍</strong><span>0x34·0x36·0x37 다운로드 흐름</span></div>
    <div class="project-metric"><strong>Backup·Restore</strong><span>PFlash 애플리케이션 보호·복구</span></div>
    <div class="project-metric"><strong>SHA-256</strong><span>SW Binary 무결성 검사</span></div>
    <div class="project-metric"><strong>Trace32 원인 분석</strong><span>Flash Loader 정렬 Trap 분석</span></div>
  </div>
  <dl class="project-details">
    <div><dt>프로젝트 목표</dt><dd>불완전하거나 변경된 업데이트 이미지로의 부팅을 방지하고 기존 애플리케이션 복구 경로를 구성했습니다.</dd></div>
    <div><dt>담당 역할</dt><dd>메모리 경계와 UDS 절차 설계, Flash 관리, 무결성 검사, Binary 변환, 디버깅과 사후 정적 코드 리뷰를 수행했습니다.</dd></div>
    <div><dt>수행 내용</dt><dd>Programming Session과 SecurityAccess 이후 Erase·Backup, RequestDownload, TransferData, TransferExit, 무결성 확인, ECUReset을 연결했습니다.</dd></div>
    <div><dt>주요 성과</dt><dd>Trace32로 source buffer 정렬 문제를 특정하고 4바이트 정렬을 보장하는 버퍼 구조로 개선했습니다.</dd></div>
  </dl>
  <footer class="project-footer">
    <div class="tag-list"><span>C</span><span>AURIX</span><span>CAN·ISO-TP</span><span>UDS</span><span>MCAL</span><span>PFlash</span><span>SHA-256</span><span>Trace32</span></div>
    <button class="project-detail-toggle" type="button" aria-expanded="false" aria-controls="bootloader-details">프로젝트 상세 보기</button>
  </footer>
  <div id="bootloader-details" class="project-detail-region" hidden>
    <div class="project-detail-inner">
      <article class="detail-block wide">
        <h4>시스템 구조와 리프로그래밍 흐름</h4>
        <p class="flow-line">Tester → CAN·ISO-TP → BswCom → BswDcm → RTE → ECU 추상화 → MCAL → PFlash·DFlash</p>
        <p class="flow-line">Programming Session → SecurityAccess → Erase·Backup → RequestDownload(0x34) → TransferData(0x36) → RequestTransferExit(0x37) → SHA-256 확인 → ECUReset</p>
      </article>
      <article class="detail-block">
        <h4>대표 문제 해결</h4>
        <p>Backup·Restore 중 발생한 Trap을 Trace32 레지스터와 Flash Loader 인수로 추적했습니다. `uint8` 버퍼가 Flash Loader의 4바이트 정렬 조건을 보장하지 않는 것을 확인하고 `uint32` 배열 기반 버퍼로 변경했습니다.</p>
      </article>
      <article class="detail-block">
        <h4>정적 코드 리뷰</h4>
        <ul>
          <li>ISO-TP 길이·순번·버퍼 상한 검증 부족</li>
          <li>TransferData payload 및 잔여 길이 제한 부족</li>
          <li>EraseMemory 세션·SecurityAccess 선행 검사 부족</li>
          <li>해시 확인 전 valid pattern 기록 순서 문제</li>
          <li>고정 Seed/Key와 고정 키 SHA-256 방식의 한계</li>
        </ul>
      </article>
      <article class="detail-block wide">
        <h4>검증 범위와 한계</h4>
        <p>교육 당시 직접 수정한 C/H 파일과 산출물 메타데이터를 기준으로 정적 확인했습니다. 현재 ECU에서 재시험하지 않음과 TASKING·MCAL 부재로 빌드를 재현하지 못한 범위를 명확히 구분하며, 실행하지 않은 프로젝트 단계의 결과는 주장하지 않습니다.</p>
      </article>
    </div>
  </div>
</article>
```

- [ ] **Step 5: Add the independent accordion controller**

Before `</body>`, preserve the existing mobile-menu script and add:

```html
<script>
  document.querySelectorAll(".project-detail-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const detail = document.getElementById(button.getAttribute("aria-controls"));
      const willExpand = button.getAttribute("aria-expanded") !== "true";

      button.setAttribute("aria-expanded", String(willExpand));
      detail.hidden = !willExpand;
      button.textContent = willExpand ? "상세 내용 접기" : "프로젝트 상세 보기";
    });
  });
</script>
```

Each control must only modify the region named by its own `aria-controls` value.

- [ ] **Step 6: Run the full test file**

Run:

```bash
python -m unittest tests/test_portfolio.py -v
```

Expected: all tests pass.

- [ ] **Step 7: Perform manual source checks**

Run:

```bash
python - <<'PY'
from pathlib import Path
html = Path("index.html").read_text(encoding="utf-8")
assert html.count('class="project-card"') >= 2
assert html.count("프로젝트 상세 보기") == 2
assert "Bootloader_Design_For_OTA" not in html
assert "IVS-Black-Box-Testing" not in html
assert "IVS-Black-Box-Validation" not in html
print("project source checks passed")
PY
```

Expected: `project source checks passed`.

- [ ] **Step 8: Commit the project UI**

```bash
git add index.html
git commit -m "feat: add in-page project details and OTA bootloader"
```

---

### Task 3: Update repository documentation and verify the complete portfolio

**Files:**
- Modify: `README.md`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: Final two-project portfolio behavior
- Produces: Repository-level description that matches the visible site

- [ ] **Step 1: Update README project composition**

Replace the current `주요 구성` bullets with:

```markdown
## 주요 구성

- 다크 기술형 Hero와 밝은 기업형 본문을 결합한 혼합형 디자인
- 차량 SW QA 업무 방식과 핵심 역량
- CANoe/CAPL 기반 Black Box Testing 대표 프로젝트
- UDS·Flash·SHA-256 기반 OTA Bootloader 프로젝트
- Private 저장소 링크 대신 카드 내부 프로젝트 상세 보기 제공
- 교육·자격·수상 내역
- 모바일 반응형, 키보드 접근성, 독립적인 펼침/접기 제어
```

Add this section before `## 배포 주소`:

```markdown
## 프로젝트 공개 원칙

원본 요구사양, 교육 내부 자료, 외부 라이브러리 및 비공개 소스는 공개하지 않습니다. 포트폴리오 페이지에는 직접 수행한 역할, 구조, 대표 문제 해결, 검증 결과와 주장 가능한 범위만 재구성해 제공합니다.
```

- [ ] **Step 2: Run regression tests**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: all discovered tests pass.

- [ ] **Step 3: Verify repository documentation matches the site**

Run:

```bash
python - <<'PY'
from pathlib import Path
readme = Path("README.md").read_text(encoding="utf-8")
html = Path("index.html").read_text(encoding="utf-8")
for term in ["Black Box Testing", "OTA Bootloader", "프로젝트 상세 보기"]:
    assert term in readme, term
    assert term in html, term
print("documentation checks passed")
PY
```

Expected: `documentation checks passed`.

- [ ] **Step 4: Commit documentation**

```bash
git add README.md
git commit -m "docs: document two-project portfolio structure"
```

- [ ] **Step 5: Final verification before review**

Run:

```bash
python -m unittest discover -s tests -v

git diff --check main...HEAD

git status --short
```

Expected:
- all tests pass;
- `git diff --check` emits no whitespace errors;
- `git status --short` is empty.
