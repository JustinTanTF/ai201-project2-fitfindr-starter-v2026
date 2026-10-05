"""
Your MCP server. ← UNIT 4, MILESTONE 1

Right now your tools only exist inside your own program. Nothing else can reach
them. MCP is an agreed shape you wrap a tool in so that anything speaking the
same protocol can call it — your agent today, a different agent tomorrow,
someone else's app after that.

**You're moving one tool. Not three.** The point is to see the seam.
`search_listings` is the one to move: it doesn't call the model, so nothing is
slow and nothing changes between runs while you're learning the shape.

    python mcp_server.py        starts the server (it will just sit there — that's right)
    python mcp_client.py        asks the server what it offers
"""

from mcp.server.fastmcp import FastMCP

from tools import search_listings as _search_listings_impl  # noqa: F401 — used below

# log_level="WARNING" keeps the server from printing an INFO line for every
# request. Without it your terminal fills with "Processing request of type
# CallToolRequest" and the output you actually care about scrolls away.
mcp = FastMCP("fitfindr", log_level="WARNING")


@mcp.tool()
def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search secondhand clothing listings by keyword, with an optional size and
    an optional price ceiling.

    description: free-text keywords to match against the listing's title,
        description, category, brand, style tags, and colors (e.g.
        "vintage graphic tee"). All keywords must appear somewhere in the
        listing's text for it to match.
    size: a size string to filter by, matched as a whole word, case-
        insensitively, against the listing's size field (e.g. "M" matches
        a listing sized "S/M" but not one sized "XL"). Pass None to skip
        size filtering.
    max_price: the highest acceptable price, in whole or fractional US
        dollars, inclusive. Pass None to skip the price filter.

    Returns a list of matching listing dicts, best keyword match first, each
    with id, title, description, category, style_tags, size, condition,
    price, colors, brand, and platform. Returns an empty list — never null,
    never an error — when nothing matches.
    """
    return _search_listings_impl(description, size, max_price)


# Two notes on the block above.
#
# The registered name is the *function* name — so the block above registers
# "search_listings", which is exactly what call_tool("search_listings", ...)
# asks for. That is also why the import at the top of this file brings the real
# implementation in under an alias: without it, the registered function and the
# one it calls would be the same name, and the tool would call itself.
#
# FastMCP builds the input schema from your type hints, which is why the hints
# are not optional here. `description: str` becomes a required string;
# `max_price: float | None = None` becomes an optional number. Getting these
# wrong is the most common reason a call is rejected.


if __name__ == "__main__":
    mcp.run()