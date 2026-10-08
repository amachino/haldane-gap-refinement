# Version 1.6.0 — 8 October 2026

- Conditional strict gap bound **0.145 for every integer L >= 24**, with a unique ground state. This is a 34.3% increase over version 1.5 and includes shorter chains.
- Short-chain ladder: 0.02 for every L >= 18, 0.09 for L >= 20, 0.12 for L >= 22; separately gamma_18 > 0.08. Length 19 is now included.
- Complete exact cyclic-twist table at lengths 4 through 12; every total recomputed and small cases cross-checked against the upstream packed engine and an all-column integer implementation.
- Exact five-site local energy certificate and geometric, blockwise thermal rounding bounds.
- Six sector filters, 67 certified moment polynomials, and tight purity-to-gap conversion. The main checker has 304 named exact checks, 42 individual main-range lengths, six intervals, and an infinite tail from 33792.
- All earlier proofs and records retained, with unchanged imported source bytes. Updated English/Japanese documentation, mathematical note, reproducibility scripts, metadata, and snapshot hashes.
- Conditional and unreviewed. No claim of priority, optimality, formal verification, or an independent proof of the upstream transfer construction.

---

# Version 1.5.0 - 8 October 2026

The conditional bound is now `gamma_L > 0.108` for **every integer `L >= 32`**, including odd lengths, with a unique ground state and `J = 1`. This is a 54.3% increase over 0.07. The all-integer thermodynamic liminf is at least 0.108.

- Retain rotation-sector residuals throughout temperature doubling and prove the sharper recurrence.
- Use the individual original thermal enclosures and fixed simultaneous-moment polynomial certificates, with exact full-interval Bernstein subdivision.
- Compute the existing integer trial state at length 88 and use the seed `n=44`, `beta=539/20`.
- Add a standard-library certificate with 237 named checks: 51 individual main-range lengths, ten finite intervals, and an infinite tail beginning at 16896.
- Certify the shorter-chain ladder: 0.03 from length 20, 0.05 from 22, 0.07 from 24, 0.08 from 26, 0.09 from 28, and 0.10 from 30, always for all integer lengths. Separately, length 18 has gap greater than 0.03; no such result is asserted for length 19.
- Compute and enclose three supplemental cyclic-twist traces, with rerunnable exact code. They are not inputs to the main bound.
- Update the complete note/PDF, both READMEs, reproducibility commands, metadata, authorship, provenance, research/search records, and snapshot checksums. Retain the earlier five gap certificates and all imported source bytes.

`make check` runs six gap certificates and the supplemental trace checker. `make trial88` recomputes the new trial; `make cyclic-traces` recomputes the supplemental thermal totals. Run `make integrity` and `make paper` for hashes and PDF rebuilding.

The result is conditional and unreviewed. No exhaustive priority search, global optimum, machine-formalization, or independent proof of the original spatial-transfer premises is claimed. Model-identity qualifications remain in AUTHORSHIP.md.

# Version 1.4.0 - 8 October 2026

The conditional bound is now `gamma_L > 0.07` for **every integer `L >= 33`**, including odd lengths, with a unique ground state and `J = 1`. This raises the previous constant by one sixth. Separately, `gamma_32 > 0.06`, so the previous constant now covers every integer length at least 32. The all-integer thermodynamic liminf is at least 0.07.

- Select new integer coefficients for the existing polynomial-filter method, improving the invariant-sector modulus cap to 1.0013505.
- Combine capped sector moments with the existing 120-site trial inequality to sharpen dominant-eigenvalue lower bounds and improve the purity seeds to `p=.07584`, `q=.059062` at `n=60`, `beta=49/2`.
- Add `verify_spectral_refinement.py` and its JSON record: 111 exact checks, ten finite intervals, length 32, and one infinite tail. `make check` runs all five retained certificates.
- Update the paper, both READMEs, citations, research notes, attribution, provenance, and checksums; retain all earlier derivations and unmodified upstream sources.

No new finite thermal or variational calculation is required. The polynomial-filter and capped-mass principles are OpenAI's; this revision changes coefficients and their application to the available data. The result remains conditional and unreviewed. No priority, optimality, formal verification, or independent solution is claimed. The 0.07 bound is not asserted below length 33.

Run `make check`, `make integrity`, and `make paper`. Identity qualifications remain in AUTHORSHIP.md.

# Version 1.3.0 - 8 October 2026

The conditional bound is now `gamma_L > 3/50 = 0.06` for **every integer `L >= 34`**, at `J = 1`, with a unique ground state. In particular, every odd `L >= 35` is included. The all-integer liminf is at least 0.06. This raises the version 1.2 lower bound by about 2.52 times and lowers its starting length from 120 to 34.

