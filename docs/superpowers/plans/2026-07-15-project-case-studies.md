# Portfolio Project Case Studies Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** OTA Bootloader와 Black Box Validation을 개발·검증 대표 Case Study로 재구성하고 수행 수준 중심의 기술 경험 섹션을 만든다.

**Architecture:** 단일 `index.html`의 기존 정적 사이트 구조를 유지한다. 프로젝트 카드 내부를 공통 정보 구조로 통일하고 `tests/test_portfolio.py`에서 순서, 문구, 접근성, 증거 링크와 반응형 토큰을 검증한다.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python `unittest`

## Global Constraints

- 대표 프로젝트는 OTA Bootloader와 Black Box Validation 두 개만 노출한다.
- OTA Bootloader를 첫 번째 프로젝트로 배치한다.
- 비공개 프로젝트 저장소 URL은 노출하지 않는다.
- 기존 증빙 PDF와 Black Box 프로젝트 PNG 자산 경로를 유지한다.
- 상세 토글 접근성 상태를 유지한다.

---

### Task 1: Define portfolio structure regression tests

**Files:**
- Modify: `tests/test_portfolio.py`

- [x] 두 대표 프로젝트의 개수와 OTA 우선 순서를 검증한다.
- [x] 프로젝트별 5줄 요약과 Key Results 박스를 검증한다.
- [x] `Code / Test / Document / Demo / Evidence` 산출물 구성을 검증한다.
- [x] 두 문제 해결 사례의 `증상 → 원인 분석 → 수정 → 재검증` 순서를 검증한다.
- [x] 수행 경험 수준과 증거 자산을 검증한다.

### Task 2: Rebuild the two project case studies

**Files:**
- Modify: `index.html`

- [x] OTA Bootloader를 첫 번째 프로젝트로 이동한다.
- [x] 두 프로젝트에 공통 5줄 요약을 적용한다.
- [x] 프로젝트별 Key Results와 통합 산출물 영역을 추가한다.
- [x] 상세 내용을 구현, 검증, 문제 해결 증거 중심으로 재작성한다.
- [x] 비공개 저장소 링크를 추가하지 않는다.

### Task 3: Replace tool list with applied experience levels

**Files:**
- Modify: `index.html`

- [x] 기존 직무 역량 카드를 수행 수준 중심의 기술 경험 카드로 교체한다.
- [x] Embedded C, 차량 통신·진단, CANoe/CAPL, Trace32, AUTOSAR/MCAL, Testing 경험 범위를 구체화한다.
- [x] 모바일과 태블릿 레이아웃을 조정한다.

### Task 4: Verify behavior and evidence retention

**Files:**
- Test: `tests/test_portfolio.py`
- Verify: `index.html`

- [x] `python -m unittest discover -s tests -v`를 실행한다.
- [x] 20개 테스트의 통과를 확인한다.
- [x] Black Box 이미지 5개와 자격·수상 증빙 5개의 경로를 확인한다.
