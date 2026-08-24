# Portfolio V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `jb-cho55/portfolio` as a Korean-first, verification-focused Vehicle Software Engineer portfolio on a clean Git root while preserving its public URL and evidence integrity.

**Architecture:** A framework-free static site lives under `site/` and is published by one gated GitHub Pages workflow. A Python standard-library audit harness verifies content contracts, internal routes, metadata, accessibility basics, and deployment configuration without adding runtime dependencies.

**Tech Stack:** Semantic HTML5, CSS, Python 3.13 `unittest` and `html.parser`, GitHub Pages Actions.

**Spec:** `docs/superpowers/specs/2026-08-24-portfolio-v2-design.md`

## Global Constraints

- Public base URL is exactly `https://jb-cho55.github.io/portfolio/`.
- Published files live only under `site/`; tests and plan documents are never uploaded.
- Project order is Black Box → CarMaker → Bootloader.
- Palette is `#f6f5f2`, `#171918`, `#686b68`, `#d7d8d3`, `#888d88`, `#ecece7`, and one accent `#2f6662`.
- No gradients, shadows, glass effects, pills, rounded card grids, hover translation, custom cursor, counters, parallax, or scroll-reveal animation.
- Do not expose private repository names, protected requirements captures, expiring Notion URLs, account data, or unredacted credentials.
- Do not expose a resume link until `site/assets/resume.pdf` exists; no resume file is in scope for this plan.
- Text files are edited with `apply_patch`; verified binary evidence assets may be copied mechanically from the legacy checkout or the named public CarMaker repository.
- Every behavior change follows RED → GREEN; every commit is preceded by the relevant test command.
- Do not push, publish, or change GitHub Pages settings during Tasks 1–4.

---

### Task 1: Standard-library site audit harness

**Files:**
- Create: `tests/site_audit.py`
- Create: `tests/test_audit_helpers.py`

**Interfaces:**
- Produces: `parse_html(path: Path) -> ParsedDocument`, `site_documents(site_root: Path) -> list[Path]`, `resolve_local_reference(site_root: Path, page: Path, reference: str) -> tuple[Path, str | None] | None`, and `heading_levels(document: ParsedDocument) -> list[int]`.
- `ParsedDocument` exposes `tags`, `ids`, `links`, `sources`, `text`, `title`, and `json_ld` collected from real HTML.

- [ ] **Step 1: Write the failing helper tests**

Create `tests/test_audit_helpers.py` with temporary real HTML files. The tests must prove: duplicate IDs are preserved for detection, query strings are ignored when resolving files, fragments are returned separately, root-relative `/portfolio/` references resolve under `site_root`, `mailto:`, `https:`, and `data:` references return `None`, and headings are returned in DOM order.

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from site_audit import heading_levels, parse_html, resolve_local_reference, site_documents


class AuditHelperTests(unittest.TestCase):
    def test_parser_preserves_duplicate_ids_and_heading_order(self):
        with TemporaryDirectory() as folder:
            page = Path(folder) / "index.html"
            page.write_text(
                '<!doctype html><html><head><title>Sample</title>'
                '<script type="application/ld+json">{"@type":"Person"}</script></head>'
                '<body><h1 id="same">A</h1><h2 id="same">B</h2><img src="x.png" alt="x"></body></html>',
                encoding="utf-8",
            )
            document = parse_html(page)
            self.assertEqual(document.ids, ["same", "same"])
            self.assertEqual(heading_levels(document), [1, 2])
            self.assertEqual(document.title, "Sample")
            self.assertEqual(document.json_ld[0]["@type"], "Person")

    def test_resolver_maps_project_root_and_fragment(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / "artifacts" / "black-box" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text("", encoding="utf-8")
            target, fragment = resolve_local_reference(
                root, page, "/portfolio/assets/a.png?v=1#result"
            )
            self.assertEqual(target, root / "assets" / "a.png")
            self.assertEqual(fragment, "result")

    def test_resolver_ignores_external_schemes(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / "index.html"
            for reference in ("mailto:a@example.com", "https://example.com", "data:image/png;base64,AA"):
                self.assertIsNone(resolve_local_reference(root, page, reference))

    def test_site_documents_returns_only_html_in_stable_order(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "b").mkdir()
            (root / "b" / "index.html").write_text("b", encoding="utf-8")
            (root / "index.html").write_text("a", encoding="utf-8")
            (root / "note.txt").write_text("x", encoding="utf-8")
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in site_documents(root)],
                ["b/index.html", "index.html"],
            )
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `python -B -m unittest tests/test_audit_helpers.py -v`

