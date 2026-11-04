#!/usr/bin/env bash
# Compatibility entry point; the validated configuration is now the default.
set -euo pipefail
CODE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
echo "局部刷新方案已转为默认配置，执行 start2.sh。"
exec bash "$CODE/start2.sh"
