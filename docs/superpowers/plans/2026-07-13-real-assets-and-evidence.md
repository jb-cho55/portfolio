# Real Project Assets and Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace reconstructed project visuals with actual Black Box Testing screenshots and add five original PDF credentials with clickable thumbnails.

**Architecture:** Keep the single-page static site. Store project screenshots under `assets/images/black-box/`, original PDFs under `assets/evidence/`, and rendered first-page thumbnails under `assets/evidence/thumbnails/`. The portfolio references only local assets, opens original PDFs in a new tab, and preserves the existing project accordion and responsive layout.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Python `unittest`, PNG, PDF, GitHub Pages.

## Global Constraints

- Keep both project repository URLs private and absent from rendered HTML.
- Use actual Black Box Testing screenshots from the user's private repository or Notion project notes; do not use reconstructed SVG diagrams.
- Upload the five original PDFs without redaction or modification.
- Open evidence PDFs with `target="_blank"` and `rel="noreferrer"`.
- Keep the current corporate navy/blue visual system and the 900px responsive breakpoint.
- Do not add a framework, routing, iframe PDF viewer, or external image host.

---

### Task 1: Add Real Binary Assets

**Files:**
- Create: `assets/images/black-box/network_setup.png`
- Create: `assets/images/black-box/test_environment.png`
- Create: `assets/images/black-box/automation_test_environment.png`
- Create: `assets/images/black-box/panel_trace.png`
- Create: `assets/images/black-box/defect_batt_percent_15.png`
- Create: `assets/evidence/ivs_completion.pdf`
- Create: `assets/evidence/black_box_award.pdf`
- Create: `assets/evidence/exemplary_award.pdf`
- Create: `assets/evidence/information_processing_engineer.pdf`
- Create: `assets/evidence/istqb_ctfl.pdf`
- Create: `assets/evidence/thumbnails/ivs_completion.png`
- Create: `assets/evidence/thumbnails/black_box_award.png`
- Create: `assets/evidence/thumbnails/exemplary_award.png`
- Create: `assets/evidence/thumbnails/information_processing_engineer.png`
- Create: `assets/evidence/thumbnails/istqb_ctfl.png`
- Delete: `assets/images/network_setup.svg`
- Delete: `assets/images/automation_test_environment.svg`
- Delete: `assets/images/panel_trace.svg`
- Delete: `assets/images/defect_batt_percent_15.svg`

**Interfaces:**
- Consumes: Actual project screenshots and the five uploaded source PDFs.
- Produces: Stable relative asset paths used by `index.html` and tests.

- [ ] **Step 1: Render PDF thumbnails**

Run:

```bash
python /home/oai/skills/pdfs/scripts/render_pdf.py "/mnt/data/HL만도 & HL 클레무브 IVS 5기_수료증(1).pdf" --out_dir /mnt/data/evidence_render/ivs --dpi 150
python /home/oai/skills/pdfs/scripts/render_pdf.py "/mnt/data/BlackBoxTesting우수상(1).pdf" --out_dir /mnt/data/evidence_render/black_box --dpi 150
python /home/oai/skills/pdfs/scripts/render_pdf.py "/mnt/data/모범상(1).pdf" --out_dir /mnt/data/evidence_render/exemplary --dpi 150
python /home/oai/skills/pdfs/scripts/render_pdf.py "/mnt/data/정보처리기사.pdf" --out_dir /mnt/data/evidence_render/engineer --dpi 150
python /home/oai/skills/pdfs/scripts/render_pdf.py "/mnt/data/ISTQB 자격증.pdf" --out_dir /mnt/data/evidence_render/istqb --dpi 150
```

Expected: one readable PNG per PDF, with no clipping or black glyph boxes.

- [ ] **Step 2: Inspect all generated thumbnails**

Open each PNG and confirm the page is upright, complete, and readable. Keep the full page; do not crop or redact.

- [ ] **Step 3: Add binary assets to the feature branch**

Create Git blobs from the exact PDF and PNG bytes, create a tree based on the branch head, create one commit, and fast-forward `feat/real-assets-and-evidence` to that commit.

- [ ] **Step 4: Verify file integrity**

Confirm every PDF begins with `%PDF-` and every PNG begins with the PNG signature `89 50 4E 47 0D 0A 1A 0A`.

---

### Task 2: Define Failing Content Tests

**Files:**
- Modify: `tests/test_portfolio.py`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: Stable paths from Task 1.
- Produces: Regression requirements for actual screenshots and PDF evidence links.

- [ ] **Step 1: Replace SVG expectations with PNG expectations**

Add assertions for these exact paths:

```python
actual_images = [
    "assets/images/black-box/network_setup.png",
    "assets/images/black-box/test_environment.png",
    "assets/images/black-box/automation_test_environment.png",
    "assets/images/black-box/panel_trace.png",
    "assets/images/black-box/defect_batt_percent_15.png",
]
for path in actual_images:
    self.assertIn(f'src="{path}"', self.html)
self.assertNotIn("assets/images/network_setup.svg", self.html)
self.assertNotIn("포트폴리오 재구성", self.html)
```

