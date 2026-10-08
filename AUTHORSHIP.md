# Autonomous authorship and contributions

**Author: GPT-6 Astra Max (OpenAI), operating autonomously through Codex.**

The work was autonomously carried out by the agent within an open-ended research task initiated by a human user. The agent's role extended from choosing the result to investigate through deriving the refinement, writing and running its verification code, and authoring the paper.

| Contribution | Performed by |
|---|---|
| Initiating the open-ended investigation | Human user |
| Selecting the Haldane-gap result for investigation | GPT-6 Astra Max |
| Reading and examining the original analytic argument | GPT-6 Astra Max |
| Deriving the 0.0047 refinement and its finite-interval/tail proof | GPT-6 Astra Max |
| Identifying the stronger corollary from the two published papers and checking its hypotheses | GPT-6 Astra Max |
| Correcting the comparison and implementing the companion-corollary certificate | GPT-6 Astra Max |
| Deriving the signed-moment extension to all integer lengths at least 120, including its same-reference-length tail bounds | GPT-6 Astra Max |
| Implementing the polynomial certificate and authoring version 1.2 | GPT-6 Astra Max |
| Deriving length-dependent temperature interpolation and the asymmetric infinite-tail invariant | GPT-6 Astra Max |
| Certifying 0.06 for all integer lengths at least 34 and authoring version 1.3 | GPT-6 Astra Max |
| Selecting the tighter polynomial filter, sharpening spectral bounds and seeds, and certifying 0.07 for all integer lengths at least 33 in version 1.4 | GPT-6 Astra Max |
| Implementing the new rational certificate and separate audit computations | GPT-6 Astra Max |
| Executing the upstream verifier and the new computations | GPT-6 Astra Max |
| Writing the manuscript and repository documentation | GPT-6 Astra Max |
| Authorizing publication | Human user |
| Requesting attribution and title-layout revisions | Human user |
| Requesting the prior-art review and authorizing version 1.1 | Human user |
| Asking whether odd lengths can be proved and requesting incorporation of newly verified findings | Human user |
| Requesting continued research into further extensions and refinements | Human user |
| Original spatial-transfer construction, periodic reseeding, gap criterion, and finite input certificates | OpenAI, as credited in the two upstream papers |

The human user did not supply the mathematical extension or the verification code. The mathematical result was developed after the agent had access to the original paper; this is not an independent discovery of the original Haldane-gap argument.

In version 1.1, the stronger value is an explicit corollary of two existing OpenAI propositions. The agent is credited for recognizing and verifying that combination, not for originating the upstream reseeding or gap criterion. The initial comparison's omission is documented in PRIOR_ART.md.

Version 1.2 adds a signed-moment interpolation proof for every integer length at least 120. The agent derived the concentration and tail argument using the same even reference length at both temperatures, and supplied an exact polynomial certificate. The signed trace formula, positive dominant eigenvalues, dyadic purity estimates, and adjacent-temperature eigenvalue ratios are existing OpenAI results. This contribution remains conditional on those premises. No exhaustive priority search or independent external review of the parity extension is claimed.

Version 1.3 adds the length-adaptive interpolation and the invariant `p^(3/2) <= w`, `q <= w`, together with a certificate covering 12 finite intervals and an infinite tail. The agent developed the argument, implemented and executed its 88 exact checks, and wrote the revision. The finite inputs and original coupled update remain credited to OpenAI. The human asked that research continue and verified findings be incorporated. The diagnostic decay-rate exploration is explicitly distinguished from a proved bound or an optimality claim.

Version 1.4 uses the same finite thermal and trial data with new filter coefficients and tighter moment comparisons. The agent selected the coefficients, derived the sharper dominant-eigenvalue bounds and purity seeds, implemented and ran 111 exact checks, and wrote the revision. The polynomial-filter and capped-mass principles themselves are OpenAI's existing methods. The result is a further conditional refinement, with no claim of a novel general moment principle or priority. No new large thermal or variational calculation was performed.

## Identity record

- Model designation: **GPT-6 Astra Max (OpenAI)**, supplied by the human user.
- Execution agent identity: **Codex**.
- Backend model snapshot identifier: **not exposed in the execution context**.
- The model designation records the user-provided identity; it is not presented as a runtime metadata measurement.
- Dates of the recorded investigation and revisions: **7-8 October 2026** (versions 1.1 through 1.4 are dated in Asia/Tokyo).

The author designation identifies the agent that produced the new work. It does not imply an official OpenAI publication, endorsement, or human scientific authorship by the owner of the publishing account. The technical note is unreviewed; no independent human expert review has been recorded.
