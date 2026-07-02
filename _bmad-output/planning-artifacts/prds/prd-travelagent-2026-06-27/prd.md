---
title: 'travelagent PRD'
status: 'draft'
created: '2026-06-27'
updated: '2026-06-27'
---

# PRD: travelagent

## 0. Document Purpose

This PRD defines the scope for `travelagent`, a Python-based seminar prototype of a multi-agent travel planning assistant built with the OpenAI Agents SDK. The document is for the implementation team preparing a 10-minute university seminar presentation on LLM-based agentic systems and multi-agent systems. It prioritizes requirements that make the SDK usage observable and discussable, especially handoffs, tool calls, extensibility, and development experience.

The PRD is not a product-launch plan. It captures a functional prototype sufficient to support credible presentation observations about the OpenAI Agents SDK. Technical implementation details beyond product requirements should remain in architecture or implementation notes.

## 1. Vision

`travelagent` should demonstrate how a multi-agent system can break a travel planning request into specialized subtasks, coordinate the outputs, and return a coherent travel recommendation. The system should cover several meaningful aspects of travel planning, including itinerary planning, transportation and route choices, packing guidance, and supporting contextual information.

The main value is not the travel plan itself, but the learning and evaluation surface it creates. The prototype should give the team concrete experience with the OpenAI Agents SDK: how agents are defined, how handoffs work in practice, how tools are called, how easy the system is to extend, and where the framework is strong or awkward.

For the seminar, there will be no required live demo. The system still needs to work well enough that the team can honestly describe what was implemented, what worked, what was difficult, and whether they would choose the framework again.

## 2. Target User

### 2.1 Jobs To Be Done

- As a seminar team member, understand how the OpenAI Agents SDK supports a concrete multi-agent use case.
- As a presenter, explain the agent architecture and framework usage clearly within a 10-minute presentation.
- As an evaluator of the SDK, observe which features are useful, missing, difficult, or manually implemented.
- As a prototype user, provide a travel request and receive a coherent travel plan assembled from multiple specialist contributions.

### 2.2 Non-Users (v1)

- Real travelers relying on the system for production-grade booking, safety, pricing, or route accuracy.
- Users expecting live travel inventory, booking flows, real-time disruptions, or guaranteed factual travel data.
- Stakeholders expecting continued product development after the seminar.

### 2.3 Key User Journeys

- **UJ-1. Paul prepares evidence for the seminar presentation.** Paul, a seminar participant, runs or inspects the prototype before preparing slides. He wants to see the full planned agent set, working handoffs, and working tool calls so the presentation can discuss real framework experience rather than only planned architecture.
- **UJ-2. A prototype user asks for a city trip plan.** A user provides a travel request with destination, duration, preferences, and constraints. The Coordinator Agent identifies the needed subtasks, delegates to specialist agents, uses tool-backed context where available, and returns a combined response with itinerary, transport guidance, and packing recommendations.
- **UJ-3. The team extends the system with another capability.** A team member adds or refines a Specialist Agent or API-backed tool and observes how much boilerplate, manual wiring, and SDK-specific knowledge are required. The result feeds the presentation's framework usage and lessons-learned sections.

## 3. Glossary

- **Coordinator Agent** — The central agent that interprets the user request, delegates work, resolves conflicts, and assembles the final response.
- **Travel Planning Assistant** — The overall multi-agent system that plans travel itineraries and packing lists around sights, activities, weather, transportation, and budget.
- **Specialist Agent** — One of the fixed domain agents: Packing List Agent, Places Agent, Transportation Agent, Budget Agent, or Itinerary Planner Agent.
- **Packing List Agent** — The Specialist Agent responsible for generating suitable packing lists from weather, trip duration, planned activities, luggage constraints, destination-specific essentials, documents, chargers, medication, toiletries, and user preferences.
- **Places Agent** — The Specialist Agent responsible for finding and evaluating suitable activities, accommodation, and restaurants, including place search, details, opening hours, visit duration, preference ranking, and booking requirements.
- **Transportation Agent** — The Specialist Agent responsible for evaluating movement between locations, including geocoding, travel times, transport mode comparison, public transport availability, airport or station transfers, and route building.
- **Budget Agent** — The Specialist Agent responsible for estimating and tracking financial feasibility, including currency conversion, activity, transport, accommodation, and meal costs, daily and total budgets, cheaper versus premium alternatives, and budget overrun flags.
- **Itinerary Planner Agent** — The Specialist Agent responsible for assembling inputs into a coherent day-by-day itinerary with time blocks, travel times, opening hours, meals, breaks, nearby-place clustering, budget and preference balance, feasibility validation, and fallback options.
- **Handoff** — An OpenAI Agents SDK mechanism by which one agent delegates part of a task to another agent.
- **Tool Call** — A model-initiated call to a provided function or tool, used here primarily to access travel-relevant data from existing open or public APIs where feasible.
- **External Data Tool** — A tool wrapper around an existing open or public API for weather, places, geocoding, routing, currency, or cost-related data.
- **Fallback Data** — A small controlled local dataset or deterministic fallback used only when an external API is unavailable, unsuitable, or too costly for the seminar prototype.
- **Travel Plan** — The final user-facing response assembled from specialist outputs.
- **Seminar Presentation** — The 10-minute presentation focused on use case, architecture, framework usage, observations, lessons learned, conclusion, and recommendations.

