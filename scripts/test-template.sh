#!/bin/bash
# Test template generation with various configurations

set -e

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${TEMPLATE_DIR}/test-output"

# Clean up
rm -rf "${OUTPUT_DIR}"
mkdir -p "${OUTPUT_DIR}"

echo "Testing copier-langgraph-agent template..."
echo "=========================================="

# Test 1: Default configuration
echo ""
echo "Test 1: Default configuration (OpenAI + PostgreSQL)"
copier copy "${TEMPLATE_DIR}" "${OUTPUT_DIR}/test-default" --defaults --trust \
  -d project_name="Default Test" \
  -d project_slug="default-test" \
  -d author_name="Test Author" \
  -d author_email="test@example.com"

cd "${OUTPUT_DIR}/test-default"
echo "  - Generated project structure"
ls -la
echo "  - Checking Python syntax..."
python3 -m py_compile src/main.py
echo "  - Test 1: PASSED"

# Test 2: Anthropic + SQLite
echo ""
echo "Test 2: Anthropic + SQLite"
copier copy "${TEMPLATE_DIR}" "${OUTPUT_DIR}/test-anthropic-sqlite" --defaults --trust \
  -d project_name="Anthropic Test" \
  -d project_slug="anthropic-test" \
  -d llm_provider="anthropic" \
  -d database="sqlite" \
  -d use_docker=false

cd "${OUTPUT_DIR}/test-anthropic-sqlite"
echo "  - Checking Python syntax..."
python3 -m py_compile src/main.py
echo "  - Test 2: PASSED"

# Test 3: Minimal configuration (no auth, no rate limiting, no prometheus)
echo ""
echo "Test 3: Minimal configuration"
copier copy "${TEMPLATE_DIR}" "${OUTPUT_DIR}/test-minimal" --defaults --trust \
  -d project_name="Minimal Test" \
  -d project_slug="minimal-test" \
  -d database="memory" \
  -d use_auth=false \
  -d use_rate_limiting=false \
  -d use_prometheus=false \
  -d use_docker=false

cd "${OUTPUT_DIR}/test-minimal"
echo "  - Checking Python syntax..."
python3 -m py_compile src/main.py
echo "  - Test 3: PASSED"

# Test 4: Full configuration with Streamlit
echo ""
echo "Test 4: Full configuration with Streamlit"
copier copy "${TEMPLATE_DIR}" "${OUTPUT_DIR}/test-full" --defaults --trust \
  -d project_name="Full Test" \
  -d project_slug="full-test" \
  -d use_streamlit=true \
  -d observability="langfuse"

cd "${OUTPUT_DIR}/test-full"
echo "  - Checking Python syntax..."
python3 -m py_compile src/main.py
echo "  - Test 4: PASSED"

echo ""
echo "=========================================="
echo "All tests passed!"
echo ""
echo "Generated projects in: ${OUTPUT_DIR}"
echo ""
echo "To test a specific project:"
echo "  cd ${OUTPUT_DIR}/test-default"
echo "  uv sync --frozen --all-extras"
echo "  uv run pytest tests/ -v"
