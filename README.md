# Exact-arithmetic refinements of periodic spin-one Haldane-gap bounds

**Version 1.3.0 · 8 October 2026 · Autonomously researched and written by GPT-6 Astra Max · Unreviewed technical note**

[Read the paper](paper/note.pdf) · [LaTeX source](paper/note.tex) · [日本語](README.ja.md)

A length-dependent choice of inverse temperature and an asymmetric purity estimate improve both the constant and the length range. Conditional on the two cited OpenAI papers, the periodic spin-one Heisenberg chain has a unique ground state and

$$
\gamma_L > \frac{3}{50}=0.06
\quad\text{for every integer }L\ge34,\qquad J=1.
$$

In particular, this includes **every odd $L\ge35$**. The thermodynamic statement is $\liminf_{L\to\infty}\gamma_L\ge3/50$ over all integer lengths. These conclusions remain conditional on the cited analytic and finite-input results. They are lower bounds, not estimates of the physical gap. For a positive coupling $J$, multiply the bound by $J$. No claim is made for this numerical bound at lengths below 34. No additional thermal or variational computation is needed.

**Correction to the version 1.0 comparison:** the previous bound of $0.0047$ improves the periodic paper's *stated* constant, but is weaker than this direct consequence of OpenAI's two published papers. The companion's stronger periodic seeds were overlooked in the initial comparison. The old proof and certificate remain valid and are retained below. We do not claim priority, optimality, an independent Haldane-gap proof, or an improvement beyond everything implied by the published OpenAI material.

| Result | Lower bound for the gap | Length range |
|---|---|---|
| Periodic paper's stated bound | $\log(20)/784\approx0.00382109$ | Every even $L\ge2304$ |
| This repository, version 1.0 | $0.0047$ | Every even $L\ge2304$ |
| Corollary extracted in version 1.1 from the two published papers | $\log(125/39)/49\approx0.02377045$ | Every even $L\ge120$ |
| Signed-moment extension in version 1.2 | $\log(125/39)/49\approx0.02377045$ | **Every integer $L\ge120$** |
| Length-adaptive refinement in version 1.3 | **$0.06$** | **Every integer $L\ge34$** |

All rows use the same periodic Hamiltonian and $J=1$. Version 1.3 raises the version 1.2 lower bound by a factor of about **2.52** and lowers the starting length from 120 to 34. The new derivation uses existing spectral inputs; it does not replace their proof. The prior-art review is limited and establishes no priority claim. See [PRIOR_ART.md](PRIOR_ART.md).

## The version 1.3 refinement

The two purity defects decay at different rates. Keeping them separate, and using a suitable inverse temperature for each length interval, avoids the losses from one common defect bound and fixed interpolation intervals.

The proof starts from the companion's published estimates at $n=60$, $\beta=49/2$, with defects $p\le0.0998$ and $q\le0.0628$. The coupled recurrence is iterated with upward rounding. Signed spatial moments at both temperatures are controlled at the same even reference length; rational bounds on the leading-eigenvalue ratio and residual ratios then certify **12 intervals covering every integer from 34 through 11519**. The shortest lengths use the earlier spectral bounds at inverse temperatures $49/4$ and $49/2$.

For the remaining lengths, the new invariant is

$$p^{3/2}\le w,\qquad q\le w,\qquad w_+=6w^2.$$

At $n=7680$, $\beta=3136$, it holds with $w=2\times10^{-83}$. The proof gives $T(L,\beta)\ge1-(15/2)w$ throughout $3n/2\le L\le3n$, including odd lengths. Doubling covers every integer $L\ge11520$, and exact exponential comparisons give the strict bound $0.06$. The [paper](paper/note.pdf) contains the full argument, finite interval table, and dependencies.

### Reproduce the current bound

```sh
python3 verify_adaptive_bound.py
```

This runs **88 exact checks** and writes [`independent_results/adaptive_bound.json`](independent_results/adaptive_bound.json). All acceptance decisions use rational arithmetic. Decimal roots propose rational parameters, whose directions are then proved by integer-power comparisons. Products are rounded outward on a $10^{-140}$ grid. The finite interval covering and the infinite-tail inequalities are checked separately.

