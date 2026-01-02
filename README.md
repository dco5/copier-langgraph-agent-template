# copier-langgraph-agent

A production-ready [Copier](https://copier.readthedocs.io/) template for creating LangGraph agent services with FastAPI.

## Overview

This template generates a complete, production-ready LangGraph agent service with:

- **LangGraph 1.0+** - Modern agent patterns with state management
- **Multi-provider LLM support** - OpenAI, Anthropic, Azure OpenAI, or Ollama
- **State persistence** - PostgreSQL (recommended), SQLite, or in-memory
- **FastAPI REST API** - Streaming and non-streaming endpoints
- **Production features** - JWT auth, rate limiting, Prometheus metrics, structured logging

## Prerequisites

- **Python 3.10+**
- **Copier 9.0.0+** - Template engine
- **Git** - For version control of generated projects
- **uv** (recommended) or pip - For package management

### Install Copier

```bash
# Using uv (recommended)
uv tool install copier

# Or using pipx
pipx install copier

# Or using pip
pip install copier
```

## Quick Start

### Create a New Project

```bash
# From GitHub (when published)
copier copy gh:your-org/copier-langgraph-agent my-agent-service

# From local directory
copier copy /path/to/this/template my-agent-service
```

### Answer the Prompts

You'll be asked to configure:

1. **Project identity** - Name, description, author
2. **Agent configuration** - Default agent name and description
3. **Python version** - 3.10, 3.11, 3.12, or 3.13
4. **LLM provider** - OpenAI, Anthropic, Azure, or Ollama
5. **Database** - PostgreSQL, SQLite, or in-memory
6. **Observability** - Langfuse, LangSmith, or none
7. **Optional features** - Docker, Streamlit UI, auth, rate limiting, etc.

### Start Development

```bash
cd my-agent-service

# Copy environment file and add your API keys
cp .env.example .env.development

# Install dependencies
make install-dev

# Start the service
make dev
```

Visit http://localhost:8000/docs for API documentation.

## Template Options

### Core Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `project_name` | str | My Agent Service | Human-readable project name |
| `project_slug` | str | (derived) | Directory and package name (lowercase, hyphens) |
| `project_description` | str | ... | Short project description |
| `author_name` | str | Your Name | Author name |
| `author_email` | str | you@example.com | Author email |

### Agent Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `agent_name` | str | assistant | Default agent name (snake_case) |
| `agent_description` | str | ... | What the agent does |

### Technical Stack

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `python_version` | choice | 3.12 | Python version (3.10-3.13) |
| `llm_provider` | choice | openai | LLM provider |
| `default_model` | str | (derived) | Default model for the provider |
| `database` | choice | postgresql | State persistence backend |

**LLM Provider Options:**
- `openai` - GPT-4.1, GPT-4.1-mini
- `anthropic` - Claude Sonnet 4, Claude Haiku 4
- `azure` - Azure OpenAI Service
- `ollama` - Local models (llama3.3, etc.)

**Database Options:**
- `postgresql` - Production-ready with pgvector support
- `sqlite` - File-based, simpler setup
- `memory` - No persistence (development only)

### Optional Features

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `use_docker` | bool | true | Docker & docker-compose configuration |
| `use_auth` | bool | true | JWT authentication |
| `use_rate_limiting` | bool | true | Request rate limiting |
| `use_prometheus` | bool | true | Prometheus metrics & Grafana dashboards |
| `use_streamlit` | bool | false | Streamlit WebUI for prototyping |
| `use_semantic_memory` | bool | true | mem0ai + pgvector (PostgreSQL only) |
| `use_trustcall` | bool | true | Automatic memory extraction |
| `include_hitl_examples` | bool | true | Human-in-the-loop code examples |

### Observability

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `observability` | choice | none | LLM tracing platform |

**Options:** `langfuse`, `langsmith`, `none`

### License

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `license` | choice | MIT | Project license |

**Options:** `MIT`, `Apache-2.0`, `BSD-3-Clause`, `Proprietary`

## Generated Project Structure

```
my-agent-service/
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── base.py          # Base agent class with LangGraph
│   │   ├── {agent_name}.py  # Your default agent
│   │   └── registry.py      # Agent registry
│   ├── api/                 # FastAPI routes
│   │   └── v1/
│   │       ├── agents.py    # Agent invoke/stream endpoints
│   │       ├── auth.py      # Authentication (if enabled)
│   │       └── health.py    # Health checks
│   ├── core/                # Core infrastructure
│   │   ├── config.py        # Settings management
│   │   ├── security.py      # JWT, password hashing
│   │   ├── logging.py       # Structured logging
│   │   ├── middleware.py    # Request middleware
│   │   ├── metrics.py       # Prometheus metrics
│   │   └── limiter.py       # Rate limiting
│   ├── services/            # Business logic
│   │   ├── llm.py           # LLM service with retries
│   │   └── database.py      # Database service
│   ├── tools/               # LangChain tools
│   ├── prompts/             # Agent system prompts
│   ├── schemas/             # Pydantic schemas
│   ├── models/              # SQLAlchemy models
│   ├── memory/              # Memory system
│   ├── client/              # Python SDK
│   └── main.py              # Application entry point
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── infrastructure/
│   ├── docker/              # Dockerfiles
│   ├── prometheus/          # Prometheus config
│   └── grafana/             # Grafana dashboards
├── streamlit_app/           # Streamlit UI (if enabled)
├── .env.example             # Environment template
├── docker-compose.yml       # Production Docker
├── docker-compose.dev.yml   # Development Docker
├── pyproject.toml           # Dependencies
├── Makefile                 # Development commands
├── langgraph.json           # LangGraph Studio config
└── README.md                # Project documentation
```

## Updating Projects

To update a generated project when the template changes:

```bash
cd my-agent-service
copier update
```

Copier will:
1. Show you what has changed
2. Apply updates to your project
3. Preserve your customizations where possible

## Development

### Testing the Template Locally

```bash
# Generate a test project with defaults
copier copy . ./test-output --defaults --trust

# Test with specific options
copier copy . ./test-output --trust \
  -d project_name="My Test Agent" \
  -d llm_provider=anthropic \
  -d database=sqlite

# Verify the generated project
cd test-output
make install-dev
make lint
make test
```

### Running Template Tests

```bash
# Run the test script
./scripts/test-template.sh
```

### CI/CD

The template includes GitHub Actions workflows that:
- Test multiple Python versions (3.10, 3.11, 3.12)
- Test multiple LLM providers (OpenAI, Anthropic)
- Test multiple databases (PostgreSQL, SQLite, Memory)
- Validate Docker builds

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTS                                 │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│  Streamlit   │   External   │   Custom     │   Python SDK      │
│     UI       │   Services   │   Clients    │   (AgentClient)   │
└──────┬───────┴──────┬───────┴──────┬───────┴───────┬───────────┘
       └──────────────┴──────────────┴───────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Service                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Auth      │  │   Rate      │  │   Request Context       │  │
│  │ Middleware  │  │  Limiter    │  │   (structlog)           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                      API Routes (v1)                            │
│  POST /agents/{name}/invoke  │  POST /agents/{name}/stream      │
│  GET  /agents/info           │  GET  /health                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Agent Registry                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   LangGraph Engine                      │    │
│  │  • State Management    • Checkpointing                  │    │
│  │  • Tool Execution      • Human-in-the-Loop             │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌─────────────────┐   ┌─────────────────┐
│    Tools      │   │     Memory      │   │   Observability │
├───────────────┤   ├─────────────────┤   ├─────────────────┤
│ Custom tools  │   │ LangGraph Store │   │ Langfuse/Smith  │
│ for your      │   │ Semantic memory │   │ Prometheus      │
│ domain        │   │ (pgvector)      │   │ Grafana         │
└───────────────┘   └─────────────────┘   └─────────────────┘
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `copier copy . ./test-output --trust`
5. Submit a pull request

## Acknowledgments

This template was created by combining and extending two excellent projects:

- [fastapi-langgraph-agent-production-ready-template](https://github.com/wassim249/fastapi-langgraph-agent-production-ready-template) by @wassim249 - Production-ready FastAPI patterns and infrastructure
- [react-agent](https://github.com/langchain-ai/react-agent) by LangChain - LangGraph agent patterns and best practices

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

Built with [Copier](https://copier.readthedocs.io/) and [LangGraph](https://langchain-ai.github.io/langgraph/).
