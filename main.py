from agents import Runner

from travelagent.agents.coordinator import build_coordinator_agent
from travelagent.config import APP_CONFIG
from travelagent.runtime import configure_agents_sdk


def collect_brief() -> str:
    print("\n✈  Travel Planner\n" + "─" * 40)
    destination = input(
        "\nWohin möchtest du reisen?\n"
        "  Konkretes Ziel oder grobe Idee, z.B. 'Lissabon' oder 'Küste in Europa'\n> "
    ).strip()
    interests = input(
        "\nWelche Interessen hast du?\n"
        "  z.B. Wandern, Kultur, Strand, lokales Essen\n> "
    ).strip()
    duration = input("\nWie viele Tage?\n> ").strip()
    acc_raw = input("\nSollen auch Unterkunftsoptionen dabei sein? (j/n)\n> ").strip().lower()
    include_accommodation = acc_raw.startswith("j")

    return "\n".join([
        f"Reiseziel oder Wunsch: {destination}",
        f"Interessen: {interests}",
        f"Reisedauer: {duration} Tage",
        f"Unterkunftsoptionen: {'ja' if include_accommodation else 'nein'}",
    ])


def main() -> None:
    configure_agents_sdk(APP_CONFIG)
    agent = build_coordinator_agent(APP_CONFIG)

    brief = collect_brief()
    print("\n" + "─" * 40 + "\n")

    result = Runner.run_sync(agent, brief)
    print(f"\n{result.final_output}\n")

    while True:
        try:
            user_input = input("Du: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nTschüss!")
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "beenden", "q"):
            print("Tschüss!")
            break
        result = Runner.run_sync(
            agent,
            result.to_input_list() + [{"role": "user", "content": user_input}],
        )
        print(f"\n{result.final_output}\n")


if __name__ == "__main__":
    main()
