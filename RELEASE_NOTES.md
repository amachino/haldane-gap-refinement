# Version 1.0.0 - 7 October 2026

This release contains a technical note autonomously researched and authored by GPT-6 Astra Max, together with a reproducible exact certificate for the conditional bound `gamma_L > 0.0047` on every even periodic spin-one chain of length at least 2304, with `J = 1`. The original stated constant is `log(20)/784`.

GPT-6 Astra Max selected the result, derived the improvement, implemented and ran the checks, and wrote the manuscript. The human user initiated the investigation, authorized computation and publication, and requested attribution and layout revisions. The model designation GPT-6 Astra Max (OpenAI) was supplied by the human user; the execution agent was Codex. A backend model snapshot identifier was not available in the session. The note is unreviewed.

The mathematical dependencies are the spatial-moment representation and initial purity estimates in OpenAI's *The periodic spin-one Haldane gap*, fixed at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The new note rederives the needed bootstrap argument. It does not claim an independent solution of the original conjecture, priority, optimality, formal verification, or independent expert review.

Contents include the paper PDF and TeX, a standard-library-only rational checker, upstream source and evidence, the recorded full finite recomputation, selected separate audit computations, licenses, and checksums.

Run `python3 verify_gap_improvement.py` to check the new bound. Run `python3 tools/check_integrity.py` before rerunning auxiliary computations to verify the distributed snapshot.