Expected: import failure because `site_audit` does not exist.

- [ ] **Step 3: Implement the audit harness**

Implement `ParsedDocument` as a dataclass and an `HTMLParser` subclass. Store start-tag attributes as dictionaries, collect text outside `script` and `style`, parse each `application/ld+json` block with `json.loads`, and raise a descriptive assertion when JSON-LD is invalid. `resolve_local_reference` must reject paths that escape `site_root` after `Path.resolve()`.

```python
@dataclass
class ParsedDocument:
    tags: list[tuple[str, dict[str, str]]]
    ids: list[str]
    links: list[str]
    sources: list[str]
    text: str
    title: str
    json_ld: list[dict]
```

- [ ] **Step 4: Run the helper tests and verify GREEN**

Run: `python -B -m unittest tests/test_audit_helpers.py -v`

Expected: 4 tests pass.

- [ ] **Step 5: Commit**

The clean-root setup commit already contains `.gitignore`, the design spec, and this plan. Stage only `tests/site_audit.py` and `tests/test_audit_helpers.py`, then commit with `test: add static site audit harness`.

---

### Task 2: Homepage and shared Engineering Editorial system

**Files:**
- Create: `tests/test_home_contract.py`
- Create: `tests/test_accessibility_contract.py`
- Create: `site/index.html`
- Create: `site/assets/css/site.css`
- Create: `site/assets/favicon.svg`
- Copy: `site/assets/images/black-box/test_environment.png`
- Copy: `site/assets/bootloader/uds-sequence.svg`
- Copy: `site/assets/images/carmaker/parking_results_6cases.png`

**Interfaces:**
- Consumes: Task 1 `parse_html` and `heading_levels`.
- Produces: shared class contracts `.site-shell`, `.editorial-grid`, `.proof-grid`, `.project-row`, `.section-index`, `.project-index`, `.project-copy`, `.project-figure`, `.claim-list`, `.evidence-grid`, `.timeline`, `.skip-link`, and `.visually-hidden` for Task 3 pages.

- [ ] **Step 1: Write the failing homepage contract tests**

The tests load the real `site/index.html` and assert:

```python
class HomeContractTests(unittest.TestCase):
    def test_positioning_and_contact_are_immediately_available(self):
        self.assertIn("차량 소프트웨어를 검증 가능한 증거로 설명합니다.", self.document.text)
        self.assertIn("CANoe/CAPL 검증 자동화와 결함 원인 분석", self.document.text)
        self.assertIn("mailto:cho.jeongbin55@gmail.com", self.document.links)
        self.assertIn("https://github.com/jb-cho55", self.document.links)
        self.assertNotIn("resume.pdf", " ".join(self.document.links))

    def test_three_flagships_are_in_priority_order(self):
        page = self.page.read_text(encoding="utf-8")
        positions = [page.index(marker) for marker in (
            'id="black-box-project"', 'id="carmaker-project"', 'id="bootloader-project"'
        )]
        self.assertEqual(positions, sorted(positions))

    def test_qualified_metrics_and_ownership_are_visible(self):
        for phrase in (
            "정적 4건 · 동적 11건", "6인 팀 최종 평가", "최대 오차 0.16 m",
            "7개 UDS 서비스", "개인 프로젝트", "팀장 · 주차 경로계획",
        ):
            self.assertIn(phrase, self.document.text)
```

Accessibility tests assert one main, one h1, a working skip link, unique IDs, heading levels that never jump by more than one, non-empty alt text, width and height on rasters, and `rel="noreferrer"` on `_blank` links.

- [ ] **Step 2: Run Task 2 tests and verify RED**

Run: `python -B -m unittest tests/test_home_contract.py tests/test_accessibility_contract.py -v`

Expected: failure because `site/index.html` does not exist.

- [ ] **Step 3: Copy only verified binary assets**

Copy Black Box and Bootloader assets from the exact legacy paths named in the spec. Fetch the CarMaker PNG from `https://raw.githubusercontent.com/jb-cho55/IVS-CarMaker-ADAS/main/docs/media/parking_results_6cases.png`. Verify it is a PNG larger than 90,000 bytes before staging it.

- [ ] **Step 4: Implement the shared stylesheet and homepage**

Use the exact visual tokens from the spec. The DOM order for every project is index → copy and detail link → figure. The homepage uses exactly one h1 and the IA in the spec. Add authentic captions including personal-contribution boundaries. Do not introduce JavaScript, a resume link, certificate thumbnails, or placeholder figures.

