#!/usr/bin/env python3
"""Offline, read-only host observation alongside an existing inventory seed.

This tool never refreshes the seed or scans a remote host. Snapshots can include
host-local paths and must be stored in an operator-selected private directory.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "ellmos.techshot.v1"
COMPARE_SCHEMA = "ellmos.techshot-comparison.v1"
MAX_PATH_ENTRIES = 512
MAX_PACKAGE_ROWS = 20000


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _key(value: object) -> str:
    normalized = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return re.sub(r"[\W_]+", "-", normalized, flags=re.UNICODE).strip("-") or "unknown"


def _component_id(name: str, publisher: str, ecosystem: str) -> str:
    return ":".join((_key(ecosystem), _key(publisher), _key(name)))


def _version(value: object) -> tuple[str | None, str]:
    if not isinstance(value, str) or not value.strip():
        return None, "unknown"
    version = value.strip()
    # Wildcards and marketing labels are not exact versions for advisory matching.
    if re.search(r"(?i)(?:\bx\b|\*|latest|current|unknown|unbekannt)", version):
        return version, "uncertain"
    return version, "reported"


def _add(groups: dict, *, name: str, publisher: str, ecosystem: str,
         version: object, source: str, install_id: str, location: str | None = None,
         exact_observation: bool = False) -> None:
    if not name:
        return
    component_id = _component_id(name, publisher, ecosystem)
    value, quality = _version(version)
    if exact_observation and value and quality == "reported":
        quality = "observed"
    group = groups.setdefault(component_id, {
        "component_id": component_id, "name": name, "publisher": publisher or None,
        "ecosystem": ecosystem, "installations": [],
    })
    installation = {"install_id": install_id, "version": value,
                    "version_quality": quality, "source": source}
    if location:
        installation["location"] = location
    if installation not in group["installations"]:
        group["installations"].append(installation)


def _windows_uninstall_rows() -> tuple[list[dict], list[str]]:
    if os.name != "nt":
        return [], ["windows-uninstall-registry:not-applicable"]
    import winreg  # Windows standard library; deliberately never use Win32_Product.

    rows, errors = [], []
    base = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    for hive_name, hive in (("HKLM", winreg.HKEY_LOCAL_MACHINE),
                            ("HKCU", winreg.HKEY_CURRENT_USER)):
        for view_name, view in (("64", winreg.KEY_WOW64_64KEY),
                                ("32", winreg.KEY_WOW64_32KEY)):
            try:
                root = winreg.OpenKey(hive, base, 0, winreg.KEY_READ | view)
            except OSError as exc:
                errors.append(f"registry:{hive_name}:{view_name}:{type(exc).__name__}")
                continue
            with root:
                count = winreg.QueryInfoKey(root)[0]
                for index in range(count):
                    try:
                        key_name = winreg.EnumKey(root, index)
                        with winreg.OpenKey(root, key_name) as key:
                            def field(name: str) -> str:
                                try:
                                    return str(winreg.QueryValueEx(key, name)[0]).strip()
                                except OSError:
                                    return ""
                            name = field("DisplayName")
                            if name:
                                rows.append({"name": name, "publisher": field("Publisher"),
                                             "version": field("DisplayVersion"),
                                             "install_id": f"{hive_name}:{view_name}:{key_name}"})
                    except OSError:
                        errors.append(f"registry:{hive_name}:{view_name}:entry-unreadable")
    return rows, errors


def _native_package_rows(system: str) -> tuple[list[dict], list[str]]:
    if system == "Windows":
        return _windows_uninstall_rows()
    if system == "Linux":
        executable = shutil.which("dpkg-query")
        command = [executable, "-W", "-f=${binary:Package}\t${Version}\n"] if executable else None
        ecosystem = "dpkg"
        if not executable:
            executable = shutil.which("rpm")
            command = [executable, "-qa", "--qf", "%{NAME}\t%{VERSION}-%{RELEASE}\n"] if executable else None
            ecosystem = "rpm"
    elif system == "Darwin":
        executable = shutil.which("brew")
        command = [executable, "list", "--versions"] if executable else None
        ecosystem = "homebrew"
    else:
        return [], ["native-packages:unsupported-platform"]
    if not command:
        return [], [f"{ecosystem}:not-installed"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], [f"{ecosystem}:{type(exc).__name__}"]
    if result.returncode:
        return [], [f"{ecosystem}:exit-{result.returncode}"]
    rows = []
    lines = result.stdout.splitlines()
    for line in lines[:MAX_PACKAGE_ROWS]:
        fields = line.split("\t", 1) if ecosystem in {"dpkg", "rpm"} else line.split(maxsplit=1)
        if len(fields) == 2 and fields[0]:
            versions = fields[1].split() if ecosystem == "homebrew" else [fields[1]]
            for version in versions:
                rows.append({"name": fields[0], "publisher": ecosystem,
                             "version": version,
                             "install_id": f"{ecosystem}:{fields[0]}:{version}"})
    errors = [f"{ecosystem}:truncated"] if len(lines) > MAX_PACKAGE_ROWS else []
    return rows, errors


def _python_candidates(explicit: list[str]) -> list[tuple[str, str]]:
    candidates = [(str(Path(sys.executable).absolute()), "running-interpreter")]
    seen = {os.path.normcase(candidates[0][0])}
    for directory in os.environ.get("PATH", "").split(os.pathsep)[:MAX_PATH_ENTRIES]:
        if not directory:
            continue
        for basename in (("python.exe", "python3.exe", "py.exe") if os.name == "nt"
                         else ("python", "python3")):
            candidate = Path(directory) / basename
            if candidate.is_file():
                resolved = str(candidate.absolute())
                if os.path.normcase(resolved) not in seen:
                    candidates.append((resolved, "PATH"))
                    seen.add(os.path.normcase(resolved))
    for raw in explicit:
        candidate = Path(raw).expanduser()
        if not candidate.is_file():
            raise ValueError(f"explicit Python path does not exist: {candidate}")
        resolved = str(candidate.absolute())
        if os.path.normcase(resolved) not in seen:
            candidates.append((resolved, "explicit"))
            seen.add(os.path.normcase(resolved))
    return candidates


def _probe_python(path: str) -> str | None:
    try:
        result = subprocess.run([path, "-I", "-S", "--version"], capture_output=True,
                                text=True, encoding="utf-8", errors="replace",
                                timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode:
        return None
    match = re.fullmatch(r"Python\s+(\S+)", (result.stdout or result.stderr).strip())
    return match.group(1) if match else None


def _physical_ram_bytes(system: str) -> tuple[int | None, str]:
    try:
        if system == "Windows" and os.name == "nt":
            class MemoryStatus(ctypes.Structure):
                _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong),
                            ("total_physical", ctypes.c_ulonglong),
                            ("available_physical", ctypes.c_ulonglong),
                            ("total_page", ctypes.c_ulonglong),
                            ("available_page", ctypes.c_ulonglong),
                            ("total_virtual", ctypes.c_ulonglong),
                            ("available_virtual", ctypes.c_ulonglong),
                            ("available_extended", ctypes.c_ulonglong)]

            status = MemoryStatus()
            status.length = ctypes.sizeof(status)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return int(status.total_physical), "GlobalMemoryStatusEx"
        elif system == "Linux":
            for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
                if line.startswith("MemTotal:"):
                    return int(line.split()[1]) * 1024, "/proc/meminfo:MemTotal"
        elif system == "Darwin":
            result = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True,
                                    text=True, timeout=5, check=False)
            if result.returncode == 0:
                return int(result.stdout.strip()), "sysctl:hw.memsize"
    except (OSError, ValueError, AttributeError, subprocess.TimeoutExpired):
        pass
    return None, "unavailable"


def _cpu_model(system: str) -> tuple[str | None, str]:
    try:
        if system == "Windows" and os.name == "nt":
            import winreg

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
                model = winreg.QueryValueEx(key, "ProcessorNameString")[0]
                if isinstance(model, str) and model.strip():
                    return model.strip(), "windows-processor-registry"
        elif system == "Linux":
            for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
                if line.startswith("model name") and ":" in line:
                    return line.split(":", 1)[1].strip(), "/proc/cpuinfo:model-name"
        elif system == "Darwin":
            result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                                    capture_output=True, text=True, timeout=5, check=False)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip(), "sysctl:machdep.cpu.brand_string"
    except (OSError, UnicodeError, subprocess.TimeoutExpired):
        pass
    return platform.processor() or None, "platform.processor"


def _hardware_observations() -> dict:
    system = platform.system()

    def observed(value: object, source: str) -> dict:
        return {"value": value if value not in (None, "") else None,
                "quality": "observed" if value not in (None, "") else "unknown",
                "source": source}

    memory, memory_source = _physical_ram_bytes(system)
    cpu, cpu_source = _cpu_model(system)
    try:
        disk = shutil.disk_usage(Path(sys.executable).anchor or "/")
        disk_total = disk.total
        disk_source = "system-interpreter-filesystem:disk_usage"
    except OSError:
        disk_total = None
        disk_source = "unavailable"
    return {
        "os": observed(f"{system} {platform.release()}".strip(), "platform"),
        "architecture": observed(platform.machine(), "platform.machine"),
        "cpu_model": observed(cpu, cpu_source),
        "logical_cpu_count": observed(os.cpu_count(), "os.cpu_count"),
        "ram_total_bytes": observed(memory, memory_source),
        "gpu_model": observed(None, "no-portable-readonly-collector-configured"),
        "system_filesystem_total_bytes": observed(disk_total, disk_source),
    }


def capture(seed_path: Path, *, slot: str, hostname: str | None = None,
            package_rows: list[dict] | None = None, python_paths: list[str] | None = None,
            probe_paths: list[str] | None = None) -> dict:
    seed_bytes = seed_path.read_bytes()
    seed = json.loads(seed_bytes.decode("utf-8-sig"))
    if not isinstance(seed, dict) or not isinstance(seed.get("system"), dict):
        raise ValueError("inventory seed must contain a system object")
    host = hostname or socket.gethostname()
    system = seed["system"]
    if system.get("name") != slot or str(system.get("hostname", "")).casefold() != host.casefold():
        raise ValueError("inventory seed does not belong to this host and slot")
    groups: dict[str, dict] = {}
    for index, row in enumerate(seed.get("software", [])):
        if not isinstance(row, dict):
            raise ValueError("inventory software row must be an object")
        _add(groups, name=str(row.get("name") or ""), publisher=str(row.get("publisher") or ""),
             ecosystem=str(row.get("install_method") or "seed"), version=row.get("version"),
             source="inventory-seed", install_id=f"seed:{index}")
    if package_rows is None:
        package_rows, package_errors = _native_package_rows(platform.system())
    else:
        package_errors = []
    for row in package_rows:
        _add(groups, name=str(row.get("name") or ""), publisher=str(row.get("publisher") or ""),
             ecosystem="windows-uninstall" if platform.system() == "Windows" else
                       str(row.get("publisher") or "native-package"),
             version=row.get("version"), source="native-installed", install_id=str(row["install_id"]),
             exact_observation=True)
    probes = {str(Path(p).absolute()) for p in (probe_paths or [])}
    python_candidates = _python_candidates([*(python_paths or []), *(probe_paths or [])])
    effective_path = shutil.which("python") or shutil.which("python3")
    python_context = {"running_executable": str(Path(sys.executable).absolute()),
                      "running_prefix": sys.prefix,
                      "running_base_prefix": sys.base_prefix,
                      "running_venv": sys.prefix != sys.base_prefix,
                      "effective_path_python": effective_path,
                      "path_candidates_in_order": [path for path, source in python_candidates
                                                   if source == "PATH"],
                      "observed_venv_markers": [path for path, _source in python_candidates
                                                if (Path(path).parent.parent / "pyvenv.cfg").is_file()]}
    for path, source in python_candidates:
        if source == "running-interpreter":
            version = platform.python_version()
        elif path in probes:
            version = _probe_python(path)
        else:
            version = None
        _add(groups, name="Python", publisher="Python Software Foundation", ecosystem="python-runtime",
             version=version, source=source, install_id=f"python:{hashlib.sha256(path.encode()).hexdigest()[:16]}",
             location=path, exact_observation=bool(version))
    components = sorted(groups.values(), key=lambda row: row["component_id"])
    for row in components:
        row["installations"].sort(key=lambda install: install["install_id"])
    return {"schema_version": SCHEMA, "captured_at_utc": _utc_now(),
            "host": {"slot": slot, "hostname": host, "os": platform.platform(),
                     "machine": platform.machine(), "processor": platform.processor(),
                     "hardware_seed": {key: system.get(key) for key in
                                       ("model_name", "cpu", "ram_gb", "gpu")},
                     "hardware_seed_quality": "inventory-reported-not-live-verified"},
            "hardware_observations": _hardware_observations(),
            "inventory": {"seed_sha256": hashlib.sha256(seed_bytes).hexdigest(),
                          "seed_stand": seed.get("_stand"), "slot": slot},
            "python_context": python_context,
            "coverage": {"native_package_source": platform.system(),
                         "native_package_errors": package_errors,
                         "path_entries_considered": min(len(os.environ.get("PATH", "").split(os.pathsep)), MAX_PATH_ENTRIES),
                         "python_candidates": len(python_candidates),
                         "complete_installation_inventory": False},
            "components": components}


def compare(left: dict, right: dict) -> dict:
    if left.get("schema_version") != SCHEMA or right.get("schema_version") != SCHEMA:
        raise ValueError("both snapshots must use the techshot v1 schema")
    a, b = left["host"]["slot"], right["host"]["slot"]
    if a == b:
        raise ValueError("compare distinct host slots")
    by_side = []
    for snapshot in (left, right):
        mapping = {}
        for row in snapshot["components"]:
            key = row["component_id"]
            if key in mapping:
                raise ValueError("duplicate component identity")
            mapping[key] = row
        by_side.append(mapping)
    changes = []
    for key in sorted(set(by_side[0]) | set(by_side[1])):
        rows = [side.get(key) for side in by_side]
        versions = [sorted({inst["version"] for inst in row["installations"]
                            if inst["version"] and inst["version_quality"] in {"observed", "reported"}})
                    if row else [] for row in rows]
        if not all(rows):
            status = "not-observed-on-one-host"
        elif not all(versions):
            status = "version-unknown"
        elif versions[0] != versions[1]:
            status = "version-drift"
        else:
            continue
        changes.append({"component_id": key, "status": status,
                        "versions": {a: versions[0], b: versions[1]},
                        "observed": {a: rows[0] is not None, b: rows[1] is not None}})
    hardware_changes = []
    for field in ("os", "architecture", "cpu_model", "logical_cpu_count",
                  "ram_total_bytes", "gpu_model", "system_filesystem_total_bytes"):
        observations = [snapshot.get("hardware_observations", {}).get(field, {})
                        for snapshot in (left, right)]
        values = [item.get("value") if item.get("quality") == "observed" else None
                  for item in observations]
        if None in values:
            status = "unknown"
        elif values[0] != values[1]:
            status = "different"
        else:
            continue
        hardware_changes.append({"field": field, "status": status,
                                 "values": {a: values[0], b: values[1]}})
    return {"schema_version": COMPARE_SCHEMA, "compared_at_utc": _utc_now(),
            "hosts": [a, b], "changes": changes,
            "hardware_changes": hardware_changes,
            "meaning": "not observed is not proof that software is absent"}


def _write_new(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    capture_parser = sub.add_parser("capture")
    capture_parser.add_argument("--seed", type=Path, required=True)
    capture_parser.add_argument("--slot", required=True)
    capture_parser.add_argument("--output", type=Path, required=True)
    capture_parser.add_argument("--python-path", action="append", default=[])
    capture_parser.add_argument("--probe-python", action="append", default=[],
                                help="explicitly trusted executable path to run with -I -S --version")
    compare_parser = sub.add_parser("compare")
    compare_parser.add_argument("--left", type=Path, required=True)
    compare_parser.add_argument("--right", type=Path, required=True)
    compare_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "capture":
            result = capture(args.seed, slot=args.slot, python_paths=args.python_path,
                             probe_paths=args.probe_python)
        else:
            result = compare(json.loads(args.left.read_text(encoding="utf-8")),
                             json.loads(args.right.read_text(encoding="utf-8")))
        _write_new(args.output, result)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"techshot: {exc}\n")
    print(json.dumps({"output": str(args.output), "schema_version": result["schema_version"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
