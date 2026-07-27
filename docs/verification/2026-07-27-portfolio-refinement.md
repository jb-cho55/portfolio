# Portfolio Refinement Verification

| ID | Verification | Status |
|---|---|---|
| PROFILE-01 | 소개 문구에 국민대·HL 부트캠프·차량 HW/SW 학습 명시 | PASS |
| BOOT-01 | Bootloader 상세 산출물 링크와 로컬 이미지 갤러리 추가 | PASS |
| BOOT-02 | UDS 서비스명과 SID 0x10·0x27·0x31·0x34·0x36·0x37·0x11 표기 | PASS |
| BOOT-03 | Memory Map figcaption 문구 변경 | PASS |
| BOOT-04 | EA_AppRestore 라벨·화살표 재배치 및 SVG ID 부여 | PASS |
| BOOT-05 | 링커 근거 제목을 근거로 변경 | PASS |
| BOOT-06 | SHA-256 문구를 요청 범위로 축약 | PASS |
| BOOT-07 | Notion 기록의 코드·PC·BTV·Breakpoint 값을 로컬 이미지화. 원본 스크린샷 바이너리는 커넥터 제약으로 미포함 | PARTIAL |
| BLACKBOX-01 | CODE·TEST·DOCUMENT·DEMO 통합 산출물 페이지 생성 | PASS |
| BLACKBOX-02 | 메인 네 버튼을 통합 페이지 앵커로 연결 | PASS |
| CREDENTIAL-01 | 마스킹 PDF 첫 페이지를 200 DPI PNG로 렌더링하고 최소 1100×1600 해상도 확인 | PASS |
| CREDENTIAL-02 | 카드 클릭 대상을 PDF에서 확대 이미지로 변경 | PASS |
| CLEANUP-01 | HTML 로컬 href/src 참조 검사 적용 | PASS |
| CLEANUP-02 | 과거 Superpowers 문서 제거: `docs/superpowers/plans/2026-07-12-corporate-portfolio-redesign.md`, `docs/superpowers/plans/2026-07-13-portfolio-project-content-refinement.md`, `docs/superpowers/plans/2026-07-13-portfolio-project-details.md`, `docs/superpowers/plans/2026-07-13-real-assets-and-evidence.md`, `docs/superpowers/plans/2026-07-14-vehicle-embedded-sw-positioning.md`, `docs/superpowers/plans/2026-07-15-project-case-studies.md`, `docs/superpowers/plans/2026-07-26-bootloader-evidence.md`, `docs/superpowers/specs/2026-07-12-corporate-portfolio-design.md`, `docs/superpowers/specs/2026-07-12-enterprise-portfolio-redesign-design.md`, `docs/superpowers/specs/2026-07-13-portfolio-project-details-design.md`, `docs/superpowers/specs/2026-07-13-portfolio-real-assets-and-evidence-design.md`, `docs/superpowers/specs/2026-07-14-vehicle-embedded-sw-positioning-design.md`, `docs/superpowers/specs/2026-07-15-project-case-study-structure-design.md`, `docs/superpowers/specs/2026-07-26-bootloader-evidence-design.md` | PASS |
| CLEANUP-03 | HTML·CSS·이미지·PDF 원본·테스트·README 보존 | PASS |
| CLEANUP-04 | 삭제 후 전체 테스트와 링크 검사 수행 | PASS |
| VERIFY-01 | ID 기반 회귀 테스트 추가 | PASS |
| VERIFY-02 | 본 검증 기록 작성 | PASS |

## Commands

- `python -m unittest discover -s tests -v`
- HTML local `href`/`src` existence scan
- Temporary signed URL marker scan

## Residual risk

BOOT-07은 Notion 커넥터가 페이지의 임시 서명 URL은 제공하지만 원본 이미지 바이너리의 안정적 내보내기 기능은 제공하지 않아 원본 스크린샷을 직접 포함하지 못했습니다. 대신 동일 Notion 기록의 실제 코드, PC, BTV, Breakpoint 값을 로컬 정적 이미지로 구성했습니다.
