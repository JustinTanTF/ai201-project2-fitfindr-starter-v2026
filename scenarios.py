"""
The runs your test needs. ← UNIT 4, MILESTONE 3
"""

SCENARIOS = [
    {
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        "name": "state — item id stays consistent",
        "query": "oversized flannel shirt",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        "name": "fit card quality — hoodie",
        "query": "vintage graphic hoodie",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "price ceiling — graphic tee under $30",
        "query": "graphic tee under $30",
        "wardrobe": "example",
        "criterion": 5,
        "tries": 1,
    },
    {
        "name": "price ceiling — denim jacket under $45",
        "query": "denim jacket under $45",
        "wardrobe": "example",
        "criterion": 5,
        "tries": 1,
    },
    {
        "name": "price ceiling — flannel shirt under $25",
        "query": "flannel shirt under $25",
        "wardrobe": "example",
        "criterion": 5,
        "tries": 1,
    },
    {
        "name": "price ceiling — vintage hoodie under $30",
        "query": "vintage hoodie under $30",
        "wardrobe": "example",
        "criterion": 5,
        "tries": 1,
    },
    {
        "name": "price ceiling — mesh top under $20",
        "query": "mesh top under $20",
        "wardrobe": "example",
        "criterion": 5,
        "tries": 1,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems