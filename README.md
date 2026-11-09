# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps find which clothes or accessory a shopper is looking for and what clothes or accessory match. How it works is a person would list a description of the clothing item and fitfindr would help find clothes based of their description through the clothing listing and find an acessory that would go along with it.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

## Tool Inventory

### `search_listings`

- **What it does:** Searches the listings file for items matching keywords from the user's description, with an optional size filter and an optional price ceiling.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None). A `None` size or price skips that filter. Size matching is case-insensitive and whole-token, so "M" matches "S/M" but not "XL" or "US 9". `max_price` is inclusive.
- **Returns:** A list of listing dicts, best keyword match first (ties broken by lower price), at most `config.SEARCH_RESULT_LIMIT` long. Each dict has `id`, `title`, `description`, `category`, `style_tags` (list), `size`, `condition`, `price` (float), `colors` (list), `brand` (str or None), and `platform`.
- **When it has nothing:** Returns an empty list `[]`, never `None` and never an exception.

### `suggest_outfit`

- **What it does:** Given a thrifted item and the user's wardrobe, asks the model for one or two outfit ideas that use the item.
- **Inputs:** `new_item` (dict, one listing), `wardrobe` (dict with an `items` key holding a list of wardrobe item dicts; the list may be empty).
- **Returns:** A non-empty string of outfit suggestions. With a non-empty wardrobe, the suggestions name specific pieces the user already owns.
- **When it has nothing:** With an empty wardrobe, returns general styling advice for the item instead of failing. If the model returns an empty response, returns a plain fallback sentence pairing the item with basics.

### `create_fit_card`

- **What it does:** Asks the model to write a short social media caption for the find, based on the item and the outfit suggestion.
- **Inputs:** `outfit` (str, from `suggest_outfit`), `new_item` (dict, one listing).
- **Returns:** A two-to-four sentence caption string that mentions the item, its price, and its platform.
- **When it has nothing:** If `outfit` is empty or whitespace, returns a descriptive message saying there is no outfit to base a caption on, without calling the model or raising. If the model returns an empty response, returns a one-line fallback with the item, price, and platform.

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` that tells the user what to change (raise the price limit, try a different size or drop it, use different keywords), then return the session without calling `suggest_outfit` or `create_fit_card`. Otherwise, take the first result as `selected_item` and continue to `suggest_outfit`, then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::parse_query`. It pulls a price from phrases like "under $30" or "below 25", a size from "size M", and treats the remaining words (minus filler like "a" and "looking for") as the description.

**What moves through the session:** `query`, then `parsed` (description, size, max_price), then `search_results`, then `selected_item`, then `outfit_suggestion`, then `fit_card`. Each tool's result is stored in the session and read back out for the next call. `error` is set only when the run ends early.

---

---

## Sample Run

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
[3] select_item
      in:  10 candidates
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: Y2K Streetwear Contrast** Pair the baby tee with your **baggy straight-leg jeans** (`w_001`) to ba…
[5] create_fit_card
      in:  dict with keys: item
      out: Found the absolute ultimate Y2K Baby Tee — Butterfly Print on depop for only $18 and I am never taking it off.…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Y2K Streetwear Contrast**
Pair the baby tee with your **baggy straight-leg jeans** (`w_001`) to balance out the fitted crop with a baggy lower half. Complete the look with your **chunky white sneakers** (`w_007`) and **black crossbody bag** (`w_010`) for an effortless off-duty model vibe.

