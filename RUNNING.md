# Running FitFindr

## Capstone run path (Path B — local with logs)

**Environment:** Python 3.11–3.13 (developed on 3.12.0), dependencies pinned in
`requirements.txt`. No local model files; the only external service is the
Gemini API, so you need a `GEMINI_API_KEY`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env          # paste your GEMINI_API_KEY into .env
python measure.py               # runs 12 queries, writes logs/runs.jsonl
```

Single query: `python app.py ask 'trainers size 8'`. Every run (finished, empty
search, or crashed) appends one JSON line to `logs/runs.jsonl`.
Read it back with `python runlog.py` or `python runlog.py --tail 10`.

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
      out: You should definitely grab this baby tee! At just $18, it's an easy win that will look amazing paired with you…
[5] create_fit_card
      in:  dict with keys: item
      out: Found the absolute dreamiest Y2K Baby Tee — Butterfly Print scrolling on depop this morning and I am so obsess…
[6] parse_query
      in:  t-shirt under $25
      out: dict with keys: description, size, max_price
[7] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 4 items: Mesh Long-Sleeve Top — Black, Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey … +1 more
[8] select_item
      in:  4 candidates
      out: Mesh Long-Sleeve Top — Black ($15.0, depop)
[9] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: 90s Grunge Streetwear** Layer the mesh top under your **white ribbed tank top** (w_003) for contra…
[10] create_fit_card
      in:  dict with keys: item
      out: Scored this sheer black Mesh Long-Sleeve Top on depop for literally $15 and I am so obsessed with the 90s grun…
[11] parse_query
      in:  trainers size 8
      out: dict with keys: description, size, max_price
[12] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 1 items: Platform Sneakers — White Chunky Sole
[13] select_item
      in:  1 candidates
      out: Platform Sneakers — White Chunky Sole ($48.0, poshmark)
[14] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: Off-Duty Model Y2K** Pair the platform sneakers with your *Baggy straight-leg jeans* (w_001) and t…
[15] create_fit_card
      in:  dict with keys: item
      out: Found the ultimate off-duty model sneakers on Poshmark for just $48 and I am never taking them off! The chunky…
[16] parse_query
      in:  trousers under $40
      out: dict with keys: description, size, max_price
[17] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 4 items: Low-Rise Cargo Pants — Khaki, Straight Leg Khaki Trousers — Olive, Corduroy Wide-Leg Pants — Rust … +1more
[18] select_item
      in:  4 candidates
      out: Low-Rise Cargo Pants — Khaki ($27.0, poshmark)
[19] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: The Ultimate Y2K Streetwear Look** Pair the low-rise cargo pants with your fitted **white ribbed t…
[20] create_fit_card
      in:  dict with keys: item
      out: Obsessed with these Low-Rise Cargo Pants I just scored on Poshmark for only $27! They’ve got that perfect slou…
[21] parse_query
      in:  purse under $30
      out: dict with keys: description, size, max_price
[22] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[23] branch: empty search
      out: Nothing matched 'purse'. To get results, raise your price limit above $30, or use fewer or more general keywor…
      →    stopping before suggest_outfit
[24] parse_query
      in:  jumper under $35
      out: dict with keys: description, size, max_price
[25] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Vintage Knit Vest — Argyle Brown/Cream, Vintage Graphic Hoodie — Faded Black, Knit Cardigan — Chunky Brown
[26] select_item
      in:  3 candidates
      out: Vintage Knit Vest — Argyle Brown/Cream ($25.0, thredUp)
[27] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: Modern Dark Academia** Layer the vintage argyle vest over your **white ribbed tank top (w_003)** a…
[28] create_fit_card
      in:  dict with keys: item
      out: Just scored this Vintage Knit Vest on thredUp for only $25 and I am so obsessed with the dark academia vibes! …
[29] parse_query
      in:  denim jacket under $50
      out: dict with keys: description, size, max_price
[30] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 7 items: Denim Jacket — Light Wash, Cropped, High-Waisted Denim Shorts — Cutoff, Denim Vest — Medium Wash, Studded … +4 more
[31] select_item
      in:  7 candidates
      out: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
[32] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: The Canadian Tuxedo (Two-Tone Denim)** Pair the light wash Wrangler jacket (`lst_007`) with your b…
[33] create_fit_card
      in:  dict with keys: item
      out: Obsessed is an understatement for how I feel about this vintage Wrangler Denim Jacket I just scored on Poshmar…
[34] parse_query
      in:  90s track jacket in size M
      out: dict with keys: description, size, max_price
[35] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 4 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +1 more
[36] select_item
      in:  4 candidates
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
[37] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: Off-Duty Streetwear** Pair the Champion track jacket with your **white ribbed tank top** (w_003) a…
  [rate limit] service pushed back. Waiting 4s (attempt 1 of 5). This is the limiter doing its job, not a bug.
[38] create_fit_card
      in:  dict with keys: item
      out: Finally scored this vintage Champion 90s Track Jacket on Poshmark for only $45 and I am never taking it off. I…
[39] parse_query
      in:  hoodie under $30
      out: dict with keys: description, size, max_price
[40] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 1 items: Vintage Graphic Hoodie — Faded Black
[41] select_item
      in:  1 candidates
      out: Vintage Graphic Hoodie — Faded Black ($26.0, depop)
  [rate limit] 15 requests used this minute. Waiting 35s. This is normal.
[42] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: Effortless 90s Grunge**   Pair the vintage faded black hoodie (`lst_015`) with your baggy dark-was…
[43] create_fit_card
      in:  dict with keys: item
      out: Finally found the ultimate 90s grunge staple on depop and I'm obsessed with how perfectly broken-in it is. Thi…
[44] parse_query
      in:  oversized flannel shirt
      out: dict with keys: description, size, max_price
[45] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 7 items: Oversized Flannel Shirt — Plaid Red/Black, Tie-Dye Long Sleeve — Pastel, Vintage Polo Shirt — Forest Green … +4 more
[46] select_item
      in:  7 candidates
      out: Oversized Flannel Shirt — Plaid Red/Black ($22.0, thredUp)
[47] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: 90s Grunge Casual**   Pair the Woolrich flannel over the **white ribbed tank top (w_003)** and **b…
[48] create_fit_card
      in:  dict with keys: item
      out: scored this vintage Woolrich Oversized Flannel Shirt on thredUp for just $22 and I'm honestly obsessed. The re…
[49] parse_query
      in:  mesh top under $20
      out: dict with keys: description, size, max_price
[50] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 8 items: Mesh Long-Sleeve Top — Black, Henley Long Sleeve — Washed Burgundy, Tie-Dye Long Sleeve — Pastel … +5 more
[51] select_item
      in:  8 candidates
      out: Mesh Long-Sleeve Top — Black ($15.0, depop)
[52] suggest_outfit
      in:  dict with keys: item_id, item, wardrobe_items
      out: **Outfit 1: 90s Grunge Streetwear** Layer the mesh top under your white ribbed tank top (w_003) for a textured…
[53] create_fit_card
      in:  dict with keys: item
      out: scored this Mesh Long-Sleeve Top on depop for literally just $15 and I am so obsessed with it. the dark goth a…
[54] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[55] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[56] branch: empty search
      out: Nothing matched 'designer ballgown'. To get results, raise your price limit above $5, or try a different size …
      →    stopping before suggest_outfit

12 runs logged, 10 completed
mean duration (completed): 7.19s
mean prompt tokens:        984
mean output tokens:        227
mean model calls:          2.1
21 model calls this session, 9844 prompt + 2266 output tokens

---

Everything about how the starter works and how to use it.

---

## Before your first class

Setup happens **before class**. The [environment setup page](../pages/ide_setup)
has the per-operating-system commands and the exact versions.

**Same API key you set up in unit 1.** Nothing new to sign up for. There is one
new package — the MCP SDK, for unit 4 — and it installs with everything else.

From inside this repo after you've forked and cloned it:

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your key into .env
python test.py
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env         # then paste your key into .env
python test.py
```

