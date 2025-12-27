#!/usr/bin/env python3
"""
Purpose: Demonstrate duplicate / near-duplicate scanning for Context Triage
Skill: skills/operator/context-triage/SKILL.md
Note: Illustrative script. Not production code. Authority: human-supervised execution.

What this script does
- Loads a context bundle (JSON) from a file path or stdin
- Normalizes text lightly (whitespace + lowercasing)
- Finds likely duplicates using:
  1) Exact hash match (post-normalization)
  2) Near-duplicate match using shingled Jaccard similarity
- Produces a grouped report suitable for operator review

What this script does not do
- It does not decide which artifact should be retained
- It does not infer scope or authority
- It does not perform semantic embedding similarity (no deps)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# ----------------------------
# Data model and loading
# ----------------------------

@dataclass
class Artifact:
    artifact_id: str
    kind: str
    authority: str
    priority: int
    title: str
    content: str


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def load_json_from_path_or_stdin(path: Optional[str]) -> Dict[str, Any]:
    if path and path != "-":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


def normalize_bundle(bundle: Dict[str, Any]) -> List[Artifact]:
    artifacts_raw = bundle.get("artifacts", [])
    if not isinstance(artifacts_raw, list):
        raise ValueError("bundle.artifacts must be a list")

    artifacts: List[Artifact] = []
    for i, a in enumerate(artifacts_raw):
        if not isinstance(a, dict):
            raise ValueError(f"artifact at index {i} must be an object")

        artifact_id = str(a.get("id") or a.get("artifact_id") or f"artifact_{i}")
        kind = str(a.get("kind") or "other").strip()
        authority = str(a.get("authority") or "other").strip()
        priority = _safe_int(a.get("priority"), default=0)
        title = str(a.get("title") or artifact_id).strip()
        content = str(a.get("content") or "").strip()

        artifacts.append(
            Artifact(
                artifact_id=artifact_id,
                kind=kind,
                authority=authority,
                priority=priority,
                title=title,
                content=content,
            )
        )
    return artifacts


# ----------------------------
# Normalization and fingerprinting
# ----------------------------

_WS_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """
    Light, stable normalization.
    - lowercases
    - collapses whitespace
    - strips edges
    """
    if not text:
        return ""
    t = text.lower()
    t = _WS_RE.sub(" ", t).strip()
    return t


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ----------------------------
# Near-duplicate detection via shingled Jaccard
# ----------------------------

def tokens(text: str) -> List[str]:
    # Keep alnum word tokens to reduce sensitivity to punctuation.
    return re.findall(r"[a-z0-9]+", text)


def shingles(word_tokens: List[str], k: int) -> List[Tuple[str, ...]]:
    if k <= 0:
        raise ValueError("k must be > 0")
    if len(word_tokens) < k:
        return []
    return [tuple(word_tokens[i : i + k]) for i in range(len(word_tokens) - k + 1)]


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = a.intersection(b)
    union = a.union(b)
    return len(inter) / float(len(union))


def near_duplicate_score(text_a: str, text_b: str, shingle_k: int) -> float:
    ta = tokens(text_a)
    tb = tokens(text_b)
    # If either text is too short for the shingle length, treat as non-duplicate.
    if len(ta) < shingle_k or len(tb) < shingle_k:
        return 0.0
    sa = set(shingles(ta, shingle_k))
    sb = set(shingles(tb, shingle_k))
    return jaccard(sa, sb)


# ----------------------------
# Grouping logic
# ----------------------------

@dataclass
class PairMatch:
    a_id: str
    b_id: str
    score: float


def exact_duplicates(artifacts: List[Artifact]) -> Dict[str, List[Artifact]]:
    """
    Groups artifacts that are identical after normalization.
    Keyed by hash.
    """
    groups: Dict[str, List[Artifact]] = {}
    for art in artifacts:
        nt = normalize_text(art.content)
        if not nt:
            continue
        h = sha256_hex(nt)
        groups.setdefault(h, []).append(art)
    # Keep only groups with 2+
    return {h: g for h, g in groups.items() if len(g) >= 2}


def near_duplicates(
    artifacts: List[Artifact],
    threshold: float,
    shingle_k: int,
    max_pairs: int,
) -> List[PairMatch]:
    """
    Returns a list of high-scoring pairs (potential near-duplicates).

    This is O(n^2) and intended for small demo bundles.
    For larger sets, add blocking by title hash or MinHash/LSH.
    """
    matches: List[PairMatch] = []
    n = len(artifacts)

    for i in range(n):
        ai = artifacts[i]
        ti = normalize_text(ai.content)
        if not ti:
            continue

        for j in range(i + 1, n):
            aj = artifacts[j]
            tj = normalize_text(aj.content)
            if not tj:
                continue

            score = near_duplicate_score(ti, tj, shingle_k=shingle_k)
            if score >= threshold:
                matches.append(PairMatch(ai.artifact_id, aj.artifact_id, score))

            if len(matches) >= max_pairs:
                return sorted(matches, key=lambda m: m.score, reverse=True)

    return sorted(matches, key=lambda m: m.score, reverse=True)


def print_groups(title: str, groups: List[List[str]]) -> None:
    print(title)
    print("-" * len(title))
    if not groups:
        print("(none)")
        print("")
        return
    for idx, g in enumerate(groups, start=1):
        print(f"Group {idx}: " + ", ".join(g))
    print("")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Context Triage demo: scan for duplicate and near-duplicate artifacts."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="-",
        help="Path to context bundle JSON. Use '-' to read from stdin.",
    )
    parser.add_argument(
        "--near-threshold",
        type=float,
        default=0.85,
        help="Jaccard similarity threshold for near-duplicate detection (0..1).",
    )
    parser.add_argument(
        "--shingle-k",
        type=int,
        default=5,
        help="Shingle size (word n-gram length) for near-duplicate detection.",
    )
    parser.add_argument(
        "--max-pairs",
        type=int,
        default=200,
        help="Maximum near-duplicate pairs to report (caps runtime).",
    )
    args = parser.parse_args()

    if not (0.0 <= args.near_threshold <= 1.0):
        print("ERROR: --near-threshold must be between 0 and 1", file=sys.stderr)
        return 2
    if args.shingle_k <= 0:
        print("ERROR: --shingle-k must be > 0", file=sys.stderr)
        return 2
    if args.max_pairs <= 0:
        print("ERROR: --max-pairs must be > 0", file=sys.stderr)
        return 2

    try:
        bundle = load_json_from_path_or_stdin(args.input)
        artifacts = normalize_bundle(bundle)
    except Exception as e:
        print(f"ERROR: failed to load/parse context bundle: {e}", file=sys.stderr)
        return 2

    if len(artifacts) < 2:
        print("Need at least 2 artifacts to scan.", file=sys.stderr)
        return 1

    # Exact duplicates
    exact = exact_duplicates(artifacts)
    exact_groups: List[List[str]] = []
    for _, group in exact.items():
        exact_groups.append([a.artifact_id for a in group])

    # Near duplicates (pair list)
    near = near_duplicates(
        artifacts=artifacts,
        threshold=args.near_threshold,
        shingle_k=args.shingle_k,
        max_pairs=args.max_pairs,
    )

    # Build near-duplicate adjacency groups (simple union-find)
    parent: Dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx

    for m in near:
        union(m.a_id, m.b_id)

    # Collect components
    comps: Dict[str, List[str]] = {}
    for a in artifacts:
        root = find(a.artifact_id)
        comps.setdefault(root, []).append(a.artifact_id)

    near_groups = [sorted(v) for v in comps.values() if len(v) >= 2]
    near_groups = sorted(near_groups, key=lambda g: (-len(g), g))

    # Print report
    print("")
    print("Duplicate Scan Report")
    print("---------------------")
    print(f"Artifacts scanned:     {len(artifacts)}")
    print(f"Exact dup groups:      {len(exact_groups)}")
    print(f"Near-dup groups:       {len(near_groups)}")
    print(f"Near threshold:        {args.near_threshold}")
    print(f"Shingle k:             {args.shingle_k}")
    print("")

    print_groups("Exact duplicates (post-normalization)", [sorted(g) for g in exact_groups])
    print_groups("Near-duplicate groups (Jaccard shingles)", near_groups)

    # Show top pairs for operator inspection
    print("Top near-duplicate pairs")
    print("------------------------")
    if not near:
        print("(none)")
        print("")
    else:
        for m in near[: min(25, len(near))]:
            print(f"{m.a_id}  <->  {m.b_id}   score={m.score:.3f}")
        print("")

    print("Operator reminder")
    print("-----------------")
    print("This scan suggests candidates for redundancy removal.")
    print("It does not decide which artifact to keep.")
    print("Prefer higher authority or most recent versions.")
    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
