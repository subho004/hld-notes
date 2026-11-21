#!/usr/bin/env python3
"""Generate the root index.html (a self-contained static site).

Usage (from anywhere):  python3 site-src/build_site.py

Reads every chapter_NN_*/notes.md plus Readme.md and embeds them as JSON inside
template.html, so the resulting index.html works from file:// or GitHub Pages.
ddia_pages/ (gitignored OCR source pages) is never read or listed.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = Path(__file__).resolve().parent / "template.html"
OUT = ROOT / "index.html"

P1 = "Part I · Foundations of Data Systems"
P2 = "Part II · Distributed Data"
P3 = "Part III · Derived Data"
P4 = "Reference"

# (folder, number, title, part, one-line summary)
CHAPTERS = [
    ("chapter_01_reliable-scalable-maintainable", 1, "Reliable, Scalable, and Maintainable Applications", P1,
     "What good looks like: tolerate faults, cope with load, and stay easy to operate and change."),
    ("chapter_02_data-models-query-languages", 2, "Data Models and Query Languages", P1,
     "Relational, document and graph models, and the query languages that go with them."),
    ("chapter_03_storage-and-retrieval", 3, "Storage and Retrieval", P1,
     "How databases lay data out on disk: LSM-trees, B-trees, and column stores for analytics."),
    ("chapter_04_encoding-and-evolution", 4, "Encoding and Evolution", P1,
     "Turning data into bytes, and keeping old and new code and data compatible."),
    ("chapter_05_replication", 5, "Replication", P2,
     "Leaders, followers, multi-leader and leaderless designs, and the problems of replication lag."),
    ("chapter_06_partitioning", 6, "Partitioning", P2,
     "Splitting data across nodes: key-range and hash partitioning, indexes, and rebalancing."),
    ("chapter_07_transactions", 7, "Transactions", P2,
     "ACID, isolation levels, and what each prevents, up to serializability."),
    ("chapter_08_trouble-with-distributed-systems", 8, "The Trouble with Distributed Systems", P2,
     "Partial failures, unreliable networks and clocks, and how little a node can know for sure."),
    ("chapter_09_consistency-and-consensus", 9, "Consistency and Consensus", P2,
     "Linearizability, ordering and causality, atomic commit, and fault-tolerant consensus."),
    ("chapter_10_batch-processing", 10, "Batch Processing", P3,
     "Unix tools, MapReduce, joins, and dataflow engines for bulk derived data."),
    ("chapter_11_stream-processing", 11, "Stream Processing", P3,
     "Event logs, change data capture, stream joins, and fault tolerance for unbounded data."),
    ("chapter_12_future-of-data-systems", 12, "The Future of Data Systems", P3,
     "Integrating derived data, unbundled databases, correctness end to end, and ethics."),
    ("chapter_13_glossary", 13, "Glossary", P4,
     "A themed cheat sheet of the book's key terms."),
]

SKIP_DIRS = {".git", "ddia_pages", "node_modules", "__pycache__", ".claude", ".agents", ".idea", ".vscode"}
SKIP_FILES = {".DS_Store", "skills-lock.json"}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def build_chapters():
    out = []
    for folder, num, title, part, tagline in CHAPTERS:
        p = ROOT / folder / "notes.md"
        if not p.exists():
            raise SystemExit(f"missing {p}")
        out.append({"id": folder, "num": num, "title": title, "part": part,
                    "tagline": tagline, "notes": read(p)})
    return out


def build_tree(chapters):
    routes = {f"{c['id']}/notes.md": f"#/{c['id']}" for c in chapters}
    routes["Readme.md"] = "#/extras"

    def walk(d: Path):
        out = []
        for e in sorted(d.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
            if e.name in SKIP_DIRS or e.name in SKIP_FILES or e.name.endswith(".pyc"):
                continue
            rel = e.relative_to(ROOT).as_posix()
            if e.is_dir():
                out.append({"n": e.name, "t": "d", "k": walk(e)})
            else:
                node = {"n": e.name, "t": "f", "s": e.stat().st_size}
                if rel in routes:
                    node["r"] = routes[rel]
                else:
                    node["h"] = rel
                out.append(node)
        return out

    return walk(ROOT)


def main():
    chapters = build_chapters()
    data = {
        "chapters": chapters,
        "readme": read(ROOT / "Readme.md") if (ROOT / "Readme.md").exists() else "",
        "tree": build_tree(chapters),
    }
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/").replace("<!--", "<\\!--")
    html = read(TEMPLATE)
    if "__DATA__" not in html:
        raise SystemExit("template.html is missing the __DATA__ placeholder")
    OUT.write_text(html.replace("__DATA__", payload), encoding="utf-8")
    (ROOT / ".nojekyll").touch()
    print(f"wrote {OUT} ({OUT.stat().st_size/1024:.0f} KB): {len(chapters)} chapters")


if __name__ == "__main__":
    main()
