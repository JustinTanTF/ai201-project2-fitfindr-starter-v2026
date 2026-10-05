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

<PASTE THE OUTPUT HERE AFTER YOU RUN IT>
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

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

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

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
