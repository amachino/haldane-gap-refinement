# An exact-arithmetic refinement of the periodic spin-one Haldane-gap bound

**Version 1.0.0 · 7 October 2026 · Autonomously researched and written by GPT-6 Astra Max · Unreviewed technical note**

[Read the paper](paper/note.pdf) · [LaTeX source](paper/note.tex) · [日本語](README.ja.md)

Conditional on the spatial-moment representation and initial purity estimates in OpenAI's *The periodic spin-one Haldane gap*, this repository certifies

$$
\gamma_L > \frac{47}{10000}=0.0047
\quad\text{for every even }L\ge2304,\qquad J=1.
$$

The thermodynamic statement is $\liminf_{L\to\infty,\ L\text{ even}}\gamma_L\ge0.0047$.
This is about a **23.0% increase in the stated lower bound** $\log(20)/784$, on the same range of lengths. It is an elementary quantitative extension of an existing proof, not an independent solution of the Haldane conjecture. The constant is a lower bound, not an estimate of the physical gap. We make no priority or optimality claim.

## What is added

Five further, upward-rounded updates of the original coupled purity recurrence retain information discarded by rounding both defects to 0.01. Five interval estimates and one infinite-tail estimate then cover every even length at least 2304. The paper gives the argument; a short certificate verifies all its numerical inequalities using exact fractions.

The two upstream mathematical inputs are Proposition 3.1 (the spatial-moment representation) and Proposition 5.5 (the initial purity bounds). The note rederives the bootstrap steps from Lemma 4.2 and Proposition 4.3. Acceptance of the underlying analytic proof remains necessary.

## Reproduce the new bound

No third-party package is required. Use Python 3.11 or later with assertions enabled:

```sh
python3 verify_gap_improvement.py
```

Expected result: `PASS: all exact inequalities for gamma_L > 0.0047, even L >= 2304.` The JSON certificate is written to `independent_results/short_certificate.json`. The script refuses optimized Python execution; do not use `-O`. Decimal logarithms and floating-point margins are informational and do not determine any assertion.

The rational certificate contains the following bounds. Every decimal in this table is exact.

| j | n | inverse temperature | p | q |
|---:|---:|---:|---:|---:|
| 0 | 2304 | 784 | 0.0084513 | 0.0054986 |
| 1 | 4608 | 1568 | 2.59e-4 | 6.45e-5 |
| 2 | 9216 | 3136 | 1.70e-7 | 8.35e-9 |
| 3 | 18432 | 6272 | 6.07e-14 | 1.40e-16 |
| 4 | 36864 | 12544 | 7.39e-27 | 3.93e-32 |
| 5 | 73728 | 25088 | 1.10e-52 | 3.09e-63 |

## What was checked

| Evidence | Scope | Interpretation |
|---|---|---|
| New exact certificate | Five updates, five intervals, one uniform tail | Proves the improved constant conditional on the stated upstream inputs |
| Fresh upstream verifier run | 27 thermal cases, two variational contractions, auxiliary checks | All finite checks passed; this reuses the upstream implementation |
| Separate integer implementation | Full 72- and 120-site contraction integers and a direct four-site check | Exact agreement with the upstream values, using code reconstructed from the manuscript |
| Separate floating-point implementation | 16 full-spectrum thermal cases on four to eight sites with twists | Diagnostic agreement within the manuscript's tolerances; not rigorous interval arithmetic |

The complete finite run finished on 7 October 2026 and took about 22 minutes. Its record is [`reproduced/verification.json`](reproduced/verification.json). It reports both `success: true` and `full_recomputation: true`. Mathematical certificates and supporting logs are included. This audit is not a Lean or other kernel-checked formal proof of the analytic argument.

## Additional reproduction

The recorded numerical environment was Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0. Install the optional numerical dependencies in a virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-audit.txt
OPENBLAS_NUM_THREADS=1 python3 independent_audit.py scalars
OPENBLAS_NUM_THREADS=1 python3 independent_audit.py trial
OPENBLAS_NUM_THREADS=1 python3 independent_audit.py thermal
```

To rerun the complete upstream finite verification, choose an output directory that does not already exist:

```sh
env -u PYTHONOPTIMIZE OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python3 -B source/verification/verify.py \
  --output "$PWD/fresh-verification" --workers 6
```

This larger calculation takes substantially longer than the new scalar certificate. The quoted runtime is an observation from one machine, not a performance guarantee. Rerunning the auxiliary audits changes runtime fields in their JSON files; the checksums describe the distributed snapshot.

Build the PDF with `make paper` (pdfLaTeX required). Check the distributed snapshot and the vendored Git blob hashes with `python3 tools/check_integrity.py`.

## Provenance, attribution, and review status

The upstream source is pinned to OpenAI Math commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`:

- [Original paper and companion files](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-periodic-spin-one-Haldane-gap-September-24-2026).
- [`source_manifest.json`](source_manifest.json) records Git blob hashes and sizes; `source/` preserves those files unmodified.
- [`PROVENANCE.md`](PROVENANCE.md) distinguishes imported files, fresh outputs, and new work.
- [`NOTICE`](NOTICE) and [`LICENSE`](LICENSE) retain the upstream attribution and Apache-2.0 terms. New material is also distributed under Apache-2.0.

**GPT-6 Astra Max autonomously performed the research and authored this work.** Within the open-ended task set by the human user, the agent selected the target result, examined the upstream proof, derived the improved bound, wrote and ran the verification programs, and wrote the paper and repository documentation. The human contribution was to initiate the investigation, authorize computation and publication, and request attribution and presentation revisions. The mathematical extension and its verification code were produced by the agent.

The model designation **GPT-6 Astra Max (OpenAI)** was supplied by the human user. The execution agent was Codex; a backend model snapshot identifier was not available in the session. See [AUTHORSHIP.md](AUTHORSHIP.md) for contribution and identity details. This is an unreviewed technical preprint, not an official OpenAI publication or endorsement. No independent human expert review has been recorded. The new arithmetic is small enough to inspect separately from the much larger source verifier. Corrections to the assumptions, proof, or implementation are welcome through the repository's issue tracker.

## Citation

Use the model author, title, version, date, and exact repository revision when citing this technical note. Citation metadata is supplied in [`CITATION.cff`](CITATION.cff) and [`citation.bib`](citation.bib); record the commit of the public version actually consulted. No DOI, arXiv identifier, or journal acceptance is claimed.
