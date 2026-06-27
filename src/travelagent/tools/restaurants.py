from agents import function_tool

_MOCK_RESTAURANTS: list[dict] = [
    {"name": "Trattoria da Marco", "area": "Old Town", "description": "Casual Italian trattoria with wood-fired pizza and a lively atmosphere.", "tags": ["italian", "mid-range", "book ahead", "lively"]},
    {"name": "La Bella Napoli", "area": "City Centre", "description": "No-frills pizza spot popular with locals at lunch.", "tags": ["italian", "budget", "cash only", "locals favourite"]},
    {"name": "Cantina Ribeira", "area": "Waterfront", "description": "Classic seafood restaurant on the river with a sunny terrace.", "tags": ["portuguese", "seafood", "mid-range", "riverside terrace", "locals favourite"]},
    {"name": "Tasca do Bairro", "area": "Residential", "description": "Tiny family-run tasca serving honest home cooking — no menu, just the day's catch.", "tags": ["portuguese", "budget", "hidden gem", "no reservations", "authentic"]},
    {"name": "O Mercado", "area": "City Centre", "description": "Busy market-style lunch spot with rotating daily specials.", "tags": ["portuguese", "budget", "great value", "busy at lunch", "no reservations"]},
    {"name": "Rooftop 28", "area": "City Centre", "description": "Rooftop bar and restaurant with panoramic views and cocktails.", "tags": ["international", "upscale", "rooftop view", "sunset spot", "pricey"]},
    {"name": "Marisqueira Atlantico", "area": "Waterfront", "description": "White-tablecloth seafood restaurant known for the freshest catch in the city.", "tags": ["seafood", "upscale", "reservation essential", "special occasion"]},
    {"name": "Quinta Moderna", "area": "Cultural Quarter", "description": "Tasting-menu restaurant with seasonal local produce.", "tags": ["fine dining", "upscale", "michelin-listed", "special occasion", "expensive"]},
    {"name": "Green Fork", "area": "University Quarter", "description": "Relaxed vegetarian and vegan cafe with daily lunch bowls.", "tags": ["vegetarian", "vegan", "mid-range", "casual", "gluten-free options"]},
    {"name": "Cafe Central", "area": "City Centre", "description": "All-day cafe for brunch, coffee and pastries — open from 7am.", "tags": ["cafe", "budget", "all-day brunch", "good for a break"]},
    {"name": "Spice Route", "area": "Cultural Quarter", "description": "Indian restaurant with a long menu and generous portions.", "tags": ["indian", "mid-range", "spicy", "good for groups"]},
    {"name": "Burger Yard", "area": "Beach District", "description": "Craft burgers and local beers near the beach.", "tags": ["american", "budget", "casual", "craft beer"]},
]


@function_tool
def search_restaurants(
    destination: str,
    preference: str | None = None,
    max_results: int = 6,
) -> list[dict]:
    """Search for restaurants and cafes in a destination.

    preference: optional free-text hint such as a cuisine type ("italian", "seafood"),
    price level ("budget", "upscale"), or vibe ("hidden gem", "special occasion").
    The preference biases the selection but never hard-filters — a varied mix is always
    returned so the user has real alternatives to compare.
    Returns objects with name, area, description, and tags.
    """
    if preference:
        pref = preference.lower()
        matched = [r for r in _MOCK_RESTAURANTS if any(pref in t for t in r["tags"])]
        others = [r for r in _MOCK_RESTAURANTS if r not in matched]
        seen = {r["name"] for r in matched}
        results = (matched + [r for r in others if r["name"] not in seen])[:max_results]
    else:
        results = _MOCK_RESTAURANTS[:max_results]
    return results  # MOCK
