# Portfolio Refinement Verification

| ID | Verification | Status |
|---|---|---|
| PROFILE-01 | 소개 문구에 국민대·HL 부트캠프·차량 HW/SW 학습 명시 | PASS |
| BOOT-01 | Bootloader 상세 산출물 링크와 이미지 갤러리 추가 | PASS |
| BOOT-02 | UDS 서비스명과 SID 0x10·0x27·0x31·0x34·0x36·0x37·0x11 표기 | PASS |
| BOOT-03 | Memory Map figcaption 문구 변경 | PASS |
| BOOT-04 | EA_AppRestore 라벨·화살표 재배치 및 SVG ID 부여 | PASS |
| BOOT-05 | 링커 근거 제목을 근거로 변경 | PASS |
| BOOT-06 | SHA-256 문구를 요청 범위로 축약 | PASS |
| BOOT-07 | 실제 CANoe·Trace32 캡처로 UDS 응답 중단, source address, DMI ALN Error와 Trap Vector Breakpoint 근거 연결 | PASS |
| BLACKBOX-01 | CODE·TEST·DOCUMENT·DEMO 통합 산출물 페이지 생성 | PASS |
| BLACKBOX-02 | 메인 네 버튼을 통합 페이지 앵커로 연결 | PASS |
| CREDENTIAL-01 | 마스킹 PDF 첫 페이지를 200 DPI PNG로 렌더링하고 최소 1100×1600 해상도 확인 | PASS |
| CREDENTIAL-02 | 카드 클릭 대상을 PDF에서 확대 이미지로 변경 | PASS |
| CLEANUP-01 | HTML 로컬 href/src 참조 검사 적용 | PASS |
| CLEANUP-02 | 과거 작업용 `docs/superpowers` 폴더와 문서 전체 제거 | PASS |
| CLEANUP-03 | HTML·CSS·이미지·PDF 원본·테스트·README 보존 | PASS |
| CLEANUP-04 | 삭제 후 전체 테스트와 링크 검사 수행 | PASS |
| VERIFY-01 | ID 기반 회귀 테스트 추가 | PASS |
| VERIFY-02 | 본 검증 기록 작성 | PASS |

## Commands

- `python -m unittest discover -s tests -v`
- HTML local `href`/`src` existence scan
- Temporary signed URL marker scan

## Residual risk

원본 CANoe·Trace32 캡처 4개를 저장소 정적 자산으로 보존하고 모든 공개 페이지에서 로컬 경로로 참조합니다.
