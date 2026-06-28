from agents import Runner

from travelagent.agents.coordinator import build_coordinator_agent
from travelagent.config import APP_CONFIG
from travelagent.runtime import configure_agents_sdk

_UI = {
    "de": {
        "destination_q": (
            "\nWohin möchtest du reisen?\n"
            "  Konkretes Ziel oder grobe Idee, z.B. 'Lissabon' oder 'Küste in Europa'\n> "
        ),
        "interests_q": (
            "\nWelche Interessen hast du?\n"
            "  z.B. Wandern, Kultur, Strand, lokales Essen\n> "
        ),
        "duration_q": "\nWie viele Tage?\n> ",
        "accommodation_q": "\nSollen auch Unterkunftsoptionen dabei sein? (j/n)\n> ",
        "yes_prefix": "j",
        "brief_accommodation_yes": "ja",
        "brief_accommodation_no": "nein",
        "prompt": "Du",
        "bye": "Tschüss!",
        "quit_words": {"exit", "quit", "beenden", "q"},
    },
    "en": {
        "destination_q": (
            "\nWhere would you like to travel?\n"
            "  Specific destination or vague idea, e.g. 'Lisbon' or 'Coastal Europe'\n> "
        ),
        "interests_q": (
            "\nWhat are your interests?\n"
            "  e.g. hiking, culture, beach, local food\n> "
        ),
        "duration_q": "\nHow many days?\n> ",
        "accommodation_q": "\nShould accommodation options be included? (y/n)\n> ",
        "yes_prefix": "y",
        "brief_accommodation_yes": "yes",
        "brief_accommodation_no": "no",
        "prompt": "You",
        "bye": "Goodbye!",
        "quit_words": {"exit", "quit", "q"},
    },
}


def collect_brief(ui: dict) -> str:
    print("\n✈  Travel Planner\n" + "─" * 40)
    destination = input(ui["destination_q"]).strip()
    interests = input(ui["interests_q"]).strip()
    duration = input(ui["duration_q"]).strip()
    acc_raw = input(ui["accommodation_q"]).strip().lower()
    include_accommodation = acc_raw.startswith(ui["yes_prefix"])

    return "\n".join([
        f"Reiseziel oder Wunsch: {destination}",
        f"Interessen: {interests}",
        f"Reisedauer: {duration} Tage",
        f"Unterkunftsoptionen: {ui['brief_accommodation_yes'] if include_accommodation else ui['brief_accommodation_no']}",
    ])


def main() -> None:
    configure_agents_sdk(APP_CONFIG)
    agent = build_coordinator_agent(APP_CONFIG)
    ui = _UI[APP_CONFIG.language]

    brief = collect_brief(ui)
    print("\n" + "─" * 40 + "\n")

    result = Runner.run_sync(agent, brief)
    print(f"\n{result.final_output}\n")

    while True:
        try:
            user_input = input(f"{ui['prompt']}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{ui['bye']}")
            break
        if not user_input:
            continue
        if user_input.lower() in ui["quit_words"]:
            print(ui["bye"])
            break
        result = Runner.run_sync(
            agent,
            result.to_input_list() + [{"role": "user", "content": user_input}],
        )
        print(f"\n{result.final_output}\n")


if __name__ == "__main__":
    main()
