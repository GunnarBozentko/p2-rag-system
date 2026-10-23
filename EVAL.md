# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.


For the dense model I used the BAAI/bge-small-en-v1.5 model with a cosine scoring similarity and chunked documents in 300 words with 50 words of overlap. I got a MRR of .562, and the changes I made from lab 12 is that we broke down the model to query against every chunk rather than just one whole article.

For the hybrid model I used the bm25 and dense models combined with a reciprocal rank fusion of k=60 and chunked documents in 300 words with 50 words of overlap. I got a MRR of .471, and the changes I made from lab 13 is that a document that gets a score of 0 from the system gets no vote from that system.

For the rerank model the first stage is hybrid and then Claude sonnet reordered the hybrid's top 20 list. The rerank model has a MRR score of .75 and the only change it made from lab 13 is that each number in the response must be numbered from 1 to 20 instead of just a list of integers.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.617 | 0.471 | 0.457 |
| rerank | 0.725 | 0.750 | 0.718 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.571 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.154 | 0.792 |
| hybrid | nDCG@10 | 0.435 | 0.203 | 0.779 |
| rerank | Recall@10 | 0.714 | 0.500 | 1.000 |
| rerank | MRR@10 | 0.714 | 0.571 | 1.000 |
| rerank | nDCG@10 | 0.697 | 0.516 | 0.980 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.008 | [-0.225, +0.208] | 0.317 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.036 | [-0.178, +0.084] | 0.193 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.062 | [-0.218, +0.082] | 0.218 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.058 | [-0.117, +0.242] | 0.261 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.091 | [-0.305, +0.110] | 0.300 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.023 | [-0.191, +0.137] | 0.240 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.100 | [-0.125, +0.325] | 0.331 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.243 | [+0.010, +0.476] | 0.339 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.200 | [-0.021, +0.416] | 0.317 | not distinguishable |
| rerank minus dense | Recall@10 | +0.167 | [-0.025, +0.350] | 0.271 | not distinguishable |
| rerank minus dense | MRR@10 | +0.188 | [-0.017, +0.392] | 0.294 | not distinguishable |
| rerank minus dense | nDCG@10 | +0.239 | [+0.052, +0.419] | 0.267 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.108 | [+0.025, +0.209] | 0.141 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.279 | [+0.128, +0.441] | 0.229 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.262 | [+0.150, +0.383] | 0.169 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

Looking at our table, we can see we have statistically significant intervals that do not include 0. If our interval does not include 0, this means we are 95% confident that the mean difference when comparing these two models/metrics is significantly distinguishable. Looking at our table we see that rerank minus BM25 for the MRR@10 metric is significant, as well as rerank minus dense for the nDCG@10 metric. We then see that Rerank minus hybrid is significant for all three metrics of Recall@10, MRR@10, and nDCG@10. All dense minus bm25, hybrid minus bm25, and hybrid minus dense include 0 in their intervals. Rerank minus BM25 included zero for recall@10 and nDCG@10. For rerank minus dense 0 was in the interval for recall@10 and MRR@10.

The minimum detectable difference at 20 queries is the true difference needed between two methods on a designated metric to correctly identify there is a distinguishable difference between the two 80% of the time. Our MDD ranges from .141 to .415. What this means when there is a gap smaller than the minimum detectable difference at 20 queries is that the differences between the models are invisible to the gold set, whether there is a true difference or not.

The claim from lecture 12 that BM25 and Dense each miss in a predictable kind of query is consistent with my observations. We saw that BM25 matches exact words, and it got a 0 for MRR@10 for the paraphrase section. Dense got a .333 MRR score for the identifier questions, which makes sense as it searches for meanings. This is not exactly proven though as we do not have an interval to go off for this. One claim that was left open was that BM25 is the baseline to beat, and dense models usually beat it on average. We can see that in our intervals for dense - BM25, all three metric intervals included 0. This means we are not able to definitively say there is a distinguishable difference in the performance of these two models. The claim from lecture 13 that can be supported is that a reranker can't rescue a document that isn't among its candidates. This is supported by my data as when the relevant section was in the hybrid's initial top 20, the reranker was able to effectively reorder the relevant section to first. If the relevant section was not in the top 20, it was missed completely.


