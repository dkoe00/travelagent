from agents import function_tool

_MOCK_DATA: dict[str, list[dict]] = {
    "museum": [
        {"name": "National History Museum", "area": "City Centre", "description": "Permanent collections on regional history and archaeology.", "tags": ["indoor", "rainy day", "budget entry"]},
        {"name": "Contemporary Art Museum", "area": "Cultural Quarter", "description": "Rotating exhibitions of local and international contemporary artists.", "tags": ["indoor", "mid-range entry", "instagram-worthy"]},
        {"name": "Maritime Museum", "area": "Waterfront", "description": "Historic ships, maps, and seafaring artefacts.", "tags": ["indoor", "budget entry", "good for kids"]},
    ],
    "historic": [
        {"name": "Old Town Fortress", "area": "Old Town", "description": "Medieval hilltop fortification with panoramic views.", "tags": ["iconic", "outdoor", "great views", "budget entry"]},
        {"name": "Cathedral Quarter", "area": "Old Town", "description": "Dense cluster of Romanesque and Gothic churches dating to the 12th century.", "tags": ["free", "outdoor", "iconic", "crowds expected"]},
        {"name": "Roman Ruins", "area": "City Centre", "description": "Excavated Roman-era foundations with an on-site interpretive centre.", "tags": ["budget entry", "outdoor", "hidden gem"]},
    ],
    "viewpoint": [
        {"name": "Hilltop Miradouro", "area": "Old Town", "description": "Popular sunset viewpoint overlooking the river and rooftops.", "tags": ["free", "outdoor", "sunset spot", "can get crowded"]},
        {"name": "Castle Terrace", "area": "Old Town", "description": "Elevated terrace inside the old castle walls with 360° views.", "tags": ["outdoor", "great views", "budget entry"]},
    ],
    "park": [
        {"name": "Botanical Garden", "area": "University Quarter", "description": "19th-century garden with rare species and shaded walking paths.", "tags": ["free", "outdoor", "peaceful", "good for a stroll"]},
        {"name": "Riverside Promenade", "area": "Waterfront", "description": "Long waterfront park with cycle lanes and weekend markets.", "tags": ["free", "outdoor", "locals favourite", "bike-friendly"]},
    ],
    "hiking": [
        {"name": "Coastal Trail", "area": "Coast", "description": "Moderate 12 km trail along cliffs with sea views and access to secluded beaches.", "tags": ["free", "outdoor", "strenuous", "great views", "half-day"]},
        {"name": "Nature Reserve Loop", "area": "Outskirts", "description": "Marked forest trail through protected scrubland, good for birdwatching.", "tags": ["free", "outdoor", "easy", "hidden gem", "half-day"]},
    ],
    "beach": [
        {"name": "Main City Beach", "area": "Beach District", "description": "Wide sandy beach with lifeguards, cafes and water-sports hire.", "tags": ["free", "outdoor", "popular", "good for families"]},
        {"name": "Hidden Cove", "area": "Coast", "description": "Small rocky cove accessible by a 20-minute coastal walk.", "tags": ["free", "outdoor", "hidden gem", "less crowded"]},
    ],
    "market": [
        {"name": "Weekly Farmers Market", "area": "City Centre", "description": "Local produce, cheeses and street food every Saturday morning.", "tags": ["free", "outdoor", "local life", "weekend only"]},
        {"name": "Artisan Craft Market", "area": "Cultural Quarter", "description": "Hand-made ceramics, textiles and jewellery from regional artists.", "tags": ["free", "outdoor", "good for souvenirs"]},
    ],
    "gallery": [
        {"name": "Photography Gallery", "area": "Cultural Quarter", "description": "Documentary and fine-art photography from Portuguese and international photographers.", "tags": ["indoor", "budget entry", "quiet", "rainy day"]},
        {"name": "Municipal Art Gallery", "area": "City Centre", "description": "Permanent collection of 20th-century paintings donated by local collectors.", "tags": ["free", "indoor", "hidden gem"]},
    ],
}

_FALLBACK: list[dict] = [
    {"name": "City Walking Tour", "area": "City Centre", "description": "Guided 2-hour walk covering the main sights and neighbourhoods.", "tags": ["budget entry", "outdoor", "good for orientation"]},
]


@function_tool
def search_activities(destination: str, category: str, max_results: int = 5) -> list[dict]:
    """Search for activities and points of interest in a destination by category.

    Categories: museum, historic, viewpoint, park, hiking, beach, market, gallery.
    Returns a list of activity objects with name, area, description, and tags.
    """
    results = _MOCK_DATA.get(category.lower(), _FALLBACK)
    return results[:max_results]  # MOCK
