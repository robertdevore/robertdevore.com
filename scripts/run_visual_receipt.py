#!/usr/bin/env python3
"""Build the site and capture the QA-001 local Lens visual/a11y receipt."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
from typing import Any
from urllib.error import HTTPError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "qa/lens/routes.json"
CONFIG = ROOT / "qa/lens/receipt.toml"


def wait_for_server(url: str, server: subprocess.Popen[str]) -> None:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if server.poll() is not None:
            raise RuntimeError(f"local static server exited with {server.returncode}")
        try:
            with urlopen(url, timeout=1):
                return
        except HTTPError:
            return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"local static server did not become ready: {url}")


def resolve_lens(explicit: str | None) -> str:
    lens = explicit or os.environ.get("LENS_BIN") or shutil.which("lens")
    if not lens:
        raise RuntimeError("Lens was not found. Set LENS_BIN to the Lens executable path.")
    lens_path = Path(lens).expanduser()
    if not lens_path.is_file() or not os.access(lens_path, os.X_OK):
        raise RuntimeError(f"Lens executable is unavailable: {lens_path}")
    return os.fspath(lens_path)


def reserve_port(port: int) -> int:
    """Use an available loopback port; a supplied port remains an assertion."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", port))
        return probe.getsockname()[1]


def artifact_summary(route_dir: Path) -> dict[str, Any]:
    required = ["lens-report.md", "lens-report.json", "accessibility.json", "screenshots/desktop.png", "screenshots/mobile.png"]
    return {
        "directory": os.fspath(route_dir.relative_to(ROOT)),
        "required_artifacts_present": {path: (route_dir / path).is_file() for path in required},
    }


def verify_not_found_fallback(base_url: str, route: dict[str, Any]) -> dict[str, Any]:
    """Prove the temporary server responds with the generated 404 document."""
    fallback_url = f"{base_url}{route['fallback_path']}"
    try:
        with urlopen(fallback_url, timeout=5) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
    except HTTPError as response:
        status = response.code
        body = response.read().decode("utf-8", errors="replace")
    expected = route["fallback_text"]
    return {
        "url": fallback_url,
        "http_status": status,
        "expected_status": 404,
        "contains_expected_text": expected in body,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-build", action="store_true", help="Use an existing generated output/ directory.")
    parser.add_argument("--port", type=int, default=0, help="Loopback port for the temporary static server (0 chooses one).")
    parser.add_argument("--lens-bin", help="Lens executable; defaults to LENS_BIN or PATH.")
    args = parser.parse_args()

    try:
        lens = resolve_lens(args.lens_bin)
        manifest = json.loads(MANIFEST.read_text())
        if manifest.get("schema_version") != "1.0.0":
            raise RuntimeError(f"unsupported receipt schema: {manifest.get('schema_version')!r}")
        if not CONFIG.is_file():
            raise RuntimeError(f"Lens configuration is missing: {CONFIG}")
        routes = manifest.get("routes")
        if not isinstance(routes, list) or not routes:
            raise RuntimeError("route manifest must contain at least one route")
        if not args.skip_build:
            subprocess.run(["./scripts/build.sh"], cwd=ROOT, check=True)
        output = ROOT / "output"
        if not (output / "404.html").is_file():
            raise RuntimeError("generated output is missing output/404.html")
    except (OSError, RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"QA-001 setup failed: {error}", file=sys.stderr)
        return 2

    try:
        port = reserve_port(args.port)
    except OSError as error:
        print(f"QA-001 setup failed: cannot bind 127.0.0.1:{args.port}: {error}", file=sys.stderr)
        return 2

    run_id = dt.datetime.now(tz=dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = ROOT / ".lens/runs" / f"qa-001-{run_id}"
    run_dir.mkdir(parents=True, exist_ok=False)
    host = "127.0.0.1"
    base_url = f"http://{host}:{port}"
    server = subprocess.Popen(
        [sys.executable, "scripts/serve_qa.py", "--directory", "output", "--host", host, "--port", str(port)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    receipt: dict[str, Any] = {
        "receipt_version": "1.0.0",
        "task": "QA-001",
        "status": "failed",
        "started_at": dt.datetime.now(tz=dt.timezone.utc).isoformat(),
        "lens": lens,
        "base_url": base_url,
        "manifest": {
            "path": os.fspath(MANIFEST.relative_to(ROOT)),
            "sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
            "schema_version": manifest["schema_version"],
        },
        "viewports": manifest.get("viewports", []),
        "routes": [],
    }
    exit_code = 0
    try:
        wait_for_server(f"{base_url}/", server)
        for route in routes:
            route_id = route["id"]
            spec = ROOT / route["spec"]
            if not spec.is_file():
                raise RuntimeError(f"route {route_id} references a missing spec: {spec}")
            route_dir = run_dir / route_id
            completed = subprocess.run(
                [lens, "check", f"{base_url}{route['path']}", "--config", os.fspath(CONFIG), "--spec", os.fspath(spec), "--out", os.fspath(route_dir), "--html", "--json"],
                cwd=Path(lens).parent,
                text=True,
            )
            route_receipt = {
                "id": route_id,
                "path": route["path"],
                "spec": route["spec"],
                "exit_code": completed.returncode,
                **artifact_summary(route_dir),
            }
            if "fallback_path" in route:
                route_receipt["fallback_probe"] = verify_not_found_fallback(base_url, route)
            receipt["routes"].append(route_receipt)
            if completed.returncode != 0:
                exit_code = 1
    except (OSError, RuntimeError, KeyError) as error:
        print(f"QA-001 receipt failed: {error}", file=sys.stderr)
        exit_code = 2
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()

    receipt["finished_at"] = dt.datetime.now(tz=dt.timezone.utc).isoformat()
    receipt["status"] = "passed" if exit_code == 0 else "failed"
    (run_dir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"QA-001 {receipt['status']}: {run_dir.relative_to(ROOT)}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
