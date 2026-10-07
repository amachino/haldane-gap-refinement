"""Exact arithmetic for the gap bound at ALL integer lengths L >= 120.

The analytic proof is in paper/note.tex, section 'Including odd lengths'.
Dependencies: the periodic paper's Proposition 3.1 and the boundary-field
paper's Proposition 3.4, at OpenAI Math commit
adc7f1241b42e322a6451854ab7e4b4c146bf78a.

This checks a polynomial identity and rational endpoint inequalities which
prove positivity on the ENTIRE interval 0 <= u <= 13/250. It does not use
a numerical grid. The concentration and signed-moment lemmas remain
analytic arguments. The previously checked finite inputs are unchanged.
Only the standard library is used; the rational exponential upper bound
is shared with verify_gap_improvement.py.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as Q
import json
from pathlib import Path

from verify_gap_improvement import exp_upper


def multiply(a, b):
    """Multiply rational polynomials stored in increasing degree order."""
    result = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return result


def subtract(a, b):
    return [(a[i] if i < len(a) else Q(0))
            - (b[i] if i < len(b) else Q(0))
            for i in range(max(len(a), len(b)))]


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled; do not run Python with -O.')
    checks = []

    def check(name, condition, evidence):
        if not condition:
            raise RuntimeError('Failed exact check: ' + name)
        checks.append({'name': name, 'passed': True, 'evidence': evidence})

    def less(name, left, right):
        check(name, left < right, {'left': str(left), 'relation': '<', 'right': str(right)})

    def equal(name, left, right):
        check(name, left == right, {'left': str(left), 'relation': '=', 'right': str(right)})

    u0, C, B = Q(13, 250), Q(6), Q(9, 2)
    r = C*u0
    n0, beta0 = 120, Q(49)
    check('even reference length at least four', n0 >= 4 and n0 % 2 == 0, {'n0': n0})
    less('positive inverse temperature', Q(0), beta0)
    less('positive initial defect', Q(0), u0)
    less('concentration lemma valid for 3u', 3*u0, Q(1, 2))
    less('quadratic recurrence contracts', r, Q(1))
    less('next defect below one', C*u0**2, Q(1))

    # d(z)=z/(2-3z) and v=6u^2. The analytic signed-moment argument gives
    # K(u)=(1-u)(1-v)(1-d(3u))/(1+d(u))^2.
    # Cancel rational factors, without numerical evaluation:
    # K(u)=(1-6u^2)(1-6u)(2-3u)^2/[2(2-9u)(1-u)].
    numerator = multiply(multiply([Q(1), Q(0), -C], [Q(1), Q(-6)]),
                         multiply([Q(2), Q(-3)], [Q(2), Q(-3)]))
    denominator = [2*x for x in multiply([Q(2), Q(-9)], [Q(1), Q(-1)])]
    difference = subtract(numerator, multiply([Q(1), -B], denominator))
    expected = [Q(0), Q(4), Q(-60), Q(243), Q(-486), Q(324)]
    check('polynomial identity for K(u)-(1-9u/2)', difference == expected,
          {'computed_coefficients': list(map(str, difference)),
           'expected_coefficients': list(map(str, expected))})
    # The numerator is u[4-60u+243u^2(1-2u)+324u^4].
    # These endpoint checks establish positivity for every 0<=u<=u0.
    less('4-60u positive on full interval', Q(0), 4-60*u0)
    less('1-2u positive on full interval', Q(0), 1-2*u0)
    less('2-9u positive on full interval', Q(0), 2-9*u0)
    less('1-u positive on full interval', Q(0), 1-u0)
    less('positive cubic coefficient', Q(0), Q(243))
    less('positive quintic coefficient', Q(0), Q(324))

    equal('purity floor', 1-B*u0, Q(383, 500))
    less('physical purity exceeds one half', Q(1, 2), 1-B*u0)
    prefactor = B/(C*(1-B*u0))
    equal('uniform prefactor', prefactor, Q(375, 383))
    less('strict final gap comparison', prefactor, Q(1))
    equal('exact decay base', r, Q(39, 125))
    equal('closed-form recurrence initial value', r/C, u0)
    equal('exact logarithm argument', 1/r, Q(125, 39))
    less('certified rounded consequence .02377', exp_upper(beta0*Q(2377, 100000)), 1/r)

    with localcontext() as ctx:
        ctx.prec = 60
        gap = (Decimal(125)/Decimal(39)).ln()/49
    result = {
        'source_commit': 'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
        'dependencies': ['Periodic paper Proposition 3.1: signed moments for every integer length',
                         'Boundary-field paper Proposition 3.4: positive dominant eigenvalues, tracked purities, and temperature ratios'],
        'finite_gap_statement': 'gamma_L > log(125/39)/49 for every integer L >= 120',
        'odd_length_statement': 'In particular, every odd L >= 121',
        'thermodynamic_statement': 'liminf over all integer L of gamma_L >= log(125/39)/49',
        'ground_state': 'unique for every integer L >= 120',
        'coupling_normalization': 'J = 1',
        'decimal_display_only': str(gap),
        'interval_proof': 'K(u)-(1-9u/2) = u[4-60u+243u^2(1-2u)+324u^4]/[2(2-9u)(1-u)] >= 0 for 0 <= u <= 13/250',
        'same_reference_length': 'Both temperatures use the same EVEN reference n_k; signed traces are then bounded for EVERY integer L >= n_k.',
        'all_arithmetic_exact_rational': True,
        'scope': 'Conditional analytic extension with an exact scalar certificate; not a formal verification of upstream analytic premises',
        'success': True, 'checks': checks,
    }
    output = Path(__file__).resolve().parent/'independent_results'/'signed_extension.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(f'PASS: {len(checks)} exact checks for the signed-moment extension.')
    print('gamma_L > log(125/39)/49 > 0.02377 for EVERY integer L >= 120, J = 1.')
    print('Includes every odd L >= 121; the ground state is unique.')
    print('Decimal display:', gap)
    print('The cited analytic and finite-input premises remain dependencies.')


if __name__ == '__main__':
    main()