Run `make check` for all **four** retained certificates, `make integrity` for source and snapshot hashes, and `make paper` to rebuild the PDF. Python 3.11 or later suffices; no third-party package is needed for the certificates. Optimized execution with `-O` is rejected.

The analytic arguments and upstream assumptions are not machine-formalized. [RESEARCH_NOTES.md](RESEARCH_NOTES.md) records the improvement, exploratory decay rates, and concrete remaining directions; exploratory numbers are not certified theorems.

## Including odd lengths

This section retains the version 1.2 proof of the smaller bound $\log(125/39)/49$ for every integer $L\ge120$.

Proposition 3.1 of the periodic paper gives the **signed** identity $Z_L(\beta)=\sum_i\mu_i(\beta)^L$ for every integer $L\ge4$. Proposition 3.4 of the boundary-field companion supplies a positive unique dominant eigenvalue at the dyadic temperatures, together with its temperature ratios and the periodic purity bounds. Its proof of positivity uses positive physical partition functions at odd lengths; it does not assume an odd-chain gap.

Set $n_k=120\,2^k$, $\beta_k=49\,2^k$, and $u_k=\frac16(39/125)^{2^k}$. The key step controls the spatial tails at **both temperatures using the same even reference length**:

$$
S(n_k,2\beta_k)=\frac{S(n_k,\beta_k)^2T(2n_k,\beta_k)}{T(n_k,\beta_k)^2}
\ge(1-u_k)^3\ge1-3u_k.
$$

The concentration estimate $d(z)=z/(2-3z)$, proved in the note for every $0\le z<1/2$, bounds the two residual absolute moments by $d(u_k)$ and $d(3u_k)$. Increasing the moment order to any integer $L\ge n_k$ preserves these bounds, even when some eigenvalues are negative. With the companion's leading-eigenvalue ratios, this gives, for every integer $n_k\le L\le2n_k$,

$$
T(L,\beta_k)\ge
\frac{(1-u_k)(1-6u_k^2)(1-d(3u_k))}{(1+d(u_k))^2}
\ge1-\frac92u_k>\frac12.
$$

The last inequality has an exact polynomial certificate on the entire interval $0\le u\le13/250$. It implies uniqueness of the physical ground state and

$$
e^{-\beta_k\gamma_L}\le\frac{375}{383}(39/125)^{2^k}<(39/125)^{2^k}.
$$

The dyadic intervals cover every integer $L\ge120$. The [paper](paper/note.pdf) gives the full proof. This is an added analytic argument using the published spectral inputs; the even-only gap proposition is not being applied to odd lengths. No new thermal or variational calculation is required.

### Reproduce the version 1.2 certificate

Use Python 3.11 or later, with no third-party packages:

```sh
python3 verify_signed_extension.py
```

This performs **21 exact checks**, including the polynomial identity and inequalities establishing its sign on the full defect interval, the purity floor, the strict prefactor, and the rounded bound $0.02377$. It writes [`independent_results/signed_extension.json`](independent_results/signed_extension.json). The analytic concentration and signed-trace arguments remain mathematical proofs in the note; the script is not a formal verification of them or the upstream premises. No grid sampling or floating-point comparison determines success.

This certificate remains available alongside the newer length-adaptive proof and the earlier even-length derivations.

## Retained version 1.1 corollary

In *A boundary-field gap for the spin-one Heisenberg chain*, Proposition 3.4 establishes **periodic-chain** estimates

$$
1-S(120,49)\le0.052,\qquad 1-T(240,49)\le0.052.
$$

These use the periodic partition function without endpoint fields, with the same shift and normalization as the periodic paper. They occur at the companion's temperature index $j=2$, so its inverse temperature is $b_2=49$, not $b_0=49/4$.

Use them in Proposition 4.3 of *The periodic spin-one Haldane gap* with $n_0=120$, $\beta_0=49$, $u_0=13/250$, and $C=6$. The exact checks give $0<u_0<1/6$, $G(u_0)<6$, $r=Cu_0=39/125<1$, and $C(1-3u_0)=633/125>3$. That proposition then gives a unique ground state and the displayed bound for every even $L\ge120$.

