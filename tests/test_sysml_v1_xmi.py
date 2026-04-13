from __future__ import annotations

from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sysml_builder.pipeline import transform_markdown


PACK_ROOT = ROOT / "testdata" / "SysMLBuilder_testdata_20cases"


class SysMLV1XmiTest(unittest.TestCase):
    def test_transform_produces_both_xmi_variants_for_generic_case(self) -> None:
        case_dir = PACK_ROOT / "cases" / "C01_power_tailgate_conditions"
        result = transform_markdown(case_dir / "requirements_en.md")

        self.assertEqual(set(result.sysml_v1_xmi), {"cameo", "ea"})

        cameo_root = ET.fromstring(result.sysml_v1_xmi["cameo"])
        ea_root = ET.fromstring(result.sysml_v1_xmi["ea"])

        self.assertEqual(cameo_root.attrib["{http://www.omg.org/spec/XMI/20131001}version"], "2.5")
        self.assertEqual(ea_root.attrib["{http://schema.omg.org/spec/XMI/2.1}version"], "2.1")

    def test_xmi_contains_sysml_v1_safe_subset_stereotypes(self) -> None:
        case_dir = PACK_ROOT / "cases" / "C01_power_tailgate_conditions"
        result = transform_markdown(case_dir / "requirements_en.md")
        root = ET.fromstring(result.sysml_v1_xmi["cameo"])
        sysml_ns = {"sysml": "http://www.omg.org/spec/SysML/20161101/SysML.xmi"}

        self.assertGreater(len(root.findall("sysml:Requirement", sysml_ns)), 0)
        self.assertGreater(len(root.findall("sysml:Block", sysml_ns)), 0)
        self.assertGreater(len(root.findall("sysml:ProxyPort", sysml_ns)), 0)
        self.assertGreater(len(root.findall("sysml:Satisfy", sysml_ns)), 0)

    def test_ea_xmi_contains_expected_diagrams(self) -> None:
        case_dir = PACK_ROOT / "cases" / "C01_power_tailgate_conditions"
        result = transform_markdown(case_dir / "requirements_en.md")
        root = ET.fromstring(result.sysml_v1_xmi["ea"])
        xmi_ns = {"xmi": "http://schema.omg.org/spec/XMI/2.1"}

        extension = root.find("xmi:Extension", xmi_ns)
        self.assertIsNotNone(extension)

        diagrams = extension.findall("./diagrams/diagram") if extension is not None else []
        self.assertEqual(len(diagrams), 3)

        props = {(diagram.find("properties").attrib["name"], diagram.find("properties").attrib["type"]) for diagram in diagrams}
        self.assertIn(("TailgateMotionStates", "Statechart"), props)
        self.assertIn(("Blocks", "Logical"), props)
        self.assertIn(("Requirements", "Custom"), props)


if __name__ == "__main__":
    unittest.main()
