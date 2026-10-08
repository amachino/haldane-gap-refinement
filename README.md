# Exact-arithmetic refinements of periodic spin-one Haldane-gap bounds

**Version 1.6.0 · 8 October 2026 · Autonomously researched and written by GPT-6 Astra Max · Unreviewed technical note**

[Read the paper](paper/note.pdf) · [LaTeX source](paper/note.tex) · [日本語](README.ja.md)

A complete cyclic-twist thermal table, sharper rigorous rounding errors, and tight purity-to-gap conversion improve the conditional result to

$$
\gamma_L > \frac{29}{200}=0.145
\quad\text{for every integer }L\ge24,\qquad J=1.
$$

The ground state is unique, including **every odd $L\ge25$**. The result assumes the cited OpenAI spatial-transfer identities and the certified finite inputs specified in the paper. The constant is **34.3% larger** than version 1.5's 0.108, and the starting length decreases from 32 to 24. The all-integer thermodynamic statement is $\liminf\gamma_L\ge0.145$. These are lower bounds, not estimates of the physical gap; multiply by $J$ for positive coupling $J$.

The shorter-chain bounds also improve, including the previously uncovered length 19:

| Strict gap lower bound | All integer lengths |
|---|---|
| $0.02$ | $L\ge18$ |
| $0.09$ | $L\ge20$ |
| $0.12$ | $L\ge22$ |
| **$0.145$** | **$L\ge24$** |

All these ground states are unique. Separately, $\gamma_{18}>0.08$. All results remain conditional and unreviewed.

**Correction to the version 1.0 comparison:** the previous bound of $0.0047$ improves the periodic paper's *stated* constant, but is weaker than this direct consequence of OpenAI's two published papers. The companion's stronger periodic seeds were overlooked in the initial comparison. The old proof and certificate remain valid and are retained below. We do not claim priority, optimality, an independent Haldane-gap proof, or an improvement beyond everything implied by the published OpenAI material.

| Result | Lower bound for the gap | Length range |
|---|---|---|
| Periodic paper's stated bound | $\log(20)/784\approx0.00382109$ | Every even $L\ge2304$ |
| This repository, version 1.0 | $0.0047$ | Every even $L\ge2304$ |
| Corollary extracted in version 1.1 from the two published papers | $\log(125/39)/49\approx0.02377045$ | Every even $L\ge120$ |
| Signed-moment extension in version 1.2 | $\log(125/39)/49\approx0.02377045$ | **Every integer $L\ge120$** |
| Length-adaptive refinement in version 1.3 | **$0.06$** | **Every integer $L\ge34$** |
| Spectral refinement in version 1.4 | $0.07$ | Every integer $L\ge33$ |
| Sector-resolved refinement in version 1.5 | **$0.108$** | **Every integer $L\ge32$** |
| Three-twist refinement in version 1.6 | **$0.145$** | **Every integer $L\ge24$** |

All rows use the same periodic Hamiltonian and $J=1$. Version 1.4 raised the version 1.3 constant by **16.7%** and included length 33. Version 1.3 had raised the version 1.2 constant by about **2.52 times** and lowered the starting length from 120 to 34. The analytic transfer representation remains an upstream premise. Version 1.6 adds finite cyclic-twist data and does not replace the analytic proof. The prior-art review is limited and establishes no priority claim. See [PRIOR_ART.md](PRIOR_ART.md).

## The version 1.6 refinement

1. Compute all nine cyclic-twist thermal traces at lengths 4 through 12 with an exact integer C++ evaluator of the published Horner construction. Small even-chain totals agree exactly with the unmodified packed engine; an odd-chain all-column check independently tests the orbit reduction.
2. Prove $H^{\mathrm{open}}_5>-35/6$ by integer positive-definiteness checks. Translation around the ring gives $H_L(g)\ge-35L/24$ for $L\ge5$. This makes the Horner matrix a strict contraction and substantially reduces certified rounding errors, including for the old integer totals.
3. Resolve the $I$, $O$, and $N$ inputs separately. Six fixed filters and 67 rational moment polynomials sharpen the seed at $(n,\beta)=(44,2009/80)$. The physical defect decreases from about .02030 to .010285.
4. Use the tight two-level purity threshold $K>(1+E^2)/(1+E)^2$, with $E\ge e^{\beta\delta}$, to certify gap greater than $\delta$. This requires no assumption about the first excitation's spin or degeneracy.

