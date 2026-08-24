# 조정빈 · Vehicle Software Engineer Portfolio

차량 소프트웨어 검증 프로젝트를 재현 가능한 근거와 명시적인 한계 중심으로 정리한 정적 포트폴리오입니다. 공개 사이트는 `site/`만 배포하며, 빌드 단계나 클라이언트 JavaScript가 필요하지 않습니다.

## 로컬 실행

저장소 루트에서 다음 명령을 실행한 뒤 `http://localhost:8000/`을 엽니다.

```powershell
python -m http.server 8000 --directory site
```

## 검증

```powershell
python -B -m unittest discover -s tests -v
```

테스트는 콘텐츠 범위, 내부 링크와 프래그먼트, 접근성 기본 계약, 메타데이터, 사이트맵, Pages 배포 게이트를 검사합니다.

## 콘텐츠 출처

- 기존 공개 포트폴리오에서 검증한 Black Box 및 Bootloader 설명과 증거 자료
- 공개 저장소 [`jb-cho55/IVS-CarMaker-ADAS`](https://github.com/jb-cho55/IVS-CarMaker-ADAS)의 CarMaker 협업 기록과 이미지
- 각 사례 페이지에 표시한 측정 범위, 개인 기여 경계, 공개할 수 없는 자료 및 재검증 한계

보호된 교육 자료, 비공개 요구사항 캡처, 만료될 수 있는 Notion 링크, 자격 증명은 배포 대상에 포함하지 않습니다.

## clean-history 백업

기존 `main` 전체 이력은 로컬 번들 `C:\Users\gmkk6\Documents\포트폴리오\portfolio-history-backup-2026-08-24.bundle`에 보존되어 있습니다.

- 기존 원격 `main`: `661b9d5186028318a1f181f4f7b0e8a822f1da63`
- 번들 SHA-256: `F9BFDA1B29213338A25D4E067B7CD13458340E7689A953B6D02EFB49944077B0`

원격 이력을 교체하기 전에는 번들의 무결성과 복원 가능성을 다시 확인해야 합니다.

## 게시 절차

1. 전체 테스트와 브라우저 검증을 통과합니다.
2. 백업 번들 해시와 기존 원격 `main` SHA를 확인합니다.
3. 보호된 release gate에서 clean-history 브랜치를 원격 `main`으로 갱신합니다.
4. `main` push로 시작된 **Test and deploy GitHub Pages** 워크플로가 test job을 통과한 뒤 `site/`만 배포하는지 확인합니다.

`workflow_dispatch`는 테스트 확인용이며 deploy job은 `refs/heads/main` push에서만 실행됩니다.
