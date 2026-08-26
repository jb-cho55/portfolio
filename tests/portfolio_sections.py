"""index.html을 프로젝트 카드 단위로 잘라내는 헬퍼.

카드가 두 개뿐이라 예전 테스트들은 "bootloader 다음이 black-box"라는 순서를 슬라이스
경계로 썼다. 지원 직무에 맞춰 카드 순서를 바꾸면 그 슬라이스가 전부 빈 문자열이 된다.
경계 규칙을 여기 한 곳에만 두고 순서에는 의존하지 않는다.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD = 'class="project-card"'


def index_html() -> str:
    return (ROOT / "index.html").read_text(encoding="utf-8")


def card(html: str, anchor: str) -> str:
    """anchor가 등장하는 지점부터 그 프로젝트 카드가 끝날 때까지.

    anchor는 `bootloader-project` 같은 카드 id여도 되고, `bootloader-debug` 처럼
    카드 안쪽 요소의 id여도 된다. 어느 쪽이든 다음 카드가 시작되기 직전에서 끊는다.
    """
    start = html.index(f'id="{anchor}"')
    nxt = html.find(CARD, start + 1)
    return html[start:] if nxt == -1 else html[start:nxt]
