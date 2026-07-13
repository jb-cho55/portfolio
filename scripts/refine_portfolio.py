from pathlib import Path


INDEX = Path("index.html")
TESTS = Path("tests/test_portfolio.py")
README = Path("README.md")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"{label} anchor not found")
    return text.replace(old, new, 1)


def refine_index() -> None:
    html = INDEX.read_text(encoding="utf-8")

    css_anchor = """    .project-note {
      color: var(--muted);
      font-size: 12px;
    }
"""
    css_add = """    .project-note {
      color: var(--muted);
      font-size: 12px;
    }

    .evidence-gallery {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }

    .evidence-item {
      overflow: hidden;
      margin: 0;
      border: 1px solid var(--line);
      border-radius: 9px;
      background: #fff;
    }

    .evidence-item img {
      display: block;
      width: 100%;
      aspect-ratio: 16 / 9;
      object-fit: contain;
      background: #eef2f7;
    }

    .evidence-item figcaption {
      padding: 10px 12px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 750;
    }

    .stage-list {
      display: grid;
      gap: 9px;
      margin: 12px 0 0;
      padding-left: 18px;
      color: var(--muted);
      font-size: 14px;
    }

    .debug-flow {
      display: grid;
      gap: 10px;
      margin-top: 12px;
    }

    .debug-step {
      padding: 12px 14px;
      border-left: 3px solid var(--blue);
      background: var(--blue-soft);
      color: #394962;
      font-size: 14px;
    }
"""
    if ".evidence-gallery {" not in html:
        html = replace_once(html, css_anchor, css_add, "detail CSS")

    media_anchor = """      .detail-block.wide {
        grid-column: auto;
      }
"""
    media_add = """      .detail-block.wide {
        grid-column: auto;
      }

      .evidence-gallery {
        grid-template-columns: 1fr;
      }
"""
    if "@media(max-width:900px)" in html and "      .evidence-gallery {\n        grid-template-columns: 1fr;" not in html:
        html = replace_once(html, media_anchor, media_add, "responsive gallery CSS")

    black_old = """                <article class="detail-block">
                  <h4>본인 수행 범위</h4>
                  <ul>
                    <li>CAN·UDS 요구사양과 Fault 상태 전이 조건 분석</li>
                    <li>CANdb 작성 및 CANoe Network Node 구성</li>
                    <li>CAPL 테스트 작성, Panel 입력 제어, Trace 분석</li>
                    <li>기대 결과·실제 결과·재현 조건·영향도 문서화</li>
                  </ul>
                </article>

                <article class="detail-block">
                  <h4>대표 검출 결과</h4>
                  <ul>
                    <li>정적 결함 4건: Signal Length, Value, Description 불일치</li>
                    <li>동적 결함 11건: 경계값, 선행 조건, Recovery, Timing 오류</li>
                    <li>Batt Percent 15% 경계값과 IGN 50 Cycle Off-by-One 확인</li>
                    <li>Steering Timing 요구사양 50±10ms 대비 약 1000±10ms 검출</li>
                  </ul>
                </article>

                <article class="detail-block wide">
                  <h4>QA 관점과 공개 범위</h4>
                  <p>요구사양 기반 시험에서 단순 Pass/Fail을 넘어 결함 근거와 영향도를 구조화했습니다. 원본 요구사양과 내부 자료는 제외하고, 직접 수행한 테스트 환경·결함 분석·개선 방향만 포트폴리오용으로 재구성했습니다.</p>
                </article>"""
    black_new = """                <article class="detail-block">
                  <h4>수행 범위</h4>
                  <ul>
                    <li>CAN·UDS 요구사양과 Fault 상태 전이 조건 분석</li>
                    <li>CANdb 작성 및 CANoe Network Node 구성</li>
                    <li>CAPL 테스트 작성, Panel 입력 제어, Trace 분석</li>
                    <li>기대 결과·실제 결과·재현 조건·영향도 문서화</li>
                  </ul>
                </article>

                <article class="detail-block">
                  <h4>대표 검출 결과</h4>
                  <ul>
                    <li>정적 결함 4건: Signal Length, Value, Description 불일치</li>
                    <li>동적 결함 11건: 경계값, 선행 조건, Recovery, Timing 오류</li>
                    <li>Batt Percent 15% 경계값과 IGN 50 Cycle Off-by-One 확인</li>
                    <li>Steering Timing 요구사양 50±10ms 대비 약 1000±10ms 검출</li>
                  </ul>
                </article>

                <article class="detail-block wide">
                  <h4>실제 수행 환경 및 Test Result</h4>
                  <div class="evidence-gallery">
                    <figure class="evidence-item">
                      <img src="assets/images/network_setup.svg" alt="IVS와 주변 ECU를 CAN 버스로 연결한 CANoe Network 구성도" loading="lazy">
                      <figcaption>CANoe Network 구성 · 포트폴리오 재구성</figcaption>
                    </figure>
                    <figure class="evidence-item">
                      <img src="assets/images/automation_test_environment.svg" alt="요구사양을 CAPL 시나리오와 Test Module로 실행하는 자동화 테스트 흐름" loading="lazy">
                      <figcaption>CAPL 자동화 테스트 환경 · 포트폴리오 재구성</figcaption>
                    </figure>
                    <figure class="evidence-item">
                      <img src="assets/images/panel_trace.svg" alt="Panel 입력 제어와 CAN Trace 확인 과정을 나타낸 검증 화면" loading="lazy">
                      <figcaption>Panel 및 Trace 화면 · 포트폴리오 재구성</figcaption>
                    </figure>
                    <figure class="evidence-item">
                      <img src="assets/images/defect_batt_percent_15.svg" alt="Batt Percent 15퍼센트 경계값의 기대 결과와 실제 결과를 비교한 Test Result" loading="lazy">
                      <figcaption>Test Result 근거 — Batt Percent 15% 경계값</figcaption>
                    </figure>
                  </div>
                </article>"""
    if "assets/images/network_setup.svg" not in html:
        html = replace_once(html, black_old, black_new, "Black Box detail")

    html = html.replace(
        "메모리 경계와 UDS 절차 설계, Flash 관리, 무결성 검사, Binary 변환, 디버깅과 사후 정적 코드 리뷰를 수행했습니다.",
        "메모리 경계와 UDS 절차 설계, Flash 관리, Backup·Restore, SHA-256 무결성 검사와 Trace32 디버깅을 수행했습니다.",
        1,
    )

    boot_old = """                <article class="detail-block">
                  <h4>대표 문제 해결</h4>
                  <p>Backup·Restore 중 발생한 Trap을 Trace32 레지스터와 Flash Loader 인수로 추적했습니다. <code>uint8</code> 버퍼가 Flash Loader의 4바이트 정렬 조건을 보장하지 않는 것을 확인하고 <code>uint32</code> 배열 기반 버퍼로 변경했습니다.</p>
                </article>

                <article class="detail-block">
                  <h4>정적 코드 리뷰</h4>
                  <ul>
                    <li>ISO-TP 길이·순번·버퍼 상한 검증 부족</li>
                    <li>TransferData payload 및 잔여 길이 제한 부족</li>
                    <li>EraseMemory 세션·SecurityAccess 선행 검사 부족</li>
                    <li>해시 확인 전 valid pattern 기록 순서 문제</li>
                    <li>고정 Seed/Key와 고정 키 SHA-256 방식의 한계</li>
                  </ul>
                </article>

                <article class="detail-block wide">
                  <h4>검증 범위와 한계</h4>
                  <p>교육 당시 직접 수정한 C/H 파일과 산출물 메타데이터를 기준으로 정적 확인했습니다. 현재 ECU에서 재시험하지 않음과 TASKING·MCAL 부재로 빌드를 재현하지 못한 범위를 명확히 구분하며, 실행하지 않은 프로젝트 단계의 결과는 주장하지 않습니다.</p>
                </article>"""
    boot_new = """                <article class="detail-block">
                  <h4>개발 단계 1 — 애플리케이션 보호 및 복구</h4>
                  <p>OTA 업데이트 중 전송 중단이나 Flash 쓰기 실패가 발생해도 기존 애플리케이션을 보호할 수 있도록 Backup·Erase·Restore 흐름을 구현했습니다.</p>
                  <ul class="stage-list">
                    <li>Application Primary를 Backup 영역으로 복사</li>
                    <li>Primary 영역 Erase 후 신규 SW Binary 기록</li>
                    <li>부팅 시 <code>valid pattern</code>으로 애플리케이션 유효성 확인</li>
                    <li>유효하지 않으면 Backup을 Primary로 복구</li>
                  </ul>
                </article>

                <article class="detail-block">
                  <h4>개발 단계 2 — SW Binary 무결성 검증</h4>
                  <p>Application 데이터의 SHA-256 계산값과 서명 영역의 32바이트 저장값을 비교해 Binary 변경 여부를 확인했습니다. 이후 교육용 고정 키와 Application 데이터를 결합한 SHA-256 검사 흐름으로 확장했습니다.</p>
                  <ul class="stage-list">
                    <li>Application Binary의 SHA-256 계산</li>
                    <li>계산값과 32바이트 저장값 비교</li>
                    <li>교육용 고정 키와 Application 데이터를 결합한 검사</li>
                    <li>검사 결과에 따라 실행 또는 복구 경로 분기</li>
                  </ul>
                </article>

                <article class="detail-block wide">
                  <h4>대표 문제 해결 — Memory Alignment Error</h4>
                  <p>프로젝트 진행 중 Backup·Restore 기능을 구현하면서 Flash 쓰기 경로에서 Memory Alignment Error로 인한 Trap을 발견해 디버깅했습니다.</p>
                  <div class="debug-flow">
                    <div class="debug-step"><strong>문제 발생</strong> — <code>FlsLoader_Write</code> 호출 과정에서 Backup·Restore가 중단되는 Trap 발생</div>
                    <div class="debug-step"><strong>원인 추적</strong> — Trace32의 Trap 관련 레지스터와 Flash Loader 인수를 확인</div>
                    <div class="debug-step"><strong>원인 확인</strong> — <code>uint8</code> source buffer가 Flash Loader의 4바이트 정렬 조건을 보장하지 않음</div>
                    <div class="debug-step"><strong>수정</strong> — 저장 버퍼를 <code>uint32</code> 배열로 변경하고 바이트 처리는 <code>uint8*</code>로 참조</div>
                    <div class="debug-step"><strong>적용 범위</strong> — Application → Backup과 Backup → Application 경로에 동일하게 적용</div>
                  </div>
                </article>"""
    if "개발 단계 1 — 애플리케이션 보호 및 복구" not in html:
        html = replace_once(html, boot_old, boot_new, "Bootloader detail")

    html = html.replace(
        "비공개 저장소 링크 대신, 본 페이지에서 직접 수행 범위·문제 해결·검증 결과와 한계를 확인할 수 있도록 구성했습니다.",
        "비공개 저장소 링크 대신, 본 페이지에서 직접 수행 범위·문제 해결·검증 결과를 확인할 수 있도록 구성했습니다.",
        1,
    )
    INDEX.write_text(html, encoding="utf-8")


