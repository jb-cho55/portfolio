# Vehicle Embedded SW Positioning Design

## Objective

Reposition the portfolio from an Embedded SW QA-only presentation to a balanced Vehicle Embedded SW Engineer portfolio that supports both development and verification applications.

## Scope

- Change document metadata, Open Graph metadata, browser title, hero eyebrow, and hero role title from `Embedded SW QA` to `Vehicle Embedded SW`.
- Rewrite the hero introduction so it presents embedded implementation and verification experience together.
- Keep the existing project order and visual layout unchanged.
- Replace the four competency cards with a balanced structure:
  1. Embedded C-based ECU implementation
  2. Vehicle communication and diagnostic protocols
  3. Requirements-based test design and automation
  4. Debugging and defect root-cause analysis
- Update automated content tests to assert the new positioning and competency copy.

## Content Design

### Hero

- Eyebrow: `Vehicle Embedded SW Portfolio`
- Role title: `Vehicle Embedded SW Engineer`
- Introduction: `국민대학교 자동차IT융합학과에서 자동차·전자·소프트웨어를 학습하고, AURIX 기반 Embedded SW 구현과 CANoe/CAPL 기반 차량 SW 검증을 수행했습니다.`

### Competency Section Introduction

`차량 SW 개발과 검증 프로젝트에서 수행한 설계·구현·테스트·문제 해결 역량을 중심으로 정리했습니다.`

### Competency Cards

1. `EMBEDDED IMPLEMENTATION` / `Embedded C 기반 ECU 기능 구현`
   - `AURIX 환경에서 UDS Bootloader, Flash Backup·Restore, SHA-256 무결성 검사 기능을 구현했습니다.`
2. `VEHICLE COMMUNICATION` / `차량 통신 및 진단 프로토콜 활용`
   - `CAN·ISO-TP·UDS 통신 흐름을 이해하고 진단 서비스와 ECU 리프로그래밍 절차에 적용했습니다.`
3. `TEST ENGINEERING` / `요구사양 기반 테스트 설계·자동화`
   - `요구사양을 테스트 조건과 판정 기준으로 구조화하고 CANoe/CAPL로 반복 시험을 자동화했습니다.`
4. `DEBUGGING & ANALYSIS` / `디버깅 및 결함 원인 분석`
   - `CAN Trace와 Trace32를 활용해 통신 동작과 Memory Alignment 오류의 재현 조건과 원인을 분석했습니다.`

## Constraints

- Preserve the existing HTML structure, CSS classes, responsive layout, project details, links, and accessibility behavior.
- Do not expose private repository links.
- Do not change project evidence or credential sections.

## Verification

- Run `python -m unittest discover -s tests -v` in the pull-request workflow.
- Confirm all old `Embedded SW QA Portfolio` and `Embedded SW QA Engineer` strings are removed from `index.html`.
- Confirm the four new competency labels, titles, and descriptions appear exactly once in the competency section.