The certificate checks **42 individual lengths, 24 through 65**, then **six intervals covering 66 through 33791**. At reference length 22528 and inverse temperature $64288/5$, the invariant starts with $w=1.05443040418529\times10^{-811}$ and covers every remaining integer length. The shorter-chain checks include **$L=19$**.

### Reproduce version 1.6

```sh
python3 verify_resolved_refinement.py
make check
make integrity
make paper
```

The main checker performs **304 named exact checks**, plus exact root-direction and full-interval polynomial comparisons. It writes [`independent_results/resolved_refinement.json`](independent_results/resolved_refinement.json). The scalar checkers need only Python 3.11+ and its standard library. `make check` runs all seven gap certificates and three auxiliary checks. Assertions must be enabled.

Recompute all new thermal integer totals with `make extended-cyclic`. This requires a C++17 compiler with OpenMP, plus NumPy/SciPy for the independent odd-chain cross-check, and took about 6.5 minutes with eight CPUs. `python3 recompute_extended_cyclic.py --quick` runs the small cases. The 88-site trial is reused and remains reproducible with `make trial88`. Earlier source bytes and verification records are retained.

The optional thermal and moment exploration scripts are explicitly non-rigorous. The temperature screen, including unsuccessful colder inputs, is recorded in [RESEARCH_NOTES.md](RESEARCH_NOTES.md). The proof is conditional, unreviewed, and not machine-formalized; no optimality or priority claim is made.

## Retained version 1.5 refinement

1. Reuse the original thermal integer totals with their individual rational enclosures. New filters bound the $J$ spectrum in $(-1.0013391,1.0013391)$ and the $N$ spectrum in $(-.8710311,.750234)$.
2. Combine the moments of orders 4 through 12 in fixed rational polynomial majorants and minorants. Exact Bernstein subdivision proves their signs on the entire spectral intervals. Signed odd moments sharpen the short-chain bounds.
3. Retain separate $I$, $J=I+2O$, and full residual masses at each doubling. The known multiplicities two and three restrict how much residual mass can concentrate. This gives a sharper spatial recurrence; the physical update is the original one.
4. Independently contract the published trial matrices at length 88. The exact negative shifted Rayleigh quotient permits the seed $(n,\beta)=(44,539/20)$.

The certificate checks each length **32 through 82**, then **ten intervals covering 83 through 16895**. At reference length 11264 and inverse temperature $34496/5$, it enters the retained asymmetric invariant, which covers every remaining integer. The additional short-chain results are checked separately. Three new cyclic-twist thermal traces are also enclosed, but are **not premises of the main gap result**.

### Reproduce version 1.5

```sh
python3 verify_sector_refinement.py
make check
make integrity
```

The main script performs **237 named exact checks**, plus exact root-direction and Bernstein-subdivision checks. It writes [`independent_results/sector_refinement.json`](independent_results/sector_refinement.json). Version 1.5 ran six gap certificates and the supplemental trace-enclosure checker; the current `make check` also includes the version 1.6 checks listed above. Python 3.11 or later and its standard library suffice; optimized execution with `-O` is rejected.

To recompute the new finite inputs:

```sh
make trial88        # integer contractions; NumPy/SciPy required, about 15 seconds in the recorded environment
make cyclic-traces  # packed integer thermal engine; standard library, about four minutes
make paper          # rebuild the complete technical note with pdflatex
```

The scalar certificate reads the recorded trial integers; `make trial88` reconstructs them from the matrix recipe and checks a four-site direct wavefunction. The cyclic traces are supplementary. The original full finite verification remains recorded from the earlier run; this revision does not claim a new full upstream run.

The optional `explore_moment_polynomials.py` and `explore_sector_rates.py` expose the numerical searches. Their outputs are **not certificates**. [RESEARCH_NOTES.md](RESEARCH_NOTES.md) records the avenues explored, unsuccessful directions, and remaining limitations. The analytic proofs and upstream premises are not machine-formalized or independently peer-reviewed.

## Retained version 1.4 refinement

The original polynomial-filter and capped-mass methods are OpenAI's. This revision selects new integer filter coefficients and combines the available moment and trial bounds more tightly:

