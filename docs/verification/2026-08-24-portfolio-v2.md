# Portfolio v2 verification record

검증일: 2026-08-24
대상 브랜치: `rebuild/engineering-editorial`
범위: 홈과 3개 사례 페이지의 로컬 릴리스 게이트. 이 기록은 게시를 수행하지 않는다.

## 실행 환경과 명령

실제 정적 사이트는 저장소 루트에서 다음 명령으로 제공했다.

```powershell
python -m http.server 8011 --directory site
```

최종 자동 검증 명령은 다음과 같다.

```powershell
python -B -m unittest discover -s tests -v
git diff --check
git fsck --no-dangling
git status --short --branch
```

링크와 배포 경로는 테스트의 `test_every_local_href_src_and_fragment_resolves` 및 `test_references_resolve_at_root_and_github_pages_mounts`로 루트 마운트와 `https://jb-cho55.github.io/portfolio/` 마운트 모두 확인했다.

## 브라우저 뷰포트 매트릭스

Codex 인앱 브라우저에서 홈, Black Box Validation, CarMaker ADAS, OTA Bootloader 네 페이지를 각각 검사했다. 각 조합에서 `documentElement.clientWidth`와 최대 `scrollWidth`를 비교하고, `lang=ko`, main 1개, h1 1개, skip target, 이미지 콘텐츠 박스 비율을 확인했다.

| 뷰포트 | 검사 페이지 | clientWidth / scrollWidth | 결과 |
| --- | --- | --- | --- |
| 1440×900 | 홈 + 사례 3개 | 1425 / 1425 | PASS |
| 1024×768 | 홈 + 사례 3개 | 1009 / 1009 | PASS |
| 768×1024 | 홈 + 사례 3개 | 753 / 753 | PASS |
| 390×844 | 홈 + 사례 3개 | 375 / 375 | PASS |
| 320×568 | 홈 + 사례 3개 | 305 / 305 | PASS |

총 20개 페이지·뷰포트 조합에서 가로 페이지 오버플로, 의미 구조 실패, 이미지 비율 오차가 없었다. 1440×900과 320×568에서는 긴 페이지를 끝까지 스크롤해 모든 지연 로딩 이미지를 실제로 로드했고, 깨진 이미지 0건을 확인했다. 사이트에는 `table` 또는 `pre` 요소가 없어 코드·표 래퍼 검사는 해당 없음이다.

브라우저 콘솔의 error/warn 로그는 0건이었다.

## 브라우저에서 확인해 수정한 결함

### 320px 최소 너비

- 수정 전 320×568: `html.clientWidth=305`, `html.scrollWidth=320`, `body min-width=320px`, 가로 오버플로 발생.
- 수정: `body`의 `min-width: 320px` 제거.
- 수정 후 같은 뷰포트: `html.clientWidth=305`, `html.scrollWidth=305`, `body min-width=0px`, 가로 오버플로 없음.

### 좁은 에디토리얼 레일의 단어 중간 줄바꿈

768px와 1024px에서 `VERIFICATION`, `INTEGRATION`이 단어 중간에서 나뉘는 것을 화면으로 확인했다. `.eyebrow`, `.section-kicker`, `.project-label`, `.timeline-label`에 `overflow-wrap: normal`과 `word-break: keep-all`을 적용했다. 768px, 1024px, 320px에서 다시 확인했으며 단어는 온전히 유지되고 페이지 가로 오버플로는 없다.

### 200% 줌 등가 경계

브라우저 제어 표면이 직접 줌 값을 제공하지 않아 1440×900을 200%로 본 것과 같은 CSS 레이아웃 폭인 720×450으로 검사했다. 수정 전 네 페이지 모두 `clientWidth=705`, `scrollWidth=717`이었고, 원인은 720px 경계에서 3열 `timeline`의 최소 열 폭이었다. 720–767px 구간에서 `timeline article`만 단일 열로 바꾼 후 네 페이지 모두 `705 / 705`로 PASS했다. 보조로 1280px 화면의 200% 등가인 640×450도 네 페이지 모두 `625 / 625`로 PASS했다.

### 다크 연락처 섹션의 초점 대비

전역 포커스 색상 `#2f6662`는 연락처 배경 `#202321`에서 `2.42:1`로, 비텍스트 초점 표시의 3:1 기준에 미달했다. `.contact-section :focus-visible`의 outline만 `var(--footer-ink)` (`#f3f2ed`)로 재정의해 대비를 `14.15:1`로 높였다. 회귀 테스트는 수정 전 `2.42:1`을 보고하며 RED였고 수정 후 GREEN이었다. 이 후속 수정에서는 브라우저 런타임을 사용할 수 없어 실제 화면 재확인은 최종 controller 검증 대상으로 남겼다.

## 키보드와 포커스

390×844에서 네 페이지의 모든 링크 49개(홈 13, Black Box 11, CarMaker 14, Bootloader 11)를 키보드 locator로 각각 포커스했다. 모두 실제 활성 요소가 되었고, `:focus-visible`이 일치하며 2px 이상의 solid outline이 보였다. 각 페이지의 첫 skip link는 포커스 시 화면 안으로 이동했고 `#main-content` 대상이 존재했다.

제약: 브라우저 자동화 표면의 raw Tab/Enter 입력은 bounded 재시도에서도 active element를 순차 이동하거나 skip link를 활성화하지 않았다. 따라서 OS 수준의 실제 Tab 순서와 Enter 활성화는 이번 세션에서 직접 관찰하지 못했다. 대신 DOM상 skip link가 첫 focusable link임을 확인했고, 모든 링크의 포커스 가능성·포커스 표시와 모든 fragment target은 브라우저 검사 및 unittest로 검증했다.

## HTTP와 자동 테스트

다음 로컬 경로는 모두 HTTP 200을 반환했다.

- `/`
- `/artifacts/black-box/`
- `/artifacts/carmaker/`
- `/artifacts/bootloader/`

추가로 CSS, OG PNG, PDF 증빙, robots.txt, sitemap.xml도 200이었고 명백히 존재하지 않는 경로는 404였다.

최종 테스트 결과: `Ran 40 tests` / `OK` / exit 0.

## Git과 복구 증거

- `git diff --check`: exit 0.
- `git fsck --no-dangling`: exit 0.
- 추적 파일 목록을 검토했으며 clean-root 사이트, 테스트, 문서, Pages workflow와 승인된 증거 자산만 포함한다.
- 이전 원격 main: `661b9d5186028318a1f181f4f7b0e8a822f1da63`.
- 전체 이력 백업: `C:\Users\gmkk6\Documents\포트폴리오\portfolio-history-backup-2026-08-24.bundle`.
- 백업 SHA-256: `F9BFDA1B29213338A25D4E067B7CD13458340E7689A953B6D02EFB49944077B0`.
- `git bundle verify`는 6개 ref와 complete history를 확인했다.

## 알려진 한계와 릴리스 판정

- 직접 200% 브라우저 줌/OS 확대를 바꾸지 못해 CSS viewport 등가 검사로 대체했다.
- raw Tab/Enter 순차 동작은 브라우저 자동화 제한으로 직접 관찰하지 못했다.
- 실제 GitHub Pages 배포와 배포 URL 확인은 이 작업 범위 밖이다.

로컬 릴리스 후보는 위 검증을 통과했다. Tasks 1–5 동안 원격 push, Pages 설정 변경, 게시를 수행하지 않았다.