**You're ready when `python test.py` passes.**

If it doesn't and you've made one honest attempt at the error, post the
**whole** output in the help channel.

> Activate the virtual environment every time you open a new terminal. You
> should see `(.venv)` at the start of your prompt.

---

## Your first five minutes

Start with the data. Your tools will only be as good as your understanding of
what they're reading, and ten minutes here saves an hour of confused debugging.

```bash
python app.py fields                    # what a listing and a wardrobe item hold
python app.py listings --full -n 6      # read six listings all the way through
python app.py examples                  # queries worth trying
python app.py ask 'vintage graphic tee under $30'
```

> **Quote your queries with single quotes**, on every operating system. In
> PowerShell, `"vintage graphic tee under $30"` in double quotes silently
> becomes `vintage graphic tee under ` — PowerShell reads `$30` as a variable
> and substitutes nothing. You get results with no price ceiling and no error
> saying so. Single quotes are literal in PowerShell, bash and zsh alike.

That last one runs the loop. All three tools are stubs, so it will tell you the
loop isn't built yet. **That's the correct starting position** — it runs, and it
does nothing.

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment. Run it whenever something feels off |
| `python app.py fields` | The fields a listing and a wardrobe item have — **Milestone 1** |
| `python app.py listings` | Browse the data. `--full` for whole records, `-n` for how many |
| `python app.py examples` | Queries worth trying, including one that matches nothing |
| `python app.py ask '...'` | Run the agent on one query — **single quotes** |
| `python app.py ask` | Keep asking until you press Enter on an empty line |
| `python agent.py` | Runs both example paths — one that matches, one that can't |
| `python mcp_server.py` | Starts your MCP server — **unit 4** |
| `python mcp_client.py` | Asks the server what it offers — **unit 4** |
| `python run_eval.py --label before` | Runs every scenario five times and writes the run log — **unit 4** |
| `python serve.py` | Serves the agent over HTTP instead of exiting — **unit 9** |

