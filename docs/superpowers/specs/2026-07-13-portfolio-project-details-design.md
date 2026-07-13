# 포트폴리오 프로젝트 상세 확장 설계

## 목적

현대오토에버 Embedded SW QA 지원용 1페이지 포트폴리오에서 비공개 GitHub 저장소 링크를 제거하고, 채용담당자가 페이지 내부에서 프로젝트의 수행 범위와 기술적 근거를 확인할 수 있도록 카드 내부 펼침/접기 상세 영역을 제공한다. Black Box Testing을 대표 프로젝트로 유지하고 OTA Bootloader를 두 번째 프로젝트로 배치한다.

## Project 01 — IVS Black Box Testing

기존 요약 카드와 정적 결함 4건, 동적 결함 11건, CAPL 자동화 성과는 유지한다.

상세 영역은 다음과 같이 수정한다.

1. `본인 수행 범위` 제목을 `수행 범위`로 변경한다.
2. 원본 요구사양과 내부 자료 제외를 설명하는 문장은 상세 영역에서 제거한다.
3. 요구사양 분석 → CANoe·CANdb·Panel 환경 구성 → 수동·CAPL 자동화 시험 → 정적·동적 시험 → 결함 분석 흐름은 유지한다.
4. 수행 범위에는 CANdb 작성, CANoe Network Node 구성, Panel 입력 제어, CAPL 테스트 작성, Trace 분석과 결함 문서화를 표시한다.
5. 대표 결함에는 Signal Length 불일치, Batt Percent 15% 경계값, IGN 50 Cycle Off-by-One, Steering Timing 사례를 표시한다.
6. 상세 영역에 수행 환경과 Test Result를 설명하는 시각 갤러리를 추가한다.

### Black Box Testing 시각 갤러리

비공개 저장소의 원본 PNG를 공개 저장소로 복사하지 않고, 수행한 테스트 환경과 결과 구조를 기반으로 포트폴리오용 SVG 4개를 재구성한다.

- CANoe Network 구성: `assets/images/network_setup.svg`
- CAPL 자동화 테스트 환경: `assets/images/automation_test_environment.svg`
- Panel 및 Trace 검증 구조: `assets/images/panel_trace.svg`
- Test Result 근거: `assets/images/defect_batt_percent_15.svg`

각 시각 자료는 실제 프로젝트에서 수행한 환경과 결과를 설명하되 원본 화면 캡처로 오인되지 않도록 캡션에 `포트폴리오 재구성`을 표시한다. 각 이미지에는 구체적인 대체 텍스트와 캡션을 제공한다. 데스크톱은 2열, 900px 이하에서는 1열로 배치한다.

## Project 02 — OTA Bootloader 설계 및 SW Binary 위변조 감지

요약 카드에는 다음 내용을 유지한다.

- 대상: Infineon AURIX TC234LP 기반 ECU
- 목표: OTA 업데이트 실패 또는 Binary 변경 시 기존 애플리케이션 보호·복구
- 핵심 기술: UDS 리프로그래밍, PFlash erase/write, Backup·Restore, SHA-256, Trace32

상세 영역에서는 기존 `정적 코드 리뷰`와 `검증 범위와 한계` 블록을 제거한다. 교육 과제 번호를 나열하지 않고 구현 목적에 따라 두 개발 단계로 통합한다.

### 개발 단계 1 — 애플리케이션 보호 및 복구

OTA 업데이트 중 전송 중단이나 Flash 쓰기 실패가 발생해도 기존 애플리케이션을 보호할 수 있도록 Backup·Erase·Restore 흐름을 구현했다. Application Primary를 Backup 영역으로 복사하고, 부팅 시 `valid pattern`을 확인해 유효하지 않은 애플리케이션이면 Backup을 Primary로 복구하도록 구성한 내용을 설명한다.

### 개발 단계 2 — SW Binary 무결성 검증

애플리케이션 데이터의 SHA-256 계산값과 서명 영역의 32바이트 저장값을 비교하는 무결성 검사를 구현했다. 이후 교육용 고정 키와 Application 데이터를 결합한 SHA-256 검사로 확장한 흐름을 설명한다. HMAC이나 비대칭 전자서명으로 표현하지 않는다.

