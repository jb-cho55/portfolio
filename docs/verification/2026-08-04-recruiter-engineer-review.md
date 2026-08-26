# Recruiter / Engineer Review Verification

채용담당자(가독성)와 직무담당자(전문성·깊이) 두 관점 점검 결과의 1차 반영분.

| ID | Verification | Status |
|---|---|---|
| A-01 | 히어로와 클로징 양쪽에 연락 가능한 `mailto` 배치 | PASS |
| A-05 | 국민대학교 재학·졸업 기간(2020.03–2026.02) 표기 | PASS |
| B-01 | SHA-256 검사의 범위·한계를 Bootloader 카드에 명시 (HMAC·전자서명 아님, 해시 재계산 공격 불가) | PASS |
| B-02 | Black Box CAPL 발췌를 원본 소스 그대로 교체 — 지어낸 `setTimer(detectionTimer, 1)` 제거 | PASS |
| B-03 | 구현 후 정적 코드 리뷰 발견사항을 `#bootloader-review` 블록으로 노출 | PASS |
| B-05 | UDS 서비스 개수 표기를 7개(0x10·0x27·0x31·0x34·0x36·0x37·0x11)로 통일, `0x31` 이중 사용 명시 | PASS |
| B-10 | CANdb Factor 0.001 미적용 결함(회복 임계 15mV)을 대표 검출 결과에 승격 | PASS |
| C-01 | 동적 결함 판정 화면 10장을 `assets/images/black-box/result_*.png`로 게시하고 TEST 섹션에 연결 | PASS |
| C-01b | 강사 요구사양 PDF 캡처(`req_p*`, `static_req*`, `static_ref*`, `static_defect*`)는 공개 자산에서 제외 | PASS |
| FIX-01 | `trace32-restore.html`의 Trap Vector 값 기대치를 실제 캡처 기준으로 정정 (`PC = 0x80027840`) | PASS |
| FIX-02 | `trace32-restore.html` Restore 방향에 `EA_AppRestore()` 함수명 보강 | PASS |
| A-02 | 저장소 비공개 사유를 프로젝트 도입부에 명시 | PASS |
| A-03 | 히어로에 직무 한 줄 소개 추가 | PASS |
| A-07 | 테스트 규모 모수 표기 (스크립트 6종·테스트케이스 24개, 단일 시나리오 404조합) | PASS |
| A-08 | `assets/og-card.png` 생성 및 `og:image`·`twitter:card` 선언 | PASS |
| A-09 | 산출물 섹션에 "엔지니어 검토용" 안내 문구 | PASS |
| B-04 | 메인 Bootloader 카드에 `근거 수준` 항목 추가 — 교육 당시 ECU 시험 기록 vs 현재 정적 대조 범위 구분 | PASS |
| B-06 | `TestWaitForMessage`·`setTimerCyclic` 실제 CAPL API명 병기 | PASS |
| B-07 | 경계값 분석·동등분할·상태 전이 테스트 기법명 명시 | PASS |
| B-08 | A-SPICE SWE.6 추적 관점 명시 | PASS |
| B-09 | ISO 26262·MISRA C·Polyspace를 교육 이수 수준으로 표기 | PASS |
| B-11 | 제공된 AURIX·MCAL 교육 환경 기반임을 역할 설명에 명시 | PASS |
| C-02 | 검증 프로젝트를 PROJECT 01로 재배치, 라벨과 도입부 문구 갱신 | PASS |
| C-04 | 기타 프로젝트 3건(CarMaker ADAS · 보안 CAN 네트워크 · DeepRacer 캡스톤) 링크 | PASS |
| FIX-03 | 프로젝트 카드 슬라이스가 카드 순서에 의존하던 테스트 8곳을 `tests/portfolio_sections.card()`로 통일 | PASS |
| FIX-04 | 본문 inline `<code>`가 전역 규칙 없이 브라우저 기본 monospace로 렌더되던 문제 — `.project-summary code, .detail-block code`에 `.debug-step code`와 동일한 처리 적용 | PASS |
| FIX-05 | `.artifact-grid`가 산출물 5개용 5열 고정이라 기타 프로젝트 3장이 컨테이너 3/5 폭에 몰리던 문제 — `@media(min-width:901px)`로 3열 지정 | PASS |
| FIX-06 | 결함 갤러리 카드가 행 높이만큼 늘어나 짧은 이미지 밑에 빈 공간이 생기던 문제 — `align-items:start` | PASS |
| UI-01 | 부트로더 근거 자료 4페이지를 `artifacts/bootloader/index.html` 1페이지 + 앵커 4개로 통합 — 블랙박스와 동일 모델 | PASS |
| UI-02 | 프로젝트 카드 안에서 두 번 반복되던 산출물 링크 그리드 제거 (디버깅 캡처 2장은 유지) | PASS |
| UI-03 | 통합 전 `test-results`의 "근거 보기" 링크가 `trace32-restore.html#restore-results` 등 **존재하지 않는 앵커**를 가리키던 문제 정정 | PASS |
| UI-04 | 산출물 링크 8개를 새 탭이 아닌 현재 창 이동으로 변경 (이미지·PDF·GitHub은 새 탭 유지) | PASS |
| UI-05 | `.project-meta`·`.meta-grid` 5등분 → `repeat(4, max-content) minmax(0,1fr)`. `담당 범위`만 줄바꿈되고 `1명`·`100%` 칸이 낭비되던 문제 해소 | PASS |
| UI-06 | 구현 문장에서 `0x31`만 볼드로 튀던 문제 — `<code>` 제거 | PASS |
| UI-07 | 이력서 PDF 자리(`.contact-resume`) 추가. `assets/resume.pdf` 배치 후 `hidden`만 제거하면 노출되며, 파일 유무와 `hidden` 상태 불일치를 테스트가 잡는다 | PASS |
| UI-08 | 산출물 페이지 섹션 탭을 sticky로 변경하고, 두 페이지에 중복 정의돼 있던 `.artifact-nav` CSS를 shared.css 한 곳으로 통합 | PASS |
| UI-09 | 프로젝트 상세 아코디언을 산출물 페이지로 통합 — 메인은 요약 카드만, 깊이는 프로젝트당 한 곳. 토글 버튼·detail region·아코디언 JS·관련 CSS 32개 규칙 삭제 | PASS |
| UI-10 | 통합 과정에서 드러난 중복 제거 — 블랙박스 실행 화면 갤러리(DEMO와 동일 5장), 부트로더 4단계 요약(TRACE32 7단계와 중복), `alignment-trap.png`·`alignment-breakpoint.png`(원본과 SHA-256 동일한 사본) | PASS |
| UI-11 | 메타 행 좌우에 남던 회색 띠 제거 — 컨테이너 배경을 흰색으로 두고 구분선은 셀 `border-left`로 이동 | PASS |
| UI-12 | 메타 행 5칸을 `repeat(5, minmax(max-content, 1fr))`로 배치 — 칸이 왼쪽에 몰리고 오른쪽 1/4이 비던 문제 해소, 세로 중앙 정렬 추가 | PASS |
| UI-13 | 아코디언을 없앤 자리에 `근거 자료 전체 보기 →` 링크 추가 — 카드마다 깊이로 가는 진입점 확보 | PASS |
| UI-14 | 사이드 섹션 레일 신설 (1400px 이상). IntersectionObserver로 현재 섹션 표시, 패널·13px·`#46536a`로 가독성 확보, 본문 폭 바깥에 고정해 카드와 겹치지 않음 | PASS |
| VERIFY-01 | ID 기반 회귀 테스트 | PASS |
| VERIFY-02 | 본 검증 기록 작성 | PASS |