**Outfit 2: Edgy Retro Mix**
Layer the tee under your **vintage black denim jacket** (`w_006`) paired with your **wide-leg khaki trousers** (`w_002`) for a cool mix of earthy tones and Y2K graphics. Ground the outfit with your **black combat boots** (`w_008`) to add a little grunge edge to the sweet butterfly print.

  Fit card: Found the absolute ultimate Y2K Baby Tee — Butterfly Print on depop for only $18 and I am never taking it off. It’s giving total off-duty model vibes when I style it with baggy low-rise jeans and chunky sneakers. Such a win!

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]
```

```
$ python -c "from tools import search_listings; print(search_listings('ballgown', size='XXS', max_price=5))"
[]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
**Outfit 1: Off-Duty Streetwear**
Pair the vintage Levi's with the **White ribbed tank top (w_003)** and layer on the **Oversized grey crewneck sweatshirt (w_004)** for that effortless, slouchy silhouette. Finish the look with the **Chunky white sneakers (w_007)** and the **Black crossbody bag (w_010)**.

**Outfit 2: Edgy Vintage**
Tuck the **White ribbed tank top (w_003)** into the 501s, cinch your waist with the **Brown leather belt (w_009)**, and throw on the **Vintage black denim jacket (w_006)**. Ground the fit with the **Black combat boots (w_008)** for a cool, texturally rich denim-on-denim moment.
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_empty_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_empty_wardrobe()))"
For an effortless weekend look, pair these vintage 501s with a crisp white boxy t-shirt tucked in, a well-worn black leather belt, and classic canvas sneakers for a timeless, casual streetwear vibe.

