#!/usr/bin/env python3
"""System checker for Linux development dependencies and resources."""

from __future__ import annotations

import argparse
import glob
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple


@dataclass
class CommandCheck:
    name: str
    found: bool
    path: Optional[str]
    version: Optional[str]
    works: Optional[bool]
    test_cmd: Optional[List[str]]
    test_output: Optional[str]


@dataclass
class IdeCheck:
    name: str
    found: bool
    locations: List[str]


@dataclass
class DiskInfo:
    path: str
    total_gb: float
    used_gb: float
    free_gb: float
    percent_used: float


@dataclass
class CpuInfo:
    cores: int
    usage_percent: Optional[float]
    load_avg: Optional[Tuple[float, float, float]]


@dataclass
class Report:
    os: str
    note: Optional[str]
    commands: Dict[str, CommandCheck]
    ides: Dict[str, IdeCheck]
    disk: DiskInfo
    cpu: CpuInfo


def run_command(cmd: List[str], timeout: float = 3.0) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except (OSError, subprocess.TimeoutExpired):
        return 1, "", ""


def check_command(name: str, cmd: List[str], test_cmd: Optional[List[str]] = None) -> CommandCheck:
    path = shutil.which(cmd[0])
    if not path:
        return CommandCheck(
            name=name,
            found=False,
            path=None,
            version=None,
            works=None,
            test_cmd=test_cmd,
            test_output=None,
        )

    code, out, err = run_command(cmd)
    version = out or err or None
    works = None
    test_output = None
    if test_cmd:
        test_code, test_out, test_err = run_command(test_cmd)
        works = test_code == 0
        test_output = test_out or test_err or None

    return CommandCheck(
        name=name,
        found=code == 0,
        path=path,
        version=version,
        works=works,
        test_cmd=test_cmd,
        test_output=test_output,
    )


def check_docker_compose() -> CommandCheck:
    docker_path = shutil.which("docker")
    if not docker_path:
        return CommandCheck(
            name="docker-compose",
            found=False,
            path=None,
            version=None,
            works=None,
            test_cmd=None,
            test_output=None,
        )

    code, out, err = run_command(["docker", "compose", "version"])
    if code == 0:
        test_cmd = ["docker", "compose", "version"]
        test_code, test_out, test_err = run_command(test_cmd)
        return CommandCheck(
            name="docker compose",
            found=True,
            path=docker_path,
            version=out or err or None,
            works=test_code == 0,
            test_cmd=test_cmd,
            test_output=test_out or test_err or None,
        )

    # fallback to legacy docker-compose binary
    return check_command(
        "docker-compose",
        ["docker-compose", "version"],
        ["docker-compose", "version"],
    )


def bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)


def get_disk_info(path: str = "/") -> DiskInfo:
    usage = shutil.disk_usage(path)
    total = bytes_to_gb(usage.total)
    used = bytes_to_gb(usage.used)
    free = bytes_to_gb(usage.free)
    percent_used = round((usage.used / usage.total) * 100, 2) if usage.total else 0.0
    return DiskInfo(path=path, total_gb=total, used_gb=used, free_gb=free, percent_used=percent_used)


def read_proc_stat() -> Optional[Tuple[int, int]]:
    try:
        with open("/proc/stat", "r", encoding="utf-8") as handle:
            line = handle.readline()
        parts = line.split()
        if parts[0] != "cpu":
            return None
        values = [int(p) for p in parts[1:]]
        idle = values[3] + values[4] if len(values) > 4 else values[3]
        total = sum(values)
        return idle, total
    except (OSError, ValueError, IndexError):
        return None


def get_cpu_info(sample_seconds: float = 1.0) -> CpuInfo:
    cores = os.cpu_count() or 0
    usage_percent = None
    load_avg = None

    if os.path.exists("/proc/stat"):
        first = read_proc_stat()
        if first:
            time.sleep(sample_seconds)
            second = read_proc_stat()
            if second:
                idle_delta = second[0] - first[0]
                total_delta = second[1] - first[1]
                if total_delta > 0:
                    usage_percent = round((1 - (idle_delta / total_delta)) * 100, 2)

    try:
        load_avg = os.getloadavg()
    except (OSError, AttributeError):
        load_avg = None

    return CpuInfo(cores=cores, usage_percent=usage_percent, load_avg=load_avg)


def check_paths(name: str, candidates: List[str]) -> IdeCheck:
    found = []
    for path in candidates:
        expanded = os.path.expanduser(path)
        matches = glob.glob(expanded)
        if matches:
            found.extend(matches)
        elif os.path.exists(expanded):
            found.append(expanded)
    return IdeCheck(name=name, found=bool(found), locations=found)


