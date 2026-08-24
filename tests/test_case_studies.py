from pathlib import Path
import unittest

from tests.site_audit import parse_html


SITE_ROOT = Path(__file__).parents[1] / "site"


class CaseStudyContractTests(unittest.TestCase):
    def _document(self, slug: str):
        page = SITE_ROOT / "artifacts" / slug / "index.html"
        self.assertTrue(page.is_file(), f"Missing case-study page: {page}")
        return parse_html(page)

    def test_case_studies_expose_the_required_section_fragments(self):
        required_ids = {
            "black-box": {"overview", "code", "test", "document", "demo"},
            "carmaker": {
                "overview",
                "architecture",
                "parking",
                "validation",
                "personal",
                "collaboration",
            },
            "bootloader": {"overview", "memory-map", "uds", "test", "trace32"},
        }
        for slug, expected_ids in required_ids.items():
            with self.subTest(slug=slug):
                document = self._document(slug)
                self.assertTrue(expected_ids.issubset(set(document.ids)))

    def test_case_studies_publish_the_verified_result_literals(self):
        required = {
            "black-box": [
                "7개 고장 시나리오",
                "CAPL 스크립트 6종",
                "테스트케이스 24개",
                "정적 결함 4건",
                "동적 결함 11건",
                "캡처가 없는 1건",
            ],
            "carmaker": [
                "6인 팀",
                "14/19 PASS",
                "51.6 m → 0.02 m",
                "최대 오차 0.16 m",
                "페어 프로그래밍",
                "N≥8",
            ],
            "bootloader": [
                "0x10",
                "0x27",
                "0x31",
                "0x34",
                "0x36",
                "0x37",
                "0x11",
                "PASS 7",
                "Evidence unavailable 2",
                "Not executed 1",
                "0x7000240D",
                "HMAC",
                "전자서명",
            ],
        }
        for slug, phrases in required.items():
            with self.subTest(slug=slug):
                text = self._document(slug).text
                for phrase in phrases:
                    self.assertIn(phrase, text)

    def test_black_box_states_ownership_evidence_gap_and_withheld_material(self):
        text = self._document("black-box").text
        for phrase in (
            "개인 프로젝트",
            "기여 100%",
            "2026.03.19–2026.03.23",
            "새 참조 프레임을 수신한 뒤에만 1 ms 타이머",
            "15건을 모두 수정했다고 주장하지 않습니다",
            "소스 저장소와 요구사항 캡처는 공개하지 않습니다",
        ):
            self.assertIn(phrase, text)

    def test_carmaker_separates_team_result_from_personal_implementation(self):
        document = self._document("carmaker")
        text = document.text
        for phrase in (
            "2026.05.21–2026.06.05",
            "팀장 · 주차 경로계획",
            "T10 20.3 m → 0.02 m",
            "T14 3.5 m → 0.04 m",
            "11개 개인 commit",
            "MATLAB 모듈 9개",
            "주차 진입 도달률 0% → 100%",
            "19개 전체 테스트가 PASS했다고 주장하지 않습니다",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("19/19 PASS", text)
        self.assertIn("personal", document.ids)
        self.assertIn("collaboration", document.ids)

    def test_bootloader_states_security_and_reverification_limits(self):
        text = self._document("bootloader").text
        for phrase in (
            "개인 교육 프로젝트",
            "AURIX TC234LP",
            "8단계",
            "Primary에서 Backup으로 복사",
            "Backup에서 Primary로 복구",
            "고정 prefix SHA-256은 HMAC도 전자서명도 아닙니다",
            "재계산 공격",
            "TASKING, EB tresos, 타겟 ECU를 현재 사용할 수 없어",
            "신규 빌드와 하드웨어 재테스트를 수행하지 못했습니다",
            "미해결 정적 리뷰",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
