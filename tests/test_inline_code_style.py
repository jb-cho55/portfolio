from pathlib import Path
import re
import unittest


class InlineCodeStyleTests(unittest.TestCase):
    def test_debug_step_code_inherits_portfolio_font(self):
        html = Path("index.html").read_text(encoding="utf-8")
        self.assertIn("<code>FlsLoader_Write</code>", html)

        match = re.search(r"\.debug-step\s+code\s*\{(?P<body>[^}]*)\}", html)
        self.assertIsNotNone(match, "Missing .debug-step code CSS rule")

        declarations = "".join(match.group("body").split())
        self.assertIn("font-family:inherit;", declarations)
        self.assertIn("font-size:inherit;", declarations)
        self.assertIn("font-weight:700;", declarations)
        self.assertIn("color:var(--navy);", declarations)


if __name__ == "__main__":
    unittest.main()
