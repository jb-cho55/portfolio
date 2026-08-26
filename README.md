# Vehicle Embedded SW Portfolio

조정빈의 차량 소프트웨어 개발·검증 포트폴리오입니다.  
CANoe/CAPL 기반 테스트 설계·자동화 검증과 AURIX 기반 OTA Bootloader 구현 경험을 중심으로 구성했습니다.

**Portfolio:** https://jb-cho55.github.io/portfolio

## 주요 내용

- **OTA Bootloader**  
  UDS 리프로그래밍, Flash Backup·Restore, SHA-256 무결성 검사, Memory Alignment Error 분석
- **Bootloader 공개 기술 산출물**  
  실제 주소 기반 Memory Map, UDS Sequence Diagram, 근거 수준을 구분한 Test Results, Trace32 Alignment Trap·Restore 분석
- **IVS Black Box Testing**  
  요구사양 분석, CANdb·CANoe 환경 구성, CAPL 자동화, 정적·동적 결함 분석
- **자격·수상 증빙**  
  IVS 수료증, 프로젝트 우수상, 모범상, 정보처리기사, ISTQB CTFL 개인정보 마스킹 증빙 PDF

## 저장소 구조

```text
.
├── index.html
├── artifacts/bootloader/          # Bootloader 독립 기술 산출물 4개
├── assets/bootloader/             # Memory Map, UDS Diagram, 공통 스타일
├── assets/images/black-box/       # Black Box Testing 실제 화면
├── assets/evidence/               # 개인정보 마스킹 자격·수상 PDF와 썸네일
├── tests/test_portfolio.py
└── tests/test_bootloader_artifacts.py
```

## 로컬 실행

```bash
python -m http.server 8000
```

## 테스트

```bash
python -m unittest discover -s tests -v
```

## 공개 범위

두 대표 프로젝트는 개인 프로젝트입니다. Bootloader 산출물에는 개인 교육 프로젝트의 실제 메모리 주소, 함수명, 핵심 코드, Trace32 명령과 결과 요약을 공개합니다. 프로젝트 원본 저장소, 만료형 Notion 첨부 URL, 계정·인증정보는 공개하지 않습니다. 첨부 화면을 안정 파일로 내보낼 수 없는 경우에는 허위 이미지를 만들지 않고 코드·주소·관찰 결과를 텍스트로 제시합니다.
