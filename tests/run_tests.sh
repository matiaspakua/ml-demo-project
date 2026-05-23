#!/usr/bin/env bash
set -euo pipefail

PYTHON=".venv/bin/python"
REPORT_DIR="tests/report"
APP_PID=""

cleanup() {
  if [ -n "$APP_PID" ]; then
    echo "Stopping Flask app (PID $APP_PID)..."
    kill "$APP_PID" 2>/dev/null || true
    wait "$APP_PID" 2>/dev/null || true
  fi
  lsof -ti:8111 | xargs kill -9 2>/dev/null || true
}
trap cleanup EXIT

echo "=== ML Demo Project — Test Suite ==="
echo ""

# ── Prepare ──────────────────────────────────────────────
mkdir -p "$REPORT_DIR/coverage"

# ── 1. Unit Tests + Coverage ─────────────────────────────
echo "--- 1. Unit Tests with Coverage ---"
$PYTHON -m pytest tests/ \
  --cov=src \
  --cov-report=term \
  --cov-report=html:"$REPORT_DIR/coverage" \
  --html="$REPORT_DIR/unit.html" \
  --self-contained-html \
  -v
echo "  Report: $REPORT_DIR/unit.html"
echo "  Coverage: $REPORT_DIR/coverage/index.html"
echo ""

# ── 2. Start App ─────────────────────────────────────────
echo "--- 2. Starting Flask app on port 8111 ---"
lsof -ti:8111 | xargs kill -9 2>/dev/null || true
$PYTHON src/run.py &
APP_PID=$!
sleep 3

if ! lsof -ti:8111 > /dev/null 2>&1; then
  echo "ERROR: App failed to start on port 8111"
  exit 1
fi
echo "  Flask app running (PID $APP_PID)"
echo ""

# ── 3. Locust Load Tests ─────────────────────────────────
echo "--- 3. Load Tests with Locust ---"
$PYTHON -m locust \
  --host=http://localhost:8111 \
  --locustfile tests/locustfile.py \
  --users=10 \
  --spawn-rate=1 \
  --run-time=30s \
  --headless \
  --only-summary \
  --html="$REPORT_DIR/load.html" \
  --logfile="$REPORT_DIR/locust.log" 2>&1
echo "  Report: $REPORT_DIR/load.html"
echo ""

# ── Summary ──────────────────────────────────────────────
echo "=== Test Suite Complete ==="
echo ""
echo "Reports:"
echo "  Unit Tests : file://$PWD/$REPORT_DIR/unit.html"
echo "  Coverage   : file://$PWD/$REPORT_DIR/coverage/index.html"
echo "  Load Tests : file://$PWD/$REPORT_DIR/load.html"
