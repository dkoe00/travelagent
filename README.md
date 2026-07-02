# travelagent

Travelagent is a Python-based multi-agent travel planning assistant. It started as a university seminar project on LLM-based agentic systems and multi-agent systems, but the project is now intended to continue beyond the seminar and become practically usable for private trip planning.

The project uses the OpenAI Agents SDK as the main framework. The near-term goal is still to keep the implementation small and understandable, while progressively replacing prototype shortcuts with reliable data sources, stronger planning logic, and workflows that are useful for real private travel decisions.

## Use Case

The assistant is intended to create travel itineraries and packing lists while considering constraints such as:

- destination and travel duration
- weather and season
- transportation options and travel times
- budget constraints
- activities and personal preferences
- accommodation and restaurants
- luggage constraints
- feasibility of the overall plan

## Planned Agent Architecture

The planned system consists of several specialized agents:

- **Coordinator Agent**: extracts user constraints, delegates subtasks, resolves conflicts, and coordinates the final response
- **Places Agent**: suggests activities, sights, accommodation, and restaurants
- **Packing List Agent**: creates adaptive packing lists based on weather, duration, activities, and luggage constraints
- **Transportation Agent**: compares transport modes, estimates travel times, and builds feasible routes
- **Budget Agent**: estimates costs, handles currencies if needed, and flags budget overruns
- **Itinerary Planner Agent**: schedules activities into feasible time blocks and creates fallback options

The current implementation is an early work in progress. At this stage, the repository focuses on the core multi-agent structure, transportation and budget tooling, and stable interfaces that can later be backed by better live data.

## Tech Stack

- Python
- uv for dependency and environment management
- OpenAI Agents SDK
- python-dotenv for local environment configuration
- Pydantic for structured data models

## Setup

Install dependencies with uv:

```bash
uv sync
```

Create a local `.env` file based on `.env.example` and configure the required LLM settings:

```env
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=your_optional_custom_endpoint_here
LLM_MODEL=your_model_name_here
ENABLE_TRACING=false
```

Do not commit `.env` or any real API keys.

## Running the App

Run the current terminal app with:

```bash
uv run python main.py
```

## Project Status

This repository is currently moving from seminar demo toward a usable private travel planning assistant. The next planned steps are:

1. wire specialist agents into the Coordinator workflow
2. complete transportation mode comparison with budget-aware recommendations
3. add live data sources for transport costs, public transport, weather, and places where feasible
4. keep deterministic fallback paths for repeatable local testing
5. replace prototype heuristics with production-quality providers as the app matures