## 4. Features

### 4.1 Multi-Agent Travel Planning Architecture

**Description:** The system exposes a Travel Planning Assistant built from a Coordinator Agent and five fixed Specialist Agents: Packing List Agent, Places Agent, Transportation Agent, Budget Agent, and Itinerary Planner Agent. The architecture must be concrete enough to support the presentation's architecture section and implemented enough to evaluate real SDK behavior. Realizes UJ-1 and UJ-2.

**Functional Requirements:**

#### FR-1: Coordinator Agent accepts and coordinates travel planning requests

The Coordinator Agent can accept a natural-language travel planning request, extract trip constraints, ask for or infer missing inputs, delegate to Specialist Agents, track shared trip state, resolve conflicts between agent outputs, and produce the final user-facing response.

**Consequences (testable):**
- Given a request with destination, duration, and preferences, the Coordinator Agent produces or initiates planning for places, transportation, budget, itinerary, and packing concerns.
- The Coordinator Agent remains responsible for the final combined Travel Plan.

#### FR-2: System includes all fixed Specialist Agents

The system must include the Coordinator Agent plus the Packing List Agent, Places Agent, Transportation Agent, Budget Agent, and Itinerary Planner Agent.

**Consequences (testable):**
- The Packing List Agent contributes weather-aware, activity-aware, duration-aware, luggage-aware packing guidance.
- The Places Agent contributes activities, accommodation, and restaurant candidates with relevant details such as opening hours, visit duration, preference ranking, and booking requirements where available.
- The Transportation Agent contributes routes, travel times, transport mode comparison, public transport availability, and airport or station transfer estimates where available.
- The Budget Agent contributes daily and total budget estimates, cost categories, cheaper versus premium alternatives, and budget overrun flags.
- The Itinerary Planner Agent assembles inputs into a feasible day-by-day plan with time blocks, meals, breaks, nearby-place clustering, and fallback options.
- Specialist responsibilities are distinguishable in code and explainable on architecture slides.

#### FR-3: Specialist outputs are integrated into one response

The Coordinator Agent can combine Specialist Agent outputs into one coherent Travel Plan.

**Consequences (testable):**
- The final response includes sections or content for itinerary, places, transportation, budget, and packing.
- The response avoids obvious contradictions between specialist outputs, such as recommending activities incompatible with stated trip duration.

### 4.2 SDK Handoffs

**Description:** Handoffs are a central OpenAI Agents SDK feature and must work in the prototype. The system should use handoffs for actual task delegation, not only as inert code examples. Realizes UJ-1, UJ-2, and UJ-3.

**Functional Requirements:**

#### FR-4: Coordinator delegates to Specialist Agents through handoffs

The Coordinator Agent uses SDK handoffs to route relevant subtasks to Specialist Agents.

**Consequences (testable):**
- A representative travel request triggers at least one actual handoff from the Coordinator Agent to a Specialist Agent.
- The implementation gives the team enough evidence to discuss how handoffs are configured and how they behave.

#### FR-5: Handoff design is observable for presentation analysis

The implementation must make it possible for the team to inspect and explain how handoffs are defined, triggered, and extended.

**Consequences (testable):**
- The code clearly shows agent roles and handoff relationships.
- The team can answer whether adding another Specialist Agent required low or high effort.

### 4.3 SDK Tool Calls and External Data

**Description:** Tool calls must work in the prototype because they are another central SDK feature. Tools should preferably wrap existing open or public APIs for travel-relevant data, with Fallback Data allowed when an API is unavailable, unsuitable, or outside the seminar prototype's effort budget. Realizes UJ-1 and UJ-2.

