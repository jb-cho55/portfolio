# Portfolio Evidence Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 포트폴리오의 Bootloader·Black Box·자격 증빙 사용성을 개선하고 불필요한 과거 작업 문서를 안전하게 정리한다.

**Architecture:** 현재 `main`의 파일 구조를 유지하면서 테스트가 요구하는 최소 변경만 적용한다. 신규 Black Box 페이지와 로컬 증빙 이미지를 추가하고, 모든 링크·이미지 경로를 자동 검사한다.

**Tech Stack:** HTML, CSS, SVG, Python unittest, GitHub Pages static assets

## Global Constraints

- 만료형 Notion S3 URL을 공개 저장소에 남기지 않는다.
- PDF 원본 증빙은 삭제하지 않는다.
- 기존 사이트 구조와 기존 테스트를 보존한다.
- 과거 `docs/superpowers` 문서만 정리 대상으로 삼는다.

---

### Task 1: 요구사항 회귀 테스트

**Files:**
- Create: `tests/test_portfolio_refinement.py`
- Modify: `tests/test_portfolio.py`

- [ ] ID별 요구사항을 검증하는 실패 테스트를 작성한다.
- [ ] `python -m unittest discover -s tests -v`를 실행해 신규 테스트가 요구사항 미구현으로 실패하는지 확인한다.
- [ ] 테스트만 커밋한다.

### Task 2: 소개 문구와 Bootloader 상세 개선

**Files:**
- Modify: `index.html`
- Modify: `artifacts/bootloader/memory-map.html`
- Modify: `assets/bootloader/memory-map.svg`
- Create: `assets/images/bootloader/alignment-trap.png`
- Create: `assets/images/bootloader/alignment-breakpoint.png`

- [ ] PROFILE-01과 BOOT-01~07을 충족하도록 최소 변경한다.
- [ ] Bootloader 관련 신규 테스트를 실행해 통과시킨다.
- [ ] 변경을 커밋한다.

### Task 3: Black Box 통합 산출물

**Files:**
- Create: `artifacts/black-box/index.html`
- Modify: `index.html`

- [ ] `code`, `test`, `document`, `demo` 섹션을 가진 통합 페이지를 만든다.
- [ ] 메인 네 버튼을 각 앵커에 연결하고 새 탭 보안 속성을 설정한다.
- [ ] Black Box 테스트를 실행해 통과시킨다.
- [ ] 변경을 커밋한다.

### Task 4: 자격·수상 확대 이미지

**Files:**
- Create: `assets/evidence/fullsize/*.png`
- Modify: `index.html`
- Modify: `tests/test_portfolio.py`

- [ ] 기존 마스킹 PDF 첫 페이지를 200 DPI 이상으로 렌더링한다.
- [ ] 카드 링크를 확대 이미지로 변경하고 PDF 원본은 유지한다.
- [ ] 자격 증빙 테스트를 실행해 통과시킨다.
- [ ] 변경을 커밋한다.

### Task 5: 저장소 정리

**Files:**
- Delete: 과거 `docs/superpowers/plans/*`
- Delete: 과거 `docs/superpowers/specs/*`
- Preserve: 현재 2026-07-27 spec/plan

- [ ] 삭제 대상이 사이트·테스트에서 참조되지 않는지 검사한다.
- [ ] 과거 작업 문서를 삭제한다.
- [ ] 전체 테스트와 링크 검사를 실행한다.
- [ ] 변경을 커밋한다.

### Task 6: 최종 검증 기록과 PR

**Files:**
- Create: `docs/verification/2026-07-27-portfolio-refinement.md`

- [ ] ID별 수정 파일과 검증 결과를 기록한다.
- [ ] 전체 단위 테스트, 로컬 링크 검사, 만료 URL 검사를 실행한다.
- [ ] Draft PR을 생성하고 검증 결과를 본문에 포함한다.
