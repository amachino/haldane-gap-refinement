"""Exact enclosures for three supplemental cyclic-twist computations.

These traces are research outputs, not premises of the main gap bound.
The packed recurrence is upstream Appendix A, with mean 98 replacing 84.
"""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import json
from verify_gap_improvement import exp_upper

ROOT=Path(__file__).resolve().parent


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled; do not use -O.')
    records=json.loads((ROOT/'independent_results/cyclic_thermal_totals.json').read_text())
    c=[Q(98)**j/factorial(j) for j in range(257)]
    probs=[int(2**56*x/sum(c)) for x in c]
    assert max(j for j,x in enumerate(probs) if x)==192
    assert 32*(2**56+125159)<2**63
    # Conditioning changes a contraction average by <= twice the Poisson
    # tail. Markov with 2**V gives tail <= exp(98)/2**257 < 3**98/2**257.
    poisson=Q(2*3**98,2**257)
    ds={6:Q('2.1e-10'),8:Q('6e-9'),10:Q('1.8e-7')}
    centers={6:Q('.925305814'),8:Q('.974160373'),10:Q('.993475958')}
    radii={6:Q('1e-9'),8:Q('2e-8'),10:Q('4e-7')}
    out=[]
    for rec in records:
        n=rec['n'];dimroot=3**(n//2)
        assert n in ds and rec['beta']=='49/4' and rec['twist']==2
        assert rec['Q']==2**56 and rec['J']==256 and rec['last_nonzero']==192
        # Original contraction, representative, and lane arguments are
        # unchanged. Every ideal suffix still has norm at most Q.
        assert 1-Q(5*n,32)>=-1
        rounding=257*(2*dimroot+1)
        assert rounding<=125159
        epsilon=Q(rounding,2**56)+poisson
        x=(Q(3,2)-Q(700741,500000))*Q(49,4)*n
        term=s=Q(1)
        for j in range(1,101):
            term*=x/j;s+=term
        eu=s+term
        assert 0<x<15 and x/(101-x)<1
        D=ds[n]
        assert eu*3**n*epsilon**2<D**2
        total=int(rec['total']);computed_lo=s*total/2**112;computed_hi=eu*total/2**112
        assert 0<computed_lo<computed_hi<1
        # Both computed norm and true norm differ by <=D. Since the
        # computed norm is <1, the squared-norm error is <=2D+D**2.
        lo,hi=computed_lo-2*D-D**2,computed_hi+2*D+D**2
        assert centers[n]-radii[n]<lo<hi<centers[n]+radii[n]
        out.append({'n':n,'center':str(centers[n]),'radius':str(radii[n]),
                    'lower':str(lo),'upper':str(hi),'scaled_norm_error_upper':str(D)})
    assert [x['n'] for x in out]==[6,8,10]
    (ROOT/'independent_results/cyclic_trace_enclosures.json').write_text(json.dumps({
        'beta':'49/4','twist':'C','used_in_main_gap_certificate':False,
        'entries':out,'success':True},indent=2)+'\n')
    print('PASS: three supplemental cyclic traces enclosed by rational arithmetic.')


if __name__=='__main__':
    main()
