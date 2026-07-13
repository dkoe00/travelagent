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

## Current Pipeline

For the full agent architecture, interaction diagram, and the `as_tool()` vs. `handoffs` design rationale, see [docs/architecture.md](docs/architecture.md).

The assistant handles both **concrete** requests ("I want to go to Albania — what can I do there?") and **vague** ones ("I want to hike along the coast somewhere in Europe"). Both feed the same pipeline; the Coordinator interactively extracts constraints and decides where to enter.

The Coordinator stays the single conversational partner. It orchestrates specialists via the SDK's `agent.as_tool()` so specialist results return to the Coordinator.

```
Vague input    → Destination Agent suggests candidates → [user picks one]
Concrete input ───────────────────────────────────────────┐
                                                           ↓
Coordinator → Places Agent → pool of POIs / restaurants / stays
            → Transportation Agent (+ Budget Agent internally)
            → Itinerary Agent → transport-aware day-by-day plan
```

## Agent Architecture

- **Coordinator Agent**: extracts constraints interactively, routes to the right entry point, orchestrates specialists, synthesizes the final response
- **Destination Agent**: turns vague constraints into ranked candidate destinations
- **Places Agent**: suggests activities, sights, accommodation, and restaurants for a destination
- **Transportation Agent**: compares route options, estimates travel times and costs, returns clusters, sequencing constraints, transfer buffers, and long-transfer warnings for itinerary planning
- **Budget Agent**: estimates transportation costs and explains cost assumptions; currently used by the Transportation Agent
- **Itinerary Planner Agent**: schedules the selected places into feasible day-by-day time blocks using transportation guidance
- **Packing List Agent**: once the itinerary is confirmed, receives control via a `handoffs=[...]` handoff (the one deliberate handoff in this system) and builds a packing list from it

## Tech Stack

- Python
- uv for dependency and environment management
- OpenAI Agents SDK
- python-dotenv for local environment configuration
- Pydantic for structured data models
- Tavily for web-backed destination and places search
- Nominatim and OSRM for early geocoding and route estimates

## Setup

Install dependencies with uv:

```bash
uv sync
```

Create a local `.env` file based on `.env.example`.

Required for the current prototype:

```env
LLM_API_KEY=your_api_key_here
TAVILY_API_KEY=your_tavily_key_here
```

Optional:

```env
LLM_BASE_URL=your_optional_custom_endpoint_here
LLM_MODEL=your_model_name_here
ENABLE_TRACING=false
LANGUAGE=de  # de (German) or en (English) — defaults to de
GOOGLE_PLACES_API_KEY=your_google_key_here   # future validation/enrichment path
```

Do not commit `.env` or any real API keys.

## Running the App

### Terminal CLI (original)

Run the terminal-based app with:

```bash
uv run python main.py
```

### Web Frontend

Start the FastAPI backend (port 8000):

```bash
uv run uvicorn travelagent.api.app:app --reload --port 8000
```

In another terminal, start the Vite frontend dev server (port 5173):

```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

**Architecture**: The FastAPI backend wraps the existing Coordinator agent and streams agent events (tool calls, text deltas) to the frontend via Server-Sent Events (SSE). The frontend renders a two-pane chat UI:
- Left: conversation with the Coordinator; specialized tool outputs (destination suggestions, places groups, itineraries) render as interactive cards
- Right: sidebar showing detected constraints (region, activity, duration, month, budget), pipeline progress (Constraints → Destination → Places → Itinerary), and recent tool-call log

**SSE Event Vocabulary** (emitted by `travelagent/api/events.py`):
| Event | Payload |
|-------|---------|
| `text_delta` | `{"delta": str}` — streamed coordinator text |
| `tool_started` | `{"tool": str, "arguments": str}` — coordinator called a specialist tool |
| `tool_finished` | `{"tool": str, "payload": any}` — tool returned (parsed JSON or structured output) |
| `constraints` | `{"region": ..., ...}` — constraint update |
| `final` | `{"text": str}` — final synthesized message |
| `error` | `{"message": str}` — run failure |
| `done` | `{}` — stream ended |

The streaming uses the SDK's `Runner.run_streamed()` + `stream_events()` (SDK-provided); SSE translation and session management are project-implemented.

## Project Status

The current prototype wires Coordinator, Destination, Places, Transportation, Budget, and Itinerary agents into one terminal flow. The next planned steps are:

1. Run and fix an end-to-end smoke test with a concrete destination.
2. Improve final Coordinator presentation of transport and budget caveats.
3. Add deterministic checks for agent construction and expected tool wiring.
4. Replace heuristic routing/cost shortcuts with stronger providers over time.
5. Future work: Packing Agent, Google Places validation, live prices, richer public transport data, and optional UI.
