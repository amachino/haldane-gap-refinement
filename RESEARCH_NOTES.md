# Continuing investigation — 8 October 2026

## Certified in version 1.3

Conditional on the pinned OpenAI analytic and finite-input premises, the periodic spin-one chain has a unique ground state and `gamma_L > 0.06` for every integer `L >= 34`, at `J = 1`. The proof and exact certificate are in `paper/note.tex` and `verify_adaptive_bound.py`.

Three changes work together:

1. Keep the unequal spatial and physical purity defects instead of immediately replacing them by a common bound. Start from the companion's printed periodic seeds at `n=60`, `beta=49/2`.
2. Choose an inverse temperature for each length interval. Keep the actual exponent in the leading-eigenvalue ratio and bound both signed residual traces at the same even reference length. Earlier spectral estimates handle short lengths.
3. For the infinite tail, track `p^(3/2) <= w` and `q <= w`. This invariant propagates under `w_next=6*w^2` and controls all integer lengths in `[3n/2,3n]`.

The exact checker covers 34 through 11519 by 12 intervals and all larger lengths by the tail argument. It makes 88 exact checks. Its rational root candidates are accepted only after powered comparisons certify their directions. No new finite thermal or variational calculation was required.

## What the exploration suggests

`python3 explore_decay_rates.py` reproduces two **non-rigorous diagnostic** sequences. It tracks `-log(2*q_k)/beta_k` under the chosen coupled update using ordinary high-precision Decimal arithmetic.

- With the printed seeds `p=.0998`, `q=.0628`, the displayed physical-defect decay rate approaches approximately **0.06054**.
- With the sharper seed expressions already appearing in the companion proof, the analogous display approaches approximately **0.06064**.

These observations explain why 0.06 is a natural, simple target for this round. They are not certified uniform lower bounds, optimality statements, upper bounds on the physical gap, or proofs that a different use of the same data cannot do better. In particular, the earlier exploratory value near 0.04069 describes the slower spatial defect; it is not a barrier once the length/temperature ratio and the asymmetric invariant are changed.

## Concrete directions that remain

| Direction | What would need to be proved or computed | Present status |
|---|---|---|
| A small increase beyond 0.06 | Use sharper seed expressions, delay the tail start, or tighten the tail coefficients while checking every finite interval | Plausible from the diagnostic recurrence; not certified here |
| Cover lengths below 34 with the same constant | Improve the residual moment bounds at those lengths, obtain additional certified finite spectra, or connect short chains by another rigorous estimate | Open in this repository; the current certificate makes no such claim |
| A substantially larger lower bound | Sharpen the initial spectral/thermal inputs or derive an update retaining more spectral information than the two purity defects | No established quantitative forecast |
| New boundary conditions, perturbations, or spin values | Supply corresponding analytic representations and certified inputs, and address boundary degeneracies where relevant | Not a consequence of this refinement |

The next useful step is to identify which input dominates the physical-defect decay rate, then test whether a sharper residual-moment estimate materially changes it. Merely iterating the same rounded recurrence much further produces progressively smaller gains. Independent mathematical review of the analytic extension is also valuable.

## Attribution and search limits

The original spatial representation, positive dominant eigenvalues, periodic seeds, and finite certificates are OpenAI's results. The length-dependent interpolation, asymmetric invariant, finite covering, and their implementation were developed in this continuing investigation by the autonomous agent. The user requested that research continue and that verified findings be incorporated.

A small public-source search for the new constant and length threshold did not identify a matching report. This is not an exhaustive priority search, and no priority or independent expert review is claimed. The fixed upstream revision and all recorded source identities remain unchanged.
