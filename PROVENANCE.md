# Provenance and reproducibility record

## Upstream

- Author: OpenAI.
- Title: *The periodic spin-one Haldane gap*.
- Manuscript date: 24 September 2026.
- Repository: https://github.com/openai/math
- Fixed commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
- Paper directory: `preprints/The-periodic-spin-one-Haldane-gap-September-24-2026/`.
- License: Apache-2.0, preserved in `source/LICENSE` and the repository-level `LICENSE`.

The files in `source/` are unmodified copies of the files identified in `source_manifest.json`. That manifest includes the paper, analytic source sections used in the audit, the finite verifier, its companion scripts, and the public evidence. The manifest's `LICENSE` entry comes from the upstream repository root; the other paths are relative to the paper directory. All Git blob SHA-1 values and byte counts were checked on retrieval and can be checked again locally. This is a selected snapshot, not a clone of the entire OpenAI Math repository or a complete upstream TeX build.

Version 1.1 additionally uses *A boundary-field gap for the spin-one Heisenberg chain*, also dated 24 September 2026, at the same fixed commit. Its directory is `preprints/A-boundary-field-gap-for-the-spin-one-Heisenberg-chain-September-24-2026/`. Selected unmodified TeX files and the upstream license are in `source_boundary/`, identified by `boundary_source_manifest.json`. The `LICENSE` entry is from the repository root; other paths are relative to this companion's paper directory. This is not a complete companion TeX build.

The upstream default branch still pointed to this revision when checked on 7 October 2026. The subsequent prior-art review found that companion Proposition 3.4 supplies stronger periodic seeds. Together with periodic Proposition 4.3, these imply `log(125/39)/49` for every even length at least 120. Version 1.0 had compared only with the periodic paper's stated `log(20)/784` bound, overlooking this stronger consequence of the full published pair. Version 1.1 corrects that comparison. The underlying propositions are OpenAI's; the explicit combination and its certificate were produced during this investigation. See PRIOR_ART.md for sources and search limitations. No priority claim is made.

## Fresh upstream computation

`reproduced/` contains a complete fresh execution of the upstream finite verification, with assertions enabled. It began at 2026-10-07 12:53:57 UTC and finished at 13:16:15 UTC. The run used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, six requested workers, and one BLAS/OpenMP thread per process. Its checks and result are recorded in `reproduced/verification.json`.

The following two nonmathematical path normalizations were made for distribution:

1. Each command's absolute interpreter path in `reproduced/verification.json` was replaced with `python3`.
2. The output path in `reproduced/logs/thermal2-arithmetic.log` was made relative to `reproduced/`.

No mathematical result, certificate integer, interval, status, timestamp, or recorded runtime was changed. The executable copies under `reproduced/` originate from the upstream verifier and remain attributable to OpenAI.

## Additional work

- `verify_spectral_refinement.py`: the version 1.4 certificate, with 111 exact checks for the tighter filter, moment and leading-eigenvalue bounds, new purity seeds, ten finite intervals, a length-32 consequence, and one infinite tail. It proves `gamma_L > 0.07` for every integer length at least 33 and `gamma_32 > 0.06`, conditional on the pinned inputs. It imports directed rational arithmetic from the retained checker. The original filter and capped-mass principles are credited to OpenAI.
- `explore_spectral_filter.py`: optional floating-point coefficient search using NumPy/SciPy. It is not part of the certificate. The accepted integer coefficients are fixed and verified independently of the optimizer in the new checker.

