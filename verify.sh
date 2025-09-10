#!/usr/bin/env bash
set -euo pipefail
shasum -a 256 -c SHA256SUMS.txt
echo "✅ archive verified"
