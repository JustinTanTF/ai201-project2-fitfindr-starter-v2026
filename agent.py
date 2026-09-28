"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price pulled out of it
        "searched": False,           # True once search_listings has run
        "search_results": [],         # everything search_listings returned
        "selected_item": None,       # the one chosen — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── query parsing (regex) ─────────────────────────────────────────────────────

def parse_query(query: str) -> dict:
    """Pull description, size, and max_price out of a plain-language query."""
    max_price = None
    size = None
    remaining = query

    # price: "under $30", "below 30", "less than $25.50", "max $40"
    m = re.search(
        r"(?:under|below|less than|max|up to)\s*\$?\s*(\d+(?:\.\d+)?)",
        remaining,
        re.I,
    )
    if not m:
        m = re.search(r"\$\s*(\d+(?:\.\d+)?)", remaining)  # bare "$30"
    if m:
        max_price = float(m.group(1))
        remaining = remaining.replace(m.group(0), " ")

    # size: "size M", "size 8", "size XXS"
    s = re.search(r"\bsize\s+([A-Za-z0-9]+)", remaining, re.I)
    if s:
        size = s.group(1).upper()
        remaining = remaining.replace(s.group(0), " ")

    # what's left is the description, minus filler words
    remaining = re.sub(
        r"\b(looking for|i want|i need|a|an|the)\b", " ", remaining, flags=re.I
    )
    description = re.sub(r"[,\s]+", " ", remaining).strip()

    return {"description": description, "size": size, "max_price": max_price}


def _empty_search_message(parsed: dict) -> str:
    """Tell the user what they could change, based on what they asked for."""
    tips = []
    if parsed.get("max_price") is not None:
        tips.append(f"raise your price limit above ${parsed['max_price']:.0f}")
    if parsed.get("size"):
        tips.append(f"try a different size than {parsed['size']} or leave size out")
    tips.append("use fewer or more general keywords")
    return (
        f"Nothing matched '{parsed.get('description', '')}'. To get results, "
        + ", or ".join(tips)
        + "."
    )


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Each pass looks at the session, decides which step is next, runs it, and
    stores the result. The branch: if search_listings returns an empty list,
    put a message in session["error"] and stop before suggest_outfit.

    Returns:
        The session dict. Check session["error"] first — if it isn't None,
        the run ended early and the later fields will still be None.
    """
    session = new_session(query, wardrobe)

    count = 0
    while True:
        count += 1
        trace.check_iterations(count)

        # step 1: parse the query
        if not session["parsed"]:
            session["parsed"] = parse_query(session["query"])

        # step 2: search
        elif not session["searched"]:
            p = session["parsed"]
            session["search_results"] = search_listings(
                p["description"], p["size"], p["max_price"]
            )
            session["searched"] = True

        # THE BRANCH: nothing came back → say what to change and stop
        elif not session["search_results"]:
            session["error"] = _empty_search_message(session["parsed"])
            return session

        # step 3: choose an item
        elif session["selected_item"] is None:
            session["selected_item"] = session["search_results"][0]

        # step 4: outfit ideas, reading the item back out of the session
        elif session["outfit_suggestion"] is None:
            session["outfit_suggestion"] = suggest_outfit(
                session["selected_item"], session["wardrobe"]
            )

        # step 5: fit card
        elif session["fit_card"] is None:
            session["fit_card"] = create_fit_card(
                session["outfit_suggestion"], session["selected_item"]
            )

        # everything is filled in
        else:
            return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )