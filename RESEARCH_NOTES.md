# Continuing investigation — 8 October 2026, version 1.7

## Certified results

Conditional on the pinned analytic premises and specified finite inputs, `gamma_L > 0.1515` for **every integer L >= 24**, with a unique ground state. This improves version 1.6's constant by about 4.48%, with the same length range. The exact checker performs 381 named checks, in addition to root-direction and continuum polynomial comparisons. It verifies eight exterior-ray filters, 117 moment polynomials, 39 individual main-range lengths, seven finite intervals, and the infinite tail starting at 32256.

The shorter all-integer bounds are **.063 from L=18, .119 from L=20, and .145 from L=22**; separately `gamma_18 > .088`. In particular, the length-19 bound rises from .02 to .063, and the earlier main constant .145 now holds from length 22. No monotonicity in length is assumed. All earlier proofs and results remain available below.

## Fourth twist and exact symmetry information

The new thermal input is the complete quarter-turn table, with nine lengths 4 through 12 at inverse temperature 49/4. The integer Horner evaluator uses Gaussian coordinates for the seam phases. Every total was recomputed; independent all-column Gaussian-integer calculations at lengths 4, 5, and 6 give overlapping rigorous norm intervals. The untwisted and half-turn four-site totals match the unmodified upstream packed engine exactly. The first complete table took 372.26 seconds with eight CPUs; this is an implementation timing, not a complexity guarantee.

The proper octahedral group has five real irreducible representations A, B, E, T, V. Physical rotational covariance equates the traces for coordinate-axis and edge-axis half-turns, although they are different classes inside the finite group. Their character difference gives `T_n = B_n + E_n` for every integer n >= 4. Polynomial density applied to the fourth-power-weighted finite spectral measure promotes this to equality of nonzero eigenvalue multiplicities. The four remaining spatial lists therefore have effective multiplicities 1, 4, 5, 3. These are not physical excitation degeneracies. The group, its character table, every central-projector product, and the inversion of the four traces are checked exactly. These are applications of standard finite-group and moment principles, not new general principles.

The certified supports are A in (-.5731783,1.0007981), B in (-.5319629,.4316513), E in (-.5775075,.6993004), and V in (-.8668243,.7170568). Reconstructing I=A+B, O=E, and N=B+E+V improves the old N support from (-.8710233,.7502156) to (-.8668243,.7170568). Fixed rational polynomial majorants and minorants use all the known moments. Their signs are certified on entire intervals, not just a sampled optimization grid. Signed odd moments particularly improve the short odd chains.

The retained three-sector recurrence starts from m=26, t=2, n=42, beta=49/2. Its approximate upper residuals are i=.008031531, j=.008876122, r=.037366075, and q=.009544010. A new exact contraction of the published trial matrices at length 84 certifies a negative shifted Rayleigh quotient; its energy per bond is approximately -1.401482105770093. A direct four-site wavefunction checks the convention. The complete 84-site contraction was recomputed, and the existing 120-site trial is reused. No new full upstream verification run is claimed.

After nine updates, the tail uses reference length 21504, inverse temperature 12544, and the exact rational `w=1.70982022810726e-827`. The outward grid remains 1e-1000, with root proposal margin 1e-450; exact powered comparisons accept every root direction. The invariant and tight finite-length purity conversion are unchanged from version 1.6.

## Exploratory calculations and directions that did not help

All values in this subsection are **non-rigorous diagnostics**, not certified gaps, global optima, upper bounds on the physical gap, or barriers to other arguments.

At base inverse temperature 12.25, four-sector capped moments with the retained recurrence gave a decay diagnostic near .14929383839. Sampled polynomial optimization raised the screen to about .15172248662, with m=26, t=2, n=42. Replacing the sampled candidates by outward-rounded exact input enclosures and continuum-verified polynomials supports the published **.1515** certificate. The extra digits of the exploratory rate are not theorem values.