The CSS must include the 1120 px and 720 px layout transitions, 320 px overflow protection, `:focus-visible`, `prefers-reduced-motion`, `prefers-contrast`, 44 px touch targets, `scroll-margin-top`, and targeted `overflow-wrap:anywhere` for technical identifiers.

- [ ] **Step 5: Run Task 2 tests and the complete suite**

Run: `python -B -m unittest tests/test_home_contract.py tests/test_accessibility_contract.py -v`

Then: `python -B -m unittest discover -s tests -v`

Expected: all tests pass.

- [ ] **Step 6: Commit**

Stage only Task 2 paths and commit with `feat: build evidence-led portfolio homepage`.

---

### Task 3: Three complete engineering case studies

**Files:**
- Create: `tests/test_case_studies.py`
- Create: `tests/test_routes_and_links.py`
- Create: `site/artifacts/black-box/index.html`
- Create: `site/artifacts/carmaker/index.html`
- Create: `site/artifacts/bootloader/index.html`
- Copy: `site/assets/images/black-box/*.png`
- Copy: `site/assets/images/bootloader/*.png`
- Copy: `site/assets/bootloader/memory-map.svg`
- Copy: `site/assets/evidence/black_box_award.pdf`
- Copy: `site/assets/images/carmaker/architecture.png`
- Copy: `site/assets/images/carmaker/parking_hybrid_astar_path.png`
- Copy: `site/assets/images/carmaker/sl_parking.png`

**Interfaces:**
- Consumes: Task 1 audit helpers and Task 2 CSS class contracts.
- Produces: four internally crawlable pages with valid fragments and no missing local asset references.

- [ ] **Step 1: Write failing case-study and route tests**

For each page, assert the exact scope and limitations in the spec. The Black Box page must include `#overview`, `#code`, `#test`, `#document`, and `#demo`; Bootloader must include `#overview`, `#memory-map`, `#uds`, `#test`, and `#trace32`. CarMaker must include `#overview`, `#architecture`, `#parking`, `#validation`, `#personal`, and `#collaboration`.

The route crawler must resolve every local `href`, `src`, and fragment using Task 1, fail on any missing file or fragment, and test the legacy home fragments `#black-box-project` and `#bootloader-project`.

Required literal checks include:

```python
required = {
    "black-box": ["7개 고장 시나리오", "CAPL 스크립트 6종", "테스트케이스 24개", "정적 결함 4건", "동적 결함 11건", "캡처가 없는 1건"],
    "carmaker": ["6인 팀", "14/19 PASS", "51.6 m → 0.02 m", "최대 오차 0.16 m", "페어 프로그래밍", "N≥8"],
    "bootloader": ["0x10", "0x27", "0x31", "0x34", "0x36", "0x37", "0x11", "PASS 7", "Evidence unavailable 2", "Not executed 1", "0x7000240D", "HMAC", "전자서명"],
}
```

- [ ] **Step 2: Run Task 3 tests and verify RED**

Run: `python -B -m unittest tests/test_case_studies.py tests/test_routes_and_links.py -v`

Expected: failures because all three detail pages are absent.

- [ ] **Step 3: Copy verified evidence assets**

Copy the named legacy assets without altering their contents. Fetch the three named CarMaker PNGs from the public repository and verify each PNG signature and a file size greater than 90,000 bytes. Do not add the 5 MB demo video in this rebuild.

- [ ] **Step 4: Implement the case-study pages**

Each page follows Context and constraints → problem → personal role → decision → implementation → validation → result → limitation → source links. Reuse the shared stylesheet and consistent site header/footer. Black Box and Bootloader preserve the verified legacy evidence depth; CarMaker distinguishes team result from personal implementation in separate, labeled sections.

- [ ] **Step 5: Run Task 3 tests and the complete suite**

Run: `python -B -m unittest tests/test_case_studies.py tests/test_routes_and_links.py -v`

Then: `python -B -m unittest discover -s tests -v`

Expected: all tests pass with no broken internal link or fragment.

- [ ] **Step 6: Commit**

Stage only Task 3 paths and commit with `feat: add three evidence-rich case studies`.

---

### Task 4: Metadata, discovery, deployment, and handoff documentation

