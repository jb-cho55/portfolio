# Portfolio Evidence Refinement Design

## Goal

차량 SW 포트폴리오의 소개 문구, Bootloader 근거, Black Box 산출물, 자격·수상 증빙 동작을 개선하고 공개 저장소에서 배포와 무관한 과거 작업 문서를 정리한다.

## Requirements

| ID | Requirement | Acceptance criteria |
|---|---|---|
| PROFILE-01 | 메인 소개 문구 변경 | 국민대학교 자동차IT융합학과와 HL만도·HL클레무브 부트캠프를 통한 차량 HW/SW 전반 학습을 명시한다. |
| BOOT-01 | Bootloader 상세 영역에 실제 캡처와 산출물 바로가기 추가 | 상세 영역에서 네 Bootloader 산출물과 Memory Alignment 캡처를 바로 열 수 있다. |
| BOOT-02 | UDS 서비스명과 SID 명시 | DiagnosticSessionControl(0x10), SecurityAccess(0x27), RoutineControl(0x31), RequestDownload(0x34), TransferData(0x36), RequestTransferExit(0x37), ECUReset(0x11)을 표시한다. |
| BOOT-03 | Memory Map 설명 수정 | `Bootloader용 링크 스크립트의 주소와 크기를 기준으로 시각화했습니다.`를 사용한다. |
| BOOT-04 | Memory Map SVG 가독성 개선 | `EA_AppRestore()` 라벨과 화살표가 다른 요소와 겹치지 않는다. |
| BOOT-05 | 제목 변경 | `링커 근거`를 `근거`로 변경한다. |
| BOOT-06 | SHA-256 문구 축약 | 사용자가 지정한 두 문장만 유지한다. |
| BOOT-07 | 실제 Alignment 이미지 사용 | Notion의 실제 캡처를 로컬 정적 파일로 저장하고 만료형 URL을 노출하지 않는다. |
| BLACKBOX-01 | 통합 산출물 페이지 생성 | `artifacts/black-box/index.html`에 `code`, `test`, `document`, `demo` 섹션을 구성한다. |
| BLACKBOX-02 | 네 버튼 연결 | 메인 CODE/TEST/DOCUMENT/DEMO 버튼이 통합 페이지의 해당 앵커를 새 탭으로 연다. |
| CREDENTIAL-01 | 확대 이미지 생성 | 마스킹 PDF 첫 페이지를 고해상도 PNG로 렌더링한다. |
| CREDENTIAL-02 | 카드 동작 변경 | 자격·수상 카드는 PDF 다운로드 대신 확대 이미지를 새 탭으로 연다. PDF 원본은 보존한다. |
| CLEANUP-01 | 참조 검사 | HTML/CSS/테스트에서 참조되지 않는 파일만 삭제 후보로 분류한다. |
| CLEANUP-02 | 과거 작업 문서 정리 | 현재 변경의 spec/plan을 제외한 과거 `docs/superpowers` 작업 문서를 제거한다. |
| CLEANUP-03 | 필수 파일 보존 | 사이트 HTML, CSS, 이미지, PDF 원본, 테스트, README는 삭제하지 않는다. |
| CLEANUP-04 | 삭제 후 검증 | 로컬 링크 존재 검사와 전체 단위 테스트를 통과한다. |
| VERIFY-01 | 자동 회귀 테스트 | 각 ID를 검증하는 테스트가 존재하고 전체 테스트가 통과한다. |
| VERIFY-02 | 검증 기록 | `docs/verification/2026-07-27-portfolio-refinement.md`에 ID별 결과를 기록한다. |

## Architecture

- 기존 `index.html`은 원본 구조를 유지하고 정확한 문자열 치환으로만 수정한다.
- Bootloader 실제 캡처는 `assets/images/bootloader/alignment-*.png`에 보관한다.
- Black Box 산출물은 하나의 독립 HTML 페이지와 기존 로컬 PNG 자산으로 구성한다.
- 자격·수상 확대 이미지는 `assets/evidence/fullsize/*.png`에 보관한다.
- PDF는 원본성 보존을 위해 유지하며 사용자 인터페이스에서만 이미지 링크로 전환한다.
- 정리는 과거 Superpowers 설계·계획 문서에 한정하며 런타임 및 증빙 자산은 보존한다.

## Testing

- `tests/test_portfolio_refinement.py`에서 ID별 요구사항을 검증한다.
- 기존 `tests/test_portfolio.py`의 PDF 링크 기대값은 확대 이미지 동작에 맞게 수정한다.
- `python -m unittest discover -s tests -v`를 실행한다.
- HTML의 모든 로컬 `href`와 `src` 대상이 존재하는지 검사한다.
- 저장소에 `prod-files-secure.s3` 또는 `X-Amz-` 문자열이 없는지 검사한다.
