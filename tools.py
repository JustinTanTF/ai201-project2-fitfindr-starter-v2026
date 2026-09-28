"""
The three FitFindr tools.

    search_listings(description, size, max_price)  -> list[dict]
    suggest_outfit(new_item, wardrobe)             -> str
    create_fit_card(outfit, new_item)              -> str

Each one can be called and tested on its own, before it is wired into the loop.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── helpers ───────────────────────────────────────────────────────────────────

STOPWORDS = {"a", "an", "the", "for", "and", "or", "in", "with", "of", "to", "looking"}


def _words(text: str) -> list[str]:
    """Lowercase alphanumeric tokens."""
    return re.findall(r"[a-z0-9]+", (text or "").lower())


def _stem(word: str) -> str:
    """Crude plural handling so 'tees' matches 'tee'."""
    return word[:-1] if len(word) > 3 and word.endswith("s") else word


def _size_matches(wanted: str, listing_size: str) -> bool:
    """
    Whole-token size match, so 'M' matches 'S/M' but 'S' does not match 'US 9'
    or 'XL'. Tokens come from splitting on anything that isn't a letter/digit.
    """
    return wanted.lower() in set(_words(listing_size))


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings for items matching a description, and optionally a size
    and a price ceiling.

    Args:
        description: keywords describing what the user wants.
        size:        size string, or None to skip. Matched as a whole token,
                     case-insensitively ("M" matches "S/M", not "XL" or "US 9").
        max_price:   maximum price, inclusive, or None to skip.

    Returns:
        A list of matching listing dicts, best keyword match first (ties broken
        by lower price), at most config.SEARCH_RESULT_LIMIT long.
        Returns [] when nothing matches — never None.
    """
    keywords = {_stem(w) for w in _words(description) if w not in STOPWORDS}
    scored = []

    for item in load_listings():
        if max_price is not None and item["price"] > max_price:
            continue
        if size and not _size_matches(size, item.get("size") or ""):
            continue

        haystack = " ".join([
            item.get("title") or "",
            item.get("description") or "",
            item.get("category") or "",
            item.get("brand") or "",
            " ".join(item.get("style_tags") or []),
            " ".join(item.get("colors") or []),
        ])
        hay_words = {_stem(w) for w in _words(haystack)}

        score = len(keywords & hay_words)
        if score == 0:
            continue
        scored.append((score, item))

    scored.sort(key=lambda pair: (-pair[0], pair[1]["price"]))
    return [item for _, item in scored][: config.SEARCH_RESULT_LIMIT]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def _describe_item(item: dict) -> str:
    """One readable line for a listing or a wardrobe item."""
    parts = [f"{k}: {v}" for k, v in item.items() if v not in (None, "", [])]
    return "; ".join(parts)


def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    Args:
        new_item: a listing dict.
        wardrobe: a wardrobe dict with an 'items' list. May be empty.

    Returns:
        A non-empty string. With an empty wardrobe, general styling advice for
        the item instead of specific combinations.
    """
    item_text = _describe_item(new_item)
    owned = (wardrobe or {}).get("items") or []

    if not owned:
        prompt = (
            "You are a thrift-fashion stylist. Someone is considering this "
            f"secondhand item:\n{item_text}\n\n"
            "They haven't told you what else they own. Give one or two outfit "
            "ideas built around it using common basics, in a few short "
            "sentences. Be specific about pieces and vibe."
        )
    else:
        wardrobe_text = "\n".join(f"- {_describe_item(w)}" for w in owned)
        prompt = (
            "You are a thrift-fashion stylist. Someone is considering this "
            f"secondhand item:\n{item_text}\n\n"
            f"Here is what they already own:\n{wardrobe_text}\n\n"
            "Suggest one or two outfits that combine the new item with pieces "
            "from their wardrobe. Name the specific wardrobe pieces you use. "
            "Keep it to a few short sentences."
        )

    result = generate(prompt)
    if not result or not str(result).strip():
        return f"Try pairing the {new_item.get('title', 'item')} with simple basics you already own."
    return str(result).strip()


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict.

    Returns:
        A two-to-four sentence caption. If `outfit` is empty or whitespace,
        returns a descriptive message instead of raising.
    """
    if not outfit or not outfit.strip():
        return "Can't write a fit card yet: there is no outfit suggestion to base it on."
    price = new_item.get("price")
    price_text = f"${price:g}" if isinstance(price, (int, float)) else f"${price}"

    prompt = (
        "Write a 2-4 sentence social media caption from someone who just "
        "thrifted this item and is showing off the find. They BOUGHT it "
        "secondhand; they are not selling it. Sound like a real person "
        "posting, not a product description. Mention the item name, its "
        f"price ({price_text}), and the platform ({new_item.get('platform')}) "
        "once each, and be specific about the vibe.\n\n"
        f"Item: {_describe_item(new_item)}\n"
        f"Outfit idea: {outfit}\n\n"
        "Return only the caption."
    )

    result = generate(prompt)
    if not result or not str(result).strip():
        return f"Found the {new_item.get('title')} for ${new_item.get('price')} on {new_item.get('platform')}."
    return str(result).strip()