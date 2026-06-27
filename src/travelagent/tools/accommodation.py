from agents import function_tool

_MOCK_ACCOMMODATION: list[dict] = [
    {"name": "Hostel Bairro Alto", "area": "Old Town", "description": "Social hostel in the heart of the old quarter, rooftop terrace included.", "tags": ["hostel", "budget", "central", "social", "rooftop"]},
    {"name": "Guest House Ribeira", "area": "Waterfront", "description": "Small family-run guesthouse with river views and a home-cooked breakfast.", "tags": ["guesthouse", "budget", "river view", "quiet", "breakfast included"]},
    {"name": "Hotel Miradouro", "area": "Old Town", "description": "Boutique hotel inside a restored 18th-century townhouse.", "tags": ["boutique", "mid-range", "historic building", "central", "character"]},
    {"name": "Apartamentos Sol", "area": "Beach District", "description": "Self-catering apartments a 5-minute walk from the beach.", "tags": ["apartment", "mid-range", "self-catering", "near beach", "good for families"]},
    {"name": "Palace Hotel Avenida", "area": "City Centre", "description": "Grand 5-star hotel on the main avenue with a spa and rooftop pool.", "tags": ["luxury", "upscale", "spa", "rooftop pool", "central"]},
    {"name": "Eco Lodge Serra", "area": "Outskirts", "description": "Off-grid eco lodge in the hills, 20 minutes from the city by bus.", "tags": ["eco", "mid-range", "peaceful", "nature", "off the beaten path"]},
]


@function_tool
def search_accommodation(
    destination: str,
    preference: str | None = None,
    max_results: int = 4,
) -> list[dict]:
    """Search for accommodation options in a destination.

    preference: optional hint such as a price level ("budget", "upscale"), type
    ("hostel", "apartment", "boutique"), or vibe ("central", "near beach", "quiet").
    Returns a varied selection even when a preference is given.
    """
    if preference:
        pref = preference.lower()
        matched = [a for a in _MOCK_ACCOMMODATION if any(pref in t for t in a["tags"])]
        others = [a for a in _MOCK_ACCOMMODATION if a not in matched]
        results = (matched + others)[:max_results]
    else:
        results = _MOCK_ACCOMMODATION[:max_results]
    return results  # MOCK
