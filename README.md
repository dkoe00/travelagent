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

## Two Entry Points, One Pipeline

The assistant handles both **concrete** requests ("I want to go to Albania — what can I do there?") and **vague** ones ("I want to hike along the coast somewhere in Europe"). Both feed the same pipeline; the Coordinator interactively extracts constraints and decides where to enter.

The pipeline is built as separable **building blocks**, each developed in isolation first. How the blocks ultimately communicate (`agent.as_tool()` vs `handoffs`) is deliberately left open until each block works on its own.

```
Vague input    → Destination Agent suggests candidates → [user picks one]
Concrete input ───────────────────────────────────────────┐
                                                           ↓
┌─ Block 1: Entry (vague → concrete) ──────────────────────────────┐
│  Coordinator  +  Destination  +  Places → pool of POIs / stays   │
└──────────────────────────────┬────────────────────────────────────┘
                               ↓   (communication TBD)
┌─ Block 2: Enrichment ────────────────────────────────────────────┐
│  Itinerary Planner  ←→  Transportation  +  Budget                 │
└──────────────────────────────┬────────────────────────────────────┘
                               ↓
                     (pipeline complete)
                               ↓
┌─ Independent, last (only if time) ───────────────────────────────┐
│  Packing List → activity- and weather-aware list                  │
└───────────────────────────────────────────────────────────────────┘
```

Within Block 1, the Coordinator stays the single conversational partner. It orchestrates specialists via the SDK's `agent.as_tool()` (results return to the Coordinator), rather than transferring control via `handoffs`.

## Agent Architecture

All agents are **core** except the Packing List, which is independent and optional.

**Block 1 — Entry** (the vague → concrete flow):

- **Coordinator Agent**: extracts constraints interactively, routes to the right entry point, orchestrates specialists, synthesizes the final response
- **Destination Agent**: turns vague constraints into ranked candidate destinations
- **Places Agent**: suggests activities, sights, accommodation, and restaurants for a destination

**Block 2 — Enrichment** (the Itinerary Planner is the connective hub):

- **Itinerary Planner Agent**: schedules the selected places into feasible day-by-day time blocks; works with Transportation and Budget to refine the plan
- **Transportation Agent**: compares transport modes, estimates travel times and costs
- **Budget Agent**: estimates costs, handles currencies, flags budget overruns

**Independent** (built last, only if time allows):

- **Packing List Agent**: fully self-contained; fetches weather itself and produces an activity- and weather-aware list once the pipeline is complete. Possible stretch: a small shadcn frontend reusing a chat component for a nicer UI.

## Work Split

- **Paul** — Block 1: Coordinator, Destination, and Places agents (the vague → concrete flow)
- **Darius** — Transportation and Budget agents, developed in isolation first

The Itinerary Planner connects the two blocks. How they integrate — and who owns the Itinerary Planner — is decided in a later phase, once Block 1 and the Transportation/Budget agents each work independently.

The current implementation is an early work in progress focused on Block 1.

## Tech Stack

- Python
- uv for dependency and environment management
- OpenAI Agents SDK
- python-dotenv for local environment configuration
- Pydantic for structured data models
- *(possible stretch)* shadcn-based mini frontend reusing a chat component, primarily for the Packing List

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

Project setup, runtime configuration, and the minimal Coordinator smoke test are done. Current focus is **Block 1**. Next planned steps:

1. Destination Agent (mock tool → wiring → real API)
2. Places Agent (mock tool → wiring → real API)
3. Coordinator wiring Destination + Places via `as_tool()`, with interactive constraint extraction
4. Structured Pydantic outputs at the Block 1 agent boundaries
5. *(in parallel, isolated)* Transportation and Budget agents
6. Itinerary Planner as the connective hub, integrating the blocks
7. *(only if time)* Packing List Agent with real weather data (Open-Meteo) + optional shadcn frontend
8. End-to-end demo scenario for the seminar presentation