If you want to dress them up slightly for evening, layer an oversized charcoal gray blazer over a fitted black ribbed tank top, and add chunky black loafers and silver hoop earrings to lean into an effortless model-off-duty aesthetic.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Still not over finding these Vintage Levi's 501 Jeans in the absolute best medium wash. Just dropped them on my depop for $38.0 and honestly debating keeping them for myself. Pair them with some beat-up white sneakers and you've got the ultimate effortless fit.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('   ', load_listings()[0]))"
Can't write a fit card yet: there is no outfit suggestion to base it on.
```

## How I Used AI

**Moment 1**

- _What I asked for:_ I asked Claude to build `search_listings` in `tools.py` from the starter's TODO (filter by price and size, score by keyword overlap, drop zeros, sort best first). I gave it my listing fields from `python app.py listings --full -n 3`.
- _What came back:_ A working search that returned `[]` on no match and matched sizes by whole token, so "M" matched "S/M". But when I ran `search_listings('graphic tee', max_price=30)`, the top result was a Mesh Long-Sleeve Top, not a graphic tee. Its description says "great for layering under a graphic tee," and every keyword hit counted equally, so it tied with the real tees and won on price.
- _What I changed:_ I weighted matches by where they occur: a keyword in the title scores 3, in `style_tags` scores 2, and elsewhere (description, category, brand, colors) scores 1. Real tees now outrank items that only mention a tee in passing. A known limit remains: the search can't read negation, so a sweatshirt described as "no graphics" still matches "graphic."

**Moment 2**

- _What I asked for:_ I asked Claude to write `create_fit_card`, which prompts the model for a 2-4 sentence caption that mentions the item, price and platform.
- _What came back:_ The caption sounded like a seller: "Just dropped them on my depop for $38.0 and honestly debating keeping them for myself." It also printed the price as `$38.0`. That's wrong for a tool meant for someone who found the item.
- _What I changed:_ I rewrote the prompt to say the person bought the item secondhand and is showing off the find, not selling it. I also formatted the price with `f"${price:g}"` so it reads `$38`. I re-ran the tool several times to check the voice and the wording variation.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

Run Log — Before
Criterion Target Try 1 Try 2 Try 3 Try 4 Try 5 Verdict

1. A matching query completes all three tools 4 of 5 PASS PASS PASS PASS PASS MET (5/5)
2. An impossible query stops before the second tool 5 of 5 PASS PASS PASS PASS PASS MET (5/5)
3. The item found by search is the item the next tool receives 5 of 5 N/A N/A N/A N/A N/A UNVERIFIABLE — trace never logged the item's id, only its title
4. The fit card is a usable caption (5 regenerations) 4 of 5 PASS PASS PASS PASS PASS MET (5/5)
5. Search respects the price ceiling (5 queries) 5 of 5 queries, 0 violations PASS PASS PASS PASS PASS MET on the single query actually tested — doesn't satisfy "5 queries" as written

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
Produced by run_eval.py::run_once -> agent.py::run_agent, calling tools.py::search_listings
(via mcp_server.py), tools.py::suggest_outfit, tools.py::create_fit_card

Query: vintage graphic tee under $30

[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
[3] select_item
      in:  10 candidates
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  dict with keys: item, wardrobe_items
      out: Hey bestie! At just $18, this Y2K butterfly baby tee is an absolute Depop steal. ...
[5] create_fit_card
      in:  dict with keys: item
      out: Found the absolute cutest Y2K Baby Tee — Butterfly Print on Depop for only $18! The pink and purple graphic gives major early 2000s off-duty model energy, and I am so obsessed with how it fits. Can't wait to style this with some baggy denim and chunky sneakers!
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

Verdicts and Diagnoses

# Criterion Target Verdict How I decided

1 A matching query completes all three tools 4/5 MET (5/5) All 5 tries reached create_fit_card without session["error"] being set, per the trace output.
2 An impossible query stops before the second tool 5/5 MET (5/5) All 5 tries hit branch: empty search and returned before suggest_outfit ran.
3 Item id stays consistent across select_item -> suggest_outfit -> create_fit_card 5/5 MISSED — unverifiable agent.py::run_agent's trace.step() calls for steps 4 and 5 only ever logged item.get("title"), never item.get("id"). The item's title stayed consistent across all 5 tries, which is suggestive, but the criterion specifically asks for an id comparison (precisely because two items could share a title), and that evidence was never captured.
4 Fit card is a usable caption (5 regenerations) 4/5 MET (5/5) All 5 cards were 2–4 sentences and named $26 and depop once each. No two openings were byte-identical. Worth flagging anyway: 2 of 5 followed the near-identical template "Scored this [item] on depop for [just/only] $26 and I am [adverb] never taking it off," which passes the literal rule but is the templating the criterion was written to catch.
5 Search respects the price ceiling (5 queries) 5 queries, 0 violations MISSED — doesn't test what's written scenarios.py had one scenario for this criterion, run 5 times with the identical query "graphic tee under $30". All 5 tries returned the same $15 item, so this demonstrates 0 violations across 1 query repeated, not across 5 distinct price ceilings.

**Diagnoses**

Criterion 3 — loop/tracing gap, not a tool or session bug. The item dict almost certainly does flow through the session unchanged (nothing in agent.py copies or reconstructs session["selected_item"] between steps), but run_agent's own instrumentation never recorded the one field (id) that would prove it. Place: agent.py::run_agent's trace.step() calls. Mechanism: those calls build an inputs dict with {"item": session["selected_item"].get("title"), ...} and never include .get("id").
Criterion 5 — test design gap, not a tools.py bug. search_listings's price filter (item["price"] > max_price, a plain comparison) is not implicated by anything in this run — every item returned respected its ceiling. The gap is that scenarios.py encoded the criterion as one scenario with 5 tries of the same query, when the criterion calls for 5 different queries, each with a price ceiling, checked once.

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] parse_query
      in:  vintage graphic hoodie
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Vintage Graphic Hoodie — Faded Black, Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey … +7 more
[3] select_item
      in:  10 candidates
      out: Vintage Graphic Hoodie — Faded Black ($26.0, depop)
[4] suggest_outfit
      in:  dict with keys: item, wardrobe_items
      out: **Outfit 1: Effortless Grunge Streetwear** Pair the vintage graphic hoodie with your baggy dark-wash straight-…
[5] create_fit_card
      in:  dict with keys: item
      out: Scored this Vintage Graphic Hoodie on depop for just $26 and I am never taking it off. That perfectly faded bl…
```