OpenAI supplied both the reseeding argument and the gap criterion. Version 1.1 contributed their explicit combination, the parameter check, an exact scalar certificate, and the corrected comparison. The reseeding uses the finite periodic inputs in Corollary 5.6 of the periodic paper, already covered by the recorded upstream verification. No additional boundary-field finite computation is needed for this corollary.

### Reproduce the version 1.1 corollary

Use Python 3.11 or later, with no third-party packages:

```sh
python3 verify_companion_corollary.py
```

The script checks **24 exact rational comparisons**: the companion's reseeding comparisons, the uniform-gap conditions, and $\exp(49\times0.02377)<125/39$. It writes [`independent_results/companion_corollary.json`](independent_results/companion_corollary.json). It uses the rational exponential upper bound in `verify_gap_improvement.py`; no numerical logarithm determines success. Optimized execution with `-O` is rejected.

This certificate is retained alongside the new all-length argument and the version 1.0 certificate.

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
| Version 1.3 exact certificate | 88 exact checks; 12 finite intervals and one asymmetric infinite tail | Checks the scalar certificate for $0.06$ at every integer length at least 34 |
| Version 1.2 exact certificate | 21 exact checks, including a polynomial identity and sign on a full interval | Checks the scalar part of the signed-moment extension to every integer length at least 120 |
| Version 1.1 exact certificate | 24 rational comparisons for reseeding and gap extraction | Checks the stronger corollary conditional on the two cited papers |
| Version 1.0 exact certificate | Five updates, five intervals, one uniform tail | Checks the retained 0.0047 bound conditional on the original seed pair |
| Fresh upstream verifier run | 27 thermal cases, two variational contractions, auxiliary checks | All finite checks passed; this reuses the upstream implementation |
| Separate integer implementation | Full 72- and 120-site contraction integers and a direct four-site check | Exact agreement with the upstream values, using code reconstructed from the manuscript |
| Separate floating-point implementation | 16 full-spectrum thermal cases on four to eight sites with twists | Diagnostic agreement within the manuscript's tolerances; not rigorous interval arithmetic |

The complete finite run finished on 7 October 2026 and took about 22 minutes. Its record is [`reproduced/verification.json`](reproduced/verification.json). It reports both `success: true` and `full_recomputation: true`. These existing finite outputs remain unchanged in version 1.3; all four small bound certificates were executed for this revision. Mathematical certificates and supporting logs are included. This audit is not a Lean or other kernel-checked formal proof of the analytic argument.

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

**GPT-6 Astra Max autonomously performed the research and authored this work.** Within the open-ended task set by the human user, the agent selected the target result, examined the upstream proof, derived the version 1.0 bound, wrote and ran the verification programs, and wrote the paper and repository documentation. During the requested prior-art review, the agent identified and verified the stronger corollary and prepared version 1.1. In response to the question about odd lengths, the agent developed the signed-moment extension, implemented its certificate, and authored version 1.2. During the requested continued investigation, the agent derived the length-adaptive interpolation and asymmetric invariant, implemented the 0.06 certificate, and authored version 1.3. The human contribution was to initiate the investigation, authorize computation and publication, ask about odd lengths, and request the prior-art review, incorporation of newly verified findings, and attribution and presentation revisions. The mathematical derivations and verification code were produced by the agent; the underlying spatial-transfer construction, reseeding argument, spectral estimates, and original gap criterion are credited to OpenAI.

The model designation **GPT-6 Astra Max (OpenAI)** was supplied by the human user. The execution agent was Codex; a backend model snapshot identifier was not available in the session. See [AUTHORSHIP.md](AUTHORSHIP.md) for contribution and identity details. This is an unreviewed technical preprint, not an official OpenAI publication or endorsement. No independent human expert review has been recorded. The new arithmetic is small enough to inspect separately from the much larger source verifier. Corrections to the assumptions, proof, or implementation are welcome through the repository's issue tracker.

## Citation

Use the model author, title, version, date, and exact repository revision when citing this technical note. Citation metadata is supplied in [`CITATION.cff`](CITATION.cff) and [`citation.bib`](citation.bib); record the commit of the public version actually consulted. No DOI, arXiv identifier, or journal acceptance is claimed.
