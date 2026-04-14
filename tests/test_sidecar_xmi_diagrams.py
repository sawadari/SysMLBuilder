from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


class SidecarXmiDiagramSmokeTest(unittest.TestCase):
    def test_ea_sidecar_xmi_contains_requirement_block_ibd_and_statechart_diagrams(self) -> None:
        if shutil.which("java") is None or (shutil.which("mvn.cmd") is None and shutil.which("mvn") is None):
            self.skipTest("java or maven is not available")

        subprocess.run(["python", "scripts\\run_sidecar_smoke.py"], cwd=ROOT, check=True)

        root = ET.fromstring((ROOT / "out" / "C01_ea_sidecar.xmi").read_text(encoding="utf-8"))
        xmi_ns = {"xmi": "http://schema.omg.org/spec/XMI/2.1"}
        extension = root.find("xmi:Extension", xmi_ns)
        self.assertIsNotNone(extension)

        diagrams = extension.findall("./diagrams/diagram") if extension is not None else []
        props = {(diagram.find("properties").attrib["name"], diagram.find("properties").attrib["type"]) for diagram in diagrams}

        self.assertIn(("Requirements", "Custom"), props)
        self.assertIn(("Blocks", "Logical"), props)
        self.assertIn(("PowerTailgateSystem Internal", "CompositeStructure"), props)
        self.assertIn(("TailgateMotionStates", "Statechart"), props)


if __name__ == "__main__":
    unittest.main()
