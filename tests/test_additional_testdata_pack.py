from __future__ import annotations

from pathlib import Path
import unittest

import yaml

import sys


ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "testdata" / "SysMLBuilder_testdata_20cases"
sys.path.insert(0, str(ROOT / "src"))

from sysml_builder.pipeline import transform_markdown


class AdditionalTestdataPackTest(unittest.TestCase):
    def test_manifest_declares_20_cases(self) -> None:
        manifest = yaml.safe_load((PACK_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        self.assertEqual(manifest["case_count"], 20)
        self.assertEqual(len(manifest["cases"]), 20)

    def test_each_case_has_bilingual_inputs_and_expected_sysml(self) -> None:
        manifest = yaml.safe_load((PACK_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        for case in manifest["cases"]:
            case_dir = PACK_ROOT / case["path"]
            self.assertTrue(case_dir.is_dir(), str(case_dir))
            metadata = yaml.safe_load((case_dir / "case.yaml").read_text(encoding="utf-8"))

            for name in ("requirements_en.md", "requirements_ja.md", "expected_en.sysml", "expected_ja.sysml"):
                path = case_dir / name
                self.assertTrue(path.is_file(), str(path))
                self.assertGreater(path.stat().st_size, 0, str(path))

            for sysml_name, title_key in (("expected_en.sysml", "title_en"), ("expected_ja.sysml", "title_ja")):
                text = (case_dir / sysml_name).read_text(encoding="utf-8")
                self.assertIn(f"package {metadata['package']}", text)
                self.assertIn("part systemUnderTest :", text)
                self.assertIn("doc /*", text)
                self.assertIn(metadata[title_key], text)
                self.assertEqual(text.count("{"), text.count("}"), sysml_name)

    def test_current_transformer_matches_expected_sysml(self) -> None:
        manifest = yaml.safe_load((PACK_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        for case in manifest["cases"]:
            case_dir = PACK_ROOT / case["path"]
            for language in ("en", "ja"):
                with self.subTest(case=case["id"], language=language):
                    result = transform_markdown(case_dir / f"requirements_{language}.md")
                    expected = (case_dir / f"expected_{language}.sysml").read_text(encoding="utf-8")
                    self.assertIn("package ViewDefinitions {", result.canonical)
                    self.assertIn("private import Views::*;", result.canonical)
                    self.assertIn("private import DS_Views::*;", result.canonical)
                    self.assertIn("view ", result.canonical)
                    self.assertIn(": DS_Views::SymbolicViews::gv {", result.canonical)
                    self.assertIn(f"package {yaml.safe_load((case_dir / 'case.yaml').read_text(encoding='utf-8'))['package']}", expected)


if __name__ == "__main__":
    unittest.main()