- `verify_adaptive_bound.py`: the version 1.3 certificate, with 88 exact checks for 12 finite intervals and one infinite tail. It certifies `gamma_L > 0.06` for every integer length at least 34, under the stated upstream premises. Decimal root proposals are certified by rational powered inequalities; all acceptance decisions and outward rounding use integer/rational arithmetic.
- `explore_decay_rates.py` and `RESEARCH_NOTES.md`: reproducible, explicitly non-rigorous diagnostic decay rates and the remaining research directions. These are not part of the gap certificate or a proof of optimality.
- `verify_signed_extension.py`: 21 exact checks for the extension to every integer length at least 120. It verifies a polynomial identity, endpoint inequalities proving its sign on the full defect interval, the purity floor, the strict gap prefactor, and the rounded bound `0.02377`. The concentration and signed-trace proof is in the note; its upstream analytic dependencies remain explicit.
- `verify_companion_corollary.py`: the stronger corollary's 24 exact rational comparisons, including the companion's reseeding arithmetic, the periodic uniform-gap criterion, and the rounded bound `0.02377`. It uses the rational Taylor upper bound from the older checker. The analytic and finite-input premises remain upstream dependencies.
- `verify_gap_improvement.py`: the small exact certificate for the 0.0047 refinement. It depends on the upstream analytic representation and seed bounds. Decimal and float outputs are explanatory only.
- `independent_audit.py`: selected computations reconstructed from the manuscript's definitions and tables. It imports no functions from the upstream implementation. For distribution, an explicit guard against disabled assertions was added.
- `independent_results/`: recorded outputs of those computations, including complete variational integers and diagnostic thermal values.
- `paper/note.tex` and `paper/note.pdf`: the technical note describing the extension and its assumptions.
- `tools/check_integrity.py`: integrity checks for the distributed snapshot and imported Git blobs. Integrity checks alone do not establish mathematical correctness.

Version 1.1 reused the recorded full finite verification without altering its results or claiming a new full run. The periodic inputs required by the companion reseeding were already included in that execution. Both scalar certificates were executed for this revision, and their output records are included. The new corollary does not require the boundary-field paper's additional open-chain thermal certificates. The revision is dated 8 October 2026 in Asia/Tokyo.

Version 1.2 extends the same bound to **every integer length at least 120**, hence every odd length at least 121. It uses the periodic paper's signed trace formula for all integer lengths and the companion's positive dominant eigenvalues, purity estimates, and adjacent-temperature leading-eigenvalue ratios. The new argument bounds both residual absolute moments at the same even reference length, using partition-function cancellation for the second temperature, before increasing the moment order to an arbitrary integer. The elementary concentration bound is proved for every defect below one half, including the `3u` value needed here. An exact polynomial identity certifies the full-interval estimate. These analytic steps were derived and written by the agent; the quoted spectral inputs are credited to OpenAI.

All three small bound certificates were executed for version 1.2. The imported source files and earlier finite verification records remain unchanged; no new full thermal run or additional finite input is claimed. The TeX/PDF, both READMEs, metadata, and snapshot checksums were updated. The date uses Asia/Tokyo. The owner's request to incorporate newly verified findings is recorded in `AGENTS.md` for continued work on this repository.

GPT-6 Astra Max autonomously conducted the investigation, derived the first refinement and the later explicit corollary, implemented and executed the checks, and authored the manuscript after reading the public sources. The human user initiated the open-ended task, authorized computation and publication, and requested the prior-art review, this update, and attribution and layout revisions. The mathematical derivations and verification code were produced by the agent. This was not a blind experiment on an unsolved problem. No claim is made about the ability to discover the original proof without seeing it, or about the capabilities or training of a private model.

The human subsequently asked whether odd lengths could also be proved and requested that new findings be incorporated. The agent derived and verified the signed-moment extension and prepared version 1.2 under that authorization.

Version 1.3 arose from the user's request to continue research into further refinements. The agent retained the two purity defects separately, used earlier periodic spectral estimates for short lengths, derived a general interval bound with rational residual ratios, and introduced the invariant `p^(3/2) <= w`, `q <= w`. The starting inequalities are in the proof of companion Proposition 3.4, with their scalar comparisons already covered by `verify_companion_corollary.py`. The first 12 intervals cover all integers from 34 through 11519; the tail starts at 11520. Its update is `w_next=6*w^2`, with `w0=2e-83` at `n0=7680`, `beta0=3136`.

All four bound certificates were run for version 1.3. The imported source bytes, their manifests, and the recorded full finite verification remain unchanged. No new full finite run, external expert review, or machine-formal verification is claimed. The exploratory values near 0.06054 and 0.06064 concern particular recurrence decay rates; only the uniform 0.06 theorem is certified in this revision.

Version 1.4 continues the same authorized research. It keeps the original finite data, chooses new integer filter coefficients, sharpens capped partition-function bounds and dominant-eigenvalue lower bounds, and starts the recurrence from `p=.07584`, `q=.059062`. The resulting certificate makes 111 exact checks and proves 0.07 at every integer length at least 33, plus 0.06 at length 32. The filter and capped-mass principles are inherited from the periodic paper; their new quantitative use and connection to the retained all-integer interpolation were developed by the agent. All five bound certificates were run. No large finite recomputation or formal/external review is claimed. Prior certificates and imported sources remain unchanged.

