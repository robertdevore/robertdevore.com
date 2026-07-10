#!/usr/bin/env python3
"""Synchronize the manifest-pinned SSG and SiteKit artifacts into this site."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path

import workspace


def source_findings(manifest: dict) -> list[str]:
    errors: list[str] = []
    for source in ("ssg", "sitekit"):
        for finding in workspace.check_source(manifest, source):
            if not finding["ok"]:
                errors.append(f"{finding['name']}: {finding['detail']}")
    for artifact in manifest["artifacts"]:
        source = workspace.source_path(manifest, artifact)
        if not source.is_file():
            errors.append(f"{artifact['source']}: source artifact is missing")
        elif workspace.sha256(source) != artifact["source_sha256"]:
            errors.append(f"{artifact['source']}: source artifact hash differs from manifest")
    return errors


def destination_findings(manifest: dict) -> list[str]:
    errors: list[str] = []
    for artifact in manifest["artifacts"]:
        destination = workspace.ROOT / artifact["destination"]
        if not destination.is_file():
            errors.append(f"{artifact['destination']}: synced artifact is missing")
        elif workspace.sha256(destination) != artifact["sha256"]:
            errors.append(f"{artifact['destination']}: synced artifact hash differs from manifest")
    return errors


def rendered_bytes(artifact: dict, source: Path) -> bytes:
    payload = source.read_bytes()
    if artifact.get("transform") == "rewrite_sitekit_font_paths":
        payload = payload.replace(b"../fonts/", b"../../fonts/")
    return payload


def write_atomically(destination: Path, payload: bytes) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verify the pinned sources and synced artifacts without writing")
    mode.add_argument("--dry-run", action="store_true", help="verify sources and list the writes without changing files")
    args = parser.parse_args()
    manifest = workspace.load_manifest()
    errors = source_findings(manifest)
    if errors:
        print("Dependency sync refused:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    if args.check:
        errors = destination_findings(manifest)
        if errors:
            print("Dependency sync check failed:")
            print("\n".join(f"- {error}" for error in errors))
            return 1
        print("Dependency sync check passed: pinned sources and synced artifacts match.")
        return 0
    for artifact in manifest["artifacts"]:
        source = workspace.source_path(manifest, artifact)
        destination = workspace.ROOT / artifact["destination"]
        if args.dry_run:
            print(f"Would sync {artifact['source']} -> {artifact['destination']}")
            continue
        payload = rendered_bytes(artifact, source)
        if workspace.sha256_bytes(payload) != artifact["sha256"]:
            print(f"Dependency sync refused: transformed {artifact['source']} does not match manifest hash")
            return 1
        write_atomically(destination, payload)
        print(f"Synced {artifact['source']} -> {artifact['destination']}")
    if args.dry_run:
        print("Dependency sync dry run passed: no files changed.")
        return 0
    errors = destination_findings(manifest)
    if errors:
        print("Dependency sync wrote files but verification failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Dependency sync passed: pinned sources and synced artifacts match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