**Functional Requirements:**

#### FR-6: System provides travel-relevant External Data Tools

The system includes External Data Tools for at least two travel-planning concerns.

**Consequences (testable):**
- Candidate tools include weather lookup, place search or details, geocoding, route or transport estimates, currency conversion, budget estimates, or packing constraints.
- Each External Data Tool has a clear owner agent or usage path.
- If an external API is unavailable, unsuitable, rate-limited, or requires unacceptable setup, the system may use Fallback Data while preserving the same tool-call interface. [ASSUMPTION: Public/open APIs will be selected during implementation based on availability, setup effort, and fit.]

#### FR-7: At least one agent performs real tool calls

At least one Specialist Agent or the Coordinator Agent uses SDK tool calls during planning.

**Consequences (testable):**
- A representative travel request triggers at least one tool call against an External Data Tool or its Fallback Data implementation.
- The team can explain what had to be implemented manually for tools and what the SDK provided.

#### FR-8: Tool output influences the Travel Plan

Tool results must affect the final Travel Plan rather than being unused diagnostics.

**Consequences (testable):**
- Weather data influences packing recommendations.
- Places and transport data influence route, schedule, or itinerary recommendations.
- Budget or currency data influences feasibility warnings or cheaper versus premium alternatives.

### 4.4 Seminar Evaluation Support

**Description:** The prototype must generate enough implementation experience to support the required presentation topics: use case and objectives, architecture, framework usage, results and observations, conclusion, and recommendations. Realizes UJ-1 and UJ-3.

**Functional Requirements:**

#### FR-9: System supports architecture explanation

The implemented architecture must be simple enough to explain in approximately two minutes while still demonstrating a real multi-agent setup.

**Consequences (testable):**
- The team can identify each agent, its responsibility, and how coordination works.
- The architecture can be represented on one slide without hiding major behavior.

#### FR-10: System supports framework usage discussion

The implementation must expose concrete SDK usage points for the presentation.

**Consequences (testable):**
- The team can discuss agent definitions, handoffs, tool calls, model or endpoint configuration, and extension effort.
- The team can describe at least one feature that was useful in practice and at least one feature that was missing, difficult, or required manual work. [ASSUMPTION: These observations will be gathered during implementation rather than specified in advance.]

#### FR-11: System supports lessons learned and recommendations

The implementation must leave the team with enough evidence to answer whether they would choose the OpenAI Agents SDK again for this use case.

**Consequences (testable):**
- The team can describe development challenges encountered.
- The team can assess suitability for larger or more dynamic multi-agent systems.
- The team can summarize main strengths and weaknesses of the framework.

### 4.5 Terminal Prototype Execution

**Description:** The current repository is a Python terminal prototype. The MVP should preserve that form factor unless the team explicitly decides otherwise. [ASSUMPTION: No web or graphical interface is required.] Realizes UJ-1 and UJ-2.

**Functional Requirements:**

#### FR-12: Prototype runs from the command line

The prototype can be executed locally through the existing `uv` workflow.

**Consequences (testable):**
- `uv sync` installs dependencies.
- `uv run python main.py` runs the current prototype path or its updated equivalent.

#### FR-13: Runtime configuration remains environment-driven

The system uses environment variables for LLM configuration and tracing settings.

**Consequences (testable):**
- `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`, and `ENABLE_TRACING` remain the supported configuration variables.
- API keys and custom endpoints are not hard-coded in agents, tools, schemas, or `main.py`.

## 5. Non-Goals (Explicit)

- No production travel booking, reservation, payment, or ticketing workflow.
- No live travel inventory, real-time route disruptions, guaranteed weather accuracy, or authoritative pricing.
- No requirement for a live demo during the seminar presentation.
- No web UI, mobile app, account system, persistence layer, or deployment pipeline for MVP.
- No post-seminar product roadmap unless the team later changes the project goal.
- No claim that travel recommendations are safe, complete, or suitable for real-world reliance.

## 6. MVP Scope

### 6.1 In Scope

- Python-based terminal prototype using the OpenAI Agents SDK.
- Coordinator Agent plus all five fixed Specialist Agents: Packing List, Places, Transportation, Budget, and Itinerary Planner.
- Working SDK handoffs for agent delegation.
- Working SDK tool calls using External Data Tools where feasible, with Fallback Data allowed to protect seminar scope.
- Travel Plan output covering itinerary, places, transportation or routes, budget, and packing.
- Environment-based LLM configuration compatible with the existing project setup.
- Enough implementation notes or observable behavior to support the seminar presentation checklist.

