# Bootloader 증거 보강 및 프로젝트 메타데이터 설계

## 목적

포트폴리오의 OTA Bootloader Case Study에 채용 담당자가 별도 권한 없이 열람할 수 있는 독립 증거 자료 4개를 추가한다. 기존의 동일 페이지 내부 앵커형 `CODE`, `TEST`, `DOCUMENT`, `DEMO` 링크를 실제 정적 산출물 링크로 교체하고, Bootloader와 Black Box Validation 프로젝트에 수행 기간·팀 규모·기여도·역할·환경 메타데이터를 동일한 형식으로 표시한다.

## 근거와 공개 범위

- 콘텐츠의 기술 사실, 날짜, 코드 조각과 디버깅 과정은 연결된 Notion의 IVS 5기 교육 기록을 근거로 작성한다.
- Bootloader 수행 기간은 `2026.03.03–2026.03.24`이다.
- Black Box Validation 수행 기간은 `2026.03.19–2026.03.23`이다.
- 두 프로젝트는 개인 프로젝트이며 팀 규모는 1명, 기여도는 100%로 표시한다.
- Memory Map과 Trace32 자료에는 실제 메모리 주소, 실제 함수명, 핵심 코드 일부를 공개한다.
- Trace32 자료에는 실제 PC·BTV·Breakpoint 주소를 공개한다.
- 교육용 프로젝트와 개인 구현을 설명하는 데 필요한 정보만 공개하며 고객사·양산 ECU·계정·인증정보는 추가하지 않는다.
- Notion의 만료형 첨부 URL을 GitHub Pages에서 직접 참조하지 않는다. 공개할 이미지는 저장소의 정적 자산으로 복사한다.
- 실행 증거가 없는 테스트 결과를 임의로 `PASS` 처리하지 않는다. 근거가 부족한 항목은 `Not executed` 또는 `Evidence unavailable`로 표시한다.

## 정보 구조

```text
artifacts/
└── bootloader/
    ├── memory-map.html
    ├── uds-sequence.html
    ├── test-results.html
    └── trace32-restore.html

assets/
└── bootloader/
    ├── memory-map.svg
    ├── uds-sequence.svg
    ├── shared.css
    ├── trace32/
    └── restore/
```

각 산출물 페이지는 포트폴리오의 시각 체계와 호환되는 독립 HTML 문서로 작성한다. 페이지 상단에는 포트폴리오로 돌아가는 링크, 문서 제목, 프로젝트 메타데이터, 공개 범위 안내를 제공한다.

## 메인 포트폴리오 변경

Bootloader의 산출물 영역을 다음 4개 실제 링크로 교체한다.

| 버튼 | 경로 | 설명 |
|---|---|---|
| MEMORY MAP | `artifacts/bootloader/memory-map.html` | PFlash 영역, 주소, 책임 함수와 복구 경로 |
| UDS SEQUENCE | `artifacts/bootloader/uds-sequence.html` | 정상 리프로그래밍과 무결성 실패·Restore 흐름 |
| TEST RESULTS | `artifacts/bootloader/test-results.html` | 테스트 케이스, 기대 결과, 실제 결과와 증거 |
| TRACE32 · RESTORE | `artifacts/bootloader/trace32-restore.html` | Alignment 오류 분석과 복구 재검증 |

모든 링크는 새 탭에서 열고 `rel="noreferrer"`를 사용한다. 기존 Bootloader 상세 펼침 영역은 기술 설명용으로 유지하되, 증거 자료의 중복 전문은 넣지 않는다.

## 프로젝트 메타데이터

### OTA Bootloader

- 유형: 개인 프로젝트
- 수행 기간: 2026.03.03–2026.03.24
- 팀 규모: 1명
- 기여도: 100%
- 역할: 메모리·진단 절차 설계, Embedded C 구현, Flash 제어, 디버깅, 검증 전담
- 환경: Infineon AURIX TC234LP, Embedded C, CAN·ISO-TP, UDS, MCAL, PFlash·DFlash, SHA-256, Trace32

### Black Box Validation

- 유형: 개인 프로젝트
- 수행 기간: 2026.03.19–2026.03.23
- 팀 규모: 1명
- 기여도: 100%
- 역할: 요구사항 분석, 테스트 환경 구성, 테스트 케이스 설계, CAPL 자동화, Trace 분석, 결함 문서화 전담
- 환경: CANoe, CAPL, CANdb, CAN, UDS, Black Box Testing, Trace Analysis

