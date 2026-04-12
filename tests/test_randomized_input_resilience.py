from __future__ import annotations

import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import tempfile
import unittest

import yaml

import sys


ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "testdata" / "SysMLBuilder_testdata_20cases"
sys.path.insert(0, str(ROOT / "src"))

from sysml_builder.pipeline import transform_markdown


def mutate_markdown(text: str, language: str, rng: random.Random) -> str:
    heading_variants = {
        "## Context": ["## Context", "## Context ", "##  Context"],
        "## 背景": ["## 背景", "## 背景 ", "##  背景"],
        "## Functional Requirements": ["## Functional Requirements", "## Functional Requirements ", "##  Functional Requirements"],
        "## 機能要求": ["## 機能要求", "## 機能要求 ", "##  機能要求"],
    }
    for source, variants in heading_variants.items():
        if source in text:
            text = text.replace(source, rng.choice(variants), 1)

    lines: list[str] = []
    for line in text.splitlines():
        if re.match(r"^\s*-\s+[A-Z0-9\-]+:", line):
            indent = " " * rng.choice([0, 2, 4])
            line = indent + line.strip()
        if line.startswith("##"):
            line = line + (" " * rng.choice([0, 1, 2]))
        lines.append(line)
        if line.startswith("##") and rng.random() < 0.6:
            lines.append("")
    mutated = "\n".join(lines) + "\n"

    if language == "en":
        mutated = mutated.replace("This case", rng.choice(["This case", "This scenario", "This test case"]), 1)
    else:
        mutated = mutated.replace("このケースは", rng.choice(["このケースは", "本ケースは", "この試験ケースは"]), 1)
    return mutated


class RandomizedInputResilienceTest(unittest.TestCase):
    def test_mutated_markdown_still_produces_structurally_valid_sysml(self) -> None:
        manifest = yaml.safe_load((PACK_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        rng = random.Random(20260412)

        for case in manifest["cases"]:
            case_dir = PACK_ROOT / case["path"]
            metadata = yaml.safe_load((case_dir / "case.yaml").read_text(encoding="utf-8"))
            for language in ("en", "ja"):
                with self.subTest(case=case["id"], language=language):
                    original = (case_dir / f"requirements_{language}.md").read_text(encoding="utf-8")
                    mutated = mutate_markdown(original, language, rng)
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        tmp_path = Path(tmp_dir)
                        shutil.copy(case_dir / "case.yaml", tmp_path / "case.yaml")
                        input_path = tmp_path / f"requirements_{language}.md"
                        input_path.write_text(mutated, encoding="utf-8")

                        result = transform_markdown(input_path)
                        canonical = result.canonical or ""

                        self.assertIn(f"package {metadata['package']}", canonical)
                        self.assertIn(f"part systemUnderTest : {metadata['structure_en'][0]};", canonical)
                        self.assertEqual(canonical.count("requirement def Req"), metadata["requirements_count"])
                        self.assertEqual(canonical.count("port def "), len(metadata["interfaces"]))
                        self.assertEqual(canonical.count("interface def "), len(metadata["interfaces_defs"]))
                        self.assertEqual(canonical.count("{"), canonical.count("}"))

    def test_generated_sysml_is_parseable_by_monticore_when_tool_is_available(self) -> None:
        tool_jar_env = os.environ.get("SYSML_MONTICORE_JAR")
        if not tool_jar_env:
            self.skipTest("SYSML_MONTICORE_JAR is not set")

        tool_jar = Path(tool_jar_env)
        sampled_cases = {
            "C01",
            "C16",
            "C19",
        }
        manifest = yaml.safe_load((PACK_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        for case in manifest["cases"]:
            if case["id"] not in sampled_cases:
                continue
            case_dir = PACK_ROOT / case["path"]
            for language in ("en", "ja"):
                with self.subTest(case=case["id"], language=language):
                    result = transform_markdown(case_dir / f"requirements_{language}.md")
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        output_path = Path(tmp_dir) / "generated.sysml"
                        output_path.write_text(result.canonical or "", encoding="utf-8")
                        completed = subprocess.run(
                            ["java", "-jar", str(tool_jar), "-nc", "-i", str(output_path)],
                            capture_output=True,
                            text=True,
                            check=False,
                        )
                        self.assertEqual(
                            completed.returncode,
                            0,
                            msg=f"{output_path}\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}",
                        )


if __name__ == "__main__":
    unittest.main()
