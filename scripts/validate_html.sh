#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
npx --yes vnu-jar@26.8.6 --errors-only --skip-non-html "${1:-output}"
