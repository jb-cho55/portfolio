# 실제 프로젝트 이미지 및 증빙 PDF 공개 설계

## 목적

기존 포트폴리오의 재구성 SVG를 제거하고, Black Box Testing 비공개 저장소에 보존된 실제 PNG 화면을 사용한다. 자격·수상 섹션에는 사용자가 제공한 원본 PDF 5개를 수정·마스킹 없이 추가하고, 썸네일 또는 링크 클릭 시 새 탭에서 원본 PDF를 열 수 있도록 한다.

## 공개 전제

- GitHub Pages에 배포된 PNG와 PDF는 누구나 열람·저장할 수 있다.
- 사용자는 생년월일, 증서번호, 자격번호, QR 코드, 증명사진을 포함한 원본 PDF의 공개를 승인했다.
- Private 프로젝트 저장소 자체의 URL과 소스 코드는 공개하지 않는다.
- Notion의 만료형 첨부 URL은 사용하지 않고, 필요한 파일을 포트폴리오 저장소의 정적 자산으로 복사한다.

## Project 01 — Black Box Testing 실제 이미지

기존 `assets/images/*.svg` 재구성 자료 4개를 제거하고 다음 실제 PNG를 `assets/images/black-box/`에 복사한다.

1. `network_setup.png` — CANoe Network 구성
2. `test_environment.png` — CANoe 테스트 환경
3. `automation_test_environment.png` — CAPL 자동화 테스트 환경
4. `panel_trace.png` — Panel 및 Trace 화면
5. `defect_batt_percent_15.png` — Batt Percent 15% Test Result

각 이미지는 다음 방식으로 표시한다.

- 데스크톱 2열, 900px 이하 1열
- 원본 비율 유지, `object-fit: contain`
- `loading="lazy"`, 구체적인 `alt`, 화면 의미를 설명하는 캡션 적용
- 썸네일 클릭 시 동일 PNG를 새 탭에서 원본 크기로 열기
- 실제 프로젝트 화면이므로 `포트폴리오 재구성` 문구는 제거

## 자격·수상 증빙

다음 원본 PDF를 `assets/evidence/`에 저장한다.

1. `ivs-completion-certificate.pdf` — HL만도·HL클레무브 IVS 5기 수료증
2. `black-box-testing-award.pdf` — Black Box Testing 프로젝트 우수상
3. `ivs-excellence-award.pdf` — IVS 모범상
4. `information-processing-engineer.pdf` — 정보처리기사
5. `istqb-ctfl-certificate.pdf` — ISTQB CTFL

각 PDF의 첫 페이지를 썸네일 이미지로 변환해 `assets/evidence/thumbnails/`에 저장한다.

- 썸네일 형식: WebP 또는 PNG
- 긴 세로 문서는 카드 내부에서 일정 높이로 잘라 보이게 하지 않고 `object-fit: contain`으로 전체 형태 유지
- 카드 클릭 또는 `원본 PDF 보기` 링크 클릭 시 `target="_blank"`로 원본 PDF 열기
- 브라우저 기본 PDF 뷰어 사용
- 원본 PDF는 수정·마스킹·압축 재저장을 하지 않는다

## 자격·수상 섹션 구조

기존 텍스트 목록을 유지하되 증빙이 있는 항목에는 `증빙 보기`를 추가한다.

- Black Box Testing 프로젝트 우수상
- IVS 모범상
- HL만도·HL클레무브 IVS 5기 수료
- 정보처리기사
- ISTQB CTFL

각 항목은 제목, 발급·수여 기관, 취득일 또는 교육 기간, 썸네일, `원본 PDF 보기`로 구성한다. 증빙이 없는 기존 항목은 텍스트 카드로 유지한다.

## 상호작용 및 접근성

- PDF 링크에는 `aria-label`로 문서명을 명확히 제공한다.
- 새 탭 열림을 시각 텍스트로 표시한다.
- 썸네일 이미지에 문서 종류와 발급기관을 포함한 `alt`를 제공한다.
- 키보드 사용자가 카드 또는 링크에 접근할 수 있도록 `:focus-visible` 스타일을 적용한다.
- 별도 JavaScript PDF 모달은 도입하지 않는다.

## 구현 범위

- `index.html`: 실제 PNG 경로, 이미지 링크, 증빙 카드, PDF 링크, 썸네일 스타일 반영
- `assets/images/black-box/`: 실제 PNG 5개 추가
- `assets/images/`: 기존 재구성 SVG 4개 제거
- `assets/evidence/`: 원본 PDF 5개 추가
- `assets/evidence/thumbnails/`: PDF 첫 페이지 썸네일 5개 추가
- `tests/test_portfolio.py`: 실제 PNG 경로, SVG 제거, PDF 링크·새 탭·접근성 검증
- `README.md`: 실제 프로젝트 화면과 원본 증빙 PDF 공개 구조 반영

## 검증 기준

1. 기존 재구성 SVG 4개가 저장소와 HTML에서 제거된다.
2. 실제 PNG 5개가 Black Box Testing 상세 영역에 표시된다.
3. 각 PNG는 클릭 시 원본 파일을 새 탭에서 연다.
4. 원본 PDF 5개가 `assets/evidence/`에 존재한다.
5. 자격·수상 항목 5개에서 PDF 링크가 노출된다.
6. 모든 PDF 링크는 `target="_blank"`, `rel="noreferrer"`를 사용한다.
7. PDF 썸네일 5개가 깨지지 않고 표시된다.
8. 모든 이미지에 `alt`, 실제 프로젝트 이미지에는 캡션이 적용된다.
9. Private 프로젝트 저장소 URL은 HTML에 포함되지 않는다.
10. 기존 프로젝트 상세 펼침·접기와 모바일 단일 열 레이아웃이 유지된다.
11. Python 단위 테스트가 모두 통과한다.

## 제외 범위

- PDF 개인정보 마스킹
- PDF 내용 편집 또는 재발급
- Private 프로젝트 저장소 공개 전환
- Notion 만료형 이미지 URL 직접 사용
- 사이트 로그인 또는 접근 제어
- PDF 모달·iframe 뷰어 구현