def collect_report() -> Report:
    system = platform.system()
    note = None
    if system.lower() != "linux":
        note = "Ten skrypt jest przeznaczony dla Linux; wyniki moga byc niepelne."

    commands = {
        "docker": check_command(
            "docker",
            ["docker", "--version"],
            ["docker", "info"],
        ),
        "docker_compose": check_docker_compose(),
        "python": check_command(
            "python3",
            ["python3", "--version"],
            ["python3", "-c", "print('ok')"],
        ),
        "java": check_command(
            "java",
            ["java", "-version"],
            ["java", "-version"],
        ),
    }

    # Python fallback if python3 missing but python exists
    if not commands["python"].found:
        commands["python"] = check_command(
            "python",
            ["python", "--version"],
            ["python", "-c", "print('ok')"],
        )

    ide_candidates = {
        "intellij": [
            "/opt/idea",
            "/opt/idea-IU",
            "/opt/idea-IC",
            "/snap/intellij-idea-ultimate/current/bin/idea.sh",
            "/snap/intellij-idea-community/current/bin/idea.sh",
            "~/.local/share/JetBrains/Toolbox/apps/IDEA*",
            "/usr/share/applications/jetbrains-idea.desktop",
        ],
        "pycharm": [
            "/opt/pycharm",
            "/opt/pycharm-community",
            "/snap/pycharm-professional/current/bin/pycharm.sh",
            "/snap/pycharm-community/current/bin/pycharm.sh",
            "~/.local/share/JetBrains/Toolbox/apps/PyCharm*",
            "/usr/share/applications/jetbrains-pycharm.desktop",
        ],
    }

    ides = {name: check_paths(name, paths) for name, paths in ide_candidates.items()}

    return Report(
        os=system,
        note=note,
        commands=commands,
        ides=ides,
        disk=get_disk_info("/"),
        cpu=get_cpu_info(),
    )


def report_to_dict(report: Report) -> Dict[str, object]:
    return {
        "os": report.os,
        "note": report.note,
        "commands": {k: asdict(v) for k, v in report.commands.items()},
        "ides": {k: asdict(v) for k, v in report.ides.items()},
        "disk": asdict(report.disk),
        "cpu": asdict(report.cpu),
    }


def format_text(report: Report) -> str:
    lines = []
    width = 78
    sep = "=" * width
    sub = "-" * width
    max_test_len = 240

    lines.append(sep)
    lines.append("RAPORT SYSTEMOWY")
    lines.append(sep)
    lines.append(f"OS: {report.os}")
    if report.note:
        lines.append(f"Uwaga: {report.note}")

    lines.append(sub)
    lines.append("KOMPONENTY")
    lines.append(sub)

    name_w = 14
    status_w = 6
    works_w = 6
    lines.append(
        f"{'Nazwa':<{name_w}} {'Status':<{status_w}} {'Dziala':<{works_w}} Sciezka / Wersja"
    )
    lines.append("-" * width)
    for key, info in report.commands.items():
        status = "OK" if info.found else "BRAK"
        works = "n/a" if info.works is None else ("TAK" if info.works else "NIE")
        path = info.path or "-"
        version = info.version or ""
        detail = f"{path} {version}".strip()
        lines.append(f"{key:<{name_w}} {status:<{status_w}} {works:<{works_w}} {detail}")

    lines.append(sub)
    lines.append("IDE")
    lines.append(sub)
    for key, info in report.ides.items():
        status = "OK" if info.found else "BRAK"
        locations = ", ".join(info.locations) if info.locations else "-"
        lines.append(f"- {key}: {status} | {locations}")

    lines.append(sub)
    lines.append("DYSK")
    lines.append(sub)
    disk = report.disk
    lines.append(
        f"- {disk.path}: total {disk.total_gb} GB, used {disk.used_gb} GB, free {disk.free_gb} GB, {disk.percent_used}% used"
    )

    lines.append(sub)
    lines.append("CPU")
    lines.append(sub)
    cpu = report.cpu
    usage = f"{cpu.usage_percent}%" if cpu.usage_percent is not None else "n/a"
    load_avg = "n/a" if cpu.load_avg is None else f"{cpu.load_avg[0]:.2f}, {cpu.load_avg[1]:.2f}, {cpu.load_avg[2]:.2f}"
    lines.append(f"- cores: {cpu.cores}")
    lines.append(f"- usage: {usage}")
    lines.append(f"- load avg: {load_avg}")

    lines.append(sub)
    lines.append("WYNIKI TESTOW")
    lines.append(sub)
    for key, info in report.commands.items():
        test_cmd = " ".join(info.test_cmd) if info.test_cmd else "-"
        works = "n/a" if info.works is None else ("TAK" if info.works else "NIE")
        output = info.test_output or ""
        if len(output) > max_test_len:
            output = output[:max_test_len].rstrip() + "..."
        lines.append(f"- {key}: dziala={works}")
        lines.append(f"  cmd: {test_cmd}")
        if output:
            lines.append(f"  out: {output}")
        else:
            lines.append("  out: -")

    lines.append(sep)
    return "\n".join(lines)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Linux system checker")
    parser.add_argument("--json", action="store_true", help="Wypisz raport jako JSON")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    report = collect_report()
    if args.json:
        print(json.dumps(report_to_dict(report), indent=2))
    else:
        print(format_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