1. The same thermal table bounds every invariant-sector eigenvalue by $U=1.0013505$, improving the former cap $1.00139$.
2. Capped sector moments give $Z_{32}(49/4)<1.08612266$ and $Z_{120}(49/4)<1.175802453$. The existing trial bound $Z_{120}(b)>1$ then forces the dominant eigenvalues above $.999999998$ at $b=49/4$ and $.9999865$ at $b=49/2$.
3. These estimates give new purity defects $p\le.07584$, $q\le.059062$ at reference length 60 and inverse temperature $49/2$, replacing $.0998$ and $.0628$.

The retained length-dependent interpolation certifies **ten finite intervals covering every integer from 33 through 11519**. At reference length 7680 and inverse temperature 3136, the asymmetric invariant holds with $w=2\times10^{-97}$; it covers every remaining integer length. A separate comparison at length 32 proves the smaller constant $0.06$. The [paper](paper/note.pdf) provides the derivation and interval table.

### Reproduce the version 1.4 bound

```sh
python3 verify_spectral_refinement.py
```

This performs **111 exact checks**, including the polynomial's behavior on both entire exterior rays, the moment bounds, the seeds, finite coverage, and infinite-tail inequalities. It writes [`independent_results/spectral_refinement.json`](independent_results/spectral_refinement.json). The optional numerical search only selected candidate filter coefficients; the certificate checks fixed integers and rational inequalities and requires no optimizer.

Run `make check` for all retained certificates, `make integrity` for source and snapshot hashes, and `make paper` to rebuild the PDF. The checkers require Python 3.11 or later and no third-party packages; `-O` is rejected. Their numerical acceptance decisions are exact, but the analytic proof and upstream premises are not machine-formalized or independently peer-reviewed.

## Retained version 1.3 refinement

The two purity defects decay at different rates. Keeping them separate, and using a suitable inverse temperature for each length interval, avoids the losses from one common defect bound and fixed interpolation intervals.

The proof starts from the companion's published estimates at $n=60$, $\beta=49/2$, with defects $p\le0.0998$ and $q\le0.0628$. The coupled recurrence is iterated with upward rounding. Signed spatial moments at both temperatures are controlled at the same even reference length; rational bounds on the leading-eigenvalue ratio and residual ratios then certify **12 intervals covering every integer from 34 through 11519**. The shortest lengths use the earlier spectral bounds at inverse temperatures $49/4$ and $49/2$.

For the remaining lengths, the new invariant is

$$p^{3/2}\le w,\qquad q\le w,\qquad w_+=6w^2.$$

At $n=7680$, $\beta=3136$, it holds with $w=2\times10^{-83}$. The proof gives $T(L,\beta)\ge1-(15/2)w$ throughout $3n/2\le L\le3n$, including odd lengths. Doubling covers every integer $L\ge11520$, and exact exponential comparisons give the strict bound $0.06$. The [paper](paper/note.pdf) contains the full argument, finite interval table, and dependencies.

### Reproduce the version 1.3 bound

```sh
python3 verify_adaptive_bound.py
```

This runs **88 exact checks** and writes [`independent_results/adaptive_bound.json`](independent_results/adaptive_bound.json). All acceptance decisions use rational arithmetic. Decimal roots propose rational parameters, whose directions are then proved by integer-power comparisons. Products are rounded outward on a $10^{-140}$ grid. The finite interval covering and the infinite-tail inequalities are checked separately.

