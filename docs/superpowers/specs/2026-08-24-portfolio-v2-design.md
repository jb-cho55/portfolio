# Portfolio V2 Design Specification

## Objective

Rebuild `jb-cho55/portfolio` as a Korean-first, evidence-led portfolio for a verification-focused Vehicle Software Engineer while preserving the public URL `https://jb-cho55.github.io/portfolio/`.

## Source of truth

- Legacy content and evidence: `C:\Users\gmkk6\Documents\포트폴리오\portfolio-legacy`
- Full Git history backup: `C:\Users\gmkk6\Documents\포트폴리오\portfolio-history-backup-2026-08-24.bundle`
- Public CarMaker evidence: `https://github.com/jb-cho55/IVS-CarMaker-ADAS`
- Approved design direction: Engineering Editorial, warm neutral palette, one muted teal accent, numbered rails, ruled project rows, authentic project figures.

## Architecture

- Framework-free static HTML and CSS.
- Deployment source is `site/`; tests and planning documents are not published.
- One shared stylesheet: `site/assets/css/site.css`.
- No required client-side JavaScript. Primary navigation remains visible at every viewport.
- Detail routes remain compatible with the existing site:
  - `/portfolio/artifacts/black-box/`
  - `/portfolio/artifacts/bootloader/`
- Add `/portfolio/artifacts/carmaker/`.
- Preserve legacy home fragments `#black-box-project` and `#bootloader-project`.

## Positioning and homepage order

1. Header: `조정빈`, `Vehicle Software Engineer`, Work / Experience / Contact.
2. Hero:
   - Eyebrow: `VERIFICATION-FOCUSED VEHICLE SW ENGINEER`
   - H1: `차량 소프트웨어를 검증 가능한 증거로 설명합니다.`
   - Description: `임베디드 SW 개발 이해를 바탕으로 CANoe/CAPL 검증 자동화와 결함 원인 분석을 수행합니다. 요구사항을 테스트 가능한 기준으로 바꾸고, 결과와 한계를 재현 가능한 자료로 남깁니다.`
   - Links: selected work, email, GitHub. Do not show a resume link because no verified `resume.pdf` exists.
3. Proof at a glance:
   - `15` defects identified in the individual Black Box project: static 4 + dynamic 11.
   - `0.16 m` maximum parking error across six final team-evaluation scenarios.
   - `7` UDS service SIDs implemented in the individual educational Bootloader project.
4. Selected work: Black Box → CarMaker → Bootloader.
5. Evidence discipline: Measured / Demonstrated / Limitation.
6. Compact experience: verification automation, embedded foundation, system integration; education and credentials as text rather than a card wall.
7. Contact.

## Flagship case contracts

### 01 Black Box Validation

- Individual project, 2026.03.19–2026.03.23, contribution 100%.
- Seven fault scenarios, six CAPL scripts, 24 test cases.
- Identified and documented four static and eleven dynamic defects; do not claim to have fixed all fifteen.
- Ten of eleven dynamic defects have published CAPL result captures; one is documented without a capture.
- Personal ownership: requirements analysis, test design, CANdb/CANoe environment, CAPL automation, Trace analysis, defect documentation.
- Show the Fresh Frame timing correction and the 1 ms timer start only after a new reference frame.
- Disclose that the source repository and requirements captures are withheld to protect training material.
- Homepage figure: `assets/images/black-box/test_environment.png`.

### 02 CarMaker ADAS

- Six-person team project, 2026.05.21–2026.06.05; role: team lead and parking path planning.
- Personal responsibility: Hybrid A*, staging strategy, Reeds-Shepp precision alignment; parking work was pair-developed with the parking-control teammate.
- Team evaluation: baseline 14/19 PASS; T05 51.6 m to 0.02 m, T10 20.3 m to 0.02 m, T14 3.5 m to 0.04 m; final six evaluation cases PASS with 0.16 m maximum error.
- Never rewrite those scopes as 19/19 PASS or as a solo result.
- Keep the separate personal implementation in its own section: eleven personal commits, nine MATLAB modules, N at least 8 repeated experiments, parking-entry reach rate 0% to 100%.
- Link the public repository, collaboration record, parking progress log, and campaign summary.
- Homepage figure: locally copied `assets/images/carmaker/parking_results_6cases.png` with team-result and personal-role provenance in the caption.