### 대표 문제 해결 — Memory Alignment Error

프로젝트의 Backup·Restore 기능을 구현하는 과정에서 Flash 쓰기 중 Memory Alignment Error로 인한 Trap을 발견하고 디버깅한 흐름으로 설명한다.

1. Backup·Restore 진행 중 `FlsLoader_Write` 호출 경로에서 Trap 발생
2. Trace32의 Trap 관련 레지스터와 Flash Loader 인수 확인
3. `uint8` source buffer가 Flash Loader의 4바이트 정렬 조건을 보장하지 않는 원인 확인
4. 저장 버퍼를 `uint32` 배열로 변경하고 바이트 단위 처리는 `uint8*`로 참조
5. Application → Backup과 Backup → Application 경로에 동일한 수정 적용

설명은 문제 발생 → 원인 추적 → 수정 → 적용 범위 순서로 구성하며, 단순 결과보다 개발 중 직접 발견하고 해결한 디버깅 역량이 드러나도록 한다.

## 상호작용 및 시각 설계

- 각 프로젝트 카드는 독립적인 `프로젝트 상세 보기` 버튼을 사용한다.
- 버튼은 `aria-expanded`, `aria-controls`를 사용하며 초기 상태는 접힘이다.
- 클릭 시 해당 카드만 펼치고 문구를 `상세 내용 접기`로 변경한다.
- 기존 흰색·남색·파란색 기업형 디자인을 유지한다.
- 상세 설명은 2열 정보 블록으로 구성하고 900px 이하에서는 1열로 전환한다.
- 시각 갤러리는 `loading="lazy"`를 적용하고 가로 비율을 유지한다.
- 모달, 별도 페이지, 프레임워크는 추가하지 않는다.

## 구현 범위

- `index.html`: Black Box 문구 수정, 시각 갤러리, OTA 개발 단계 2개, Memory Alignment Error 문제 해결 흐름 반영
- `assets/images/`: 프로젝트 수행 구조를 설명하는 포트폴리오용 SVG 4개 추가
- `tests/test_portfolio.py`: 제거 문구, 신규 제목, 개발 단계, Memory Alignment Error, 이미지 경로와 접근성 검증
- `README.md`: 시각 갤러리와 OTA 단계형 설명 추가를 반영

## 검증 기준

1. `본인 수행 범위`가 존재하지 않고 `수행 범위`가 표시된다.
2. Black Box 상세 영역에 제거 요청 문장이 존재하지 않는다.
3. Black Box 상세 영역에 CANoe, CAPL 자동화, Panel·Trace, Test Result 시각 자료 4개가 표시된다.
4. 모든 시각 자료에 `alt`, 캡션, `loading="lazy"`가 적용된다.
5. 재구성한 자료는 원본 화면으로 표현하지 않고 캡션에서 재구성 여부를 명시한다.
6. OTA 상세 영역에 `개발 단계 1 — 애플리케이션 보호 및 복구`가 표시된다.
7. OTA 상세 영역에 `개발 단계 2 — SW Binary 무결성 검증`이 표시된다.
8. `정적 코드 리뷰`와 `검증 범위와 한계` 블록이 존재하지 않는다.
9. 대표 문제 해결 제목과 본문에 `Memory Alignment Error`가 표시된다.
10. 문제 해결 설명이 프로젝트 진행 중 발견 → Trace32 분석 → 4바이트 정렬 원인 → `uint32` 버퍼 수정 순서로 구성된다.
11. 두 프로젝트의 펼침/접기와 모바일 단일 열 배치가 유지된다.
12. Python 단위 테스트가 모두 통과한다.

## 제외 범위

- Private 저장소 공개 전환
- 원본 요구사양이나 교육 내부 자료 공개
- 비공개 저장소의 원본 화면을 공개 저장소로 복사
- OTA 프로젝트 4의 `+0x05/-0x05` 변환 설명
- 기존 정적 코드 리뷰 발견사항과 빌드·재시험 한계 문구
- 모달, 라우팅, 프레임워크 도입
