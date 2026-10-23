"""Ablation of dense: the same retriever with potion-retrieval-32M in place of bge-small-en-v1.5.

Only the embedding model changes. The chunks, the scoring (cosine similarity, a document scores
its best chunk) and every other setting come from p2.toml as they do for dense, so a difference
between the two runs is the model's.
"""

from __future__ import annotations

from p2 import embed
from p2.retrievers.dense import Dense

NEEDS_CLAUDE = False
BASE = "dense"


def build(corpus, cfg):
    dense = {**cfg.table("dense"), "model": embed.POTION}
    return Dense(corpus, cfg.replace(tables={**cfg.tables, "dense": dense}))