---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 11 of 11 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.


The system that answered was rerank. The reason why I chose rerank over BM25, Dense, and Hybrid, was because it was the only model that had a distinguishable difference than the other models, (0 was not in the confidence intervals for the mean difference).

I did not change anything in prompts/answer.txt. There is nothing to compare since there is one prompt, and it got 8 of 8 verified and 4 of 4 declined.



I chose to look into question a04: How often must an underground metal or nonmetal mine hold evacuation drills? I believe the claims in the answer are backed up. Claim 1 states that underground mine evacuation drills must be held at least once every six months, and this is backed up in the text as there is a quote that directly mentions this claim. Claim 2 states that drills must be held for each shift at some time other than a shift change and involve all persons underground, which is also backed up in the text as there is a quote that directly mentions this claim. Section 57 also holds information for underground metal and nonmetal mines, so this checks out.

I chose to look into question a05: How many hours of training must a new underground miner receive before being assigned to work duties? I believe the claims in the answer are backed up. Claim 1 states that each new underground miner must receive no less than 40 hours of training before being assigned to work duties, and this is backed up in the text as there is a quote that directly mentions this claim. Claim 2 states that approximately 8 of those hours are given at the minesite, and this is also mentioned in the text as there is a quote that directly mentions this claim. Section 48 is about trianing rules so this makes sense.

I chose to look into question a07: How high must berms or guardrails be on the banks of roadways at metal and nonmetal mines? I believe the claims in the answer are backed up. Claim 1 states that Berms or guardrails must be at least mid-axle height of the largest self-propelled mobile equipment that usually travels the roadway, and this is backed up in the text as there is a quote that directly mentions this claim. Claim 2 states that The same height requirement appears in 30 CFR 57.9300, and after checking this is also true. Section 57 also holds information for underground metal and nonmetal mines, so this checks out.


---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

My corpus is 1005 arXiv abstracts from the stat.AP category under CC0, CC BY, or CC BY-SA, which are an allowed source in the brief. It describes different applied statistics studies, with 431 of them from 2024 and 574 of them from 2025. There are 196,504 words, so the corpus averages about 196 words per document, and all the texts combined are about 1.4 MB. This is about 275,000 tokens. Each document has its own license, with 928 of them CC BY 4.0, 54 CC BY-SA, and 23 CC0. All were checked on 2026-10-15 by uv run p2 license --online, and all license checks came back okay. The documents I was least sure about were 2411.13356, 2505.00510 and 2511.02682, and this is because they were very short (about 50 words). I decided to keep them to see how the RAG system can perform on shorter document sizes as well.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.


I have 10 queries written by hand and 45 written by claude. This allows for enough queries to be able to tell if there is a distinguishable difference between dense and hybrid. There are 19 identifier, 19 mixed, and 17 paraphrase queries. This was to give an even amount of differing query types so all models can play to their strengths and to see how our models generalize to differing questions. 

The candidates were chosen by combining the bm25's top 5, dense's top 5, hybrid's top 5, plus the source the query was written from. Each candidate was read in full before being labeled relevant or not.

I will decide if a document is relevant if the abstract answers the question rather than if the abstract is about the same topic. I will use a binary scale where 1 represents the abstract is relevant, and documents not listed are not relevant. A paper that uses the method the query names but doesn't answer the question will not be labeled relevant. A paper that answers only part of a two-part question will be labeled relevant.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.818 | 0.738 | 0.754 |
| dense | 0.955 | 0.907 | 0.917 |
| hybrid | 0.973 | 0.824 | 0.858 |
| rerank | 0.973 | 0.961 | 0.959 |

