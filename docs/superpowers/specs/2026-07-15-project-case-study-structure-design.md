# Project Case Study Structure Design

**Date:** 2026-07-15  
**Repository:** `jb-cho55/portfolio`

## Objective

채용 담당자가 두 대표 프로젝트에서 직무 적합성, 본인 기여, 구현 범위, 검증 근거와 문제 해결 능력을 빠르게 판단할 수 있도록 정보 구조를 재설계한다.

## Information hierarchy

1. OTA Bootloader를 개발 직무 대표 프로젝트로 첫 번째에 배치한다.
2. IVS Black Box Validation을 검증 직무 대표 프로젝트로 두 번째에 배치한다.
3. 각 프로젝트 최상단에 `목표 / 역할 / 구현 / 검증 / 결과` 5줄 요약을 둔다.
4. 요약 바로 아래에 `Key Results` 박스를 배치해 정량·판정 가능한 성과를 노출한다.
5. 산출물은 `Code / Test / Document / Demo / Evidence` 5개 범주로 통일한다.
6. 상세 영역의 문제 해결 사례는 `증상 → 원인 분석 → 수정 → 재검증` 순서로 통일한다.

## Technical experience section

도구 목록 대신 수행 경험과 적용 수준을 함께 표시한다.

- 프로젝트 적용
- 프로토콜 적용
- 자동화 구현
- 원인 분석
- 교육·실습 적용
- 자격·프로젝트 적용

각 항목에는 실제 프로젝트에서 수행한 작업과 범위를 명시하고, 전문·숙련 등 과장된 수준 표현은 사용하지 않는다.

## Privacy and evidence

- 비공개 프로젝트 저장소 URL은 공개하지 않는다.
- 공개 가능한 화면, 내부 앵커, 자격·수상 PDF를 산출물 링크로 사용한다.
- Black Box Validation의 실제 CANoe 화면과 Test Result 이미지는 유지한다.
- 교육·자격·수상 증빙 PDF와 썸네일은 유지한다.

## Accessibility and responsive behavior

- 상세 내용 토글은 `aria-expanded`, `aria-controls`, `hidden` 상태를 동기화한다.
- 데스크톱, 태블릿, 모바일에서 5열 산출물과 4단 문제 해결 흐름을 단계적으로 축소한다.
- Pretendard, 1080px 본문 폭, 1.7 행간을 유지한다.

## Acceptance criteria

- 대표 프로젝트 카드는 정확히 2개다.
- OTA Bootloader가 Black Box Validation보다 먼저 노출된다.
- 두 프로젝트에 5줄 요약, Key Results, 5종 산출물이 모두 존재한다.
- 두 문제 해결 사례가 동일한 4단 구조를 사용한다.
- 기술 경험 섹션은 6개 수행 수준 카드로 구성된다.
- 기존 자격·수상 증빙과 Black Box 이미지가 유지된다.
- 전체 단위 테스트가 통과한다.
