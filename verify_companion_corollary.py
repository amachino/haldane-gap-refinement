"""Exact scalar certificate for the corollary log(125/39)/49, even L >= 120.

Dependencies at OpenAI Math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a:
  The periodic spin-one Haldane gap: Propositions 3.1, 4.3, Corollary 5.6.
  A boundary-field gap for the spin-one Heisenberg chain: Proposition 3.4.

The latter proposition concerns PERIODIC partition functions in this step.
This checks its reseeding arithmetic and the former paper's gap criterion.
It does not independently establish the analytic or finite-input premises.
The exponential bound is the rational Taylor bound used by the v1.0 checker.
Only Python's standard library is required. Decimal values are display-only.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as Q
import json
from pathlib import Path

from verify_gap_improvement import exp_upper


def f(u):
    if not 0 <= u < 1:
        raise ValueError("Purity defect outside [0, 1).")
    return u * u / (2 * (1 - u) ** 2)


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled; do not run Python with -O.")
    checks = []

    def less(name, left, right):
        if not left < right:
            raise RuntimeError(f"Failed exact comparison: {name}")
        checks.append({"name": name, "left": str(left), "relation": "<",
                       "right": str(right), "passed": True})

    ell, U, V = Q('.999'), Q('1.00139'), Q('.872')
    mJ, mN = Q('1.0657205'), Q('.2783155')
    A, B = mJ - ell**12, mN - V**12
    # These four inequalities justify the residual moment expressions.
    less('positive residual J mass', Q(0), A)
    less('residual J mass below leading mass', A, ell**12)
    less('positive residual N mass', V**12, mN)
    less('N mass below twice its entry cap', mN, 2*V**12)
    less('J cube-root majorant', A, Q('.426635')**3)
    less('N cube-root majorant', B, Q('.439736')**3)
    D32_upper = (Q('.426635')**8 + 3*(V**32 + Q('.439736')**8))/ell**32
    D120 = (A**10 + 3*(V**120 + B**10))/ell**120
    less('D(32) upper bound', D32_upper, Q('.0442'))
    less('D(120) upper bound', D120, Q('.00000025'))
    less('largest spatial probability exceeds .968',
         Q('.0604996'), 2*Q('.032')*Q('.968'))
    less('fractional power majorant', Q('.9856')**9, Q('.968')**4)
    less('residual moment at length 32',
         U**64*(1+Q('.0442'))**2/Q('.9856') - 1, Q('.2092'))
    less('residual spectral ratio', Q('.2092'), Q('.9525')**32)
    s = (1 + Q('.9525')**60)**-2
    R_upper = U**120*(1+Q('.00000025')) - 1
    less('positive physical tail bound', Q(0), R_upper)
    t_lower = (1 + R_upper**2)**-2
    less('spatial seed at n=60, beta=49/2', Q('.9002'), s)
    less('physical seed at n=120, beta=49/2', Q('.9372'), t_lower)
    less('first coupled output', f(1-Q('.9002')**2*Q('.9372')), Q('.0502'))
    less('second coupled output', f(1-Q('.9372')**2*(1-Q('.0502'))), Q('.0198'))

    # beta=49 is b_2 in the companion, and the new b_0 in the gap criterion.
    n0, beta, u, C = 120, Q(49), Q(13, 250), Q(6)
    less('both outputs below common seed', max(Q('.0502'), Q('.0198')), u)
    G = sum((1-u)**-k for k in (1, 2, 3))**2/2
    r = C*u
    less('bootstrap positive defect', Q(0), u)
    less('bootstrap defect upper limit', u, Q(1, 6))
    less('bootstrap G coefficient', G, C)
    less('bootstrap contraction', r, Q(1))
    less('bootstrap strict gap condition', Q(3), C*(1-3*u))
    # Certify a convenient decimal consequence without approximating a log.
    target = Q(2377, 100000)
    less('rounded bound gamma > .02377', exp_upper(beta*target), 1/r)
    if n0 < 4 or n0 % 2 or beta <= 0 or 1/r != Q(125, 39):
        raise RuntimeError('Invalid bootstrap parameters or logarithm argument.')

    with localcontext() as ctx:
        ctx.prec = 60
        gap = (Decimal(125)/Decimal(39)).ln()/49
    result = {
        'source_commit': 'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
        'dependencies': ['Periodic paper Proposition 3.1 and Proposition 4.3',
                         'Boundary-field paper Proposition 3.4; periodic seeds from Corollary 5.6 of the periodic paper'],
        'status': 'Explicit corollary extracted from previously published propositions; no priority claim',
        'coupling_normalization': 'J = 1',
        'finite_gap_statement': 'gamma_L > log(125/39)/49 for every even L >= 120',
        'thermodynamic_statement': 'liminf over even L of gamma_L >= log(125/39)/49',
        'decimal_display_only': str(gap),
        'certified_rounded_lower_bound': str(target),
        'parameters': {'n0': n0, 'beta': str(beta), 'u0': str(u), 'C': str(C), 'r': str(r)},
        'all_comparisons_exact_rational': True,
        'success': True, 'checks': checks,
    }
    output = Path(__file__).resolve().parent/'independent_results'/'companion_corollary.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(f'PASS: {len(checks)} exact rational comparisons for the companion-paper corollary.')
    print('gamma_L > log(125/39)/49 > 0.02377, every even L >= 120, J = 1.')
    print('Decimal display:', gap)
    print('The cited analytic and finite-input premises remain dependencies.')


if __name__ == '__main__':
    main()