Version 1.5 reuses the original thermal integer totals and their certified Appendix B enclosures, retaining separate rational intervals instead of one common error. New fixed polynomials are certified on full intervals by exact Bernstein subdivision. The added sector-resolved recurrence leads to 0.108 for every integer length at least 32, with 237 named checks, plus root and polynomial comparisons. All six retained gap certificates and the supplemental trace checker were executed. The 88-site trial is a new arbitrary-precision integer contraction, independently reconstructed from the already-published matrix entry recipe; its norm and energy convention were checked against a four-site direct wavefunction. `verify_trial88.py` reproduces its stored integers. NumPy 2.3.5 and SciPy 1.17.0 were used through the existing independent reconstruction module.

Three new cyclic-twist thermal totals at inverse temperature 49/4 and lengths 6, 8, 10 were computed with the unmodified upstream packed recurrence, changing only its rational Poisson coefficients from mean 84 to mean 98. `recompute_cyclic_traces.py` reproduces this calculation; `verify_cyclic_traces.py` checks the adapted error inequalities and trace enclosures. These traces do not enter the main theorem. They are not described as a new independent thermal implementation or a fresh full upstream verification. The main scalar certificate requires only the standard library and the recorded finite inputs. Earlier source bytes, certificates, and full-run records are preserved.

The model designation GPT-6 Astra Max (OpenAI) was supplied by the human user. The execution agent was Codex. A backend model snapshot identifier was not available in the session; the model designation is user-supplied provenance rather than a runtime metadata measurement. [AUTHORSHIP.md](AUTHORSHIP.md) records the contribution and identity scope.

## Version 1.6 computations

The complete C-twisted table at inverse temperature 49/4 and lengths 4 through 12 was computed with `compute_thermal_moments.cpp`, using Q=2^55, cutoff 280, and exact Poisson coefficient floors with mean 98. Its algorithm is an independently implemented evaluator of the pinned Horner construction, not a new thermal identity. `recompute_extended_cyclic.py` rebuilt the distributed C++ source and reproduced every stored total. Small even cases match the unmodified upstream packed engine exactly after setting the same coefficients. At odd length five, a separate all-column sparse integer implementation yields overlapping certified norm intervals. No timing or host path enters the acceptance records.

`verify_local_energy.py` proves positivity of 6 H_open,5 + 35 I by fraction-free integer elimination in every magnetization block. Translating this local bound gives H_L(g) >= -35 L/24 for L>=5, and hence a strict contraction bound for the retained thermal Horner matrix. `thermal_error_bounds.py` uses the geometric propagation of floors, with block dimensions counted exactly. This sharpens both the existing two-twist totals and the new cyclic totals; imported integer data are not modified.

`verify_resolved_refinement.py` certifies six full-ray filters, 67 full-interval moment polynomials, the seed at n=44 and beta=2009/80, nine sector updates, 42 individual main-range lengths, six intervals, and the tail from L=33792. Its 304 named checks prove 0.145 for every integer L>=24, plus the shorter-chain ladder and uniqueness. Product rounding uses a 10^-1000 grid and root proposals a 10^-450 margin. Exponentials use a rational Taylor bound at a reduced argument followed by upward-rounded squaring. All numerical acceptance decisions use exact arithmetic. The 88-site and 120-site trials are reused.

The tight purity-to-gap conversion and the translated local energy argument are elementary ingredients; this work claims their quantitative application and explicit certificates, not invention of general probability or local-energy methods. The temperature scans and sampled moment optimizations are non-rigorous research diagnostics. The revision preserves earlier result records and all pinned source bytes. No new complete upstream run, external peer review, or formalization is claimed.

## Limits

The improvement has a short exact arithmetic certificate, but the original analytic construction is not formalized or independently reconstructed in this repository. A fresh run of the original finite verifier and a separate implementation of selected calculations are different levels of evidence. The selected variational contractions, new cyclic thermal evaluator, local energy check, and scalar certificates have independently implemented exact-arithmetic components. Separate floating-point thermal screens remain diagnostic only. Independent implementations and internal cross-checks do not amount to independent expert review. No independent human expert review or journal review is recorded.