**Empty search**

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] branch: empty search
      out: Nothing matched 'designer ballgown'. To get results, raise your price limit above $5, or try a different size …
      →    stopping before suggest_outfit
```

**On the MCP move:** I moved only `search_listings`. In `mcp_server.py` it is registered with `@mcp.tool()` (the real implementation is imported from `tools.py` under an alias, so the tool doesn't call itself), and its type hints (`description: str`, `size: str | None`, `max_price: float | None`) become the input schema. In `agent.py::_run_loop`, step 2 now calls `mcp_client.call_tool("search_listings", {...})` instead of calling the function directly, and the trace step is named `search_listings (via MCP)`. `suggest_outfit` and `create_fit_card` are still plain function calls. `python mcp_client.py` lists the one tool with its three parameters. The results were the same as the direct call (same 10 items, same order), but each call now starts `mcp_server.py` as a separate subprocess over stdio, which is why empty-search runs still take about 1–2 s even though they make no model calls.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**
What I changed: Two things. (1) In agent.py, added item_id to the inputs dict logged for the suggest_outfit trace step, so the item's id — not just its title — would be visible alongside select_item's output. (2) In scenarios.py, replaced the single "price ceiling" scenario (one query, run 5 times) with 5 scenarios, each a different query with a different price ceiling, each needing only 1 try since the price filter is deterministic — which required adding a per-scenario "tries" override, read in run_eval.py's main loop via scenario.get("tries", args.tries).
**Which failure it was meant to fix:**
Which failure it was meant to fix: Criterion 5's "one query isn't five queries" gap, and criterion 3's missing id evidence.

### Run Log — After

Run Log — After
Criterion Target Try 1 Try 2 Try 3 Try 4 Try 5 Verdict

1. A matching query completes all three tools 4/5 PASS PASS PASS PASS PASS MET (5/5)
2. An impossible query stops before the second tool 5/5 PASS PASS PASS PASS PASS MET (5/5)
3. Item id stays consistent 5/5 N/A N/A N/A N/A N/A STILL UNVERIFIABLE — see below
4. Fit card is a usable caption (5 regenerations) 4/5 PASS PASS PASS PASS PASS MET (5/5)
5. Search respects the price ceiling (5 distinct queries: tee<=$30, jacket<=$45, flannel<=$25, hoodie<=$30, mesh top<=$20) 5/5, 0 violations PASS PASS PASS PASS PASS MET (5/5) — $15, $42, $22, $26, $15, all under their ceilings

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

     Criterion 5 — yes, clearly. The after-run actually exercises 5 distinct price ceilings instead of one query repeated, and all 5 returned non-empty results that respected their ceiling. That's the criterion as originally written, satisfied for the first time.

Criterion 3 — no, my fix didn't work, and I know because the new trace still reads in: dict with keys: item_id, item, wardrobe_items for suggest_outfit — that's just the key names, not the actual id value; every dict-typed input in this whole log renders the same way (e.g. parse_query's output is always printed as dict with keys: description, size, max_price, never the values). So adding item_id as a dict key didn't make it visible. On top of that, I never made the matching edit to create_fit_card's trace call — it still only logs dict with keys: item, unchanged from the before run. This criterion needs a real fix, not the one I tried.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

     Criterion 3 is still unmeasured. The real fix is to stop passing the id inside a dict (which trace.step() collapses to key-names-only) and instead bake it into a formatted string, e.g. inputs=f"item_id={session['selected_item'].get('id')}", applied to both the suggest_outfit and create_fit_card trace calls. I ran out of time to confirm this against trace.py's actual formatting logic before submitting, so I'm reporting it as unresolved rather than claiming a fix that isn't verified.

Criterion 4's templating risk. All 5 fit cards pass the letter of "no shared opening sentence," but 2–3 of 5 across both runs lean on the same "scored + item + price + and I am [adverb] never taking it off" structure. Not a failure by the written rule, but if I had more time I'd tighten create_fit_card's prompt in tools.py to explicitly ask for varied sentence openings, then re-test.
select_item always takes index [0] from the search results — no criterion tests whether that's actually the "best" choice (vs. closest to budget, best condition, etc.), so this is unexplored, not necessarily broken.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

# Capstone

## What This Extends

FitFindr (my unit 3/4 agent: `search_listings` → `suggest_outfit` → `create_fit_card`). New: synonym matching in `tools.py::search_listings`, plus a structured run log (`runlog.py`, `logs/runs.jsonl`).

## The Shape

**C — extend one capability.** Search now expands each query word into a group of equivalents (`t-shirt`→`tee`, `trainers`→`sneakers`, `trousers`→`pants`, `purse`→`bag`, `jumper`→`sweater`, …; `tools.py::SYNONYM_GROUPS`), so wording that doesn't literally appear in a listing can still find it.

**Out of scope:** The things out of scope are inventory conetents and price filters which are unchanged. There are also no changes to how results being ranked or which tools are being picked. There are also no new tools.

## Running It

Path B (local with logs). See [RUNNING.md](RUNNING.md).

## Instrumentation

`agent.py::run_agent` writes one JSON line per run to `logs/runs.jsonl` via `runlog.py::write`, in a `finally` block so crashes are logged too. Fields: `ts`, `input`, `parsed`, `synonym_groups` (which expansions fired), `n_results`, `selected_id`, `ids_seen` (item id at select / suggest_outfit / create_fit_card), `outcome` (`completed` / `empty_search` / `crashed`), `output`, `error`, `duration_s`, `model_calls`, `prompt_tokens`, `output_tokens`.


Last 12 entries from `python runlog.py --tail 12`:

```
$ python runlog.py --tail 12
{"ts": "2026-11-09T02:32:56+00:00", "input": "vintage graphic tee under $30", "parsed": {"description": "vintage graphic tee", "size": null, "max_price": 30.0}, "synonym_groups": [["tee", "tshirt"]], "n_results": 10, "selected_id": "lst_002", "ids_seen": {"selected": "lst_002", "suggest_outfit": "lst_002", "create_fit_card": "lst_002"}, "outcome": "completed", "output": "Finally scored this Y2K Baby Tee — Butterfly Print on depop for just $18 and I'm obsessed with the pastel pink and purple vibes! Throwing it on with baggy jeans and chunky sneakers gives me the exact effortless streetwear look I was going for.", "error": null, "duration_s": 9.247, "model_calls": 2, "prompt_tokens": 964, "output_tokens": 193}
{"ts": "2026-11-09T02:32:59+00:00", "input": "t-shirt under $25", "parsed": {"description": "t-shirt", "size": null, "max_price": 25.0}, "synonym_groups": [["tee", "tshirt"]], "n_results": 4, "selected_id": "lst_017", "ids_seen": {"selected": "lst_017", "suggest_outfit": "lst_017", "create_fit_card": "lst_017"}, "outcome": "completed", "output": "scored this black Mesh Long-Sleeve Top on depop for just $15 and I am so obsessed with the 90s grunge energy it brings. layering it over a white tank with some beat-up combat boots gives me the ultimate moody street style vibe without even trying.", "error": null, "duration_s": 3.399, "model_calls": 2, "prompt_tokens": 982, "output_tokens": 219}
{"ts": "2026-11-09T02:33:02+00:00", "input": "trainers size 8", "parsed": {"description": "trainers", "size": "8", "max_price": null}, "synonym_groups": [["kick", "sneaker", "trainer"]], "n_results": 1, "selected_id": "lst_019", "ids_seen": {"selected": "lst_019", "suggest_outfit": "lst_019", "create_fit_card": "lst_019"}, "outcome": "completed", "output": "Found my ultimate 2000s dream shoe on Poshmark and I am notokay!! These Platform Sneakers with the chunky soles and velcro straps were an absolute steal at $48, and that lived-in yellowing just makes the late 90s skater vibe even better. Can’t wait to style these with some baggy denim and a zip hoodie.", "error": null, "duration_s": 3.113, "model_calls": 2, "prompt_tokens": 981, "output_tokens": 235}
{"ts": "2026-11-09T02:33:05+00:00", "input": "trousers under $40", "parsed": {"description": "trousers", "size": null, "max_price": 40.0}, "synonym_groups": [["pant", "slack", "trouser"]], "n_results": 4, "selected_id": "lst_011", "ids_seen": {"selected": "lst_011", "suggest_outfit": "lst_011", "create_fit_card": "lst_011"}, "outcome": "completed", "output": "Found these Low-Rise Cargo Pants on Poshmark for just $27and I am officially living my 2000s off-duty model dream. The distressed hems and million pockets give off the ultimate grungy Y2K streetwear vibe. Can't wait to layer these with an oversized crewneck and combat boots!", "error": null, "duration_s": 2.776, "model_calls": 2, "prompt_tokens": 1018, "output_tokens": 251}
{"ts": "2026-11-09T02:33:06+00:00", "input": "purse under $30", "parsed": {"description": "purse", "size": null, "max_price": 30.0}, "synonym_groups": [["bag", "crossbody", "handbag", "purse", "tote"]], "n_results": 0, "selected_id": null, "ids_seen": {}, "outcome": "empty_search", "output": "Nothing matched 'purse'. To get results, raise your price limit above $30, or use fewer or more general keywords.", "error": null, "duration_s": 0.886, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0}
{"ts": "2026-11-09T02:33:09+00:00", "input": "jumper under $35", "parsed": {"description": "jumper", "size": null, "max_price": 35.0}, "synonym_groups": [["jumper", "knit", "knitwear", "pullover", "sweater"]], "n_results": 3, "selected_id": "lst_030", "ids_seen": {"selected": "lst_030", "suggest_outfit": "lst_030", "create_fit_card": "lst_030"}, "outcome": "completed", "output": "Obsessed with this Vintage Knit VestI just scored on thredUp for only $25! The brown and cream argyle pattern gives off the ultimate dark academia vibes, and it’s going to look so good layered over everything this fall.", "error": null, "duration_s": 3.101, "model_calls": 2, "prompt_tokens": 1008, "output_tokens":228}
{"ts": "2026-11-09T02:33:12+00:00", "input": "denim jacket under $50", "parsed": {"description": "denim jacket", "size": null, "max_price":50.0}, "synonym_groups": [["coat", "jacket"]], "n_results": 7, "selected_id": "lst_007", "ids_seen": {"selected": "lst_007", "suggest_outfit": "lst_007", "create_fit_card": "lst_007"}, "outcome": "completed", "output": "Found my dream vintage streetwear staple on Poshmark for only $42 and I am never taking it off! This light wash Wrangler Denim Jacket has the absolute best structured shoulders and is just begging tobe customized. Can't wait to style it with some baggy dark denim for the ultimate 90s double-denim moment.", "error": null, "duration_s": 3.412, "model_calls": 2, "prompt_tokens": 966, "output_tokens": 222}
{"ts": "2026-11-09T02:33:15+00:00", "input": "90s track jacket in size M", "parsed": {"description": "90s track jacket in", "size": "M", "max_price": null}, "synonym_groups": [["coat", "jacket"]], "n_results": 4, "selected_id": "lst_004", "ids_seen": {"selected": "lst_004", "suggest_outfit": "lst_004", "create_fit_card": "lst_004"}, "outcome": "completed", "output": "Still not over this navy and white Champion trackjacket I scored on Poshmark for just $45! It’s got that exact 90s athletic streetwear vibe I’ve been hunting for, and the material is so lightweight for layering. Already planning to throw it on over a ribbed tank and baggy jeans this weekend.", "error": null, "duration_s": 2.793, "model_calls": 2, "prompt_tokens": 973, "output_tokens": 222}
{"ts": "2026-11-09T02:33:55+00:00", "input": "hoodie under $30", "parsed": {"description": "hoodie", "size": null, "max_price": 30.0}, "synonym_groups": [["hooded", "hoodie"]], "n_results": 1, "selected_id": "lst_015", "ids_seen": {"selected": "lst_015", "suggest_outfit": "lst_015", "create_fit_card": "lst_015"}, "outcome": "completed", "output": "Managed to score this Vintage Graphic Hoodie on depop for just $26 and I am never taking it off. That faded charcoal wash and cozy pilled interior give it the absolute ultimate effortless grunge vibe. Can't wait to live in this all autumn long paired with baggy denim and beat-up boots.", "error": null, "duration_s": 39.521, "model_calls": 2, "prompt_tokens": 933, "output_tokens": 184}
{"ts": "2026-11-09T02:33:59+00:00", "input": "oversized flannel shirt", "parsed": {"description": "oversized flannel shirt", "size": null, "max_price": null}, "synonym_groups": [], "n_results": 7, "selected_id": "lst_003", "ids_seen": {"selected": "lst_003", "suggest_outfit": "lst_003", "create_fit_card": "lst_003"}, "outcome": "completed", "output": "Score! Just snagged this oversized red and black Woolrich flannelon thredUp for only $22 and the 90s grunge layering potential is off the charts. It's got that perfect lived-in streetwear vibe and honestly, I'm never taking it off.", "error": null, "duration_s": 4.223, "model_calls": 2, "prompt_tokens": 992, "output_tokens": 222}
{"ts": "2026-11-09T02:34:03+00:00", "input": "mesh top under $20", "parsed": {"description": "mesh top", "size": null, "max_price": 20.0}, "synonym_groups": [], "n_results": 8, "selected_id": "lst_017", "ids_seen": {"selected": "lst_017", "suggest_outfit": "lst_017", "create_fit_card": "lst_017"}, "outcome": "completed", "output": "Scored this absolute steal on depop for only $15 and I am so obsessed with it. This Mesh Long-Sleeve Top is giving major 90s grunge and Y2K energy, and it's going to look so good layered under all my oversized crewnecks. Can't wait to style this with some baggy denim and beat-up combat boots!", "error": null, "duration_s": 3.785, "model_calls": 2, "prompt_tokens": 1021, "output_tokens": 277}
{"ts": "2026-11-09T02:34:04+00:00", "input": "designer ballgown size XXS under $5", "parsed": {"description": "designer ballgown", "size": "XXS", "max_price": 5.0}, "synonym_groups": [], "n_results": 0, "selected_id": null, "ids_seen": {}, "outcome": "empty_search", "output": "Nothing matched 'designer ballgown'. To get results, raise your price limit above $5, or try a different size than XXS or leave size out, or use fewer or more general keywords.", "error": null, "duration_s": 1.639, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0}
```

## What It Costs

Measured with `python measure.py` (cache off, 10 completed runs): mean **7.54 s**, **984 prompt + 225 output tokens**, **2.0 model calls** per completed run. An empty-search run costs 0 model calls (~1–2 s, MCP subprocess start-up only).

Daily Cost: 
prompt: 100 x 984 = 98400 tokens 
Output: 100 x 225 = 22500 tokens 
Model call: 100 x 2 = 200 per day 

I'm on the free tier, so my actual cost is **$0**. At the paid rate for gemini-3.5-flash-lite ($0.30 per 1M input / $2.50 per 1M output, per Google's Gemini API pricing page, checked 2026-11-08), 100 runs/day is 98,400 prompt tokens (0.0984M × $0.30 = $0.030) plus 22,500 output tokens (0.0225M × $2.50 = $0.056), about **$0.086/day, ≈ $2.57/month**.


---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
