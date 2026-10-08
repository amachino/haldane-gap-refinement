"""Exact scalar certificate for gamma_L > 7/100 at every integer L >= 33.

Conditional on the pinned spatial-transfer, sector-moment, and trial inputs.
No numerical optimization is needed to run this certificate. Root proposals
are accepted only after exact powered comparisons; imported arithmetic
helpers use directed rational rounding. See paper/note.tex for the proof.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json

from verify_gap_improvement import exp_upper
from verify_adaptive_bound import (
    rounded, power, significant_upper, f, d, root_candidate,
)

TARGET = Q(7, 100)


def root_upper(value, exponent, check, name):
    candidate = root_candidate(value, exponent, True)
    check(name, candidate > 0 and power(candidate, exponent, False) >= value)
    return candidate


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled; do not run Python with -O.')
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError('Failed exact check: '+name)
        checks.append({'name': name, 'passed': True})

    # The published sector moments at beta*=49/4. Each center has absolute
    # error at most 30e-6. The raw (Z,Z_P) centers are in units of 1e-6.
    raw = [(124885379,65757),(2925,2960742),(12870614,286599),
           (54069,1920414),(4639283,510140),(195455,1514846),
           (2654823,675419),(377629,1314544),(1900547,787405)]
    eps = Q(30,10**6)
    moments = [Q(z+3*p,4*10**6) for z,p in raw]
    polynomial = [12328,32348,-499897,-339164,1787190]
    coefficients = [sum(polynomial[i]*polynomial[k-i]
                        for i in range(5) if 0 <= k-i < 5)
                    for k in range(9)]
    filter_upper = sum(c*m+abs(c)*eps for c,m in zip(coefficients,moments))
    U, V = Q('1.0013505'), Q('.872')
    for sign in (-1,1):
        shifted = [sum(comb(i,j)*a*sign**i*U**(i-j)
                       for i,a in enumerate(polynomial) if i>=j)
                   for j in range(5)]
        check(f'J filter: sign {sign} exterior monotonicity', all(x>0 for x in shifted))
        check(f'J filter: sign {sign} endpoint exclusion', U**4*shifted[0]**2 > filter_upper)
    mJ, mN = Q('1.0657205'), Q('.2783155')
    check('J twelfth moment from published centers', mJ == moments[-1]+eps)
    check('N twelfth moment from published centers', mN == Q(raw[-1][0]-raw[-1][1],4*10**6)+eps)
    check('J capped-mass domain', 0 < U**12 < mJ < 2*U**12)
    check('N capped-mass domain', 0 < V**12 < mN < 2*V**12)

    # Capped mass gives Z_m <= U^m+(mJ-U^12)^(m/12)
    # +3*(V^m+(mN-V^12)^(m/12)). Certify the two cubic roots
    # needed at m=32. At m=120 every exponent is an integer.
    tailJ32 = root_upper((mJ-U**12)**8,3,check,'Z32: J cubic-root direction')
    tailN32 = root_upper((mN-V**12)**8,3,check,'Z32: N cubic-root direction')
    Z32, Z120 = Q('1.08612266'), Q('1.175802453')
    check('Z32 upper bound', U**32+tailJ32+3*(V**32+tailN32) < Z32)
    check('Z120 upper bound', U**120+(mJ-U**12)**10+3*(V**120+(mN-V**12)**10) < Z120)

    # Improve the known positive leading eigenvalue at beta* using Z120>1.
    ell_old, ell = Q('.999'), Q('.999999998')
    A120 = (mJ-ell_old**12)**10+3*(V**120+(mN-V**12)**10)
    check('beta* leading lower bound from trial120', ell**120+A120 < 1)
    check('beta* lower-bound domains', 0 < ell_old < ell < U and ell**12 < mJ)
    residualJ32 = root_upper((mJ-ell**12)**8,3,check,'R32: J cubic-root direction')
    residual32, rho0 = Q('.04236466'), Q('.872001')
    check('beta* residual moment 32', (residualJ32+3*(V**32+tailN32))/ell**32 < residual32)
    check('beta* J residual modulus', mJ-ell**12 < V**12)
    check('beta* residual eigenvalue ratio', V < rho0*ell)

    # At 2*beta*, sum |mu_i|^32 <= Z32^2 = M and sum |mu_i|^120 >1.
    # If every |mu_i|^32 <= v=ell2^32, capped mass would give
    # 1 < Z120(2*beta*) <= ell2^120+(M-v)^(15/4) <1.
    # The fourth-power comparison below eliminates this fractional power.
    ell2, rho1, c0 = Q('.9999865'), Q('.947852'), Q('.997290')
    M, v = Z32**2, ell2**32
    check('2beta* capped-mass domain', 0 < M/2 < v < M and ell2 < 1)
    check('2beta* leading lower bound from trial120', (M-v)**15 < (1-ell2**120)**4)
    check('2beta* residual moment 32', M < v*(1+rho1**32))
    check('initial temperature ratio', 0 < c0 < 1 and c0*U**2 < ell2)
    seed_p, seed_q = Q('.07584'), Q('.059062')
    check('new spatial purity seed at n=60', 1-(1+rho1**60)**-2 < seed_p)
    check('new physical purity seed at L=120', 1-(1+(Z120-1)**2)**-2 < seed_q)
    check('all initial residual ratios below one', 0 < rho0 < 1 and 0 < rho1 < 1)
    spectral_inputs = {
        'beta_star':'49/4', 'thermal_centers_Z_ZP_in_units_1e-6':raw,
        'sector_absolute_error':str(eps), 'J_filter_quartic_coefficients':polynomial,
        'J_filter_sum_upper':str(filter_upper), 'U':str(U), 'V':str(V),
        'mJ':str(mJ), 'mN':str(mN), 'Z32_upper':str(Z32), 'Z120_upper':str(Z120),
        'lambda_beta_star_lower':str(ell), 'lambda_2beta_star_lower':str(ell2),
        'R_beta_star_32_upper':str(residual32), 'rho_beta_star_upper':str(rho0),
        'rho_2beta_star_upper':str(rho1), 'temperature_ratio_lower':str(c0),
    }
    rows = []
    p, q = seed_p, seed_q
    for j in range(8):
        n, beta = 60*2**j, Q(49, 2)*2**j
        a = 1-(1-p)**2*(1-q)
        p_next = significant_upper(f(a))
        q_next = significant_upper(f(1-(1-q)**2*(1-p_next)))
        check(f'row {j}: even reference and positive temperature', n % 2 == 0 and n >= 4 and beta > 0)
        check(f'row {j}: concentration domains', 0 < p < Q(1,2) and 0 < a < Q(1,2) and 0 < q < 1)
        check(f'row {j}: first rounded coupled update', f(a) <= p_next < 1)
        check(f'row {j}: second rounded coupled update', f(1-(1-q)**2*(1-p_next)) <= q_next < 1)
        rows.append({'j':j, 'n':n, 'beta':beta, 'p':p, 'q':q, 'a':a, 'p_next':p_next})
        p, q = p_next, q_next

    levels = []
    levels.append({'name':'initial', 'n':32, 'beta':Q(49,4), 'c':c0,
                   'tail':residual32, 'rho':rho0,
                   'next_tail':rho1**32, 'next_rho':rho1})
    # Rows 0..5 suffice for the finite range; row 7 starts the infinite tail.
    for row in rows[:-2]:
        j, n = row['j'], row['n']
        a0, a1 = d(row['p']), d(row['a'])
        g = (1-row['p_next'])*(1-row['q'])
        c = root_candidate(g, 2*n, False)
        rho0 = root_candidate(a0, n, True)
        rho1 = root_candidate(a1, n, True)
        check(f'level {j}: candidate ranges', 0 < c < 1 and 0 < rho0 < 1 and 0 < rho1 < 1)
        check(f'level {j}: lower temperature ratio', power(c,2*n,True) <= g)
        check(f'level {j}: first residual ratio', power(rho0,n,False) >= a0)
        check(f'level {j}: second residual ratio', power(rho1,n,False) >= a1)
        levels.append({'name':str(j), 'n':n, 'beta':row['beta'], 'c':c,
                       'tail':a0, 'rho':rho0, 'next_tail':a1, 'next_rho':rho1})

    thresholds = {}
    for level in levels:
        upper = exp_upper(level['beta']*TARGET)
        thresholds[level['name']] = upper/(1+upper)

    def interval_lower(level, start, end):
        if not level['n'] <= start <= end:
            raise ValueError('Invalid interpolation interval.')
        tail = rounded(level['tail']*power(level['rho'],start-level['n'],True), True)
        next_tail = rounded(level['next_tail']*power(level['next_rho'],start-level['n'],True), True)
        if next_tail >= 1:
            return Q(0)
        leading = power(level['c'],end,False)
        return rounded(leading*(1-next_tail)/(1+tail)**2, False)

    # Greedy search is only a way to find a small covering. Every chosen
    # interval and every endpoint is subsequently certified independently.
    last_finite = 3*rows[-1]['n']//2 - 1
    start, intervals = 33, []
    while start <= last_finite:
        candidates = []
        for level in levels:
            if level['n'] > start:
                continue
            threshold = thresholds[level['name']]
            if interval_lower(level,start,start) <= threshold:
                continue
            low, high = start, last_finite
            while low < high:
                mid = (low+high+1)//2
                if interval_lower(level,start,mid) > threshold:
                    low = mid
                else:
                    high = mid-1
            candidates.append((low,level))
        if not candidates:
            raise RuntimeError(f'No certified interval starts at length {start}.')
        end, level = max(candidates,key=lambda item:item[0])
        lower = interval_lower(level,start,end)
        check(f'finite interval {start}..{end}: gamma > 7/100', Q(1,2) < lower and lower > thresholds[level['name']])
        intervals.append({'first':start, 'last':end, 'level':level['name'],
                          'beta':str(level['beta']), 'purity_lower':str(lower)})
        start = end+1
    check('finite cover starts at 33', intervals[0]['first'] == 33)
    check('finite cover has no missing integer', all(a['last']+1 == b['first'] for a,b in zip(intervals,intervals[1:])))
    check('finite cover meets the infinite tail', intervals[-1]['last']+1 == 11520)

    # One extra short-length consequence; no lower moment is inferred
    # from a higher moment. The initial reference is exactly 32 here.
    length32_lower = interval_lower(levels[0],32,32)
    length32_exp = exp_upper(Q(49,4)*Q(3,50))
    check('length 32: gamma > 3/50', length32_lower > Q(1,2) and length32_exp < length32_lower/(1-length32_lower))

    # Invariant p^(3/2)<=w, q<=w. Write x=w^(1/3)<=1/100.
    # Then p_next<=3*x^4 and q_next<=3*w^2; consequently the invariant
    # propagates under w_next=6*w^2. No root evaluation is needed to check it.
    w0, C, B, xmax = Q('2e-97'), Q(6), Q(15,2), Q(1,100)
    p0, q0, beta0 = rows[-1]['p'], rows[-1]['q'], rows[-1]['beta']
    check('tail initial spatial invariant, squared', p0**3 <= w0**2)
    check('tail initial physical invariant', q0 <= w0)
    check('tail cube-root domain', 0 < w0 <= xmax**3)
    check('tail contraction', C*w0 < 1)
    acoef, qcoef = 2+xmax, 2+3*xmax
    check('tail first update coefficient', acoef**2/(2*(1-acoef*xmax**2)**2) <= 3)
    check('tail second update coefficient', qcoef**2/(2*(1-qcoef*xmax**3)**2) <= 3)
    check('tail spatial invariant propagates', 3**3 < C**2)
    check('tail physical invariant propagates', 3 <= C)
    check('tail concentration implies d(p)<=p', xmax**2 <= Q(1,3))
    check('tail concentration implies d(a)<=a', acoef*xmax**2 <= Q(1,3))
    check('tail raised residual coefficient', acoef**3 < 9)
    check('tail purity-defect coefficient', 2*(1+3*xmax)+3+2 < B)
    check('tail positive factors and purity floor', B*xmax**3 < Q(1,2))
    tail_exp = exp_upper(beta0*TARGET)
    check('tail exponential contraction', tail_exp*C*w0 < 1)
    check('tail physical odds below target exponential', tail_exp*B*w0/(1-B*w0) < 1)
    check('tail dyadic intervals cover all larger integers', rows[-1]['n'] == 7680 and beta0 == 3136 and rows[-1]['n'] % 2 == 0)

    def serialized(record):
        return {key: str(value) if isinstance(value,Q) else value for key,value in record.items()}

    result = {
        'source_commit':'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
        'statement':'Conditional on the cited upstream premises: unique ground state and gamma_L > 7/100 for every integer L >= 33, J=1',
        'odd_lengths':'Every odd L >= 33',
        'thermodynamic_statement':'liminf over all integer lengths of gamma_L >= 7/100',
        'additional_statement':'gamma_32 > 3/50; hence gamma_L > 3/50 for every integer L >= 32',
        'length32_purity_lower':str(length32_lower),
        'spectral_inputs':spectral_inputs,
        'initial_purity_seeds':{'n':60,'beta':'49/2','p':str(seed_p),'q':str(seed_q)},
        'coupled_rounding':'12 significant decimal digits, always upward, using integer arithmetic',
        'power_rounding':'Directed rational rounding to multiples of 10^-140 after each positive product',
        'root_candidates':'Decimal proposals only; directions certified by rational integer-power enclosures',
        'rows':[serialized(row) for row in rows],
        'levels':[serialized(level) for level in levels],
        'finite_intervals':intervals,
        'tail':{'start':11520,'n0':7680,'beta0':3136,'w0':str(w0),'C':str(C),'B':str(B),
                'invariant':'p^(3/2) <= w and q <= w', 'recurrence':'w_next=6*w^2',
                'interpolation_intervals':'[3*n_k/2,3*n_k]',
                'purity_bound':'T(L,beta_k) >= 1-(15/2)*w_k'},
        'all_acceptance_decisions_exact_rational':True,
        'scope':'An analytic extension with an exact scalar certificate, conditional on upstream results; not a formal proof or an independent proof of the premises',
        'checks':checks,'success':True,
    }
    output=Path(__file__).resolve().parent/'independent_results'/'spectral_refinement.json'
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS: {len(checks)} exact checks; {len(intervals)} finite intervals and one infinite tail.')
    print('gamma_L > 7/100 = 0.07, unique ground state, every integer L >= 33, J=1.')
    print('Includes every odd L >= 33; also gamma_32 > 3/50. The cited upstream premises remain dependencies.')
    print('Finite intervals:',[(r['first'],r['last'],r['level']) for r in intervals])


if __name__ == '__main__':
    main()