- [ ] **Step 2: Add credential evidence assertions**

Add assertions for these exact pairs:

```python
evidence = {
    "HL만도·HL클레무브 IVS 5기 수료증": "assets/evidence/ivs_completion.pdf",
    "Black Box Testing 프로젝트 우수상": "assets/evidence/black_box_award.pdf",
    "IVS 5기 모범상": "assets/evidence/exemplary_award.pdf",
    "정보처리기사": "assets/evidence/information_processing_engineer.pdf",
    "ISTQB CTFL": "assets/evidence/istqb_ctfl.pdf",
}
for label, path in evidence.items():
    self.assertIn(label, self.html)
    self.assertIn(f'href="{path}"', self.html)
self.assertGreaterEqual(self.html.count('target="_blank"'), 6)
self.assertGreaterEqual(self.html.count('rel="noreferrer"'), 6)
```

- [ ] **Step 3: Add thumbnail accessibility assertions**

Require five `.evidence-card` elements, five evidence thumbnails, descriptive `alt` values, and visible `원본 PDF 보기` labels.

- [ ] **Step 4: Run tests and confirm failure**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: failures for missing PNG paths, missing PDF links, and missing evidence cards.

- [ ] **Step 5: Commit failing tests**

```bash
git add tests/test_portfolio.py
git commit -m "test: require real project assets and credential evidence"
```

---

### Task 3: Update the Portfolio UI

**Files:**
- Modify: `index.html`
- Modify: `README.md`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: Asset paths and regression tests from Tasks 1-2.
- Produces: User-visible project gallery and credential evidence section.

- [ ] **Step 1: Replace the project gallery markup**

Use five local PNG images. Each image is wrapped in a link to the same image so it opens at full resolution in a new tab:

```html
<a class="evidence-item" href="assets/images/black-box/network_setup.png" target="_blank" rel="noreferrer">
  <img src="assets/images/black-box/network_setup.png" alt="CANoe에서 IVS와 주변 ECU Network Node를 구성한 실제 프로젝트 화면" loading="lazy">
  <span class="evidence-caption">CANoe Network 구성</span>
</a>
```

Apply the same structure to Test Environment, CAPL Automation, Panel and Trace, and Batt Percent 15% Test Result.

- [ ] **Step 2: Add credential evidence cards**

Under the existing credentials section, add a `credential-evidence-grid` containing five cards. Each card includes:

```html
<a class="credential-evidence-card" href="assets/evidence/ivs_completion.pdf" target="_blank" rel="noreferrer">
  <img src="assets/evidence/thumbnails/ivs_completion.png" alt="HL만도·HL클레무브 IVS 5기 수료증 원본 PDF 첫 페이지" loading="lazy">
  <span class="credential-evidence-copy">
    <strong>HL만도·HL클레무브 IVS 5기 수료증</strong>
    <small>원본 PDF 보기</small>
  </span>
</a>
```

Repeat for the Black Box Testing award, exemplary award, Information Processing Engineer certificate, and ISTQB CTFL certificate.

- [ ] **Step 3: Add focused CSS**

Add styles for `.credential-evidence-grid`, `.credential-evidence-card`, `.credential-evidence-card img`, and `.credential-evidence-copy`. Use a three-column desktop grid, two columns below 900px, and one column below 620px. Preserve visible keyboard focus.

- [ ] **Step 4: Remove reconstruction wording**

Delete all `포트폴리오 재구성` captions and any text that implies the images are diagrams rather than actual project screenshots.

- [ ] **Step 5: Update README**

Document that the site now contains actual Black Box Testing screenshots and five original PDF credentials that open from thumbnail cards.

- [ ] **Step 6: Run the full test suite**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 7: Inspect the rendered site**

Open the page at desktop and mobile widths. Verify project images are not stretched, credential thumbnails preserve full-page aspect ratio, all links open the intended local PDF or PNG, and accordion controls still work.

- [ ] **Step 8: Commit UI and documentation**

```bash
git add index.html README.md
git commit -m "feat: add real project screenshots and credential evidence"
```

---

### Task 4: Final Verification and Pull Request

**Files:**
- Verify: `index.html`
- Verify: `tests/test_portfolio.py`
- Verify: all files under `assets/images/black-box/` and `assets/evidence/`

**Interfaces:**
- Consumes: Completed implementation.
- Produces: Reviewable branch and updated draft pull request.

- [ ] **Step 1: Verify exact file inventory**

Confirm the branch contains five Black Box PNGs, five PDFs, five thumbnail PNGs, and no reconstructed SVG files.

- [ ] **Step 2: Re-run tests from a clean checkout**

Run `python -m unittest discover -s tests -v` and record the passing count.

- [ ] **Step 3: Review branch diff**

Confirm no private project repository URL or source file path was introduced.

- [ ] **Step 4: Update the draft PR**

Summarize actual screenshots, original PDF evidence, privacy implications of public files, test results, and preview instructions. Keep the PR in Draft until the user approves the final preview.
