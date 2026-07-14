# Vehicle Embedded SW Positioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition the portfolio as a Vehicle Embedded SW Engineer portfolio while preserving its existing design and evidence structure.

**Architecture:** Update copy only in the single-page `index.html` and keep all CSS classes, layout, JavaScript behavior, links, and project sections intact. Extend the existing Python content tests so the new hero positioning and four balanced competency cards are enforced.

**Tech Stack:** HTML, CSS, JavaScript, Python `unittest`, GitHub Pages

## Global Constraints

- Preserve the existing HTML structure and responsive design.
- Preserve project ordering, evidence links, accessibility attributes, and private repository protections.
- Use the exact copy approved in `docs/superpowers/specs/2026-07-14-vehicle-embedded-sw-positioning-design.md`.
- Do not add dependencies.

---

### Task 1: Update positioning and competency content

**Files:**
- Modify: `index.html`
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: Existing `.hero`, `.section-heading`, `.fit-grid`, and `.fit-card` markup.
- Produces: Vehicle Embedded SW metadata, hero copy, and four balanced competency cards validated by Python tests.

- [ ] **Step 1: Update the tests for the new hero and competency copy**

Replace the old hero sentence assertion and add assertions for:

```python
self.assertIn("Vehicle Embedded SW Portfolio", self.html)
self.assertIn("Vehicle Embedded SW Engineer", self.html)
self.assertIn(
    "국민대학교 자동차IT융합학과에서 자동차·전자·소프트웨어를 학습하고, AURIX 기반 Embedded SW 구현과 CANoe/CAPL 기반 차량 SW 검증을 수행했습니다.",
    self.html,
)

for competency in [
    "EMBEDDED IMPLEMENTATION",
    "Embedded C 기반 ECU 기능 구현",
    "VEHICLE COMMUNICATION",
    "차량 통신 및 진단 프로토콜 활용",
    "TEST ENGINEERING",
    "요구사양 기반 테스트 설계·자동화",
    "DEBUGGING & ANALYSIS",
    "디버깅 및 결함 원인 분석",
]:
    self.assertIn(competency, self.html)
```

Also assert that `Embedded SW QA Portfolio` and `Embedded SW QA Engineer` are absent.

- [ ] **Step 2: Run the tests to verify the old content fails**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: The updated positioning test fails because `index.html` still contains the old QA-only copy.

- [ ] **Step 3: Update `index.html` with the approved content**

Change the metadata, page title, hero eyebrow, hero role title, hero introduction, competency section introduction, and four competency cards exactly as specified in the design document. Do not modify CSS classes or element hierarchy.

- [ ] **Step 4: Run the complete test suite**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: All tests pass.

- [ ] **Step 5: Review the final diff**

Confirm that the final diff contains only:

```text
index.html
 tests/test_portfolio.py
 docs/superpowers/specs/2026-07-14-vehicle-embedded-sw-positioning-design.md
 docs/superpowers/plans/2026-07-14-vehicle-embedded-sw-positioning.md
```

Confirm no private repository URL, project evidence path, CSS rule, or JavaScript behavior changed.