Run `make check` for all retained certificates, `make integrity` for source and snapshot hashes, and `make paper` to rebuild the PDF. Python 3.11 or later suffices; no third-party package is needed for the certificates. Optimized execution with `-O` is rejected.

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
| Version 1.6 exact certificate | 304 named checks plus root and full-interval polynomial checks; 42 individual main-range lengths, six intervals, infinite tail | Certifies 0.145 for all integers at least 24 and the shorter-chain ladder from 18 |
| Version 1.6 exact finite inputs | Nine cyclic-twist totals recomputed, small independent cross-checks, five-site energy certificate, geometric error enclosures | The complete cyclic table and sharper errors enter the main result |
| Version 1.5 exact certificate | 237 named checks plus root and full-interval polynomial checks; 51 individual lengths, ten finite intervals, infinite tail | Certifies 0.108 for all integers at least 32 and the shorter-chain ladder |
| Version 1.5 exact finite inputs | 88-site integer contraction, four-site direct check, three cyclic-twist thermal totals and enclosures | Trial enters version 1.5; its three cyclic traces are supplementary to that result |
| Version 1.4 exact certificate | 111 exact checks; ten finite intervals, length 32, and an infinite tail | Checks the scalar certificate for $0.07$ at every integer length at least 33, and $0.06$ at length 32 |
| Version 1.3 exact certificate | 88 exact checks; 12 finite intervals and one asymmetric infinite tail | Checks the scalar certificate for $0.06$ at every integer length at least 34 |
| Version 1.2 exact certificate | 21 exact checks, including a polynomial identity and sign on a full interval | Checks the scalar part of the signed-moment extension to every integer length at least 120 |
| Version 1.1 exact certificate | 24 rational comparisons for reseeding and gap extraction | Checks the stronger corollary conditional on the two cited papers |
| Version 1.0 exact certificate | Five updates, five intervals, one uniform tail | Checks the retained 0.0047 bound conditional on the original seed pair |
| Fresh upstream verifier run | 27 thermal cases, two variational contractions, auxiliary checks | All finite checks passed; this reuses the upstream implementation |
| Separate integer implementation | Full 72- and 120-site contraction integers and a direct four-site check | Exact agreement with the upstream values, using code reconstructed from the manuscript |
| Separate floating-point implementation | 16 full-spectrum thermal cases on four to eight sites with twists | Diagnostic agreement within the manuscript's tolerances; not rigorous interval arithmetic |

The complete finite run finished on 7 October 2026 and took about 22 minutes. Its record is [`reproduced/verification.json`](reproduced/verification.json). It reports both `success: true` and `full_recomputation: true`. These existing finite outputs remain unchanged. All seven gap certificates and three auxiliary checks were executed for version 1.6, and all nine new cyclic totals were recomputed. The 88-site contraction and both cyclic tables are recorded separately. Mathematical certificates and supporting logs are included. This audit is not a Lean or other kernel-checked formal proof of the analytic argument.

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

**GPT-6 Astra Max autonomously performed the research and authored this work.** Within the open-ended task set by the human user, the agent selected the target result, examined the upstream proof, derived the version 1.0 bound, wrote and ran the verification programs, and wrote the paper and repository documentation. During the requested prior-art review, the agent identified and verified the stronger corollary and prepared version 1.1. In response to the question about odd lengths, the agent developed the signed-moment extension, implemented its certificate, and authored version 1.2. During the requested continued investigation, the agent derived the length-adaptive interpolation and asymmetric invariant, implemented the 0.06 certificate, and authored version 1.3. Continuing the investigation, the agent selected the tighter filter, derived the new spectral bounds and seeds, implemented the 0.07 certificate, and authored version 1.4. In version 1.5 the agent derived the sector-resolved recurrence, certified simultaneous moment bounds, computed the 88-site trial and supplemental cyclic traces, and wrote the new all-integer certificate and exposition. In version 1.6 the agent computed the complete cyclic table, proved the local energy and geometric error bounds, applied tight purity extraction, and authored the 0.145 certificate and revision. The human contribution was to initiate the investigation, authorize computation and publication, ask about odd lengths, and request the prior-art review, incorporation of newly verified findings, and attribution and presentation revisions. The mathematical derivations and verification code were produced by the agent; the underlying spatial-transfer construction, reseeding argument, spectral estimates, and original gap criterion are credited to OpenAI.

The model designation **GPT-6 Astra Max (OpenAI)** was supplied by the human user. The execution agent was Codex; a backend model snapshot identifier was not available in the session. See [AUTHORSHIP.md](AUTHORSHIP.md) for contribution and identity details. This is an unreviewed technical preprint, not an official OpenAI publication or endorsement. No independent human expert review has been recorded. The new arithmetic is small enough to inspect separately from the much larger source verifier. Corrections to the assumptions, proof, or implementation are welcome through the repository's issue tracker.

## Citation

Use the model author, title, version, date, and exact repository revision when citing this technical note. Citation metadata is supplied in [`CITATION.cff`](CITATION.cff) and [`citation.bib`](citation.bib); record the commit of the public version actually consulted. No DOI, arXiv identifier, or journal acceptance is claimed.
