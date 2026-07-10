#!/usr/bin/env python3
"""Resolve and verify the pinned local website workspace without host-specific paths."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "workspace-dependencies.json"


def load_manifest() -> dict:
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def resolve_source(manifest: dict, source: str) -> Path:
    entry = manifest["runtime"] if source == "runtime" else manifest["sources"][source]
    override = os.environ.get(entry["environment"])
    return Path(override).expanduser().resolve() if override else (ROOT / entry["path"]).resolve()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git_revision(path: Path) -> str | None:
    if not (path / ".git").exists() or shutil.which("git") is None:
        return None
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def check_source(manifest: dict, source: str) -> list[dict]:
    entry = manifest["runtime"] if source == "runtime" else manifest["sources"][source]
    path = resolve_source(manifest, source)
    findings: list[dict] = []
    if not path.is_dir():
        return [{"name": source, "ok": False, "detail": f"missing source at {path}; set {entry['environment']}"}]
    revision = git_revision(path)
    if revision is None:
        findings.append({"name": source, "ok": False, "detail": f"cannot read git revision at {path}"})
    elif revision != entry["revision"]:
        findings.append({"name": source, "ok": False, "detail": f"revision {revision}, expected {entry['revision']}"})
    else:
        findings.append({"name": source, "ok": True, "detail": f"{path} at pinned revision"})
    return findings


def source_path(manifest: dict, artifact: dict) -> Path:
    source, relative = artifact["source"].split(":", 1)
    return resolve_source(manifest, source) / relative


def artifact_findings(manifest: dict, include_sources: bool) -> list[dict]:
    findings: list[dict] = []
    for artifact in manifest["artifacts"]:
        destination = ROOT / artifact["destination"]
        if include_sources:
            source = source_path(manifest, artifact)
            if not source.is_file():
                findings.append({"name": artifact["source"], "ok": False, "detail": "source artifact is missing"})
            elif sha256(source) != artifact["source_sha256"]:
                findings.append({"name": artifact["source"], "ok": False, "detail": "source artifact hash differs from manifest"})
        if not destination.is_file():
            findings.append({"name": artifact["destination"], "ok": False, "detail": "synced artifact is missing"})
        elif sha256(destination) != artifact["sha256"]:
            findings.append({"name": artifact["destination"], "ok": False, "detail": "synced artifact hash differs from manifest; run scripts/sync_dependencies.sh"})
    return findings


def doctor(manifest: dict, requirement: str, as_json: bool) -> int:
    findings: list[dict] = []
    if requirement in {"all", "runtime"}:
        findings.extend(check_source(manifest, "runtime"))
        binary = resolve_source(manifest, "runtime") / manifest["runtime"]["binary"]
        findings.append({"name": "kujo binary", "ok": binary.is_file() and os.access(binary, os.X_OK), "detail": str(binary)})
    if requirement in {"all", "sync"}:
        findings.extend(check_source(manifest, "ssg"))
        findings.extend(check_source(manifest, "sitekit"))
        findings.extend(artifact_findings(manifest, include_sources=True))
    if requirement in {"all", "validator"}:
        findings.append({"name": "python", "ok": sys.version_info >= (3, 10), "detail": sys.version.split()[0]})
        try:
            import bs4  # noqa: F401
            findings.append({"name": "beautifulsoup4", "ok": True, "detail": "importable"})
        except ImportError:
            findings.append({"name": "beautifulsoup4", "ok": False, "detail": "install with python3 -m pip install -r requirements.txt"})
    ok = all(finding["ok"] for finding in findings)
    report = {"manifest": str(MANIFEST_PATH), "requirement": requirement, "ok": ok, "checks": findings}
    if as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for finding in findings:
            print(f"{'PASS' if finding['ok'] else 'FAIL'} {finding['name']}: {finding['detail']}")
        print(f"Doctor {'passed' if ok else 'failed'}: {len(findings)} checks")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    doctor_parser = subparsers.add_parser("doctor", help="check pinned workspace prerequisites")
    doctor_parser.add_argument("--require", choices=("all", "runtime", "sync", "validator"), default="all")
    doctor_parser.add_argument("--json", action="store_true", help="emit a machine-readable report")
    subparsers.add_parser("kujo-bin", help="print the pinned Kujo binary path")
    args = parser.parse_args()
    manifest = load_manifest()
    if args.command == "doctor":
        return doctor(manifest, args.require, args.json)
    print(resolve_source(manifest, "runtime") / manifest["runtime"]["binary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