메타데이터는 두 프로젝트의 헤더 또는 인트로 바로 아래에서 동일한 컴포넌트와 순서로 표시한다. 모바일에서는 단일 열로 전환한다.

## 산출물 1 — Memory Map

### 목적

Bootloader가 Application 보호·Backup·Restore·무결성 검사를 위해 PFlash와 상태 정보를 어떻게 분리하는지 실제 주소 기반으로 설명한다.

### 필수 내용

- AURIX TC234LP PFlash 전체 관점
- Bootloader 영역
- Application Primary 영역
- Application Backup 영역
- Signature 또는 SHA-256 저장 영역
- Valid Pattern 또는 상태 저장 영역
- 각 영역의 시작·종료 주소와 크기
- 각 영역을 읽거나 쓰는 실제 함수
- 정상 업데이트와 실패 복구 시 데이터 이동 방향
- 링커 설정 또는 메모리 매크로를 근거로 한 주소 출처 설명

### 표현

- 상단에는 비례형 또는 구획형 SVG Memory Map을 제공한다.
- 하단에는 `영역 / 주소 범위 / 크기 / 용도 / 관련 함수 / 변경 시점` 표를 제공한다.
- 주소가 Notion 기록과 저장소에서 교차 확인되지 않으면 추정하지 않고 해당 행을 제외한다.

## 산출물 2 — UDS Sequence Diagram

### 참여 객체

- Tester
- BswCom
- BswDcm
- EcuAbsFls
- FlsLoader
- PFlash

### 정상 흐름

1. DiagnosticSessionControl `0x10`
2. SecurityAccess `0x27`
3. RoutineControl `0x31`을 통한 Application Backup과 Erase
4. RequestDownload `0x34`
5. TransferData `0x36`
6. RequestTransferExit `0x37`
7. RoutineControl `0x31`을 통한 CheckProgrammingDependencies
8. SHA-256 비교
9. 성공 응답 후 ECU Reset

### 실패·복구 흐름

- Block Sequence 불일치 또는 TransferData 오류 시 NRC와 전송 중단 정책을 표시한다.
- SHA-256 불일치 시 Application을 실행 가능 상태로 처리하지 않는다.
- Backup→Application Restore 호출과 재검증 흐름을 표시한다.

### 표현

- SVG 또는 HTML/CSS 기반 시퀀스 다이어그램을 사용한다.
- 정상 흐름과 실패·복구 흐름을 시각적으로 구분하되 색상만으로 의미를 전달하지 않는다.
- 서비스 ID, 핵심 함수명과 응답 결과를 텍스트로 함께 표시한다.

## 산출물 3 — 테스트 케이스·결과표

### 표 컬럼

`ID / 검증 목적 / 사전 조건 / 입력·절차 / 기대 결과 / 실제 결과 / 판정 / 증거`

### 초기 테스트 세트

1. 정상 리프로그래밍
2. Block Sequence 불일치
3. TransferData 길이 초과
4. 전송 중단
5. Binary 변경 및 SHA-256 불일치
6. Application Backup 성공
7. 무결성 실패 후 Restore
8. Restore 후 Application 실행
9. Application→Backup 데이터 비교
10. Backup→Application 데이터 비교
11. 비정렬 버퍼 사용 시 오류 재현
12. 4바이트 정렬 수정 후 회귀 시험

### 판정 정책

- `PASS`: 실행 화면, 로그, 메모리 비교 또는 명확한 기록이 존재한다.
- `FAIL`: 기대 결과와 다른 실행 결과가 기록되어 있다.
- `Not executed`: 테스트를 수행하지 않았다고 기록되어 있다.
- `Evidence unavailable`: 수행 주장은 있으나 공개 가능한 증거가 없다.

각 증거 셀은 Trace32·로그 이미지, 코드 조각 또는 관련 산출물의 정확한 앵커로 연결한다.

## 산출물 4 — Trace32 디버깅 및 Restore

### 디버깅 서사

1. `FlsLoader_Write()` 호출 중 CAN 응답과 Backup·Restore 흐름이 중단되는 증상
2. `EA_AppToBackup()`을 의심 지점으로 설정
3. 함수 Breakpoint와 Trap Vector 범위 Breakpoint 설정
4. `PC = 0x7000EC24`, `BTV = 0x80027800` 확인
5. `Break.Set 0x80027800++0xFF /Program /Onchip`으로 Trap Vector 추적
6. source buffer와 Flash Write 정렬 조건 점검
7. 저장 버퍼를 4바이트 정렬 가능한 `uint32` 기반 배열로 변경하고 바이트 접근은 `uint8*`로 처리
8. Application→Backup과 Backup→Application 양방향 Write·Read 재검증
9. SHA-256 판정과 Restore 후 Application 실행 확인

