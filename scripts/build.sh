#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/workspace.py doctor --require runtime
python3 scripts/bundle_css.py --check
KUJO_BIN="${KUJO_BIN:-$(python3 scripts/workspace.py kujo-bin)}"
rm -rf output
"$KUJO_BIN" run ./build.kujo -- --site-url https://robertdevore.com
python3 scripts/inline_critical_css.py output
python3 scripts/harden_generated_output.py output
