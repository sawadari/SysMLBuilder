from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sysml_builder.pipeline import transform_markdown, write_result


CASE_DIR = ROOT / "example" / "vehicle_practice_expression_views"


class VehiclePracticeExpressionViewsRoundtripTest(unittest.TestCase):
    def test_markdown_roundtrips_to_expected_sysml(self) -> None:
        source = CASE_DIR / "input" / "vehicle_practice_expression_views_requirements.md"
        expected = (CASE_DIR / "output" / "vehicle_practice_expression_views_canonical.sysml").read_text(encoding="utf-8")

        result = transform_markdown(source)

        self.assertEqual(result.case_id, "vehicle_practice_expression_views")
        self.assertEqual(result.canonical, expected)
        self.assertIsNone(result.overlay)
        self.assertIn("Display > Display Exposed Elements", result.cameo_display_guide)
        self.assertIn("Display > Display Connectors", result.cameo_display_guide)
        self.assertIn("https://docs.nomagic.com/SYSML2P/2026x/displaying-elements-in-symbolic-views-254422731.html", result.cameo_display_guide)
        self.assertIn("RequirementsTreeView", result.canonical)
        self.assertIn("PartsTreeView", result.canonical)
        self.assertIn("ActionsNestedView", result.canonical)
        self.assertIn("StatesNestedView", result.canonical)
        self.assertIn("DS_Views::SymbolicViews::iv", result.canonical)
        self.assertIn("DS_Views::SymbolicViews::afv", result.canonical)
        self.assertIn("DS_Views::SymbolicViews::stv", result.canonical)

    def test_write_result_emits_cameo_display_guide_markdown(self) -> None:
        source = CASE_DIR / "input" / "vehicle_practice_expression_views_requirements.md"
        result = transform_markdown(source)

        with TemporaryDirectory() as tmp:
            written = write_result(result, Path(tmp))
            guide_path = Path(tmp) / "vehicle_practice_expression_views_cameo_display_guide.md"

            self.assertIn(guide_path, written)
            self.assertTrue(guide_path.exists())
            guide_text = guide_path.read_text(encoding="utf-8")
            self.assertIn("## View ごとの使い分け", guide_text)
            self.assertIn("### System Interconnection", guide_text)
            self.assertIn("2026x Hot Fix 1", guide_text)


if __name__ == "__main__":
    unittest.main()
