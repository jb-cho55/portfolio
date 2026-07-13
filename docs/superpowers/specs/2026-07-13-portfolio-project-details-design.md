# 포트폴리오 프로젝트 상세 확장 설계

## 목적

현대오토에버 Embedded SW QA 지원용 1페이지 포트폴리오에서 비공개 GitHub 저장소 링크를 제거하고, 채용담당자가 페이지 내부에서 프로젝트의 수행 범위와 증거를 확인할 수 있도록 프로젝트 카드 내부 펼침/접기 기능을 추가한다. 기존 Black Box Testing을 대표 프로젝트로 유지하고, OTA Bootloader를 두 번째 프로젝트로 추가한다.

## 정보 구조

### Project 01 — IVS Black Box Testing

기존 카드의 요약 정보는 유지한다. 카드 하단의 GitHub 저장소 링크는 제거하고 `프로젝트 상세 보기` 버튼으로 교체한다. 버튼을 누르면 카드 내부에 다음 내용이 펼쳐진다.

1. 테스트 흐름: 요구사양 분석 → CANoe/CANdb/Panel 환경 구성 → 수동·CAPL 자동화 시험 → 정적·동적 시험 → 결함 분석
2. 본인 수행 범위: 요구사양 분석, CANdb 작성, Network Node 구성, CAPL 테스트 작성, Trace 분석, 결함 문서화
3. 대표 결함: 정적 결함 4건과 동적 결함 11건 중 신호 길이, 15% 경계값, IGN 50 Cycle, Steering Timing 사례
4. QA 관점: 기대 결과·실제 결과·재현 조건·영향도 구분과 개선 방향 제시
5. 공개 범위: 원본 요구사양과 내부 자료는 제외하고 재구성한 포트폴리오임을 명시

### Project 02 — OTA Bootloader 설계 및 SW Binary 위변조 감지

Black Box Testing 아래에 동일한 시각 체계의 두 번째 프로젝트 카드를 배치한다.

요약 카드에는 다음 내용을 노출한다.

- 목표: OTA 업데이트 실패 또는 Binary 변경 시 기존 애플리케이션 보호·복구
- 대상: Infineon AURIX TC234LP 기반 ECU
- 핵심 수행: UDS 리프로그래밍, PFlash erase/write, Backup·Restore, SHA-256 무결성 검사
- 대표 문제 해결: Flash Loader source buffer 정렬 Trap 원인 분석 및 개선
- 기술: C, CAN, ISO-TP, UDS, MCAL, PFlash, SHA-256, Trace32

`프로젝트 상세 보기`를 누르면 다음 내용이 펼쳐진다.

1. 시스템 구조: Tester → CAN/ISO-TP → BswCom → BswDcm → RTE → ECU 추상화 → MCAL → Flash
2. 리프로그래밍 흐름: Programming Session → SecurityAccess → Erase/Backup → 0x34 → 0x36 → 0x37 → 무결성 확인 → ECUReset
3. 본인 수행 범위: 메모리 경계 설계, 진단 서비스 연결, Flash 관리, 무결성 검사, Binary 변환, 디버깅, 사후 정적 리뷰
4. 대표 문제 해결: 4바이트 정렬 조건을 만족하도록 `uint32` 기반 버퍼로 변경
5. 정적 리뷰 발견사항: ISO-TP 길이·순번 검증, TransferData 상한, 접근 제어, valid pattern 기록 순서, 고정 키 방식의 한계
6. 검증 범위와 한계: 현재 저장소는 실행 가능한 전체 프로젝트가 아니며, 게시 소스·메타데이터 기반 정적 확인 범위만 주장

## 상호작용 설계

- 각 카드에는 독립적인 `프로젝트 상세 보기` 버튼을 둔다.
- 버튼은 `button` 요소로 구현하고 `aria-expanded`, `aria-controls`를 사용한다.
- 초기 상태는 접힘이다.
- 클릭 시 해당 카드의 상세 영역만 펼치고 버튼 문구를 `상세 내용 접기`로 변경한다.
- JavaScript가 비활성화된 환경에서도 요약 카드의 핵심 정보는 모두 확인할 수 있어야 한다.
- 상세 영역은 기존 카드 내부에 이어지며 모달이나 별도 페이지를 사용하지 않는다.

## 시각 설계

- 기존 흰색·남색·파란색 기업형 디자인을 유지한다.
- 프로젝트 간 구분을 위해 카드 사이에 충분한 수직 여백을 둔다.
- 상세 영역은 연한 배경과 상단 경계선으로 요약 영역과 구분한다.
- 상세 내용은 긴 문단보다 2열 정보 블록, 짧은 목록, 단계형 흐름을 사용한다.
- 900px 이하에서는 모든 상세 블록을 1열로 전환한다.
- 과도한 애니메이션은 사용하지 않고 높이 변화와 투명도 전환만 짧게 적용하거나, 접근성 설정에 따라 애니메이션을 제거한다.

## 구현 범위

- `index.html`: 두 프로젝트 카드, 펼침/접기 마크업, CSS, JavaScript 추가
- `tests/test_portfolio.py`: 비공개 GitHub 프로젝트 링크 제거, 두 프로젝트 존재 여부, 상세 버튼과 접근성 속성, OTA 핵심 내용 검증
- `README.md`: 프로젝트 구성을 Black Box Testing + OTA Bootloader로 갱신

별도 이미지 파일은 추가하지 않는다. 시스템 구조와 리프로그래밍 흐름은 텍스트 기반 흐름도로 표현해 로딩과 유지보수 부담을 줄인다.

## 검증 기준

1. Black Box Testing 카드에 외부 프로젝트 저장소 링크가 없다.
2. Black Box Testing과 OTA Bootloader 카드 모두 `프로젝트 상세 보기` 버튼을 가진다.
3. 각 버튼은 올바른 `aria-expanded`와 `aria-controls`를 가진다.
4. 클릭 시 대상 상세 영역만 펼쳐지고 버튼 문구와 접근성 상태가 함께 변경된다.
5. OTA 카드에 UDS, Backup·Restore, SHA-256, Trace32 정렬 Trap, 정적 코드 리뷰가 표시된다.
6. Black Box Testing 카드에 정적 4건, 동적 11건, CAPL 자동화, 요구사양 기반 시험이 표시된다.
7. 900px 이하에서 프로젝트와 상세 영역이 단일 열로 표시된다.
8. 기존 학력·교육·자격·수상 및 직무 역량 섹션은 유지된다.
9. Python 단위 테스트가 모두 통과한다.

## 제외 범위

- Private 저장소 공개 전환
- 저장소 Collaborator 자동 초대
- 외부 프로젝트 상세 페이지 생성
- 모달, 라우팅, 프레임워크 도입
- 실제 ECU 재시험 결과 또는 공개되지 않은 요구사양 추가
