"""Exact certificate for gamma_L > 3/50 at every integer length L >= 34.

Conditional on the pinned OpenAI spatial-transfer and periodic spectral
inputs, as detailed in paper/note.tex. All acceptance decisions use exact
rational arithmetic. Decimal roots only propose rational candidates; their
directions are certified by integer powers. Positive products are rounded
outward on a 10**-140 grid to keep the finite certificate small.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
import json

from verify_gap_improvement import exp_upper


GRID = 10**140
TARGET = Q(3, 50)


def rounded(value, upper):
    """Directed rounding of a nonnegative rational to multiples of 1/GRID."""
    if value < 0:
        raise ValueError('Expected a nonnegative rational.')
    numerator = value.numerator * GRID
    integer, remainder = divmod(numerator, value.denominator)
    return Q(integer + int(upper and remainder != 0), GRID)


def power(value, exponent, upper):
    """Rational lower/upper enclosure of a nonnegative integer power."""
    if not isinstance(exponent, int) or exponent < 0:
        raise ValueError('Expected a nonnegative integer exponent.')
    result, base = Q(1), rounded(value, upper)
    while exponent:
        if exponent & 1:
            result = rounded(result * base, upper)
        exponent //= 2
        if exponent:
            base = rounded(base * base, upper)
    return result


def significant_upper(value, digits=12):
    """Round a positive rational up to a short decimal, using integers only."""
    if value <= 0:
        raise ValueError('Expected a positive rational.')
    exponent = len(str(value.numerator)) - len(str(value.denominator))
    ten = Q(10)**exponent
    if value < ten:
        exponent -= 1
    unit = Q(10)**(exponent-digits+1)
    ratio = value / unit
    ceiling = -(-ratio.numerator // ratio.denominator)
    return ceiling * unit


def f(value):
    if not 0 <= value < 1:
        raise ValueError('Purity defect outside [0, 1).')
    return value**2 / (2*(1-value)**2)


def d(value):
    if not 0 <= value < Q(1, 2):
        raise ValueError('Concentration requires a defect below one half.')
    return value / (2-3*value)


def root_candidate(value, exponent, upper):
    """Propose a root enclosure; the caller must certify its direction."""
    with localcontext() as context:
        context.prec = 180
        dec = Decimal(value.numerator)/Decimal(value.denominator)
        root = (dec.ln()/exponent).exp()
        center = Q(int(root*GRID), GRID)
    # Leave room for absolute rounding errors after powers of tiny moments.
    # This is merely a candidate: exact powered comparisons below are required.
    margin = Q(1, 10**100)
    return center + (margin if upper else -margin)


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled; do not run Python with -O.')
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError('Failed exact check: '+name)
        checks.append({'name': name, 'passed': True})

    # The companion proof gives S(60,49/2)>.9002, T(120,49/2)>.9372.
    # Its other finite comparisons are independently rerun by make check.
    rows = []
    p, q = Q('.0998'), Q('.0628')
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
    c0 = Q('.9967754')
    check('initial leading-eigenvalue ratio', 0 < c0 < 1 and (c0*Q('1.00139')**2)**72 < Q('.968'))
    levels.append({'name':'initial', 'n':32, 'beta':Q(49,4), 'c':c0,
                   'tail':Q('.0442'), 'rho':Q('.874'),
                   'next_tail':Q('.9525')**32, 'next_rho':Q('.9525')})
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
    start, intervals = 34, []
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
        check(f'finite interval {start}..{end}: gamma > 3/50', Q(1,2) < lower and lower > thresholds[level['name']])
        intervals.append({'first':start, 'last':end, 'level':level['name'],
                          'beta':str(level['beta']), 'purity_lower':str(lower)})
        start = end+1
    check('finite cover starts at 34', intervals[0]['first'] == 34)
    check('finite cover has no missing integer', all(a['last']+1 == b['first'] for a,b in zip(intervals,intervals[1:])))
    check('finite cover meets the infinite tail', intervals[-1]['last']+1 == 11520)

    # Invariant p^(3/2)<=w, q<=w. Write x=w^(1/3)<=1/100.
    # Then p_next<=3*x^4 and q_next<=3*w^2; consequently the invariant
    # propagates under w_next=6*w^2. No root evaluation is needed to check it.
    w0, C, B, xmax = Q('2e-83'), Q(6), Q(15,2), Q(1,100)
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
        'statement':'Conditional on the cited upstream premises: unique ground state and gamma_L > 3/50 for every integer L >= 34, J=1',
        'odd_lengths':'Every odd L >= 35',
        'thermodynamic_statement':'liminf over all integer lengths of gamma_L >= 3/50',
        'initial_purity_seeds':{'n':60,'beta':'49/2','p':'.0998','q':'.0628'},
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
    output=Path(__file__).resolve().parent/'independent_results'/'adaptive_bound.json'
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS: {len(checks)} exact checks; {len(intervals)} finite intervals and one infinite tail.')
    print('gamma_L > 3/50 = 0.06, unique ground state, every integer L >= 34, J=1.')
    print('Includes every odd L >= 35; cited analytic and finite-input premises remain dependencies.')
    print('Finite intervals:',[(r['first'],r['last'],r['level']) for r in intervals])


if __name__ == '__main__':
    main()
