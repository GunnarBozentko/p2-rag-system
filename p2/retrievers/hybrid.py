"""Hybrid retrieval: reciprocal rank fusion (RRF) of two systems' full rankings.

Ported from the 13 lab's rrf() (pipeline.py): each document scores the sum of 1 / (k + rank) over
the rankings, with k = 60 and ranks starting at 1. It uses ranks only, so it does not matter that
bm25 scores run to 20 and cosine similarities stay below 1.

The systems and k come from p2.toml:

    [hybrid]
    systems = ["bm25", "dense"]
    k = 60

Both rankings are full (every document, or every chunk for search_chunks), so a document that is
11th in both lists can still reach the fused top 10.
A document that a system scores exactly 0 (bm25 when it shares no word with the query) is left
out of that system's ranking: its place among the zeros is document id order, not evidence, so it
gets no vote from that system.
"""

from __future__ import annotations

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False


def rrf(rankings, k=60):
    """Fuse rankings (lists of ids, best first) into [(id, score), ...], best first."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1 / (k + rank)
    return order(scores.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        settings = cfg.table("hybrid")
        self.names = list(settings.get("systems", ["bm25", "dense"]))
        self.rrf_k = settings.get("k", 60)
        self.systems = [retrievers.build(name, corpus, cfg) for name in self.names]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))
        models = [getattr(s, "model", None) for s in self.systems]
        self.model = ", ".join(m for m in models if m) or None

    def search(self, text, k):
        rankings = [[docid for docid, score in s.search(text, self.n_docs) if score != 0] for s in self.systems]
        return rrf(rankings, self.rrf_k)[:k]

    def search_chunks(self, text, k):
        rankings = [[cid for cid, score in s.search_chunks(text, self.n_chunks) if score != 0] for s in self.systems]
        return rrf(rankings, self.rrf_k)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
