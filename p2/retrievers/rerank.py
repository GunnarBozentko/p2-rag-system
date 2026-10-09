"""Listwise reranking: Claude reorders a first-stage system's top 20.

Ported from the 13 lab's rerank_one() (pipeline.py): the candidates go to Claude as numbered
passages (the first PASSAGE_CHARS characters of each), the schema forces the reply into
{"order": [n numbers]}, a reply that is not each of 1 to n once keeps the first-stage order, and
the documents below the candidates keep their first-stage order underneath.
Unlike the lab's schema, each number is limited to 1..n, so a number that names no passage
cannot come back.

One claude -p call per query, through p2.claude.call, which caches replies in .cache/claude/ and
records the tokens in the run's trace (commit the trace with the run file).

The settings come from p2.toml:

    [rerank]
    first_stage = "hybrid"
    candidates = 20
    passage_chars = 600

A score in the run file is 1 / final rank, so it falls as the rank grows; only the order matters.
"""

from __future__ import annotations

import sys

from p2 import claude, retrievers

NEEDS_CLAUDE = True

PROMPT = """Below are {n} passages from a collection of documents, numbered 1 to {n}, and a search query.
Order the passages from the most useful for answering the query to the least useful.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


def schema(n):
    return {
        "type": "object",
        "properties": {
            "order": {
                "type": "array",
                "items": {"type": "integer", "minimum": 1, "maximum": n},
                "minItems": n,
                "maxItems": n,
            }
        },
        "required": ["order"],
    }


class Rerank:
    def __init__(self, corpus, cfg):
        settings = cfg.table("rerank")
        self.first_name = settings.get("first_stage", "hybrid")
        self.candidates = settings.get("candidates", 20)
        self.passage_chars = settings.get("passage_chars", 600)
        self.first = retrievers.build(self.first_name, corpus, cfg)
        self.cfg = cfg
        self.model = cfg.model
        self.doc_text = {docid: doc.text for docid, doc in corpus.docs.items()}
        self.chunk_text = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)

    def reorder(self, query, ids, text_of):
        """The candidate ids in Claude's order, or in the first-stage order if the reply is unusable."""
        n = len(ids)
        if n < 2:
            return ids
        passages = "\n\n".join(f"[{i}] {text_of[x][: self.passage_chars]}" for i, x in enumerate(ids, 1))
        prompt = PROMPT.format(n=n, query=query, passages=passages)
        reply = claude.call(prompt, schema(n), model=self.model, cache_dir=claude.cache_folder(self.cfg))
        if reply.error:
            print(f"    rerank: the call failed ({reply.error}); keeping the {self.first_name} order", file=sys.stderr)
            return ids
        order = (reply.output or {}).get("order")
        if not isinstance(order, list) or sorted(order) != list(range(1, n + 1)):
            print(f"    rerank: the reply was not each of 1 to {n} once ({order}); keeping the {self.first_name} order", file=sys.stderr)
            return ids
        return [ids[i - 1] for i in order]

    def _search(self, text, k, first_search, text_of):
        ranked = [x for x, _ in first_search(text, max(k, self.candidates))]
        top, rest = ranked[: self.candidates], ranked[self.candidates :]
        final = self.reorder(text, top, text_of) + rest
        return [(x, 1 / rank) for rank, x in enumerate(final[:k], 1)]

    def search(self, text, k):
        return self._search(text, k, self.first.search, self.doc_text)

    def search_chunks(self, text, k):
        return self._search(text, k, self.first.search_chunks, self.chunk_text)


def build(corpus, cfg):
    return Rerank(corpus, cfg)