**Files:**
- Create: `tests/test_metadata_and_deployment.py`
- Modify: `site/index.html`
- Modify: `site/artifacts/black-box/index.html`
- Modify: `site/artifacts/carmaker/index.html`
- Modify: `site/artifacts/bootloader/index.html`
- Create: `site/404.html`
- Create: `site/robots.txt`
- Create: `site/sitemap.xml`
- Create: `site/.nojekyll`
- Create: `site/assets/og-card.svg`
- Create: `site/assets/og-card.png`
- Create: `.github/workflows/pages.yml`
- Create: `README.md`

**Interfaces:**
- Consumes: all pages and audit helpers.
- Produces: a test-gated Pages artifact containing only `site/`.

- [ ] **Step 1: Write failing metadata and deployment tests**

Tests require unique title and description, canonical, matching `og:url`, absolute OG image, valid JSON-LD, four sitemap URLs matching the four canonicals, and a 1200 by 630 PNG. Home JSON-LD must be `Person`; each case page must be `TechArticle` whose author is a `Person` named `조정빈`.

Workflow tests require the current verified action majors, `needs: test`, `path: site/`, and deploy only on `refs/heads/main`. The workflow must grant only `contents: read` globally and `pages: write`, `id-token: write` to the deploy job.

- [ ] **Step 2: Run Task 4 tests and verify RED**

Run: `python -B -m unittest tests/test_metadata_and_deployment.py -v`

Expected: failures for missing canonical, JSON-LD, sitemap, OG card, and workflow.

- [ ] **Step 3: Implement metadata and discovery files**

Use these canonical URLs exactly:

```text
https://jb-cho55.github.io/portfolio/
https://jb-cho55.github.io/portfolio/artifacts/black-box/
https://jb-cho55.github.io/portfolio/artifacts/carmaker/
https://jb-cho55.github.io/portfolio/artifacts/bootloader/
```

Create a neutral OG card from a 1200 by 630 SVG using the approved palette and render it to PNG without adding an image-generation dependency. The 404 page links to `/portfolio/` and uses the shared CSS.

- [ ] **Step 4: Implement the Pages workflow and README**

The test job uses `actions/checkout@v7`, `actions/setup-python@v6`, and `python -B -m unittest discover -s tests -v`. The deploy job uses `actions/configure-pages@v6`, `actions/upload-pages-artifact@v5`, and `actions/deploy-pages@v5`; it depends on test and runs only for a main-branch push. README documents local serving from `site/`, the test command, clean-history backup location, content provenance, and publication procedure.

- [ ] **Step 5: Run all automated verification**

Run: `python -B -m unittest discover -s tests -v`

Then serve with: `python -m http.server 8000 --directory site`

Expected: all tests pass and the server returns 200 for all four routes.

- [ ] **Step 6: Commit**

Stage only Task 4 paths and commit with `feat: add metadata and gated pages deployment`.

---

### Task 5: Browser visual QA and release gate

**Files:**
- Modify only files implicated by verified browser defects.
- Create: `docs/verification/2026-08-24-portfolio-v2.md`

**Interfaces:**
- Consumes: completed site from Tasks 1–4.
- Produces: a verification record and a release candidate; it does not publish.

- [ ] **Step 1: Start the real site and inspect five viewports**

Run `python -m http.server 8000 --directory site` and inspect home plus all case pages at 1440×900, 1024×768, 768×1024, 390×844, and 320×568. Check 200% zoom, keyboard-only navigation, skip link, focus visibility, no horizontal page scroll, readable code/table wrappers, and image aspect ratios.

- [ ] **Step 2: Add a failing regression test for every functional defect**

For broken links, missing accessible names, wrong metadata, or invalid fragments, add the smallest failing unittest before changing production. Purely visual CSS corrections are recorded with before/after viewport evidence and rechecked at the same viewport.

- [ ] **Step 3: Fix only observed defects and rerun verification**

Run the relevant focused test after each fix, then run `python -B -m unittest discover -s tests -v` once all viewports are clean.

- [ ] **Step 4: Write the verification record**

Record commands, test count, five viewport results, known limitations, backup bundle path and SHA-256 `F9BFDA1B29213338A25D4E067B7CD13458340E7689A953B6D02EFB49944077B0`, old remote main `661b9d5186028318a1f181f4f7b0e8a822f1da63`, and state explicitly that no remote push occurred during Tasks 1–5.

- [ ] **Step 5: Commit**

Stage only verified Task 5 paths and commit with `docs: record portfolio v2 verification`.

- [ ] **Step 6: Final branch review**

Review the entire clean-root branch against the design spec and verify the Git tree contains only intended files. The publication command remains outside this task and requires the release gate in the controlling session.