### 6.2 Out of Scope for MVP

- Production-grade travel data integrations or guaranteed API completeness.
- UI beyond terminal execution.
- Authentication, user profiles, saved trips, or long-term memory.
- Automated slide generation.
- Comprehensive evaluation benchmark across many frameworks.
- Full scalability implementation for large dynamic multi-agent systems; only reasoned assessment from prototype experience is required.

## 7. Success Metrics

**Primary**

- **SM-1:** Multi-agent completeness: the prototype includes the Coordinator Agent and all five fixed Specialist Agents with distinct responsibilities. Validates FR-1, FR-2, FR-3.
- **SM-2:** SDK handoff evidence: at least one representative travel request exercises real SDK handoff behavior. Validates FR-4, FR-5.
- **SM-3:** SDK tool-call evidence: at least one representative travel request exercises real SDK tool-call behavior through an External Data Tool or compatible Fallback Data, and the tool output affects the final Travel Plan. Validates FR-6, FR-7, FR-8.
- **SM-4:** Presentation readiness: the team can answer every item in the seminar presentation checklist using actual implementation experience. Validates FR-9, FR-10, FR-11.

**Secondary**

- **SM-5:** Repeatability: the main prototype path can be run locally with documented `uv` commands and controlled API or Fallback Data behavior. Validates FR-12, FR-13.
- **SM-6:** Extensibility learning: the team can describe the effort required to add or modify a Specialist Agent or tool. Validates FR-5, FR-10, FR-11.

**Counter-metrics (do not optimize)**

- **SM-C1:** Travel realism should not be optimized at the expense of SDK observability. The prototype exists to evaluate framework usage, not to be the best travel planner.
- **SM-C2:** Architecture complexity should not be optimized upward. More agents are only useful if they improve the seminar's evaluation evidence.

## 8. Presentation Alignment

The implementation should support the required presentation structure:

- **Introduction of use case and objectives:** Explain why travel planning is suitable for demonstrating multi-agent coordination.
- **Agentic system architecture:** Show Coordinator Agent, Specialist Agents, handoffs, and tools.
- **Framework usage and development experience:** Discuss how the OpenAI Agents SDK was used and what manual work remained.
- **Results, observations, and lessons learned:** Report how handoffs, tool calls, extension, and configuration behaved in practice.
- **Conclusion and recommendations:** State whether the team would choose the framework again and why.

The implementation should also prepare answers to these checklist questions:

- What was the use case, and how was it realized?
- How suitable is the framework for this use case?
- Which framework features were most useful in practice?
- Which framework features were missing or difficult to use?
- What had to be implemented manually that the team expected the framework to provide?
- How easy was it to extend the system with additional agents, tools, or capabilities?
- What challenges occurred during development?
- How scalable is the framework for larger or more dynamic multi-agent systems?
- What are the main strengths and weaknesses of the framework?
- Would the team choose this framework again? Why or why not?

## 9. Constraints and Guardrails

- Keep secrets in `.env`; never commit real API keys.
- Prefer existing open or public APIs over self-built mock tools where setup effort and reliability are acceptable.
- Keep a small Fallback Data path available when an external API would make the seminar prototype fragile.
- Keep the implementation aligned with the existing `src/travelagent/` package layout.
- Avoid hard-coding model names in agents; use runtime configuration.
- Do not wire tools into the Coordinator Agent without updating instructions that currently say not to use tools.
- Treat the project as a bounded seminar prototype, not an expandable product platform.

## 10. Open Questions

1. Which exact open or public APIs will be used for weather, places, geocoding/routing, transport availability, currency conversion, and cost estimates?
2. Which External Data Tools are required for MVP, and which can fall back to controlled local data?
3. Should the final Travel Plan use a structured Pydantic output model or a plain textual response?
4. Will tracing be enabled and used as presentation evidence?
5. What representative travel request should be used as the main development and presentation scenario?
6. What observations should be captured during implementation: friction log, screenshots, tracing output, code snippets, or slide notes?

## 11. Assumptions Index

- §4.4 / FR-10 — Observations about useful, missing, or difficult SDK features will be gathered during implementation rather than specified in advance.
- §4.5 — No web or graphical interface is required for MVP.
- §4.3 / FR-6 — Public/open APIs will be selected during implementation based on availability, setup effort, and fit.
