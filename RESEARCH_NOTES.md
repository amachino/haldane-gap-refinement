# Continuing investigation — 8 October 2026, version 1.5

## Certified results

Conditional on the pinned spatial-transfer and finite-input premises, `gamma_L > 0.108` for every integer `L >= 32`, with a unique ground state and `J=1`. The main certificate has 237 named exact checks, additional root-direction and Bernstein checks, 51 individual main-range lengths, ten finite intervals, and an infinite tail starting at 16896. The shorter all-integer bounds are 0.03 from length 20, 0.05 from 22, 0.07 from 24, 0.08 from 26, 0.09 from 28, and 0.10 from 30. Length 18 separately has gap greater than 0.03. All earlier results are retained below as historical records.

## What produced the gain

**Individual input errors.** The original integer thermal totals come with much sharper individual intervals than the common printed error of 30e-6. Re-enclosing those existing totals, without rerunning the thermal engine, narrows some low-order errors to roughly 1e-10. The exact original enclosure formulas are preserved and re-evaluated.

**Simultaneous moments.** Treat the fourth-power-weighted spatial spectrum as a positive measure. Polynomial majorants and minorants of each desired power use all the known moments at once. The fixed rational coefficients are verified on the full spectral support by Bernstein subdivision. This is not acceptance of a sampled linear program. Joint J-sector bounds further sharpen the initial seed after the first N-sector improvement. The final caps are `U=1.0013391`, `V=.8710311`, and positive N cap `.750234`.

**Sector information during iteration.** Instead of reducing everything immediately to a total purity defect, retain the invariant residual, the full J residual, and the total residual. The other two lists have multiplicities two and three. Convex maximization at four explicit vertices bounds the residual after the leading eigenvalue is removed. This supplies the new spatial update. Physical cancellation and squaring are unchanged from the upstream argument. The paper proves uniqueness and positivity of the required spatial eigenvalue at every step, rather than presuming it at a new temperature.

**A different starting point.** The optimum among the screened reference lengths lies near `n=44`, `beta=26.95`, using the moment of order 26. The published trial matrices are newly contracted at length 88, verifying a negative shifted Rayleigh quotient with arbitrary-precision integers. A direct four-site wavefunction checks the convention. The final start uses the exact rational inverse temperature `539/20`.

**Negative odd moments.** For short odd rings, simply discarding negative N eigenvalues loses substantial information. Certified polynomial upper bounds on the signed odd N moments improve the partition-function denominator. This yields the new ladder of shorter-chain bounds. It does not treat signed odd moments as probabilities.

## Explorations and limits

`explore_sector_rates.py` compares ordinary and sector-resolved updates for the same trial-compatible starting choices. The values below are non-rigorous late-iteration decay diagnostics, not proved gaps or upper bounds:

| Reference length, moment, temperature multiplier | Ordinary update | Sector-resolved update |
|---|---:|---:|
| 36, 24, 1.775 | about 0.064235 | about 0.105742 |
| 44, 26, 2.2 | about 0.085663 | about 0.108319 |
| 60, 26, 3.1 | about 0.090342 | about 0.101359 |

A broader screen tried reference lengths 36, 40, 42, 44, 46, 48, and 60, base moments 22 through 32 in steps of two, and multipliers 1 through 3.25 in steps of .025. The largest diagnostic in this grid was near .108319 at reference 44, moment 26, multiplier 2.2. Intermediate trial lengths in this screen were hypothetical candidates; only the chosen new length 88 was subsequently certified. This is not a global parameter optimum, a barrier for the method, or an upper bound on the physical gap. Further recurrence iterations could support finer decimal improvements, but 0.108 is the proved rounded bound reported here.

Three extra cyclic-twist traces at inverse temperature 49/4 and lengths 6, 8, 10 were computed and separately certified. Their centers and radii are in `independent_results/cyclic_trace_enclosures.json`. A filter using only the added I-sector information gave a cap around 1.00244 in numerical exploration, weaker than the J-sector cap already available. Reseeding with those traces did not supersede the selected certificate. They are therefore recorded as additional results rather than hidden dependencies.

A sampled J-sector moment optimization at order 88 improved the capped upper bound by less than 1e-6, whereas the order-26 improvement was around .00146 and was incorporated after continuum certification. The order-88 screen was not promoted to a new certified bound. Trying to force a negative N eigenvalue directly from a one-polynomial Rayleigh quotient gave too weak a magnitude estimate to improve the certificate. The eventual signed odd-moment majorants were more useful.

The current short-length calculation does not give a useful positive bound at length 19: the available lower purity estimate fails to cross one half. This is a limitation of these estimates, not a claim about the chain's actual gap or ground state. No conclusion below the proved ranges follows by rooting a higher-moment upper bound.

## Remaining research directions

A substantial next increase appears to require stronger thermal information at a new temperature, further constraints on the spatial spectrum, or an improvement to the physical-purity update. None is established here, and the diagnostic rates do not prove that these are the only routes. Direct spectral information for shorter odd chains may close the length-19 gap in this particular certificate. Changing boundary conditions or the Hamiltonian would require new premises; the periodic result does not imply those variants.

The proof and new scalar checks were produced and reviewed internally by the same autonomous agent. Independent mathematical review remains outstanding. The result is a refinement conditional on the cited OpenAI analytic premises, not an independent solution of those premises or a priority claim.

---

The following is the previous research log. Its open questions and “current” values refer to version 1.4 and are superseded where the new results above apply.

# Retained version 1.4 research log

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
