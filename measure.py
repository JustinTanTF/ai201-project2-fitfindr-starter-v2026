#!/usr/bin/env python3
"""
Run a fixed batch of queries through the agent, cache OFF, so runlog.py gets
real records and we get a measured per-run cost.

    python measure.py              12 queries (default)
    python measure.py --n 20

Prints mean duration, mean tokens and total model calls for completed runs.
"""

import argparse

import config

config.CACHE_ENABLED = False  # real answers only

import generate
import runlog
from agent import run_agent
from utils.data_loader import get_example_wardrobe

QUERIES = [
    "vintage graphic tee under $30",
    "t-shirt under $25",
    "trainers size 8",
    "trousers under $40",
    "purse under $30",
    "jumper under $35",
    "denim jacket under $50",
    "90s track jacket in size M",
    "hoodie under $30",
    "oversized flannel shirt",
    "mesh top under $20",
    "designer ballgown size XXS under $5",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=len(QUERIES))
    args = ap.parse_args()

    start_count = len(runlog.read())
    for q in (QUERIES * 5)[: args.n]:
        try:
            run_agent(q, get_example_wardrobe())
        except Exception as exc:  # noqa: BLE001 — already logged by run_agent
            print(f"CRASHED on {q!r}: {exc}")

    new = runlog.read()[start_count:]
    done = [r for r in new if r["outcome"] == "completed"]
    print(f"\n{len(new)} runs logged, {len(done)} completed")
    if done:
        n = len(done)
        print(f"mean duration (completed): {sum(r['duration_s'] for r in done)/n:.2f}s")
        print(f"mean prompt tokens:        {sum(r['prompt_tokens'] for r in done)/n:.0f}")
        print(f"mean output tokens:        {sum(r['output_tokens'] for r in done)/n:.0f}")
        print(f"mean model calls:          {sum(r['model_calls'] for r in done)/n:.1f}")
    print(generate.usage())


if __name__ == "__main__":
    main()
