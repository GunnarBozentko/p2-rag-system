"""Dense retrieval: embed every chunk once, embed the query, and rank chunks by cosine similarity.

Ported from the 12 lab's dense_rankings (retrieve.py): there it was one matrix product of query
vectors against article vectors; here it is one query vector against every chunk vector, and
ChunkScorer lifts the chunk scores to documents (a document scores its best chunk).

The model comes from p2.toml:

    [dense]
    model = "BAAI/bge-small-en-v1.5"          # or "minishlab/potion-retrieval-32M"

Without that table it is bge-small-en-v1.5. The chunk vectors are cached per model in
.cache/vectors/, so switching models back and forth only encodes the corpus once for each.
"""

from __future__ import annotations

import numpy as np

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        self.model = cfg.table("dense").get("model", embed.BGE)
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)

    def score_chunks(self, text: str) -> np.ndarray:
        if not len(self.chunks):
            return np.zeros(0, dtype=np.float32)
        query = self.embedder.encode([text])[0]  # unit length, like the chunk vectors
        return self.vectors @ query  # dot product of unit vectors = cosine similarity


def build(corpus, cfg):
    return Dense(corpus, cfg)
