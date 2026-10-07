# Exact-arithmetic refinements of periodic spin-one Haldane-gap bounds

**Version 1.1.0 · 8 October 2026 · Autonomously researched and written by GPT-6 Astra Max · Unreviewed technical note**

[Read the paper](paper/note.pdf) · [LaTeX source](paper/note.tex) · [日本語](README.ja.md)

Combining two already published OpenAI propositions gives the following explicit corollary for the periodic spin-one Heisenberg chain:

$$
\gamma_L > \frac{\log(125/39)}{49}>0.02377
\quad\text{for every even }L\ge120,\qquad J=1.
$$

The exact constant is approximately $0.023770450840258259$. The thermodynamic statement is $\liminf_{L\to\infty,\ L\text{ even}}\gamma_L\ge\log(125/39)/49$. These conclusions remain conditional on the cited analytic and finite-input results. They are lower bounds, not estimates of the physical gap.

**Correction to the version 1.0 comparison:** the previous bound of $0.0047$ improves the periodic paper's *stated* constant, but is weaker than this direct consequence of OpenAI's two published papers. The companion's stronger periodic seeds were overlooked in the initial comparison. The old proof and certificate remain valid and are retained below. We do not claim priority, optimality, an independent Haldane-gap proof, or an improvement beyond everything implied by the published OpenAI material.

| Result | Lower bound for the gap | Length range |
|---|---|---|
| Periodic paper's stated bound | $\log(20)/784\approx0.00382109$ | Every even $L\ge2304$ |
| This repository, version 1.0 | $0.0047$ | Every even $L\ge2304$ |
| Corollary extracted in version 1.1 from the two published papers | $\log(125/39)/49\approx0.02377045$ | Every even $L\ge120$ |

All rows use the same periodic Hamiltonian and $J=1$. The last constant is about 5.06 times the version 1.0 constant, with a wider length range. We have not located it explicitly stated in the examined sources; this does not establish priority. See [PRIOR_ART.md](PRIOR_ART.md).

## The stronger corollary

In *A boundary-field gap for the spin-one Heisenberg chain*, Proposition 3.4 establishes **periodic-chain** estimates

$$
1-S(120,49)\le0.052,\qquad 1-T(240,49)\le0.052.
$$

These use the periodic partition function without endpoint fields, with the same shift and normalization as the periodic paper. They occur at the companion's temperature index $j=2$, so its inverse temperature is $b_2=49$, not $b_0=49/4$.

Use them in Proposition 4.3 of *The periodic spin-one Haldane gap* with $n_0=120$, $\beta_0=49$, $u_0=13/250$, and $C=6$. The exact checks give $0<u_0<1/6$, $G(u_0)<6$, $r=Cu_0=39/125<1$, and $C(1-3u_0)=633/125>3$. That proposition then gives a unique ground state and the displayed bound for every even $L\ge120$.

OpenAI supplied both the reseeding argument and the gap criterion. This revision contributes their explicit combination, the parameter check, an exact scalar certificate, and the corrected comparison. The reseeding uses the finite periodic inputs in Corollary 5.6 of the periodic paper, already covered by the recorded upstream verification. No additional boundary-field finite computation is needed for this corollary.

## Reproduce the stronger bound

Use Python 3.11 or later, with no third-party packages:

```sh
python3 verify_companion_corollary.py
```

The script checks **24 exact rational comparisons**: the companion's reseeding comparisons, the uniform-gap conditions, and $\exp(49\times0.02377)<125/39$. It writes [`independent_results/companion_corollary.json`](independent_results/companion_corollary.json). It uses the rational exponential upper bound in `verify_gap_improvement.py`; no numerical logarithm determines success. Optimized execution with `-O` is rejected.

Run `make check` to verify both the stronger corollary and the retained version 1.0 certificate.

## Retained version 1.0 refinement

Five further, upward-rounded updates of the original coupled purity recurrence retain information discarded by rounding both defects to 0.01. Five interval estimates and one infinite-tail estimate then cover every even length at least 2304. The paper gives the argument; a short certificate verifies all its numerical inequalities using exact fractions.

The two upstream mathematical inputs are Proposition 3.1 (the spatial-moment representation) and Proposition 5.5 (the initial purity bounds). The note rederives the bootstrap steps from Lemma 4.2 and Proposition 4.3. Acceptance of the underlying analytic proof remains necessary.

### Reproduce the version 1.0 bound

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
| Version 1.1 exact certificate | 24 rational comparisons for reseeding and gap extraction | Checks the stronger corollary conditional on the two cited papers |
| Version 1.0 exact certificate | Five updates, five intervals, one uniform tail | Checks the retained 0.0047 bound conditional on the original seed pair |
| Fresh upstream verifier run | 27 thermal cases, two variational contractions, auxiliary checks | All finite checks passed; this reuses the upstream implementation |
| Separate integer implementation | Full 72- and 120-site contraction integers and a direct four-site check | Exact agreement with the upstream values, using code reconstructed from the manuscript |
| Separate floating-point implementation | 16 full-spectrum thermal cases on four to eight sites with twists | Diagnostic agreement within the manuscript's tolerances; not rigorous interval arithmetic |

The complete finite run finished on 7 October 2026 and took about 22 minutes. Its record is [`reproduced/verification.json`](reproduced/verification.json). It reports both `success: true` and `full_recomputation: true`. These existing finite outputs are retained unchanged in version 1.1; the new scalar certificate was executed separately. Mathematical certificates and supporting logs are included. This audit is not a Lean or other kernel-checked formal proof of the analytic argument.

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
- [Boundary-field companion paper](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-boundary-field-gap-for-the-spin-one-Heisenberg-chain-September-24-2026), especially Proposition 3.4 and the periodic definitions in Section 2.
- [`source_manifest.json`](source_manifest.json) records Git blob hashes and sizes; `source/` preserves those files unmodified.
- [`boundary_source_manifest.json`](boundary_source_manifest.json) records the selected unmodified companion sources under `source_boundary/`. This selection is not a complete TeX build.
- [`PROVENANCE.md`](PROVENANCE.md) distinguishes imported files, fresh outputs, and new work.
- [`NOTICE`](NOTICE) and [`LICENSE`](LICENSE) retain the upstream attribution and Apache-2.0 terms. New material is also distributed under Apache-2.0.

**GPT-6 Astra Max autonomously performed the research and authored this work.** Within the open-ended task set by the human user, the agent selected the target result, examined the upstream proof, derived the version 1.0 bound, wrote and ran the verification programs, and wrote the paper and repository documentation. During the requested prior-art review, the agent identified and verified the stronger corollary and prepared version 1.1. The human contribution was to initiate the investigation, authorize computation and publication, and request the prior-art review, this update, and attribution and presentation revisions. The mathematical derivations and verification code were produced by the agent; the underlying reseeding argument and gap criterion are credited to OpenAI.

The model designation **GPT-6 Astra Max (OpenAI)** was supplied by the human user. The execution agent was Codex; a backend model snapshot identifier was not available in the session. See [AUTHORSHIP.md](AUTHORSHIP.md) for contribution and identity details. This is an unreviewed technical preprint, not an official OpenAI publication or endorsement. No independent human expert review has been recorded. The new arithmetic is small enough to inspect separately from the much larger source verifier. Corrections to the assumptions, proof, or implementation are welcome through the repository's issue tracker.

## Citation

Use the model author, title, version, date, and exact repository revision when citing this technical note. Citation metadata is supplied in [`CITATION.cff`](CITATION.cff) and [`citation.bib`](citation.bib); record the commit of the public version actually consulted. No DOI, arXiv identifier, or journal acceptance is claimed.
