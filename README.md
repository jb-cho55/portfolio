# 조정빈 · Vehicle SW Portfolio

요구사항 기반 시험, CANoe/CAPL 자동화와 Trace32 원인 분석을 정리한 차량 SW 검증 포트폴리오입니다.

**[포트폴리오](https://jb-cho55.github.io/portfolio/)** · [GitHub 프로필](https://github.com/jb-cho55)

## CANoe/CAPL 기반 차량 ECU Black Box Testing

CANoe 시뮬레이션 기반 IVS 교육 과제입니다. 제공된 요구사항을 기준으로 시험 설계, CANdb·주변 노드·Panel 구성, CAPL 작성과 결함 분석을 담당했습니다. 실차·HIL 검증으로 제시하지 않습니다.

- 7개 고장 시나리오. 보관 테스트 소스 6종의 testcase 선언 24개.
- 화면에는 Brake_Error를 포함한 7개 모듈이 있으나 해당 모듈의 소스는 보관 자료에 없습니다.
- Batt Percent 정수 0~100 × IGN 2 × ENG 2 = 404조합. 전체 시스템 전수 검증과 구분합니다.
- 정적 검토 4건(표기 개선 2건 포함), 동적 결함 11건. 동적 판정 캡처 10건 공개.
- IGN 50 cycle 요구에 대해 49회에서 Clear된 사례와 시험–결과–결함 연결표를 제공합니다.
- Fresh Frame 기준의 측정 변경과 남은 오라클·타이밍 불확도를 구분합니다.

[시험 결과](https://jb-cho55.github.io/portfolio/artifacts/black-box/#test) · [추적표·결함 보고서](https://jb-cho55.github.io/portfolio/artifacts/black-box/#document) · [보관 코드·개선 설계](https://jb-cho55.github.io/portfolio/artifacts/black-box/#code)

추적용 ID는 2026-09-28에 원본 문서·코드·판정 화면을 연결하며 새로 부여했습니다. 원본 요구사항 ID나 새 시험 실행 결과가 아닙니다. 원본 문서에 먼저 반영한 뒤 공개 가능한 요약을 게시했습니다.

## UDS를 통한 Flash Backup & Restore

AURIX TC234LP에서 요구사항에 따라 UDS 7개 서비스를 연결한 리프로그래밍, Flash App 영역 백업·복원과 SHA-256 비교 분기를 구현했습니다. 링커 스크립트로 Primary·Backup 영역을 지정하고 AUTOSAR 기반 MCAL·RTE 인터페이스를 활용했습니다. Trace32에서 홀수 주소의 word 접근과 Alignment Trap을 연결하고, uint32 저장 공간으로 버퍼 정렬을 확보한 전후 코드를 제공합니다.

공개 캡처·소스와 수행 서술을 구분하며, 현재 새 빌드나 ECU 재시험 결과는 아닙니다. 이후 발견한 길이·권한 검사 및 valid pattern 순서 개선안은 **미적용·미검증**입니다. 고정 Seed/Key와 키 접두어 SHA-256은 교육용이며 HMAC이나 전자서명이 아닙니다.

[요구사항·구현 대조](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#requirements) · [메모리 맵](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#memory-map) · [진단 흐름](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#uds) · [공개 확인 자료](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#test) · [Trace32](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#trace32)

## 협업 프로젝트

[CarMaker ADAS 통합·주차](https://github.com/jb-cho55/IVS-CarMaker-ADAS) — 6인 팀장·주차 알고리즘 담당. 공개 문서의 주차 결과는 최대 오차 0.16m, T05는 Staging 적용 전후 51.6m→0.02m입니다. 팀 PR 기록 22건과 본인의 역할을 분리해 소개합니다. 해당 시험 조건의 팀·주차 파트 결과이며 개인 단독 성과나 전체 상황의 성능 보장이 아닙니다.

[보안 CAN 차량 네트워크](https://github.com/jb-cho55/Autonomous-Computing-Platform-FinalProject) · [DeepRacer 캡스톤](https://github.com/jb-cho55/Capstone_DeepRacer_KOOKNET_2025)

## 구조와 검증

`index.html`은 결과·역할 요약, `artifacts/`는 상세 근거, `assets/`는 이미지와 도식입니다. 메인은 목표→결과→대표 캡처→역할·트러블슈팅 순서입니다.

```sh
python -m http.server 8000
python -B -m unittest discover -s tests -v
```

웹 테스트는 콘텐츠·링크·구조 검사입니다. CAPL 실행이나 ECU 검증을 대신하지 않습니다. 교육 원본 저장소의 비공개 상태를 유지하고 보호된 요구사항 이미지는 공개 사이트에 복사하지 않습니다.
