#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/workspace.py doctor --require runtime
KUJO_BIN="${KUJO_BIN:-$(python3 scripts/workspace.py kujo-bin)}"
rm -rf output
"$KUJO_BIN" run ./build.kujo -- --site-url https://robertdevore.com
