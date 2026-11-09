"""
Structured run log: one JSON object per line in logs/runs.jsonl.

Every call to agent.run_agent writes exactly one record, whether it finished,
stopped early on an empty search, or crashed. Read it back with:

    python runlog.py            summary of the log
    python runlog.py --tail 10  last 10 records
"""

import datetime as dt
import json
import sys
from pathlib import Path

import config

LOG_DIR = config.ROOT / "logs"
LOG_FILE = LOG_DIR / "runs.jsonl"


def write(record: dict) -> None:
    """Append one record. Logging must never break a run, so failures are swallowed."""
    try:
        LOG_DIR.mkdir(exist_ok=True)
        record = {"ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), **record}
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as exc:  # noqa: BLE001
        print(f"[runlog] could not write log: {exc}", file=sys.stderr)


def read(path: Path = LOG_FILE) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


if __name__ == "__main__":
    records = read()
    if "--tail" in sys.argv:
        n = int(sys.argv[sys.argv.index("--tail") + 1])
        for r in records[-n:]:
            print(json.dumps(r, ensure_ascii=False))
        sys.exit(0)
    by_outcome: dict[str, int] = {}
    for r in records:
        by_outcome[r["outcome"]] = by_outcome.get(r["outcome"], 0) + 1
    print(f"{len(records)} records in {LOG_FILE}")
    for outcome, count in sorted(by_outcome.items()):
        print(f"  {outcome}: {count}")
