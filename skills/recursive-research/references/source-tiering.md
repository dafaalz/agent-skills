# Source tiering

Assign one tier to every source before you read it. Read this file at Step 3 and at Step 4.4 of the main workflow.

## Tier table

| Tier | Qualifies | Weight |
|---|---|---|
| T1 | Peer reviewed papers, academic press books, official standards (W3C, IETF, ISO, WHO, FDA), primary archives, official datasets, statistics offices | 5 |
| T2 | Official repositories of active projects, blogs from citable authors, recorded conference talks with a paper, Wikipedia with T1 or T2 citations, reports with published methodology | 3 |
| T3 | Blogs citing T1 or T2, upvoted forum answers with citations, recorded interviews with named experts, industry posts with clear authorship | 2 |
| Rejected | No named author, marketing without data, SEO aggregators, tutorials with no citations, social posts without verifiable context, unsupervised AI content | 0 |

## Rejection rule

Reject on any of these conditions, and record the condition in `sources-rejected.md`.

1. The author is absent or unnamed.
2. The claim carries no data, no method, and no citation.
3. The page repeats another source without adding evidence.
4. The content comes from a model with no documented human review.

## Ledger fields

Write one row per source in the matching ledger.

| Field | Value |
|---|---|
| Title | Exact page or paper title |
| URL | Full address, or the local path for a file |
| Author | Named author or issuing body |
| Date | Publication date, or `n.d.` when absent |
| Tier | T1, T2, T3, or Rejected |
| Reason | The sentence from the tier table that grants the tier |

## Seed sources by domain

Present the list for the matching domain, and let the user add or reject entries before Step 4.

| Domain | Seed sources |
|---|---|
| Science and papers | arXiv, Semantic Scholar, Google Scholar, Connected Papers, OpenReview |
| Medicine and biology | PubMed, Cochrane Library, WHO, ClinicalTrials.gov |
| Humanities and social science | JSTOR, SSRN, Project MUSE |
| Code and technology | GitHub, Context7, IETF RFCs, W3C specifications |
| Data and statistics | World Bank, OECD Data, Our World in Data, Pew Research, Eurostat |
| Art and culture | Europeana, Google Arts and Culture, Internet Archive, Project Gutenberg |
| General | Wikipedia as a starting index, then follow its references to T1 or T2, plus Wikidata |

## Local files

Read local paths with `Read`, `Grep`, and `Glob`. Prioritize `.md`, `.pdf`, `.txt`, `.doc`, `.docx`, `.html`, and `.epub`. Tier a local file by the same table, and treat an unsigned dump with no provenance as Rejected.