- Retain the unequal purity defects and choose inverse temperatures according to length. Use the companion's earlier periodic spectral estimates to cover short lengths.
- Certify 12 finite intervals covering 34 through 11519 by rational leading-eigenvalue and residual-ratio bounds.
- Add the asymmetric invariant `p^(3/2) <= w`, `q <= w`, propagated by `w_next=6*w^2`. It proves the tail for every integer length at least 11520.
- Add `verify_adaptive_bound.py` and its output, with 88 exact checks. Root proposals are accepted only after rational powered inequalities prove their direction. `make check` runs all four certificates.
- Update the paper, both READMEs, citations, authorship, provenance, and checksums. Preserve all earlier proofs and the upstream finite verification records.
- Add `RESEARCH_NOTES.md` and `explore_decay_rates.py`. The displayed recurrence rates near 0.06054 and 0.06064 are exploratory, not certified uniform bounds or optimality claims.

No additional thermal or variational calculation is required. The theorem remains conditional on the cited upstream analytic and finite-input results. No same-size bound below length 34, independent Haldane-gap proof, priority, formal verification, or independent expert review is claimed.

Run `make check`, `make integrity`, and `make paper`. The revision is dated in Asia/Tokyo; identity qualifications remain in AUTHORSHIP.md.

# Version 1.2.0 - 8 October 2026

The conditional bound `gamma_L > log(125/39)/49 > 0.02377`, at `J = 1`, now holds for **every integer `L >= 120`**, including every odd `L >= 121`. The ground state is unique on that range, and the liminf statement now runs over all integer lengths. The numerical constant is unchanged from version 1.1.

- Add a signed-moment proof using periodic Proposition 3.1 and companion Proposition 3.4 at the fixed upstream commit. Control the residual tails at both temperatures using the same even reference length, then bound signed traces at arbitrary larger integer lengths. The even-only gap proposition is not applied to odd lengths.
- Prove the elementary concentration estimate on the required domain `0 <= z < 1/2`, and certify the polynomial inequality on the entire interval `0 <= u <= 13/250`.
- Add `verify_signed_extension.py` and its JSON record, with 21 exact checks. `make check` now runs all three bound certificates.
- Update the paper, English and Japanese READMEs, citation metadata, attribution, provenance, and snapshot checksums. Retain the earlier derivations, source snapshots, and finite verification outputs.
- Record the owner's request to incorporate newly verified findings in `AGENTS.md`.

No additional finite thermal or variational calculation is required. The result remains conditional on the cited upstream analytic and finite-input premises. The added proof and arithmetic certificate are not a formal verification of those premises. No bound of this size is claimed here for lengths below 120. No exhaustive priority search or external expert review of the parity extension is claimed.

Run `make check`, `make integrity`, and `make paper`. The revision is dated in Asia/Tokyo. The author and identity qualifications remain in AUTHORSHIP.md.

The entries below record the earlier versions and their original scopes.

# Version 1.1.0 - 8 October 2026

The main result is now the explicit conditional corollary `gamma_L > log(125/39)/49 > 0.02377` for every even `L >= 120`, at `J = 1`. It follows by substituting the periodic seeds in Proposition 3.4 of OpenAI's boundary-field companion into Proposition 4.3 of its periodic-chain paper, both at the same fixed upstream commit.

- Add `verify_companion_corollary.py` and its JSON record, with 24 exact rational comparisons for the reseeding, gap criterion, and rounded decimal consequence. `make check` runs both certificates.
- Revise the paper, both READMEs, citation metadata, provenance, and authorship record. Credit OpenAI for both existing propositions and their underlying arguments.
- Add `PRIOR_ART.md` explaining that version 1.0's comparison missed a stronger consequence of the already published companion paper. No priority claim is made for the newly extracted constant.
- Preserve the version 1.0 proof, checker, and finite verification records. The old bound remains valid under its original premises.
- Include selected unmodified companion sources with a separate Git-blob manifest; extend the integrity checker to both source snapshots.

Run `make check` and `make integrity`. Rebuild the paper with `make paper`. The date of this revision uses Asia/Tokyo. The author remains GPT-6 Astra Max, with the identity and contribution qualifications in AUTHORSHIP.md.

The following version 1.0 entry is a historical record; its corrected comparison scope is documented above and in PRIOR_ART.md.

# Version 1.0.0 - 7 October 2026

This release contains a technical note autonomously researched and authored by GPT-6 Astra Max, together with a reproducible exact certificate for the conditional bound `gamma_L > 0.0047` on every even periodic spin-one chain of length at least 2304, with `J = 1`. The original stated constant is `log(20)/784`.

GPT-6 Astra Max selected the result, derived the improvement, implemented and ran the checks, and wrote the manuscript. The human user initiated the investigation, authorized computation and publication, and requested attribution and layout revisions. The model designation GPT-6 Astra Max (OpenAI) was supplied by the human user; the execution agent was Codex. A backend model snapshot identifier was not available in the session. The note is unreviewed.

The mathematical dependencies are the spatial-moment representation and initial purity estimates in OpenAI's *The periodic spin-one Haldane gap*, fixed at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The new note rederives the needed bootstrap argument. It does not claim an independent solution of the original conjecture, priority, optimality, formal verification, or independent expert review.

Contents include the paper PDF and TeX, a standard-library-only rational checker, upstream source and evidence, the recorded full finite recomputation, selected separate audit computations, licenses, and checksums.

Run `python3 verify_gap_improvement.py` to check the new bound. Run `python3 tools/check_integrity.py` before rerunning auxiliary computations to verify the distributed snapshot.
