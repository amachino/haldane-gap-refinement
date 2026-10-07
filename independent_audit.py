"""Independent reconstruction of selected Haldane-paper computations.

Source: OpenAI, The periodic spin-one Haldane gap (2026-09-24),
commit adc7f1241b42e322a6451854ab7e4b4c146bf78a.
No functions from the supplied verification implementation are imported.
Floating diagonalization is a diagnostic; rational and integer checks are exact.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
import json
from math import comb
from pathlib import Path
import time

import numpy as np
from scipy.linalg import eigvalsh

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "independent_results"
RESULTS.mkdir(exist_ok=True)


def save(name, data):
    (RESULTS / name).write_text(json.dumps(data, indent=2) + "\n")


def rounded_up(x, digits):
    scale = 10**digits
    z = x * scale
    return F(-(-z.numerator // z.denominator), scale)


def squaring_bound(u):
    assert 0 <= u < 1
    return u*u/(2*(1-u)**2)


def coupled_step(p, q):
    # Evaluate cancellation-free versions of 1 - (1-p)^2 (1-q).
    d = 2*p - p*p + q*(1-p)**2
    p_next = squaring_bound(d)
    e = 2*q - q*q + p_next*(1-q)**2
    return p_next, squaring_bound(e)


def envelope_coefficient(u):
    return sum((1-u)**(-k) for k in (1, 2, 3))**2 / 2


def gap_decimal(u, C, beta):
    with localcontext() as context:
        context.prec = 75
        r = C*u
        rd = Decimal(r.numerator)/Decimal(r.denominator)
        return str(-rd.ln()/Decimal(beta))


def rational_exp_upper(x):
    """Rigorous upper bound on exp(x), x >= 0, by Taylor plus geometric tail."""
    assert x >= 0
    order = 4*(x.numerator//x.denominator)+64
    term=total=F(1)
    for k in range(1,order+1):
        term*=x/k
        total+=term
    first_omitted=term*x/(order+1)
    ratio=x/(order+2)
    assert 0<=ratio<1
    return total+first_omitted/(1-ratio)


def scalar_audit():
    # Build the degree-12 filter certificates from the printed thermal table.
    table = [(124885379,65757),(2925,2960742),(12870614,286599),
             (54069,1920414),(4639283,510140),(195455,1514846),
             (2654823,675419),(377629,1314544),(1900547,787405)]
    moment = {
        'J': {n:F(z+3*t,4*10**6) for n,(z,t) in enumerate(table,4)},
        'N': {n:F(z-t,4*10**6) for n,(z,t) in enumerate(table,4)},
    }
    eps=F(30,10**6)
    caps={'J':F(100139,100000),'N':F(872,1000)}
    rows=[]
    for sector, poly in [('J',[7,17,-280,-185,1000]),('N',[12,0,-394,0,1000])]:
        coefficients=defaultdict(int)
        for i,c in enumerate(poly):
            for j,d in enumerate(poly):
                coefficients[i+j+4] += c*d
        upper=sum(c*moment[sector][k]+abs(c)*eps for k,c in coefficients.items())
        for sign in (-1,1):
            # Every coefficient of F(sign*(cap+y))-upper is nonnegative,
            # with a strictly positive constant: a rigorous exterior bound.
            expansion=[sum(c*sign**k*comb(k,j)*caps[sector]**(k-j)
                           for k,c in coefficients.items() if k>=j)
                       for j in range(13)]
            assert expansion[0]>upper and all(x>=0 for x in expansion[1:])
            rows.append({'sector':sector,'sign':sign,'margin':str(expansion[0]-upper),
                         'margin_float':float(expansion[0]-upper)})
    masses={s:moment[s][12]+eps for s in moment}
    lo=F(999,1000)

    def capped(mass, cap, power):
        count=mass//cap
        return count*cap**power+(mass-count*cap)**power

    def nontrivial(k):
        return 3*capped(masses['N'],caps['N']**12,k//12)

    assert capped(masses['J'],lo**12,6)+nontrivial(72)<1

    def remainder(k):
        return nontrivial(k)+(masses['J']-lo**12)**(k//12)

    p=1-(1+remainder(36)/lo**36)**(-2)
    q=1-(caps['J']**72+remainder(72))**(-2)
    initial={'p':str(p),'q':str(q),'p_float':float(p),'q_float':float(q)}
    # Reproduce the manuscript's upward rounding: p is rounded before q.
    expected=[(151249,2500000,433453,2500000),
              (343303,5000000,1632381,10000000),
              (44601,625000,361773,2500000),
              (632939,10000000,1055161,10000000),
              (375793,10000000,445941,10000000),
              (84513,10000000,27493,5000000)]
    iterations=[]
    for j,(pn,pd,qn,qd) in enumerate(expected,1):
        p=rounded_up(squaring_bound(2*p-p*p+q*(1-p)**2),7)
        q=rounded_up(squaring_bound(2*q-q*q+p*(1-q)**2),7)
        assert (p,q)==(F(pn,pd),F(qn,qd))
        iterations.append({'j':j,'p':str(p),'q':str(q)})

    # An independently derived improvement using additional certified steps.
    # Round upward on an increasingly fine *absolute* grid to keep integers small.
    improvements=[]
    for k in range(7):
        u=max(p,q);C=F(5);beta=784*2**k
        assert 0<u<F(1,6) and envelope_coefficient(u)<C
        assert C*u<1 and C*(1-3*u)>3
        improvements.append({'extra_steps':k,'minimum_even_length':2304*2**k,
                             'beta':beta,'p':str(p),'q':str(q),'u':str(u),
                             'C':str(C),'gap_bound_decimal':gap_decimal(u,C,beta)})
        if k<6:
            digits=20*2**k
            p=rounded_up(squaring_bound(2*p-p*p+q*(1-p)**2),digits)
            q=rounded_up(squaring_bound(2*q-q*q+p*(1-q)**2),digits)

    # A short, readable certificate for Delta >= log(10000/13)/1568.
    p=F(84513,10**7);q=F(27493,5*10**6)
    p1,q1=coupled_step(p,q)
    assert p1<F(26,100000) and q1<F(65,1000000)
    # Avoid huge constants in the main result: one extra iteration gives u=0.00026.
    u=F(26,100000)
    assert envelope_coefficient(u)<5 and 5*(1-3*u)>3
    simple={'minimum_even_length':4608,'beta':1568,'u':str(u),'r':str(5*u),
            'exact_bound':'log(10000/13)/1568',
            'decimal':gap_decimal(u,F(5),1568)}

    # Cover the initial dyadic intervals explicitly, then apply Proposition 4.3.
    # This upgrades the bound to 0.0047 for *all* even L >= 2304, not merely
    # for the larger n at which the improved envelope starts.
    target=F(47,10000)
    intervals=[]
    for k,row in enumerate(improvements[:5]):
        pp,qq=F(row['p']),F(row['q'])
        K=(1-pp)**2*(1-qq)
        assert K>F(1,2)
        exp_hi=rational_exp_upper(target*row['beta'])
        odds=K/(1-K)
        assert exp_hi<odds
        intervals.append({'minimum_length':row['minimum_even_length'],
                          'maximum_length':2*row['minimum_even_length'],
                          'beta':row['beta'],'purity_lower':str(K),
                          'exp_upper_less_than_purity_odds':True,
                          'relative_margin':float(odds/exp_hi-1)})
    last=improvements[5]
    exp_hi=rational_exp_upper(target*last['beta'])
    reciprocal=1/(5*F(last['u']))
    assert exp_hi<reciprocal
    uniform={'target':str(target),'minimum_even_length':2304,
             'finite_intervals':intervals,
             'tail_starts_at_even_length':last['minimum_even_length'],
             'tail_beta':last['beta'],'tail_C':5,'tail_u':last['u'],
             'tail_relative_margin':float(reciprocal/exp_hi-1),
             'all_comparisons_exact_rational':True}
    save('scalar_audit.json',{'filter_margins':rows,'initial':initial,
                            'manuscript_rounds':iterations,'improvements':improvements,
                            'simple_improvement':simple,
                            'uniform_improvement':uniform,'success':True})
    print('PASS independent exact scalar reconstruction and additional iterations',flush=True)
    print('PASS gap > 47/10000 for all even L >= 2304, conditional on paper input lemmas',flush=True)
    for row in improvements:
        print('extension',row['extra_steps'],row['minimum_even_length'],row['gap_bound_decimal'][:22],flush=True)


def trial_matrices():
    ells=[1,1,1,1,3,3,3,5]
    diagonals=[-289,-84,-9,33,-22,27,71,-11]
    pair_values={(1,5):-11,(1,6):-35,(1,7):-28,(2,5):-23,(2,6):16,
                 (2,7):-49,(3,5):-6,(3,6):-25,(3,7):-20,(4,5):-34,
                 (4,6):9,(4,7):-32,(5,8):1,(6,8):2,(7,8):-16}
    labels=[(a,d) for a,l in enumerate(ells,1) for d in range(-l,l+1,2)]
    matrices={s:np.zeros((26,26),dtype=object) for s in (-1,0,1)}
    for i,(a,d) in enumerate(labels):
        l=ells[a-1];r=(d+l)//2
        for j,(b,e) in enumerate(labels):
            k=ells[b-1]
            for s in matrices:
                if e!=d+2*s or abs(k-l)>2 or (k==l and a!=b):continue
                if k>l:
                    p=pair_values[a,b]
                    factors={-1:2*(l+1-r)*(l+2-r),0:2*(r+1)*(l-r+1),1:(r+1)*(r+2)}
                elif k==l:
                    p=diagonals[a-1]
                    factors={-1:2*(l-r+1),0:d,1:-(r+1)}
                else:
                    p=-pair_values[b,a]
                    factors={-1:2,0:-2,1:1}
                matrices[s][i,j]=p*factors[s]
    return labels,matrices


def physical_block(n, magnetization, theta=0.0):
    words=[w for w in product((-1,0,1),repeat=n) if sum(w)==magnetization]
    lookup={w:i for i,w in enumerate(words)}
    complex_case=abs(theta)>1e-14 and abs(theta-np.pi)>1e-14
    H=np.zeros((len(words),len(words)),dtype=complex if complex_case else float)
    for col,w in enumerate(words):
        H[col,col]=sum(w[j]*w[(j+1)%n] for j in range(n))
        for j in range(n):
            k=(j+1)%n
            for step in (-1,1):
                if not (-1<=w[j]+step<=1 and -1<=w[k]-step<=1):continue
                v=list(w);v[j]+=step;v[k]-=step
                phase=np.exp(1j*theta*step) if k==0 else 1.0
                H[lookup[tuple(v)],col]+=phase if complex_case else float(np.real(phase))
    assert np.max(abs(H-H.conj().T))<1e-12
    return words,H


def exact_trial_audit():
    started=time.perf_counter()
    labels,A=trial_matrices()
    B={(s,t):A[s]@A[t] for s,t in product((-1,0,1),repeat=2)}
    T=sum(np.kron(m,m) for m in A.values())
    physical_pairs=list(product((-1,0,1),repeat=2))
    h=np.zeros((9,9),dtype=int)
    for j,(s,t) in enumerate(physical_pairs):
        h[j,j]=s*t
        for step in (-1,1):
            if -1<=s+step<=1 and -1<=t-step<=1:
                h[physical_pairs.index((s+step,t-step)),j]=1
    O=sum(int(h[i,j])*np.kron(B[x],B[y])
          for i,x in enumerate(physical_pairs) for j,y in enumerate(physical_pairs) if h[i,j])
    diffs=np.array([d-e for a,d in labels for b,e in labels])
    assert all(T[i,j]==0 and O[i,j]==0 for i,j in zip(*np.where(diffs[:,None]!=diffs[None,:])))
    totals={n:[0,0] for n in (4,72,120)}
    dimensions=[]
    for diff in sorted(set(diffs)):
        idx=np.flatnonzero(diffs==diff)
        x=T[np.ix_(idx,idx)];o=O[np.ix_(idx,idx)]
        dimensions.append(len(idx))
        for n in totals:
            # NumPy's binary exponentiation is independent of the supplied runner.
            norm=int(np.trace(np.linalg.matrix_power(x,n)))
            t=np.linalg.matrix_power(x,n-2)
            energy=sum(int(t[i,j])*int(o[j,i]) for i in range(len(idx)) for j in range(len(idx)))
            totals[n][0]+=energy;totals[n][1]+=norm
        print('independent MPS block',int(diff),len(idx),'completed',flush=True)
    assert dimensions==[1,8,32,80,136,162,136,80,32,8,1]
    # Direct four-site wavefunction cross-check, no transfer-contraction formula.
    words,H=physical_block(4,0)
    psi=np.array([int(np.trace(A[w[0]]@A[w[1]]@A[w[2]]@A[w[3]])) for w in words],dtype=object)
    physical_norm=sum(v*v for v in psi)
    physical_energy=sum(psi[i]*int(H[i,j])*psi[j] for i in range(len(words)) for j in range(len(words)))
    assert physical_norm==totals[4][1] and physical_energy==4*totals[4][0]
    records=[]
    for n,(U,V) in totals.items():
        if n>4:
            assert V>0 and 500000*U+700741*V<0
            record=json.loads((ROOT/f'source/verification/computations/evidence/trials/certificate{n}.json').read_text())
            expected_U=int(next(record[k] for k in ['num','one_bond_energy_numerator','U'] if k in record))
            expected_V=int(next(record[k] for k in ['norm','V'] if k in record))
            assert (U,V)==(expected_U,expected_V)
        records.append({'length':n,'U':str(U),'V':str(V),'energy_per_bond':float(F(U,V)),
                        'floor_1e12':10**12*U//V})
    save('trial_audit.json',{'success':True,'records':records,'block_dimensions':dimensions,
                           'four_site_direct_check':True,'seconds':time.perf_counter()-started})
    print('PASS independent integer MPS reconstruction for 72 and 120 sites',flush=True)


def thermal_diagnostic():
    # Full-spectrum diagonalization in magnetization blocks through n=8.
    # All +/-M sectors are explicitly included, unlike the supplied orbit reductions.
    started=time.perf_counter();records=[]
    table1={4:[124885379,65757],5:[2925,2960742],6:[12870614,286599],
            7:[54069,1920414],8:[4639283,510140]}
    table2={6:[8945303,346734,939987],8:[3741281,567167,984108]}
    for n in range(4,9):
        for g,theta in enumerate((0,np.pi,2*np.pi/3)):
            if g==2 and n not in table2:continue
            eigenvalues=[]
            for m in range(-n,n+1):
                _,H=physical_block(n,m,theta)
                eigenvalues.extend(eigvalsh(H,check_finite=False,driver='evr'))
            eigenvalues=np.sort(eigenvalues)
            assert len(eigenvalues)==3**n
            for beta,table,eps in [(12.25,table1,3e-5),(10.5,table2,1e-5)]:
                if n not in table or g>=len(table[n]):continue
                trace=float(np.exp(-beta*(eigenvalues+float(F(700741,500000))*n)).sum())
                center=table[n][g]/1e6
                assert abs(trace-center)<eps
                row={'n':n,'twist':g,'beta':beta,'trace':trace,'center':center,
                     'difference':trace-center,'paper_tolerance':eps,'status':'floating diagnostic'}
                records.append(row)
                print('independent thermal',n,g,beta,trace,flush=True)
    save('thermal_diagnostic.json',{'success':True,'records':records,'seconds':time.perf_counter()-started})


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Assertions must be enabled; do not run Python with -O.')
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['scalars','trial','thermal'])
    args=parser.parse_args()
    {'scalars':scalar_audit,'trial':exact_trial_audit,'thermal':thermal_diagnostic}[args.mode]()
