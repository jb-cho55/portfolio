# 조정빈 · Vehicle SW Verification Portfolio

차량 ECU의 요구사양을 테스트 조건과 판정 기준으로 바꾸고, CANoe/CAPL 자동화와 Trace 분석으로 결함을 재현한 경험을 정리했습니다. AURIX Bootloader 개발·디버깅 경험을 함께 소개합니다.

**[포트폴리오 웹사이트](https://jb-cho55.github.io/portfolio/)** · [GitHub 프로필](https://github.com/jb-cho55)

## 대표 프로젝트

### CANoe/CAPL 기반 차량 ECU Black Box Validation

- 요구사양 분석, CANdb·CANoe 환경 구성, 수동·자동화 시험, 결함 문서화를 수행한 개인 프로젝트입니다.
- 고장 시나리오 7개를 CAPL 스크립트 6종·테스트케이스 24개로 구성했습니다. Batt Percent 시나리오는 101 × Ignition 2 × Engine 2 = 404조합을 시험했습니다.
- 정적 결함 4건과 동적 결함 11건을 식별했습니다. 동적 결함 중 10건의 실제 판정 화면을 공개합니다.
- 최신 수신 프레임을 기준으로 타이밍 측정을 시작하도록 동기화 로직을 수정했습니다.
- Black Box Testing 프로젝트 우수상을 받았습니다.

[코드·문제 해결](https://jb-cho55.github.io/portfolio/artifacts/black-box/#code) · [시험 결과](https://jb-cho55.github.io/portfolio/artifacts/black-box/#test) · [실행 화면](https://jb-cho55.github.io/portfolio/artifacts/black-box/#demo)

### AURIX UDS Bootloader · Flash Backup/Restore

- 제공된 AURIX TC234LP·MCAL 교육 환경에서 UDS 리프로그래밍, Application Backup·Restore와 SHA-256 비교 분기를 구현한 개인 프로젝트입니다.
- CAN 응답 중단을 Trace32로 추적하고, source buffer의 4바이트 정렬 위반을 원인으로 특정했습니다. 공개 자료에는 레지스터·DMI 캡처와 수정 전후 코드가 포함됩니다.
- 정상 다운로드·무결성 불일치·양방향 Flash 복사는 **당시 기록**을 기준으로 설명합니다. 현재 새 빌드나 ECU 재시험을 수행한 결과는 아닙니다.
- 이후 정적 리뷰에서 valid pattern 선기록, 길이 상한·권한 검사 누락을 발견했습니다. **개선안은 미적용·미검증**이며, 모든 오류·중단 상황에서 안전한 부팅을 보장하는 구현으로 제시하지 않습니다.

[메모리 맵](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#memory-map) · [구현 흐름과 한계](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#uds) · [시험 판정·근거](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#test) · [Trace32 분석](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#trace32) · [미해결 코드 리뷰](https://jb-cho55.github.io/portfolio/artifacts/bootloader/#review)

## Bootloader 시험표를 읽는 기준

시험 판정과 근거 유형은 별도로 표시합니다. 원본 로그가 비공개인 경우, 공개된 요약·코드·화면과 구분합니다.

| 판정 | 의미 |
|---|---|
| 기록상 PASS | 당시 실행·재검증 기록에 통과 결과가 서술됨. 현재 재시험 또는 독립 검증을 뜻하지 않음 |
| 정적 확인 | 코드·설계 기록만 확인. 실행 시험 통과가 아님 |
| 근거 부족 | 수행 서술은 있으나 판정을 뒷받침하는 자료가 부족함 |
| 실행 미확인 | 실행 여부 자체를 확인할 기록이 없음. 미실행으로 단정하지 않음 |

고정 키 접두어 SHA-256은 HMAC이나 전자서명이 아니며, 해시까지 다시 계산하는 공격자를 방어하지 못합니다. 기능 흐름의 구현, 당시 시험 기록, 이후 발견한 결함, 아직 적용하지 않은 개선안을 구분해 읽어 주세요.

## 다른 공개 프로젝트

- [CarMaker ADAS 통합 자율주행](https://github.com/jb-cho55/IVS-CarMaker-ADAS) — 6인 팀 프로젝트의 팀장·주차 알고리즘 담당
- [보안 CAN 차량 네트워크](https://github.com/jb-cho55/Autonomous-Computing-Platform-FinalProject) — ERIKA Enterprise RTOS ECU와 OP-TEE 게이트웨이를 연결한 보안 데모
- [DeepRacer 캡스톤](https://github.com/jb-cho55/Capstone_DeepRacer_KOOKNET_2025) — 팀장·제어 파트 담당

## 저장소 구조

```text
index.html                       포트폴리오 메인
artifacts/black-box/index.html    Black Box 코드·시험·실행 화면
artifacts/bootloader/index.html   Bootloader 구현·시험 근거·정적 리뷰
assets/bootloader/               메모리 맵·UDS 도식·공통 스타일
assets/images/                  프로젝트 캡처
assets/evidence/                개인정보를 마스킹한 자격·수상 증빙
tests/                          웹사이트 콘텐츠·링크 회귀 테스트
```

## 로컬 실행 및 웹사이트 검증

```bash
python -m http.server 8000
python -B -m unittest discover -s tests -v
```

테스트는 이 정적 웹사이트의 콘텐츠·링크·구조를 검사합니다. CAPL 시험 실행, Bootloader 빌드 또는 ECU 동작 검증을 대신하지 않습니다.

## 공개 범위

교육 자료 보호를 위해 두 대표 프로젝트의 원본 저장소는 비공개로 유지합니다. 공개 가능한 코드 발췌·캡처·주소·결과 요약과 개인정보를 마스킹한 자격·수상 증빙만 게시합니다. 계정·인증정보, 보호된 교육 자료와 만료형 첨부 URL은 포함하지 않습니다.