## Commands

- `python -m unittest discover -s tests -v` — 76 tests, OK
- CSS 중괄호 균형 검사 — `index.html` 175/175, `shared.css` 62/62
- 고립 마크업 기호 스캔 — 0건
- `python -m http.server 8000` + Chrome 실제 렌더링 확인 (히어로 · 두 프로젝트 카드 · 메타 행 · sticky 섹션 탭 · OVERVIEW · CODE REVIEW · 결함 갤러리 10장 · CAPL 코드 블록 · 기타 프로젝트 · 학력)
- HTML 구조 감사 — 태그 짝·미닫힘·중복 id·헤딩 레벨 점프 0건
- 링크·앵커 검증 99건 — `assets/resume.pdf`(의도된 hidden 자리표시자) 외 문제 0건
- 콘솔 오류 0건

## 근거 메모

- **FIX-01**: 기존 테스트가 기대하던 `PC = 0x7000EC24`는 `assets/images/bootloader/trap-vector-breakpoint.png`(Trace32 Register view 캡처) 어디에도 없다. 캡처의 실제 값은 `PC 80027840`, `BTV 80027800`, `A5 7000240D`이며 페이지 기술이 옳았다. 이 실패는 본 작업 이전부터 존재했다.
- **C-01**: 게시한 10장은 모두 CANoe 테스트 리포트의 판정 행이며, 게시 전 전수 육안 확인했다. 요구사양 문서 내용이나 개인정보는 포함되지 않는다. 동적 결함 11건 중 Brake·Accel·Vehicle 독립 검출 결함 1건은 캡처가 없어 문서로만 남겼고, 페이지에도 그렇게 밝혔다.
- **FIX-04~06**: 브라우저로 실제 렌더링을 보기 전에는 셋 다 드러나지 않았다. 문자열 단위 테스트만으로는 잡히지 않는 종류의 결함이라, 회귀 테스트를 CSS 선언 존재 여부로 걸어 두었다.
- **B-03**: 노출한 발견사항은 정적 검토 결과이며, 개선안을 구현·빌드·ECU 검증한 결과가 아니라는 점을 같은 블록에 명시했다.