### 03 OTA Bootloader

- Individual educational project, 2026.03.03–2026.03.24, contribution 100%.
- Provided AURIX TC234LP and MCAL training environment.
- Seven service SIDs: 0x10, 0x27, 0x31, 0x34, 0x36, 0x37, 0x11. The flow contains eight steps because 0x31 appears in two routines.
- Primary-to-backup copy and restore-to-primary failure path.
- Trace32 evidence: `copyBuf`, `A5`, and `DEADD` converge on `0x7000240D`; fix uses a `uint32` backing array for four-byte alignment.
- Public test status: PASS 7, Evidence unavailable 2, Not executed 1.
- State that fixed-prefix SHA-256 is not HMAC or a digital signature and cannot prevent a recomputation attack.
- State that current TASKING, EB tresos, and target ECU are unavailable, so the new build and hardware re-test were not performed.
- Preserve the unresolved static-review findings rather than presenting a production-ready secure bootloader.
- Homepage figure: `assets/bootloader/uds-sequence.svg`.

## Visual system

```css
:root {
  color-scheme: light;
  --paper: #f6f5f2;
  --ink: #171918;
  --muted: #686b68;
  --line: #d7d8d3;
  --line-strong: #888d88;
  --wash: #ecece7;
  --accent: #2f6662;
  --footer: #202321;
  --footer-ink: #f3f2ed;
  --page-max: 1280px;
  --rail: 10rem;
  --header-height: 4.5rem;
}
```

- Use Pretendard with Korean system-font fallbacks.
- Hero size is fluid from 44 px to 72 px; body is 16–17 px at 1.65–1.75 line height.
- Project separation uses numbering, typography, whitespace, and 1 px rules.
- No gradients, shadows, glass effects, pills, rounded card grids, hover translation, custom cursor, counters, parallax, or scroll-reveal animation.
- Desktop at 1120 px and wider: rail + copy + figure.
- Tablet at 720–1119 px: reduced rail, copy above figure.
- Mobile below 720 px: one column and a horizontal metadata row; no vertical 44 px rail.
- Page-level horizontal scrolling is prohibited at 320 px and at 200% zoom.

## Semantic and accessibility contract

- `lang="ko"`, exactly one `main`, exactly one `h1`, and a visible-on-focus skip link on every HTML page.
- Heading order: h1 → h2 → h3 without skipped levels.
- Number rails are decorative and `aria-hidden="true"`.
- Use `dl` for metrics, evidence states, and label/value claims.
- Every raster image has explicit width and height; below-fold images use lazy loading and async decoding.
- Status is always conveyed by visible text, never by teal alone.
- Focus indicators use at least a 2 px outline with offset. Interactive targets are at least 44 by 44 px on touch layouts.
- `prefers-reduced-motion: reduce` disables smooth scrolling, animation, and transitions.
- Tables and code blocks have keyboard-scrollable wrappers.
- External links that open a new tab have `rel="noreferrer"` and a visible or accessible new-tab indication.

## Metadata and publication

- Every page has a unique title, description, canonical URL, Open Graph title/description/URL/image, and valid JSON-LD.
- Home JSON-LD type is `Person`; case pages are `TechArticle` with `Person` author.
- `sitemap.xml` contains the four canonical URLs and no extras.
- `robots.txt`, `404.html`, `.nojekyll`, favicon, and a 1200 by 630 neutral OG image are published.
- GitHub Actions must run the complete unittest suite before uploading only `site/` and deploying Pages.
- Current action majors verified on 2026-08-24: `actions/checkout@v7`, `actions/configure-pages@v6`, `actions/upload-pages-artifact@v5`, `actions/deploy-pages@v5`.

## Git and release safety

- The clean branch has no parent commit.
- Do not force-push or change Pages configuration until tests, link audit, visual QA, and final review all pass.
- The old remote main expected by the publication lease is `661b9d5186028318a1f181f4f7b0e8a822f1da63`.
- Publish with an explicit force-with-lease for `refs/heads/main`, then change Pages build type to workflow and wait for the deployment result.
