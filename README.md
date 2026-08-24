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

아래 순서는 전체 테스트, 브라우저 검증, 백업 번들 해시 확인을 마친 release gate에서만 실행합니다. 각 명령이 성공한 것을 확인한 뒤 다음 단계로 이동합니다.

1. 검증을 마친 배포 대상의 commit SHA를 고정합니다.

   ```powershell
   $releaseSha = git rev-parse HEAD
   if ([string]::IsNullOrWhiteSpace($releaseSha)) { throw "Release SHA를 확인할 수 없습니다." }
   ```

2. 원격 `main`이 백업한 기존 SHA와 정확히 같은지 확인합니다. 다르면 중단하고 원격 변경 사항을 먼저 조사합니다.

   ```powershell
   $expectedOldMain = "661b9d5186028318a1f181f4f7b0e8a822f1da63"
   $remoteMain = git ls-remote origin refs/heads/main | ForEach-Object { ($_ -split '\s+')[0] }
   if ($remoteMain -ne $expectedOldMain) { throw "원격 main이 백업 기준과 다릅니다." }
   ```

3. 로컬 HEAD가 고정한 release SHA에서 바뀌지 않았을 때만 guarded push를 실행하고, 원격이 그 SHA를 가리키는지 다시 확인합니다.

   ```powershell
   if ((git rev-parse HEAD) -ne $releaseSha) { throw "검증 후 로컬 HEAD가 변경됐습니다." }
   git push --force-with-lease=refs/heads/main:661b9d5186028318a1f181f4f7b0e8a822f1da63 origin HEAD:refs/heads/main
   if ($LASTEXITCODE -ne 0) { throw "Guarded push가 실패했습니다." }
   $publishedMain = git ls-remote origin refs/heads/main | ForEach-Object { ($_ -split '\s+')[0] }
   if ($publishedMain -ne $releaseSha) { throw "원격 main이 release SHA와 다릅니다." }
   ```

4. push가 성공한 뒤에만 Pages의 **Build and deployment** source를 **GitHub Actions**로 변경합니다. CLI 명령 대신 GitHub UI의 `Settings → Pages → Build and deployment → Source → GitHub Actions`를 사용해도 됩니다.

   ```powershell
   gh api --method PUT repos/jb-cho55/portfolio/pages -f build_type=workflow
   if ($LASTEXITCODE -ne 0) { throw "Pages source 변경이 실패했습니다." }
   ```

5. 고정한 release SHA로 실행을 조회하고, 반환된 `headSha`가 일치하는 실행만 기다립니다. 실행 결과가 성공인지 확인하고 실패 로그도 검사합니다.

   ```powershell
   $runs = gh run list --workflow pages.yml --branch main --event push --commit $releaseSha --limit 1 --json databaseId,headSha | ConvertFrom-Json
   $run = $runs | Select-Object -First 1
   if ($null -eq $run) { throw "Release SHA의 workflow 실행을 찾지 못했습니다." }
   if ($run.headSha -ne $releaseSha) { throw "조회한 workflow의 headSha가 release SHA와 다릅니다." }
   gh run watch $run.databaseId --exit-status
   $result = gh run view $run.databaseId --json headSha,status,conclusion,url | ConvertFrom-Json
   if ($result.headSha -ne $releaseSha -or $result.conclusion -ne "success") { throw "Release workflow가 성공하지 않았습니다." }
   gh run view $run.databaseId --log-failed
   ```

6. Pages 설정과 공개 홈·세 사례 경로를 직접 검증합니다. 네 경로가 모두 HTTP 200을 반환하기 전에는 게시가 완료됐다고 판단하지 않습니다.

   ```powershell
   $pages = gh api repos/jb-cho55/portfolio/pages | ConvertFrom-Json
   if ($pages.build_type -ne "workflow") { throw "Pages build_type이 workflow가 아닙니다." }
   $routes = @(
     "https://jb-cho55.github.io/portfolio/",
     "https://jb-cho55.github.io/portfolio/artifacts/black-box/",
     "https://jb-cho55.github.io/portfolio/artifacts/carmaker/",
     "https://jb-cho55.github.io/portfolio/artifacts/bootloader/"
   )
   foreach ($route in $routes) {
     $status = curl.exe --silent --show-error --output NUL --write-out "%{http_code}" $route
     if ($status -ne "200") { throw "$route returned HTTP $status" }
   }
   ```

`workflow_dispatch`는 테스트 확인용이며 deploy job은 `refs/heads/main` push에서만 실행됩니다.
