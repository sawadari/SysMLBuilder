from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
import yaml

import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sysml_builder.parser import parse_markdown
from sysml_builder.pipeline import transform_markdown
from sysml_builder.renderer import render_projection_manifest
from sysml_builder.sidecar import build_sidecar_request, write_sidecar_request
from sysml_builder.transformer import build_contracts
from sysml_builder.common_ir import build_common_ir


PACK_ROOT = ROOT / "testdata" / "SysMLBuilder_testdata_20cases"


class CommonIrPipelineTest(unittest.TestCase):
    def test_transform_produces_common_ir_and_v1_projection(self) -> None:
        case_dir = PACK_ROOT / "cases" / "C01_power_tailgate_conditions"
        result = transform_markdown(case_dir / "requirements_en.md")

        self.assertEqual(result.common_ir.schema_version, "common_semantic_ir_v1alpha1")
        self.assertEqual(result.common_ir.package_name, "C01PowerTailgateConditions")
        self.assertGreater(len(result.common_ir.requirements), 0)
        self.assertGreater(len(result.common_ir.blocks), 0)
        self.assertEqual(result.v1_projection.projection_profile, "safe_subset_v1_5")
        self.assertGreater(len(result.v1_projection.interface_blocks), 0)

    def test_profile_case_common_ir_carries_allocations_and_satisfy(self) -> None:
        path = ROOT / "testdata" / "gfse_derived" / "case01_vehicle_explicit_high_requirements.md"
        parsed = parse_markdown(path)
        contracts = build_contracts(parsed)
        manifest = render_projection_manifest(parsed.case_id)
        common_ir = build_common_ir(parsed, contracts, manifest)

        self.assertGreater(len(common_ir.allocations), 0)
        self.assertGreater(len(common_ir.satisfies), 0)
        self.assertEqual(common_ir.requirements[0].subject, "Vehicle")

    def test_sidecar_request_can_be_serialized(self) -> None:
        case_dir = PACK_ROOT / "cases" / "C01_power_tailgate_conditions"
        result = transform_markdown(case_dir / "requirements_en.md")
        request = build_sidecar_request(result.v1_projection, "cameo")

        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "request.yaml"
            write_sidecar_request(request, output)
            payload = yaml.safe_load(output.read_text(encoding="utf-8"))

        self.assertEqual(payload["target"], "cameo")
        self.assertEqual(payload["model"]["projection_profile"], "safe_subset_v1_5")
        self.assertEqual(payload["model"]["package_name"], "C01PowerTailgateConditions")


if __name__ == "__main__":
    unittest.main()