## 제외 판단

- **`IVS_JETRACER`는 기타 프로젝트에 넣지 않았다.** 2024 SEA:ME 해커톤 주최측 스타터 저장소를 받은 형태라 README가 본인 글이 아니고 머지 충돌 마커가 남아 있다. 면접에서 말할 경험 소재로는 유효하지만 열람용 산출물로는 오히려 신뢰를 깎는다.
- **화이트박스·커버리지는 표기하지 않았다.** 수행 이력이 없으므로 "학습 중" 표기도 넣지 않는다.

## UI 판단 근거

부트로더 카드가 22,518자, 블랙박스 카드가 9,695자로 2.3배였다. 원인은 디자인이 아니라 정보구조 두 가지 — 같은 곳으로 가는 링크 그리드가 카드 안에서 두 번 반복됐고, 산출물 모델이 프로젝트마다 달랐다(블랙박스 1페이지+앵커 vs 부트로더 4페이지). 전면 리디자인 대신 중복 제거와 모델 통일로 처리했다. 파일 4개가 1개로 줄었다.

## 통합 후 구조

```
index.html                       요약 카드 2개 + 산출물 링크 + 기타 프로젝트
artifacts/black-box/index.html   OVERVIEW · CODE · TEST · DOCUMENT · DEMO
artifacts/bootloader/index.html  OVERVIEW · MEMORY MAP · UDS · TEST · TRACE32 · CODE REVIEW
```

깊이 있는 내용은 프로젝트당 산출물 페이지 한 곳에만 둔다. `index.html`은 56,998자에서 42,220자로 줄었다.

## 작업 중 스스로 만든 결함 2건

렌더링을 직접 보지 않았으면 놓쳤을 것들이라 기록해 둔다.

- **CSS 규칙 반쪽 삭제** — `.detail-block` 관련 CSS를 정규식으로 지우면서 `.project-summary code, .detail-block code {…}` 규칙의 뒷줄만 잘려 `.project-summary code,` 가 남았다. 그 상태로는 바로 다음 `.project-summary` 규칙까지 무효가 돼 카드 패딩이 사라진다. 메인에 `<code>`가 하나도 남지 않았으므로 규칙 자체를 제거하는 것으로 정리했다.
- **마크업 잔해 `>`** — detail region 제거에 쓴 `</?div\b` 패턴이 닫는 `>`를 포함하지 않아 두 카드 하단에 `>` 문자가 남았다. HTML 파서 감사는 이를 본문 텍스트로 보기 때문에 잡지 못했고, 화면을 보고서야 발견했다.
- **메타 행 회색 띠를 두 번 놓침** — 처음에는 줄바꿈만 보고 "한 줄에 들어가니 해결"로 판단했고, 행 양 끝에 남은 회색 padding 띠를 보지 못했다. 사용자가 캡처를 보내준 뒤에야 원인을 찾았다. 화면을 봤더라도 무엇을 볼지 정하지 않으면 놓친다.

## Residual

- 이력서 PDF 미보유 — 연락 경로는 이메일만 제공한다.
- A-SPICE 단과과정과 함께 표기된 "취업특강"을 학습 이력에 남길지는 미결이다.
- 모바일 실물 렌더링은 확인하지 않았다. 데스크톱 열람이 주 경로라 우선순위에서 제외한다는 판단이며, 미해결 위험이 아니다. 기존 미디어쿼리(`900px`·`700px`·`600px`)와 `flex-wrap`은 그대로 유지하고, 사이드 레일은 `1400px` 이상에서만 나타나므로 좁은 화면에서는 상단 sticky 내비가 같은 역할을 한다.
- 이메일은 난독화 없이 `mailto`로 노출한다. 스크립트 실패 시 연락 경로가 사라지는 위험보다 스팸 수신 비용이 작다고 판단했다.