### 공개할 코드·명령

- `EA_AppToBackup()`
- `EA_AppRestore()`
- `FlsLoader_Write()` 호출부
- 정렬 수정 전후 핵심 코드 조각
- 실제 Trace32 Breakpoint 명령
- PC·BTV 주소

### 화면 구성

- 증상, 가설, 관찰, 원인, 수정, 재검증 순서의 Case Study 구조
- Trace32 화면은 중요한 주소·레지스터·콜스택 위치가 보이도록 캡션을 제공한다.
- Restore 결과는 Primary와 Backup 영역의 비교 근거를 함께 제공한다.

## 공통 UI·접근성

- 포트폴리오와 동일한 Pretendard 기반 타이포그래피와 Navy·Blue 계열 변수를 재사용한다.
- 각 독립 페이지는 1080px 이하의 콘텐츠 폭과 반응형 단일 열 레이아웃을 사용한다.
- 표는 작은 화면에서 가로 스크롤을 허용하고 행 제목이 유지되도록 한다.
- 모든 이미지에 구체적인 `alt`와 캡션을 제공한다.
- 링크와 버튼은 키보드 포커스가 명확해야 한다.
- `prefers-reduced-motion`을 준수한다.
- JavaScript는 내비게이션 또는 경량 상호작용에만 사용하며 핵심 정보 열람에 필수적이지 않아야 한다.

## 구현 범위

- `index.html`: Bootloader 산출물 링크와 두 프로젝트 메타데이터 컴포넌트 추가
- `artifacts/bootloader/memory-map.html`: 실제 주소 기반 Memory Map 문서
- `artifacts/bootloader/uds-sequence.html`: 정상·실패·Restore 시퀀스 문서
- `artifacts/bootloader/test-results.html`: 테스트 케이스·결과표
- `artifacts/bootloader/trace32-restore.html`: Trace32 디버깅·Restore Case Study
- `assets/bootloader/shared.css`: 독립 산출물 공통 스타일
- `assets/bootloader/*.svg`: Memory Map과 UDS Sequence 시각 자료
- `assets/bootloader/trace32/`, `assets/bootloader/restore/`: 공개 가능한 실제 이미지
- `tests/test_portfolio.py`: 링크, 메타데이터, 접근성, 파일 존재, 공개 문구 검증
- 필요 시 산출물 전용 테스트 파일 추가
- `README.md`: 공개 산출물 구조와 로컬 열람 방법 갱신

## 검증 기준

1. Bootloader 산출물 4개가 실제 독립 HTML 파일로 존재한다.
2. 메인 페이지의 4개 산출물 링크가 각 독립 페이지를 새 탭에서 연다.
3. 두 프로젝트에 유형, 수행 기간, 팀 규모, 기여도, 역할, 환경이 표시된다.
4. 두 프로젝트 모두 `개인 프로젝트`, `1명`, `100%`가 명확히 표시된다.
5. Memory Map에는 교차 확인된 실제 주소와 함수명만 표시된다.
6. UDS Sequence에는 정상 흐름과 SHA-256 실패 후 Restore 흐름이 모두 표시된다.
7. 테스트 결과표에는 12개 초기 테스트 항목과 판정 정책이 표시된다.
8. 증거 없는 항목이 임의로 `PASS` 처리되지 않는다.
9. Trace32 문서에는 실제 PC, BTV, Breakpoint 명령과 정렬 수정 전후 코드가 표시된다.
10. Notion 만료형 첨부 URL이 공개 HTML에 포함되지 않는다.
11. 모든 이미지에 `alt`와 캡션이 존재한다.
12. 모든 새 탭 링크는 `target="_blank"`와 `rel="noreferrer"`를 사용한다.
13. 데스크톱과 모바일에서 콘텐츠를 읽을 수 있다.
14. 기존 프로젝트 펼침·접기와 자격·수상 링크가 깨지지 않는다.
15. 전체 Python 테스트가 통과한다.

## 제외 범위

- Private Bootloader 저장소 공개 전환
- 전체 소스 코드 공개
- 고객사·양산 ECU 정보 추가
- 실제 암호 키 또는 인증 비밀 공개
- 실행 증거가 없는 테스트 결과 생성
- Notion 페이지 자체를 공개 링크로 전환
- PDF 산출물 추가
- 기존 Black Box 실제 이미지와 자격 증빙 구조의 재설계
