from agents import Runner

from travelagent.agents.coordinator import build_coordinator_agent
from travelagent.config import APP_CONFIG
from travelagent.runtime import configure_agents_sdk


def main() -> None:
    configure_agents_sdk(APP_CONFIG)
    agent = build_coordinator_agent(APP_CONFIG)
    result = Runner.run_sync(
        agent,
        "Plan a simple 3-day city break in Lisbon for a solo traveler.",
    )
    print(result.final_output)


if __name__ == "__main__":
    main()
