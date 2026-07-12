# Corporate Portfolio Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current personal-branding landing page with a concise corporate-submission portfolio for an Embedded SW QA Engineer application.

**Architecture:** Keep the site dependency-free and static. Use one `index.html` with semantic sections and embedded CSS so GitHub Pages can deploy without a build step. Validate required content and responsive behavior with a small Python test script.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript only where necessary, Python 3 structural tests, GitHub Pages.

## Global Constraints

- The first screen must show `국민대학교 자동차IT융합학과 졸업`, `ISTQB CTFL`, and `Black Box Testing 프로젝트 우수상`.
- `812시간` must appear in the education section, not as a hero metric.
- The hero copy must use `직접 수행했습니다`, not `분석해 왔습니다`.
- The featured project must include goal, role, execution, and result.
- The page must remain responsive below 900px.
- No framework, package manager, animation library, external font, or build process.

---

### Task 1: Add structural acceptance tests

**Files:**
- Create: `tests/test_portfolio.py`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: `index.html`
- Produces: a `unittest` suite that validates required corporate-portfolio content

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


class PortfolioContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = Path("index.html").read_text(encoding="utf-8")

    def test_hero_contains_corporate_summary(self):
        self.assertIn("국민대학교 자동차IT융합학과 졸업", self.html)
        self.assertIn("ISTQB CTFL", self.html)
        self.assertIn("Black Box Testing 프로젝트 우수상", self.html)
        self.assertIn("직접 수행했습니다", self.html)
        self.assertNotIn("분석해 왔습니다", self.html)

    def test_education_contains_ivs_hours(self):
        self.assertIn('id="education"', self.html)
        self.assertIn("812시간", self.html)

    def test_project_contains_required_fields(self):
        for label in ["프로젝트 목표", "담당 역할", "수행 내용", "주요 성과"]:
            self.assertIn(label, self.html)

    def test_links_and_responsive_layout_exist(self):
        self.assertIn("https://github.com/jb-cho55", self.html)
        self.assertIn("https://github.com/jb-cho55/IVS-Black-Box-Validation", self.html)
        self.assertIn("@media(max-width:900px)", self.html.replace(" ", ""))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_portfolio.py -v`

Expected: FAIL because the current page does not contain the approved corporate summary and may be empty.

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/test_portfolio.py
git commit -m "test: define corporate portfolio requirements"
```

### Task 2: Replace the page with the Executive Brief layout

**Files:**
- Modify: `index.html`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: content requirements from Task 1
- Produces: a dependency-free corporate portfolio page deployable from the repository root

- [ ] **Step 1: Implement the semantic page structure**

Create these sections in order:

```html
<header>...</header>
<main>
  <section id="hero">...</section>
  <section id="core-fit">...</section>
  <section id="projects">...</section>
  <section id="education">...</section>
  <section id="credentials">...</section>
</main>
<footer>...</footer>
```

Use this exact hero copy:

```html
<p class="hero-copy">
  국민대학교 자동차IT융합학과에서 자동차·전자·소프트웨어 융합 지식을 쌓고,
  CANoe/CAPL 기반 차량 SW 테스트 설계와 자동화 검증을 직접 수행했습니다.
</p>
```

Use these exact summary items:

```html
<li><strong>국민대학교</strong><span>자동차IT융합학과 졸업</span></li>
<li><strong>ISTQB CTFL</strong><span>SW Testing Foundation Level</span></li>
<li><strong>프로젝트 우수상</strong><span>Black Box Testing 자동화 검증</span></li>
```

- [ ] **Step 2: Implement the four Core Fit items**

```html
<article><h3>Test Design</h3><p>요구사항을 전제조건·입력·기대결과·판정 기준으로 구체화했습니다.</p></article>
<article><h3>Test Automation</h3><p>CANoe/CAPL로 반복 테스트를 자동화하고 동일 조건의 회귀 검증을 수행했습니다.</p></article>
<article><h3>Defect Analysis</h3><p>CAN Trace와 Signal 상태를 비교해 결함 발생 조건과 원인을 좁혔습니다.</p></article>
<article><h3>Embedded SW Understanding</h3><p>CAN·UDS·AUTOSAR·A-SPICE를 기반으로 차량 SW 구조와 검증 흐름을 학습했습니다.</p></article>
```

- [ ] **Step 3: Implement the featured project card**

Use the following field labels and content:

```html
<dt>프로젝트 목표</dt>
<dd>차량 ECU의 Fault Detection·Recovery·Clear 요구사항을 정량 기준으로 검증</dd>
<dt>담당 역할</dt>
<dd>테스트 케이스 설계, CANdb 구성, CANoe 환경 설정, CAPL 자동화, 결함 분석 및 문서화</dd>
<dt>수행 내용</dt>
<dd>요구사항을 테스트 조건과 판정 기준으로 전환하고 정적·동적 검증 결과를 비교</dd>
<dt>주요 성과</dt>
<dd>정적 결함 4건과 동적 동작 결함을 검출하고 프로젝트 우수상 수상</dd>
```

- [ ] **Step 4: Implement education and credentials**

```html
<section id="education">
  <h2>교육사항</h2>
  <article>
    <h3>HL만도·HL클레무브 Intelligent Vehicle School 5기</h3>
    <p>2025.12–2026.06 · 812시간</p>
  </article>
  <article>
    <h3>A-SPICE 단과과정 및 취업특강</h3>
    <p>2025.12–2026.01 · 14시간</p>
  </article>
</section>
```

Credentials must include `ISTQB CTFL`, `정보처리기사`, `Black Box Testing 프로젝트 우수상`, and `IVS 5기 모범상 · 부반장`.

- [ ] **Step 5: Add corporate visual styling**

Use white section backgrounds, a navy hero/header, one blue accent, minimal shadows, `max-width: 1120px`, and a single-column layout at `max-width: 900px`. Remove decorative vehicle orbit graphics and fake signal charts.

- [ ] **Step 6: Run the acceptance tests**

Run: `python -m unittest tests/test_portfolio.py -v`

Expected: `Ran 4 tests ... OK`.

- [ ] **Step 7: Commit the redesign**

```bash
git add index.html
git commit -m "feat: redesign portfolio for corporate submission"
```

### Task 3: Perform deployment verification

**Files:**
- Verify: `index.html`
- Verify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: final page from Task 2
- Produces: verified GitHub Pages source on `main`

- [ ] **Step 1: Run all tests again**

Run: `python -m unittest discover -s tests -v`

Expected: `Ran 4 tests ... OK`.

- [ ] **Step 2: Check the HTML for empty or truncated content**

Run:

```bash
python - <<'PY'
from pathlib import Path
p = Path("index.html")
text = p.read_text(encoding="utf-8")
assert p.stat().st_size > 5000
assert text.strip().endswith("</html>")
print(p.stat().st_size, "bytes; HTML complete")
PY
```

Expected: a byte count above 5000 and `HTML complete`.

- [ ] **Step 3: Push the verified changes to `main`**

```bash
git push origin main
```

- [ ] **Step 4: Confirm the public page**

Open `https://jb-cho55.github.io/portfolio/` and verify the hero, project card, education section, GitHub links, and mobile layout.