Useful flags on `ask`:

| Flag | What it does |
|---|---|
| `--trace` | Print the loop step by step, once you've added the trace calls |
| `--empty-wardrobe` | Run as a user with nothing saved — one of unit 4's failure modes |

---

## Which command goes with which milestone

### Unit 3 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Read the data, run the starter | `app.py fields`, `app.py listings --full`, `app.py ask` |
| 2 | Spec your three tools | README, **Tool Inventory** |
| 3 | Write your acceptance criteria | `criteria.md` |
| 4 | Build the three tools | `tools.py`, tested one at a time from a terminal |
| 5 | Wire the loop and the state | `agent.py::run_agent` |
| 6 | Write it up | README |

### Unit 4 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Move one tool onto MCP | `mcp_server.py`, then `mcp_client.call_tool` in `run_agent` |
| 2 | Break it on purpose, then trace it | `trace.py`, `app.py ask --trace` |
| 3 | Run your test | `scenarios.py`, then `run_eval.py --label before` |
| 4 | Call each criterion, diagnose the misses | README |
| 5 | Fix one thing and re-run | `run_eval.py --label after` |
| 6 | Say what's still broken | README |

---

## Running it somewhere else — **unit 9**

Everything above exits when the command finishes. A host has nothing to keep
running, so before you can deploy this you need something that stays up.
`serve.py` is that: the same `run_agent()`, behind two HTTP routes.

On your machine:

```bash
python serve.py
curl -X POST http://localhost:5000/ask \
  -H 'Content-Type: application/json' \
  -d '{"query": "vintage graphic tee under $30"}'
```

On a host, the start command is:

```bash
gunicorn serve:app
```

| Thing | What it means |
|---|---|
| `PORT` | The host tells your app which port to listen on by setting this. Both `serve.py` and `gunicorn` read it, and `serve.py` falls back to `5000` on your machine. Don't hard-code a port |
| `POST /ask` | `{"query": "...", "wardrobe": {...}}` — wardrobe optional. Returns the session dict, `error` and all |
| `GET /health` | Says `ok` if the app is awake |
| It answers one request at a time | On purpose. A second request waits for the first to finish, and prints `[serve] another request is still running` while it waits. An MCP tool call starts a whole second Python process, and the free tier's 512 MB has no room for two of those at once — and `generate.py`'s rate-limit counting assumes one caller. The reasoning is written out in `serve.py` |
| `gunicorn serve:app`, exactly | Not `-k gevent`, not `-k eventlet`, not wrapped for uvicorn. `mcp_client.call_tool` uses `asyncio.run()`, which won't start inside a running event loop, so an async worker breaks **every** MCP call — and only once you've deployed it |
| The first request is slow | The free tier puts your app to sleep after about fifteen minutes of nothing. The next request wakes it up and waits for it — around a minute. Not a bug, and worth knowing before you demo it |

`serve.py` ships with **no logging and no timing in it**, on purpose. You add
that yourself in the follow-along, before you deploy — instrumenting first is
the point of the session.

