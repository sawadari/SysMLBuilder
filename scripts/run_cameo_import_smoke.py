from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAMEO_HOME = Path(r"C:\Program Files\Magic Systems of Systems Architect")
PLUGIN_ROOT = ROOT / "tools" / "cameo_smoke_action"
ACTION_SOURCES = list((PLUGIN_ROOT / "src").rglob("*.java"))


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

def run_no_check(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=False,
        text=True,
        capture_output=True,
    )


def read_vm_options(cameo_home: Path) -> list[str]:
    vm_options_path = cameo_home / "bin" / "vm.options"
    options: list[str] = []
    for raw_line in vm_options_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("--add-opens "):
            line = "--add-opens=" + line[len("--add-opens ") :]
        elif line.startswith("--add-exports "):
            line = "--add-exports=" + line[len("--add-exports ") :]
        options.append(line)
    extra_option = "--add-exports=java.xml/com.sun.org.apache.xml.internal.serialize=ALL-UNNAMED"
    if extra_option not in options:
        options.append(extra_option)
    return options


def build_action_jar(cameo_home: Path) -> Path:
    javac = shutil.which("javac") or "javac"
    jar = shutil.which("jar") or "jar"
    build_root = ROOT / "out" / "cameo_smoke_action"
    classes_dir = build_root / "classes"
    plugin_dir = build_root / "plugin"
    action_jar = plugin_dir / "cameo-import-smoke-plugin.jar"
    classes_dir.mkdir(parents=True, exist_ok=True)
    plugin_dir.mkdir(parents=True, exist_ok=True)

    plugin_jar = next((cameo_home / "plugins" / "com.nomagic.magicdraw.emfuml2xmi_v5").glob("emfuml2xmi_v5-*.jar"))
    plugin_common_jar = next((cameo_home / "plugins" / "com.nomagic.magicdraw.emfuml2xmi_v5" / "lib").glob("emfuml2_common-*.jar"))
    classpath = os.pathsep.join([str(cameo_home / "lib" / "classpath.jar"), str(plugin_jar), str(plugin_common_jar)])

    run(
        [javac, "-proc:none", "-encoding", "UTF-8", "-cp", classpath, "-d", str(classes_dir), *[str(path) for path in ACTION_SOURCES]],
        cwd=ROOT,
    )
    if action_jar.exists():
        action_jar.unlink()
    run([jar, "cf", str(action_jar), "-C", str(classes_dir), "."], cwd=ROOT)
    shutil.copyfile(PLUGIN_ROOT / "plugin.xml", plugin_dir / "plugin.xml")
    return action_jar


def main() -> int:
    cameo_home = Path(os.environ.get("CAMEO_HOME", str(DEFAULT_CAMEO_HOME)))
    if not cameo_home.exists():
        raise SystemExit(f"Cameo install not found: {cameo_home}")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    run(["python", "scripts\\run_sidecar_smoke.py"], cwd=ROOT, env=env)

    action_jar = build_action_jar(cameo_home)
    plugin_dir = action_jar.parent
    plugin_root = plugin_dir.parent
    cameo_import_path = ROOT / "out" / "C01_cameo_sidecar.uml"
    output_path = ROOT / "out" / "C01_cameo_imported.mdzip"
    log_path = ROOT / "out" / "C01_cameo_import_smoke.log"

    java = str(cameo_home / "jre" / "bin" / "java.exe")
    vm_options = read_vm_options(cameo_home)
    classpath = os.pathsep.join([str(cameo_home / "lib" / "classpath.jar")])
    command = [
        java,
        "-Xmx2G",
        *vm_options,
        "-cp",
        classpath,
        f"-Dmd.plugins.dir={cameo_home / 'plugins'};{plugin_root}",
        f"-Desi.system.config={cameo_home / 'data' / 'application.conf'}",
        "-Dfile.encoding=UTF-8",
        "-DLOCALCONFIG=true",
        "-Dcom.nomagic.magicdraw.commandline.action=local.sysmlbuilder.cameo.CameoImportSmokeAction",
        "com.nomagic.magicdraw.commandline.CommandLineActionLauncher",
        "NOGUI",
        "--xmi",
        str(cameo_import_path),
        "--output",
        str(output_path),
    ]
    result = run_no_check(command, cwd=cameo_home)
    log_path.write_text(result.stdout + "\n" + result.stderr, encoding="utf-8")
    if result.returncode != 0:
        raise SystemExit(
            "Cameo import smoke failed. See "
            f"{log_path} and C:\\Users\\sawad\\AppData\\Local\\.magic.systems.of.systems.architect\\2026x\\msosa.log"
        )
    print(output_path)
    print(log_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
