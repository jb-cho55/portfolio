# Vehicle SW QA Portfolio

조정빈의 차량 소프트웨어 개발·검증 포트폴리오입니다.  
CANoe/CAPL 기반 테스트 설계·자동화 검증과 AURIX 기반 OTA Bootloader 구현 경험을 중심으로 구성했습니다.

**Portfolio:** https://jb-cho55.github.io/portfolio

## 주요 내용

- **IVS Black Box Testing**  
  요구사양 분석, CANdb·CANoe 환경 구성, CAPL 자동화, 정적·동적 결함 분석
- **OTA Bootloader**  
  UDS 리프로그래밍, Flash Backup·Restore, SHA-256 무결성 검사, Memory Alignment Error 분석
- **자격·수상 증빙**  
  IVS 수료증, 프로젝트 우수상, 모범상, 정보처리기사, ISTQB CTFL 개인정보 마스킹 증빙 PDF

## 저장소 구조

```text
.
├── index.html                    # 포트폴리오 페이지
├── assets/
│   ├── images/black-box/         # Black Box Testing 실제 화면
│   └── evidence/                 # 개인정보 마스킹 자격·수상 PDF와 썸네일
└── tests/test_portfolio.py       # 콘텐츠·접근성 회귀 테스트
```

## 로컬 실행

별도 빌드 과정이 없는 정적 웹사이트입니다.

```bash
python -m http.server 8000
```

브라우저에서 `http://localhost:8000`으로 접속합니다.

## 테스트

```bash
python -m unittest discover -s tests -v
```

## 공개 범위

프로젝트 원본 저장소와 소스 코드는 비공개로 유지합니다. 포트폴리오에는 공개 가능한 실제 수행 화면과 식별번호·검증 코드를 마스킹한 자격·수상 PDF만 포함합니다.
