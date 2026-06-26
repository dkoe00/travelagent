# travelagent

Travelagent is a Python-based prototype of a multi-agent travel planning assistant built for a university seminar on LLM-based agentic systems and multi-agent systems.

The project uses the OpenAI Agents SDK as the main framework under investigation. The goal is not only to build a working travel assistant, but also to understand, demonstrate, and critically evaluate how the SDK supports multi-agent system development.

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

The current implementation is an early work in progress. At this stage, the repository focuses on project setup, configuration, and minimal SDK smoke tests.

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

## Running the Prototype

Run the current terminal prototype with:

```bash
uv run python main.py
```

## Project Status

This repository is currently in the implementation setup phase. The next planned steps are:

1. finalize the runtime configuration for OpenAI-compatible custom endpoints
2. implement the minimal Coordinator Agent smoke test
3. add mock tools for weather, places, transportation, and budgeting
4. implement specialist agents and evaluate handoffs/delegation patterns
5. prepare a demo scenario for the seminar presentation