55 judged queries; nDCG uses binary labels; a random ranking of the 1,005 documents would get recall@10 near 0.010.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | mixed (n=19) | paraphrase (n=17) | identifier (n=19) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.412 | 1.000 |
| bm25 | MRR@10 | 0.904 | 0.261 | 1.000 |
| bm25 | nDCG@10 | 0.919 | 0.294 | 1.000 |
| dense | Recall@10 | 1.000 | 0.853 | 1.000 |
| dense | MRR@10 | 0.961 | 0.794 | 0.954 |
| dense | nDCG@10 | 0.970 | 0.807 | 0.964 |
| hybrid | Recall@10 | 1.000 | 0.912 | 1.000 |
| hybrid | MRR@10 | 0.947 | 0.518 | 0.974 |
| hybrid | nDCG@10 | 0.957 | 0.609 | 0.981 |
| rerank | Recall@10 | 1.000 | 0.912 | 1.000 |
| rerank | MRR@10 | 1.000 | 0.912 | 0.965 |
| rerank | nDCG@10 | 1.000 | 0.897 | 0.974 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=10) | claude (n=45) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 1.000 | 0.778 | +0.222 | [+0.111, +0.356] | hand higher |
| bm25 | MRR@10 | 0.850 | 0.713 | +0.137 | [-0.108, +0.345] | not distinguishable |
| bm25 | nDCG@10 | 0.886 | 0.725 | +0.161 | [-0.038, +0.338] | not distinguishable |
| dense | Recall@10 | 0.900 | 0.967 | -0.067 | [-0.289, +0.078] | not distinguishable |
| dense | MRR@10 | 0.738 | 0.944 | -0.207 | [-0.481, +0.033] | not distinguishable |
| dense | nDCG@10 | 0.775 | 0.949 | -0.175 | [-0.416, +0.036] | not distinguishable |
| hybrid | Recall@10 | 1.000 | 0.967 | +0.033 | [+0.000, +0.089] | not distinguishable |
| hybrid | MRR@10 | 0.867 | 0.814 | +0.053 | [-0.154, +0.230] | not distinguishable |
| hybrid | nDCG@10 | 0.899 | 0.848 | +0.050 | [-0.110, +0.189] | not distinguishable |
| rerank | Recall@10 | 1.000 | 0.967 | +0.033 | [+0.000, +0.089] | not distinguishable |
| rerank | MRR@10 | 0.933 | 0.967 | -0.033 | [-0.189, +0.078] | not distinguishable |
| rerank | nDCG@10 | 0.950 | 0.961 | -0.011 | [-0.128, +0.078] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | -0.189 | +0.100 | -0.289 | [-0.522, -0.111] | bm25 gains more on hand queries |
| MRR@10 | -0.231 | +0.113 | -0.344 | [-0.663, -0.033] | bm25 gains more on hand queries |
| nDCG@10 | -0.224 | +0.111 | -0.335 | [-0.624, -0.066] | bm25 gains more on hand queries |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.63 (10 queries), claude 0.50 (45 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 10 hand and 45 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | +0.136 | [+0.036, +0.245] | 0.147 | dense higher |
| dense minus bm25 | MRR@10 | +0.169 | [+0.063, +0.281] | 0.161 | dense higher |
| dense minus bm25 | nDCG@10 | +0.163 | [+0.064, +0.270] | 0.152 | dense higher |
| hybrid minus bm25 | Recall@10 | +0.155 | [+0.073, +0.255] | 0.135 | hybrid higher |
| hybrid minus bm25 | MRR@10 | +0.085 | [+0.016, +0.160] | 0.105 | hybrid higher |
| hybrid minus bm25 | nDCG@10 | +0.104 | [+0.041, +0.172] | 0.096 | hybrid higher |
| hybrid minus dense | Recall@10 | +0.018 | [-0.045, +0.091] | 0.096 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.083 | [-0.160, -0.013] | 0.107 | dense higher |
| hybrid minus dense | nDCG@10 | -0.060 | [-0.127, +0.001] | 0.093 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.155 | [+0.073, +0.255] | 0.135 | rerank higher |
| rerank minus bm25 | MRR@10 | +0.222 | [+0.121, +0.333] | 0.157 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.205 | [+0.113, +0.307] | 0.143 | rerank higher |
| rerank minus dense | Recall@10 | +0.018 | [-0.045, +0.091] | 0.096 | not distinguishable |
| rerank minus dense | MRR@10 | +0.054 | [-0.018, +0.130] | 0.108 | not distinguishable |
| rerank minus dense | nDCG@10 | +0.042 | [-0.026, +0.113] | 0.102 | not distinguishable |
| rerank minus hybrid | Recall@10 | +0.000 | [+0.000, +0.000] | - | identical on every query |
| rerank minus hybrid | MRR@10 | +0.137 | [+0.065, +0.218] | 0.110 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.101 | [+0.049, +0.161] | 0.081 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time. Two systems that score the same on every query have no interval to speak of, so their MDD is shown as -.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

For our intervals, we see that dense, hybrid, and rerank beat bm25 on all 3 metrics as none of the intervals include 0. For example, dense minus BM25 had the interval of [+0.036, +0.245] for recall@10. We see that rerank beat hybrid on MRR@10 and nDCG@10, but for recall@10 they had identical scoring on every query. Rerank minus dense was not distinguishable at all as all the intervals included 0. Hybrid minus dense had only one interval that did not include 0, and this was for MRR@10 and the interval is [-0.160, -0.013], so dense outperformed hybrid on this metric.

The hand and claude written queries tell mostly similar stories. One story that does not agree is that bm25's recall@10 differs from hand to claude as the interval does not include 0, [+0.111, +0.356]. It is higher for the hand queries. Also, bm25's lead over dense is larger on the hand queries than on the claude ones. We see this as all metrics for claude minus hand the intervals do not include 0.

My prediction that hybrid would beat dense did not hold. There is more on this in section 9 in my 598 Rider section covering this. Rerank had the highest scores but it was not distinguishable from dense, so we can not say for certain that rerank outperformed all other models. This is because both models performed very well and were close to the ceiling. Bm25 came last as expected, but my judgement that it would not perform well due to the statistical jargon was not correct, as it did very well on the identifier queries. It lacked greatly on the paraphrase queries.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
_No ablation runs yet: `uv run p2 run --corpus own --system NAME --ablation` writes one to runs/own/ablation/, then `uv run p2 score` fills this table._
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
_No ablation runs yet: `uv run p2 run --corpus own --system NAME --ablation` writes one to runs/own/ablation/, then `uv run p2 score` fills this table._
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

TODO: write the ablation: the one change, the hypothesis, the result and the claim.

The one change I made is that I swapped the dense retriever's embedding model from bge-small-en-v1.5 to potion-retrieval-32M. My hypothesis is that I expect dense MRR@10 to decrease compared to the original dense MRR@10 score for my personal corpus. This is because dense potion-retrieval-32M performed worse than dense bge-small-en-v1.5 on the shared corpus when I ran it previously to test it myself in stage 1.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|

TODO: add one row for each failure you analyzed, and write two or three sentences on the pattern you see across them.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

TODO: write the cross-corpus comparison.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 187,426 | 3,940 | 97.4 | 15,619 | 328 | 8.1 |
| traces/answers-rerank.r1.jsonl | rerank | 12 | 24 | 0 | 194,475 | 4,162 | 119.1 | 16,206 | 347 | 9.9 |
| traces/answers-rerank.r2.jsonl | rerank | 12 | 24 | 0 | 208,079 | 4,366 | 105.2 | 17,340 | 364 | 8.8 |
| traces/answers-rerank.r3.jsonl | rerank | 12 | 24 | 0 | 212,328 | 4,034 | 157.9 | 17,694 | 336 | 13.2 |
| traces/own-own-rerank.jsonl | rerank | 55 | 55 | 2 | 568,314 | 5,005 | 180.5 | 10,333 | 91 | 3.3 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 20 | 200,932 | 1,820 | 68.0 | 10,047 | 91 | 3.4 |
| traces/shared-practice-rerank.r1.jsonl | rerank | 20 | 20 | 0 | 230,951 | 2,171 | 96.9 | 11,548 | 109 | 4.8 |
| traces/shared-practice-rerank.r2.jsonl | rerank | 20 | 20 | 0 | 204,625 | 1,930 | 98.3 | 10,231 | 96 | 4.9 |
| traces/shared-practice-rerank.r3.jsonl | rerank | 20 | 20 | 0 | 225,004 | 2,150 | 110.4 | 11,250 | 108 | 5.5 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 2 | 478,196 | 4,626 | 144.4 | 11,955 | 116 | 3.6 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.243 | [-0.476, -0.010] | 10,047 | 3.4 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.188 | [-0.392, +0.017] | 10,047 | 3.4 | not distinguishable |
| shared practice: hybrid minus rerank | 20 | -0.279 | [-0.441, -0.128] | 10,047 | 3.4 | rerank higher |
| own: bm25 minus rerank | 55 | -0.222 | [-0.333, -0.121] | 10,333 | 3.3 | rerank higher |
| own: dense minus rerank | 55 | -0.054 | [-0.130, +0.018] | 10,333 | 3.3 | not distinguishable |
| own: hybrid minus rerank | 55 | -0.137 | [-0.218, -0.065] | 10,333 | 3.3 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 55 | 0.06 | 1.0 |
| traces/retrieval/own-own-dense.jsonl | dense | 55 | 0.43 | 7.8 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 55 | 0.52 | 9.4 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.05 | 2.4 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.28 | 14.1 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.29 | 14.3 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.10 | 2.5 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.33 | 8.3 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.56 | 14.1 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
Repeated runs of rerank on shared/practice:

| Run | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| rerank.r1 | 0.700 | 0.750 | 0.711 |
| rerank.r2 | 0.700 | 0.750 | 0.711 |
| rerank.r3 | 0.700 | 0.750 | 0.705 |
| range (max minus min) | 0.000 | 0.000 | 0.006 |

| Comparison | Metric | Mean difference | 95% interval | Reading |
| --- | --- | ---: | ---: | --- |
| rerank.r1 minus hybrid | Recall@10 | +0.083 | [+0.000, +0.175] | not distinguishable |
| rerank.r2 minus hybrid | Recall@10 | +0.083 | [+0.000, +0.175] | not distinguishable |
| rerank.r3 minus hybrid | Recall@10 | +0.083 | [+0.000, +0.175] | not distinguishable |
| rerank.r1 minus hybrid | MRR@10 | +0.279 | [+0.128, +0.441] | rerank.r1 higher |
| rerank.r2 minus hybrid | MRR@10 | +0.279 | [+0.128, +0.441] | rerank.r2 higher |
| rerank.r3 minus hybrid | MRR@10 | +0.279 | [+0.128, +0.441] | rerank.r3 higher |
| rerank.r1 minus hybrid | nDCG@10 | +0.255 | [+0.139, +0.378] | rerank.r1 higher |
| rerank.r2 minus hybrid | nDCG@10 | +0.255 | [+0.139, +0.378] | rerank.r2 higher |
| rerank.r3 minus hybrid | nDCG@10 | +0.248 | [+0.135, +0.372] | rerank.r3 higher |

Repeated answers shared/rerank:

| File | Verified (in) | 95% interval | Declined (out) | 95% interval |
| --- | ---: | ---: | ---: | ---: |
| rerank.r1 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r2 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r3 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| range (max minus min) | 0.000 |  | 0.000 |  |

Each repeat answers the same questions, so the repeats are not independent trials and their counts are not pooled into one interval.
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