---

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting worth changing — **TEMPERATURE and the cache are at the top** |
| `tools.py` | Your three tools. **Stubs — you build these** |
| `agent.py` | The planning loop and the session. **Stub — you build this** |
| `generate.py` | The only thing that calls out to a service. Handles pacing and quota |
| `trace.py` | The trace helper, and the loop's stop condition |
| `app.py` | The command line |
| `serve.py` | The same agent over HTTP, for deploying — **unit 9** |
| `mcp_server.py` | Your MCP server — **unit 4, you register the tool** |
| `mcp_client.py` | Calling an MCP tool from your agent. Given to you |
| `scenarios.py` | What your test runs. **You fill this in** |
| `run_eval.py` | Runs the scenarios repeatedly and writes the run log |
| `criteria.md` | Your five acceptance criteria. **You fill this in** |
| `data/` | 40 listings and the wardrobe schema |
| `utils/data_loader.py` | Loading the data. Use this rather than reading the files yourself |
| `results/` | Run logs. **Commit these** — they're your evidence |

---

## The two settings people go looking for

Both are at the top of `config.py`, and the brief points at them by name.

If your fit cards come out **word-for-word identical** every time, it is one of:

- **`CACHE_ENABLED`** — while you build, identical prompts reuse the answer
  already received. That's deliberate; it makes debugging free. `run_eval.py`
  turns it off automatically.
- **`TEMPERATURE`** — at `0.0` the model gives you the same words every time.
  It ships at `0.9`.

---

## About rate limits

**This is the heaviest pair in the course for call volume.** Two of your three
tools call the model, so one agent run is several requests, and a few runs back
to back while debugging can cross the per-minute limit.

`generate.py` handles it:

- **It paces itself** and says when it's waiting. **A pause is the starter
  doing its job, not a bug.**
- **It reuses answers** to prompts already sent, while you build.
- **It stops** if a session makes an unreasonable number of calls, rather than
  draining your day's allowance. For an agent, that usually means a loop isn't
  ending — look for that before raising the number.
- **It counts your calls** and prints the total when you exit.

`config.MAX_ITERATIONS` is the loop's own stop condition. Your loop this unit
is short enough that you may never hit it. Keep it — a missing stop condition
is the most common architectural failure in production agents.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `The planning loop isn't built yet` | Correct, at the start. That's the TODO in `agent.py` |
| `No GEMINI_API_KEY found` | No `.env`, or the key wasn't pasted in. On Windows check it didn't save as `.env.txt` |
| A message saying the model couldn't be reached | Usually a bad key. This is also **exactly what unit 4 Milestone 2 asks you to trigger on purpose** |
| `[rate limit] ... Waiting 34s` | Working as intended. Leave it |
| `[serve] another request is still running` | Also working as intended. `serve.py` answers one request at a time; yours is queued behind one that's mid-run |
| `QuotaGuard: This session has made 300 requests` | A loop isn't ending. Find it before raising the budget |
| `The loop ran 11 times, past MAX_ITERATIONS` | Same thing, caught earlier |
| `The server doesn't offer a tool called '...'` | Nothing registered in `mcp_server.py` yet, or the name doesn't match |
| MCP returns a string where you expected a list | You're not going through `mcp_client.call_tool`, which unwraps it |
| Fit cards identical every run | `CACHE_ENABLED` or `TEMPERATURE`. See above |
| `--trace` prints nothing | You haven't added `trace.step()` calls yet — unit 4, Milestone 2 |
| `IncompleteFieldDefinitionWarning: Field 'lifespan'` | Harmless noise from the MCP library's dependencies. Not your code, not an error. Ignore it |
| A price ceiling you typed is being ignored | You used double quotes in PowerShell. `$30` vanished. Use single quotes |
| `UnicodeEncodeError: 'charmap' codec can't encode` | Shouldn't happen — `config.py` sets the console to UTF-8. If you see it, you're running a file that doesn't import `config` |

Still stuck after one honest attempt? Post in the help channel with the full
error, what you ran, and what you expected.

---

## A note on committing

At least four new commits in unit 3, at least four more in unit 4. Your commit
history is what shows your criteria existed before your results did.

**Do not delete and recreate this repository.** You submit the same URL both
units.

`results/` is deliberately **not** in `.gitignore`.
