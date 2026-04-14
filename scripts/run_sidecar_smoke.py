from __future__ import annotations

import os
import subprocess
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    mvn = shutil.which("mvn.cmd") or shutil.which("mvn") or "mvn"
    java = shutil.which("java") or "java"

    input_md = ROOT / "testdata" / "SysMLBuilder_testdata_20cases" / "cases" / "C01_power_tailgate_conditions" / "requirements_en.md"
    request_yaml = ROOT / "out" / "C01_cameo_sidecar.yaml"
    output_xmi = ROOT / "out" / "C01_cameo_sidecar.xmi"
    request_yaml_ea = ROOT / "out" / "C01_ea_sidecar.yaml"
    output_xmi_ea = ROOT / "out" / "C01_ea_sidecar.xmi"

    subprocess.run(
        ["python", "-m", "sysml_builder.sidecar_cli", str(input_md), "--target", "cameo", "-o", str(request_yaml)],
        cwd=ROOT,
        env=env,
        check=True,
    )
    run([mvn, "-q", "package"], ROOT / "sidecar")
    run(
        [
            java,
            "-jar",
            str(ROOT / "sidecar" / "target" / "sysml-v1-sidecar-0.1.0-SNAPSHOT-jar-with-dependencies.jar"),
            "--input",
            str(request_yaml),
            "--output",
            str(output_xmi),
        ],
        ROOT,
    )
    subprocess.run(
        ["python", "-m", "sysml_builder.sidecar_cli", str(input_md), "--target", "ea", "-o", str(request_yaml_ea)],
        cwd=ROOT,
        env=env,
        check=True,
    )
    run(
        [
            java,
            "-jar",
            str(ROOT / "sidecar" / "target" / "sysml-v1-sidecar-0.1.0-SNAPSHOT-jar-with-dependencies.jar"),
            "--input",
            str(request_yaml_ea),
            "--output",
            str(output_xmi_ea),
        ],
        ROOT,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
