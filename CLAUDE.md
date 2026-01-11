# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Copier template** for generating production-ready LangGraph agent services with FastAPI. The template source files are in `{{project_slug}}/` and use Jinja2 templating (`.jinja` extension). The `copier.yml` file defines all template variables and configuration options.

## Common Commands

### Testing the Template

```bash
# Generate a test project with defaults
copier copy . ./test-output --defaults --trust

# Generate with specific options
copier copy . ./test-output --trust \
  -d project_name="My Test Agent" \
  -d llm_provider=anthropic \
  -d database=sqlite

# Run the test script (tests multiple configurations)
./scripts/test-template.sh
```

### Testing Generated Projects

After generating a project into `test-output/`:

```bash
cd test-output/test-default
uv sync --frozen --all-extras
uv run pytest tests/ -v
uv run ruff check src/ tests/
uv run mypy src/

# Run a single test
uv run pytest tests/unit/test_config.py::test_settings_load -v

# Lint + test together
make check

# Run LangGraph Studio for interactive debugging
make studio
```

## Architecture

### Template Structure

- `copier.yml` - Template configuration: all variables, choices, computed values, and conditional exclusions
- `{{project_slug}}/` - Template files that get copied to generated projects
  - `.jinja` files are processed by Copier with variable substitution
  - Non-jinja files are copied as-is

### Generated Project Architecture

The template generates a LangGraph agent service with this structure:

```
src/
├── agents/           # Agent implementations
│   ├── base.py       # BaseAgent ABC with invoke/stream, checkpointing, metrics
│   ├── {name}.py     # Concrete agent (builds LangGraph StateGraph)
│   └── registry.py   # AgentRegistry for multi-agent management
├── api/v1/           # FastAPI routes
│   └── agents.py     # POST /agents/{name}/invoke, /stream (SSE), /history
├── core/             # Infrastructure
│   ├── config.py     # Pydantic Settings with env-specific loading
│   ├── security.py   # JWT auth (when use_auth=true)
│   ├── limiter.py    # Rate limiting (when use_rate_limiting=true)
│   └── metrics.py    # Prometheus metrics (when use_prometheus=true)
├── services/
│   ├── llm.py        # LLMService with retry logic, multi-provider support
│   └── database.py   # Database connections and checkpointer setup
├── tools/            # LangChain tools for agents
└── prompts/          # System prompts (markdown files)
```

### Key Patterns

**Agent Implementation**: Agents extend `BaseAgent`, implement `build_graph()` to define the LangGraph StateGraph, and `get_tools()` for available tools. The base class handles checkpointing (PostgreSQL/SQLite/Memory), streaming, and metrics.

**Conditional Code**: Template files use Jinja2 conditionals (`{%- if use_auth %}...{%- endif %}`) to include/exclude features based on template variables. When modifying templates, maintain these conditionals. Always test template changes with multiple configurations using `./scripts/test-template.sh`.

**Configuration**: Settings are loaded from environment-specific `.env` files (`.env.development`, `.env.production`) via Pydantic Settings.

## Template Variables

Key variables that affect code generation (see `copier.yml` for full list):

- `llm_provider`: openai | anthropic | azure | ollama (sets default, runtime switchable)
- `default_model`: any model name supported by the provider (user can input custom)
- `database`: postgresql | sqlite | memory
- `use_auth`, `use_rate_limiting`, `use_prometheus`: boolean feature flags
- `observability`: langfuse | langsmith | none
- `agent_name`: snake_case name for the default agent

## Multi-Provider LLM Support

Generated projects support **runtime provider switching**. The `llm_provider` template variable sets the default, but users can switch providers by:

1. Setting `LLM_PROVIDER` environment variable
2. Installing the required provider package: `pip install '.[openai]'`, `pip install '.[anthropic]'`, etc.
3. Configuring the appropriate API keys

The `src/services/llm.py` uses dynamic imports to load only the required provider at runtime.