A separate recurrence retaining more octahedral projection caps gave a diagnostic near .15172294523. This is no material further gain in the screened parameters. The comparison also used slightly different sampling grids, so the tiny difference must not be attributed solely to the recurrence. `explore_octahedral_flow.py` is not used in any acceptance check.

A coarse four-twist screen without polynomial optimization gave:

| Base inverse temperature | Capped-moment decay diagnostic |
|---|---:|
| 11.5 | .14137300 |
| 12.0 | .14724686 |
| 12.25 | .14929384 |
| 12.5 | .15072695 |
| 13.0 | .15209631 |

The low-spectrum trace estimates in this screen are not rigorous enclosures. Temperature 13 is a useful next candidate, but would need a new certified table for all four boundary rotations. The screen establishes neither a certified gain nor an optimal temperature. `explore_quarter_inputs.py`, `explore_quarter_parameters.py`, and `explore_quarter_polynomials.py` expose the optional numerical exploration. Fixed accepted rational coefficients are distributed separately.

A purity-only shortcut was also examined. For a two-level probability list with p=(1+sqrt(1-2u))/2 and 1-p, the purity defect is u, and squaring and normalizing gives exactly `u^2 / (2*(1-u)^2)`. Thus the original pure-purity squaring inequality is saturated for every 0 <= u <= 1/2. A universally stronger update requires information beyond that one purity number. This elementary identity is not a novelty claim and does not rule out model-specific improvements.

The new certified lower purity estimates for lengths 18 through 23 are approximately .62266, .56886, .69639, .69456, .75429, and .75877. The length-19 estimate now lies comfortably above one half. The final statements use the rounded strict gap constants above, not floating-point logarithms of these displays.

## Remaining questions and scope

The most concrete next step is to assess a complete colder four-twist table, possibly at beta=13, using the same exact methodology. Moments beyond order 12 may be more valuable, but the present full-column algorithm becomes much more expensive with length; a favorable diagnostic or a more efficient certified evaluator should precede that investment. Stronger information about excitation weights could also improve the physical update. Neither the existing scans nor the saturated one-number inequality rules these routes out.

The finite group and thermal-engine cross-checks, the complete quarter-turn recomputation, the 84-site recomputation, and all retained scalar certificates pass. The analytic arguments were developed and internally reviewed by the same autonomous agent. Independent mathematical review remains outstanding. The limited public-source follow-up did not identify an independent report of this precise quarter-turn refinement; it is not an exhaustive priority search. This release makes no claim of global optimality, priority, or an independent replacement for the upstream Haldane-gap proof.

---

The following version 1.6 log is retained as a historical record. Its current bounds and unresolved directions are superseded where the version 1.7 results above apply.

# Continuing investigation — 8 October 2026, version 1.6

## Certified results

Conditional on the pinned analytic premises and specified finite inputs, `gamma_L > 0.145` for **every integer L >= 24**, with a unique ground state. The main checker has 304 named exact checks, 67 full-interval polynomial certificates, 42 individual main-range lengths, six finite intervals, and an infinite tail beginning at 33792. The shorter bounds are .02 from L=18, .09 from L=20, and .12 from L=22; separately gamma_18 > .08. Length 19 is now covered. The earlier .108 result and all older derivations remain intact.

## What changed

The new cyclic-twist table covers every length 4 through 12 at beta=49/4. Separating I and O lowers the bound on the dominant I eigenvalue from the earlier J-based cap 1.0013391 to 1.0008406. The other full supports are I > -.59564, O in (-.577508,.699301), and N in (-.8710233,.7502156). The three-twist initialization uses m=28, n=44, and beta=2009/80. Its bounds are approximately i=.01139428, j=.01252915, r=.03797597, and q=.01028467. The physical defect is about half the preceding seed's .02030009. These displays are not the acceptance values; exact fractions are in the certificate.

