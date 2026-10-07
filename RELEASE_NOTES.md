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
