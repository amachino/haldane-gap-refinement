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

The upstream default branch still pointed to this revision when checked on 7 October 2026. Targeted public searches and upstream issue/PR searches did not identify an earlier instance of this specific 0.0047 refinement. These limited searches do not establish priority or rule out unindexed related work.

## Fresh upstream computation

`reproduced/` contains a complete fresh execution of the upstream finite verification, with assertions enabled. It began at 2026-10-07 12:53:57 UTC and finished at 13:16:15 UTC. The run used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, six requested workers, and one BLAS/OpenMP thread per process. Its checks and result are recorded in `reproduced/verification.json`.

The following two nonmathematical path normalizations were made for distribution:

1. Each command's absolute interpreter path in `reproduced/verification.json` was replaced with `python3`.
2. The output path in `reproduced/logs/thermal2-arithmetic.log` was made relative to `reproduced/`.

No mathematical result, certificate integer, interval, status, timestamp, or recorded runtime was changed. The executable copies under `reproduced/` originate from the upstream verifier and remain attributable to OpenAI.

## Additional work

- `verify_gap_improvement.py`: the small exact certificate for the 0.0047 refinement. It depends on the upstream analytic representation and seed bounds. Decimal and float outputs are explanatory only.
- `independent_audit.py`: selected computations reconstructed from the manuscript's definitions and tables. It imports no functions from the upstream implementation. For distribution, an explicit guard against disabled assertions was added.
- `independent_results/`: recorded outputs of those computations, including complete variational integers and diagnostic thermal values.
- `paper/note.tex` and `paper/note.pdf`: the technical note describing the extension and its assumptions.
- `tools/check_integrity.py`: integrity checks for the distributed snapshot and imported Git blobs. Integrity checks alone do not establish mathematical correctness.

GPT-6 Astra Max autonomously conducted the investigation, derived the improvement, implemented and executed the checks, and authored the manuscript after reading the public source. The human user initiated the open-ended task, authorized computation and publication, and requested attribution and layout revisions. The mathematical extension and its verification code were produced by the agent. This was not a blind experiment on an unsolved problem. No claim is made about the ability to discover the original proof without seeing it, or about the capabilities or training of a private model.

The model designation GPT-6 Astra Max (OpenAI) was supplied by the human user. The execution agent was Codex. A backend model snapshot identifier was not available in the session; the model designation is user-supplied provenance rather than a runtime metadata measurement. [AUTHORSHIP.md](AUTHORSHIP.md) records the contribution and identity scope.

## Limits

The improvement has a short exact arithmetic certificate, but the original analytic construction is not formalized or independently reconstructed in this repository. A fresh run of the original finite verifier and a separate implementation of selected calculations are different levels of evidence. Only the selected variational contractions and scalar checks are independently implemented using exact arithmetic; the independent thermal calculation is floating-point diagnostic work. No independent human expert review or journal review is recorded.