A separate five-site open-chain calculation proves H_open,5 > -35/6 using positive integer principal minors. Summing translated local inequalities gives H_L(g) >= -35 L/24 for every L>=5 and all three boundary twists. This improves the Horner contraction modulus to 1-L/384 for the thermal lengths. Rounding errors can then be summed geometrically and separately by magnetization block, including for the existing two-twist totals. In Eisenstein coordinates both floor errors are in [-1,0], where a^2-a*b+b^2 <= 1, so a cyclic vector floor also costs at most sqrt(d). At length 12, the new cyclic half-width is about 4.17e-7 and the resolved I half-width about 4.19e-7.

The tight elementary conversion from purity K>1/2 uses K > (1+E^2)/(1+E)^2 with E >= exp(beta*delta). It requires no assumption about the first excitation's spin or multiplicity. This improves finite-length coverage, not the limiting exponential rate. The certified length-19 purity exceeds .50776; the earlier failure to cross one half was an input limitation.

The ninth recurrence update reaches q of order 10^-811. The new checker therefore uses a 10^-1000 outward grid and 10^-450 root proposal margin. Every root direction is still accepted by exact powered comparisons. A coarser root margin caused a failed finite cover during development; increasing arithmetic resolution resolved that failure without changing an inequality or relaxing acceptance. Earlier checkers retain their defaults.

## Temperature exploration and unsuccessful directions

The initial plan was to obtain colder data. A non-rigorous low-spectrum calculation screened temperatures using moments of orders 4 through 12. Eigenvalues and the omitted-state trace estimates in that screen are numerical diagnostics, not rigorous enclosures.

| Base inverse temperature | Two-sector, capped-moment diagnostic | Three-sector, capped-moment diagnostic |
|---|---:|---:|
| 10.5 | .10035 | not screened in that run |
| 12.25 | .10416 | .14220 |
| 13 | .09581 | not screened in that run |
| 14 | .07841 | .13633 |
| 15 | .05737 | not screened in that run |
| 16 | .03384 | .10574 |
| 18 and 20 | no usable seed in the scanned grid | not screened in that run |

Adding sampled moment optimization to the three-sector screen at 12.25 gave about .145204. The final rigorous inputs have a recurrence decay diagnostic near .145180; only **.145 with the full length cover** is the theorem. These are local/grid searches, not global optima or bounds on what colder data, higher moment orders, or other proofs could achieve.

`explore_thermal_inputs.py --refresh` reconstructs the optional low-spectrum cache. `explore_thermal_parameters.py --two-sectors 12.25` and `explore_thermal_parameters.py --lp 12.25` expose the two-sector and three-sector screens. `explore_resolved_polynomials.py` proposes additional sampled polynomial duals from the certified moment intervals. No optimizer is called by a gap checker.

The original sensitivity experiment artificially scaled seed bounds; its apparent .2 or .28 rates were counterfactual diagnostics. The actual new finite calculations certify .145. Simply extending the old recurrence or lowering the temperature at the same moment orders did not provide this gain. The complete symmetry information and tighter finite-length conversion did.

## Verification and remaining questions

All nine new thermal totals were recomputed from the C++ source. Independent small even cases matched the unmodified upstream packed engine exactly with the same coefficients. The five-site all-column integer check avoids orbit reduction and its rigorous norm intervals overlap. `recompute_extended_cyclic.py` reproduces those checks and the complete table; `--quick` selects the small cases. No new full upstream computation is claimed. The existing 88- and 120-site variational inputs are reused.

Further substantial progress could come from new moment orders beyond 12, additional rigorously controlled low-temperature information, or a sharper physical-purity update that retains more excitation information. The screened rate near .14518 is not a method barrier. Reaching the expected physical gap would require stronger uniform control over excitation weights and length dependence. Independent mathematical review remains outstanding. No priority or optimality claim is made for the new quantitative result or the elementary tools used here.

---

The following log is retained from version 1.5. Its current values and open questions are historical; the length-19 gap and incomplete cyclic table are resolved above.

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
