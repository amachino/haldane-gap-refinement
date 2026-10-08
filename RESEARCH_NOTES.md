# Continuing investigation — 8 October 2026

## Certified in version 1.4

Conditional on the pinned OpenAI analytic and finite-input premises, the periodic spin-one chain has a unique ground state and `gamma_L > 0.07` for every integer `L >= 33`, at `J = 1`. Separately, `gamma_32 > 0.06`, with a unique ground state; hence the previous constant 0.06 now holds for every integer length at least 32. The proof is in `paper/note.tex`; `verify_spectral_refinement.py` performs 111 exact checks.

The gain uses the same finite thermal and trial data. No matrix exponential or variational contraction was newly needed:

1. A numerical search suggested a tighter quartic polynomial filter for the invariant sector. The final integer coefficients are `[12328,32348,-499897,-339164,1787190]`. Exact endpoint comparisons and positivity of all shifted coefficients prove a modulus cap of `1.0013505`, improving `1.00139`.
2. Apply the existing capped-mass lemma directly with that cap. This couples the maximum leading contribution with the mass remaining for the other eigenvalues, rather than maximizing both independently. It bounds `Z32` and `Z120` at inverse temperature `49/4`.
3. Combine the upper bound on `Z32` at doubled temperature with the known strict lower bound `Z120 > 1`. If no spatial eigenvalue exceeds `.9999865`, capped mass would force `Z120 < 1`, a contradiction. The odd signed trace ensures positivity of the unique dominant eigenvalue.
4. The sharper eigenvalue bounds yield purity defects `p <= .07584`, `q <= .059062` at reference length 60 and inverse temperature `49/2`. The previous length-dependent interpolation and asymmetric invariant now certify 0.07.

Ten finite intervals cover every integer from 33 through 11519. The infinite tail starts from `n=7680`, `beta=3136`, and `w=2e-97`. The separate length-32 comparison uses a reference moment of order 32. No upper bound on a higher moment is incorrectly transferred to a lower moment.

The polynomial-filter and capped-mass principles, including the idea of forcing a dominant eigenvalue by comparing two moments, are OpenAI's existing methods. This revision contributes a sharper instantiation, its quantitative all-integer consequence, and the certificate. It does not claim a new general moment lemma or priority.

## What the explorations do and do not show

`python3 explore_decay_rates.py` displays **non-rigorous diagnostic** values of `-log(2*q_k)/beta_k` under the coupled update, using ordinary high-precision Decimal arithmetic:

| Seed choice | Observed late-iteration value | Role |
|---|---:|---|
| Printed companion seeds `.0998`, `.0628` | About 0.06054254 | Version 1.3 baseline |
| Earlier, unrounded companion seed expressions | About 0.06063859 | Prior exploration |
| Version 1.4 certified seeds `.07584`, `.059062` | About 0.07093244 | Current recurrence diagnostic |

These values are not proved uniform gap bounds, upper bounds on the physical gap, or optimality barriers. Version 1.4 demonstrates why the earlier value near 0.0606 was not a limit on what could follow from the same finite data. The earlier spatial-defect rate near 0.04069 likewise was not a barrier once interpolation ratios were changed.

`python3 explore_spectral_filter.py` reproduces an optional floating-point coefficient search. It uses NumPy/SciPy and a fixed random seed; optimizer and library variations can change the candidate. The exact certificate uses fixed integer coefficients and does not depend on this search.

Screening also considered different starting inverse temperatures and separate filters for positive and negative eigenvalues in the other sector. These are candidates for further study, not certified improvements in this release. A filter tailored to one exterior ray must not be used as an absolute-value cap without controlling the other ray.

## Concrete directions that remain

| Direction | Required work | Present status |
|---|---|---|
| Increase 0.07 using the current seeds | Tighten scalar constants or delay the tail start, while certifying every finite interval | The recurrence diagnostic suggests only modest gains from this choice alone |
| Improve seeds further from the same data | Optimize both sector filters and starting temperature, or exploit several moment constraints together | Numerical screening is promising; no additional theorem recorded |
| Prove 0.07 at length 32, or 0.06 below 32 | Bound the required lower-order residual moments directly, obtain certified finite spectra, or derive a different short-chain argument | Open here; taking roots of a larger-moment upper bound is insufficient |
| Obtain a substantially larger lower bound | Improve input enclosures, add certified moments or trial lengths, or retain more information in the purity update | No established quantitative forecast or optimality claim |
| Change boundary conditions, perturb the model, or change spin | Establish the corresponding transfer representation and finite inputs; address degeneracies | Not a consequence of this refinement |

The next useful investigation is a joint moment bound or a different initial temperature, rather than simply running the same recurrence many more times. Independent mathematical review remains valuable.

## Retained version 1.3 result

Version 1.3 certified `gamma_L > 0.06` for every integer `L >= 34`. It kept the two defects separate, chose a temperature by length, and introduced `p^(3/2) <= w`, `q <= w`, propagated by `w_next=6*w^2`. Its 88-check certificate covers 12 finite intervals and an infinite tail starting with `w=2e-83`. The earlier proof, checker, and JSON output are retained unchanged. Version 1.4 reuses this interpolation and invariant with stronger seeds.

## Attribution and search limits

The original spatial representation, sector identities, spectral and variational inputs, filter and moment principles, and coupled update are OpenAI's. The explicit refinements and exact certificates were autonomously developed by the agent in this investigation, at the user's request to continue research and incorporate verified findings.

A small follow-up public-source search did not identify a matching report of the precise new constant and range. This is not an exhaustive priority search. No independent expert review is claimed. All fixed source identities and prior finite calculation records remain unchanged.
