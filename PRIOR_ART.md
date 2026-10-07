# Prior-art review and corrected scope

Recorded in version 1.1.0, 8 October 2026 (Asia/Tokyo). The review began on 7 October 2026 UTC. This is a bounded public-source investigation, not a priority certificate.

## Decisive published inputs

Both sources below were already present in OpenAI Math commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a` before this repository's first publication:

1. [The periodic spin-one Haldane gap](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-periodic-spin-one-Haldane-gap-September-24-2026/paper.pdf), dated 24 September 2026. Proposition 4.3 is the general two-purity uniform-gap criterion; Proposition 3.1 supplies the spatial-moment representation. Corollary 5.6 collects the finite periodic inputs used by the companion.
2. [A boundary-field gap for the spin-one Heisenberg chain](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-boundary-field-gap-for-the-spin-one-Heisenberg-chain-September-24-2026/paper.pdf), also dated 24 September 2026. Section 2 defines the periodic partition function with the same normalization and no endpoint fields. Proposition 3.4, at its index `j=2`, gives the two periodic defects at `(n,beta)=(120,49)` bounded by `0.052`.

Taking `n0=120`, `beta0=49`, `u0=13/250`, and `C=6` in the first paper's criterion therefore gives

`gamma_L > log(125/39)/49` for every even `L >= 120`, at `J = 1`.

This number was extracted during this review. We have not located it explicitly stated in the examined publications. Its premises and the gap-extraction method are already published, so it must be described as an explicit corollary of those results. The scalar checker does not make the underlying analytic argument independent.

## Correction to version 1.0

Version 1.0 proved `gamma_L > 0.0047` for every even `L >= 2304` by retaining asymmetric purity bounds for five more updates. That remains a valid conditional refinement of the periodic paper's stated `log(20)/784` bound on the same length range.

The initial comparison omitted the stronger periodic seeds in the boundary-field companion. The `0.0047` result should therefore not be described as surpassing the consequences of all the already published OpenAI material. Version 1.1 promotes the stronger corollary, adds its certificate and dependencies, and retains the older derivation and records. Earlier release notes are historical records.

## Other public material examined

- The original periodic paper's GitHub commit history and public pull-request search showed no later revision of that paper during the review.
- [yuxuanwang2009/haldane-gap-explainer](https://github.com/yuxuanwang2009/haldane-gap-explainer), in particular `analysis/bootstrap_table.py` and `data/bootstrap_dyadic.csv`, reproduces the original coupled updates and continues the common-envelope recurrence. Its displayed uniform bound remains the original `log(20)/784`. Continuing a recurrence is therefore not itself a new mathematical method.
- [The Haldane review material in tobiasosborne/ai-agents-seminar](https://github.com/tobiasosborne/ai-agents-seminar/tree/af6b2d5caa126407fa1f26b4dc6a9a50650867b3/CQT-talk-2026/haldane-designs/context), specifically `review-268-haldane.md` and `haldane-proof-ideas.md`, discusses the original proof and purity argument. The review identifies itself as an AI review; we do not treat it as independent human expert validation. No matching certified uniform `0.0047` improvement was found there.
- Public web and arXiv searches, GitHub code and repository searches, and public discussions were checked for the paper title, the constants `0.0047` and `0.004704`, the purity bootstrap, and stronger uniform gap bounds. No independent report of the same certified refinement was identified. Searches for the newly extracted `0.02377` constant likewise did not identify a matching explicit report.

Search indexing, very recent posts, unavailable discussions, and private or unpublished work limit this review. Failure to locate a result is not evidence of priority. Older numerical estimates of a physical gap near `0.4105` are a different type of claim from a certified uniform lower bound for all lengths in a specified range.

## Version 1.2: parity extension and search scope

Version 1.2 adds an argument for the same bound at **every integer length at least 120**, including odd lengths at least 121. The signed trace formula for all integer lengths is already in periodic Proposition 3.1. Positive dominant eigenvalues, dyadic purity estimates, and adjacent-temperature ratios are already in companion Proposition 3.4. The added proof controls the residual absolute moments at both temperatures using the same even reference length and derives a full-interval polynomial bound before extracting the physical gap.

This proof does not apply the even-only gap proposition outside its stated domain. It also does not make the upstream premises independent. The earlier search described above focused on the constants and the even-length refinement; it was not an exhaustive search for an existing version of this signed-moment extension. The record therefore makes no claim of priority for the parity argument, nor of a fresh literature search or external expert validation in version 1.2.

## Version 1.3: length-adaptive refinement

The new conditional result is `gamma_L > 0.06` for every integer `L >= 34`. Its finite inputs, original coupled purity update, signed transfer representation, and positive dominant eigenvalues are already in the two pinned OpenAI manuscripts. The added work is the length-dependent interpolation, use of the unequal defects, the asymmetric tail invariant, and the resulting exact certificate.

On 8 October 2026 (Asia/Tokyo), a small additional public web search used the combinations `Haldane 0.06 OpenAI gap`, `Haldane 0.0606`, and `Haldane L 34 OpenAI`. No matching report of this certified constant and length range was identified. The public [OpenAI overview](https://github.com/openai/math/blob/main/overview.tex) continues to describe the periodic result for even rings and the companion's odd open chains with endpoint fields. This bounded search is not an exhaustive review and does not establish priority. Exploratory recurrence rates are not new certified theorems. The mathematical statement remains conditional on the original analytic and finite-input premises.

## Attribution for the continuing investigation

OpenAI is credited for both upstream propositions and their proofs. GPT-6 Astra Max performed this investigation, identified the cross-paper corollary, checked the normalization and hypotheses, implemented the scalar certificate, and revised the note. The human user requested the prior-art review and authorized the repository update. No new external mathematical review is claimed.

The agent subsequently derived the signed-moment extension and its exact scalar certificate after the human asked about odd lengths. The human requested that newly verified findings be incorporated into this repository.