def refine_tests() -> None:
    text = TESTS.read_text(encoding="utf-8")
    text = text.replace(
        "        positions = [self.html.index(term) for term in expected]\n        self.assertEqual(positions, sorted(positions))\n",
        "        detail = self.html[self.html.index('id=\"bootloader-details\"'):]\n        positions = [detail.index(term) for term in expected]\n        self.assertEqual(positions, sorted(positions))\n",
        1,
    )
    TESTS.write_text(text, encoding="utf-8")


def refine_readme() -> None:
    text = README.read_text(encoding="utf-8")
    if "Black Box Testing 상세 갤러리" not in text:
        text = text.replace(
            "- CANoe/CAPL 기반 Black Box Testing 대표 프로젝트\n",
            "- CANoe/CAPL 기반 Black Box Testing 대표 프로젝트\n- CANoe·CAPL·Panel·Trace·Test Result를 시각화한 Black Box Testing 상세 갤러리\n",
            1,
        )
    if "2단계 구현 설명" not in text:
        text = text.replace(
            "- UDS·Flash·SHA-256 기반 OTA Bootloader 프로젝트\n",
            "- UDS·Flash·SHA-256 기반 OTA Bootloader 프로젝트\n- 애플리케이션 보호·복구와 SW Binary 무결성 검증의 2단계 구현 설명\n- Memory Alignment Error를 Trace32로 분석하고 4바이트 정렬 버퍼로 개선한 문제 해결 사례\n",
            1,
        )
    text = text.replace(
        "검증 결과와 주장 가능한 범위만 재구성해 제공합니다.",
        "검증 결과와 문제 해결 과정을 포트폴리오용으로 재구성해 제공합니다.",
        1,
    )
    README.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    refine_index()
    refine_tests()
    refine_readme()
