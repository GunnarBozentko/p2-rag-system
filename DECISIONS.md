# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.


I picked the corpus I did for stage 2 as it talks about statistical studies on multiple different areas. I chose this as I was a statistics major in my undergrad, and I found reading about new studies very interesting. I expected hybrid to beat dense as it combines dense for paraphrase queries and bm25 for identifier queries. I expect overall rerank to perform the best as it performed the best on the original corpus. I also expected bm25 to perform the worst as keywords may lead to multiple different documents for the query with different meanings as there is a lot of statistical jargon that is repeated. (I wrote this after I ran uv run p2 score, but this is what I would have expected. Also, in the brief's pacing plan, it says to complete decision log last over the weekend, so I did not see this question until after running the scores on my corpus.)

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.


One fork in the road I had was judging my candidate pool for the gold set. At first, I tried the top 10 from bm25 and dense plus a keyword search which gave me 1276 candidates. I took out the keyword search and still got 953 candidates, which I decided was still too much. I then decided to use the top 5 from bm25, dense, and hybrid, which resulted in 549 candidates. The decision came down to time vs bias. With the first method, I would have to review over 1000 different abstracts, whereas the second method introduced a little bias as ranks 6 through 10 are not fully judged, so nDCG@10 come out a bit lower for each system. I added the hybrid pool as well as without it it would have left out 81 documents that neither bm25 nor dense had in their top 5. Leaving these documents out would have tilted my PREREG hypothesis that hybrid beats dense against hybrid because hybrid's picks may have been left out as not relevant. I decided the extra time saved was worth the little bias when judging nDCG@10.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

One time Claude wrote something and I did not take it was for the Claude generated queries for my own corpus for queries o11 to o55. Claude drafted from a random sample of 75 abstracts, and the first draft of queries used the abstracts' own words. This meant for the paraphrase queries, the content-word overlap was between .3 to .45 where in the shared corpus the content-word overlap was around .11. Content-word overlap matters as paraphrase queries that have a large word overlap will be easier for bm25. This would have overstated bm25 on the class type for the queries that are meant to test it. I noticed this by checking each draft's overlap with the p2.score.content_words, and this is also the same check I used to help dictate which class my hand-written queries went into. What I did to change this is that I had the paraphrase queries remade by Claude to have a lower content-word score. The final content-word overlap for my paraphrase queries are now between .09 and .3.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

One number I do not fully trust is rerank's nDCG@10 with a score of 0.959 on my own corpus. The reasoning for this is because ranks 6 through 10 were not fully judged, which is the bias I described in question 2 as well. Consequently, nDCG@10 may be off in either direction due to only the top 5 retrieved abstracts for bm25, dense, and hybrid models being judged for each query. Rerank was not in the pool, so even some of its top 10 are not scored as relevant as they are unread. What would have to be true for me to trust this number would be if I looked at the top 10 retrieved documents for each query from each of these methods to decide if they are relevant or not. I had Claude count to see how many of each system's top 10 documents that were never judged, and it resulted in about 35 to 48% of each system's top 10 never read. Adding these abstracts in could have changed the nDCG@10 score.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

One thing that is wrong in my system currently is that the reranker still has the 600 character passage limit in passage_chars in p2.toml. The median abstract body is 1324 characters, so rerank is missing about half of the abstracts for each reading. For example for o03, 2405.18020 is the relevant document, but the words harvest and heat (which are in the query) do not appear until past the 1000th character. What I would do next would be to expand the character limit to at least 1500 characters. I would find out whether it matters by running a new test on rerank with the character limit increased, and then getting 95% intervals for the new rerank minus the old rerank. 
