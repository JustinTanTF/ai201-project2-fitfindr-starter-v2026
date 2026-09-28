# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:** Search is a plain keyword-overlap match with no synonyms,
so some phrasings miss ("t-shirt" will not find a listing tagged "tee"). Two
tools also call the model, which can hit rate limits or return an empty
response. 4 of 5 leaves room for those failures, while 5 of 5 would punish the
search for not understanding language it was never built to understand.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:** This path involves no model. It depends only on
`search_listings` returning `[]` and the loop checking for an empty list, both
of which are deterministic. If it fails once, that is a bug in the branch, not
noise, so anything below 5 of 5 would be hiding a real defect.

---

## 3. The item found by search is the item the next tool receives

Across 5 matching queries, in 5 of 5 runs the `id` of `session["selected_item"]`
is identical to the `id` of the item passed into `suggest_outfit` and into
`create_fit_card`, checked by logging each tool's arguments and comparing them.

**Why this target:** The item moves through the session as a plain dict with no
model in between, so there is no legitimate reason for it to change. State
failures look like tool failures ("the outfit doesn't match the item"), which
makes them easy to misdiagnose, so I want a check that compares ids directly
and a target with no slack.

---

## 4. The fit card is a usable caption

Across 5 different items, at least 4 of 5 fit cards are 2 to 4 sentences, name
the item's price and platform, and no two of the 5 cards start with the same
sentence.

**Why this target:** The card comes from a model, so the wording changes from
run to run and one card can drift (skip the price, run to five sentences).
Requiring 5 of 5 would fail on a single stray output and tell me little about
the tool. 4 of 5 catches a prompt that is systematically wrong. The
no-shared-opening rule is checked across all five because repeated openings
are the sign of a template rather than a caption.

---

## 5. Search respects the price ceiling

For 5 queries that each include a price ceiling, 0 returned listings cost more
than that ceiling (all 5 queries, no exceptions).

**Why this target:** The price filter is a plain numeric comparison in
`search_listings`, with no model involved, so a listing over the ceiling can
only mean the filter is broken. Returning an item the user said they cannot
afford is the most visible way this tool could fail, so the target is zero
violations.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->