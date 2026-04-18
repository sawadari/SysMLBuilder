from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sysml_builder.pipeline import transform_markdown


CASE_DIR = ROOT / "example" / "dont_panic_batmobile"


class DontPanicBatmobileRoundtripTest(unittest.TestCase):
    def test_markdown_roundtrips_to_expected_sysml(self) -> None:
        source = CASE_DIR / "input" / "dont_panic_batmobile_requirements.md"
        expected = (CASE_DIR / "output" / "dont_panic_batmobile_canonical.sysml").read_text(encoding="utf-8")

        result = transform_markdown(source)

        self.assertEqual(result.case_id, "dont_panic_batmobile")
        self.assertEqual(result.canonical, expected)
        self.assertIsNone(result.overlay)
        self.assertIn("package Dont_Panic_Batmobile", result.canonical)
        self.assertIn("view 'structural Modeling' : DS_Views::SymbolicViews::gv;", result.canonical)
        self.assertIn("view 'behavioral modelling' : DS_Views::SymbolicViews::gv;", result.canonical)
        self.assertIn("view 'use cases modelling' : DS_Views::SymbolicViews::gv;", result.canonical)
        self.assertIn("view 'requirements modelling' : DS_Views::SymbolicViews::gv;", result.canonical)
        self.assertIn("view index : DS_Views::SymbolicViews::gv;", result.canonical)


if __name__ == "__main__":
    unittest.main()
