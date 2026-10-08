"""Display exploratory decay rates; this is NOT a rigorous certificate.

The physical-defect diagnostic -log(2*q_k)/beta_k is computed by ordinary
Decimal arithmetic. It is neither a proved bound on the chain's gap nor a
proof that this method cannot improve. Run verify_spectral_refinement.py for
the exact, certified theorem.
"""

from decimal import Decimal as D, localcontext
import json


def sequence(p, q):
    def f(x):
        return x*x/(2*(1-x)**2)
    rows = []
    for k in range(9):
        beta = D('24.5')*2**k
        rate = -(2*q).ln()/beta
        rows.append({'k': k, 'n': 60*2**k, 'beta': str(beta),
                     'physical_defect_decay_rate_display_only': f'{rate:.18f}'})
        p_next = f(1-(1-p)**2*(1-q))
        q_next = f(1-(1-q)**2*(1-p_next))
        p, q = p_next, q_next
    return rows


def main():
    with localcontext() as context:
        context.prec = 400
        rounded = sequence(D('.0998'), D('.0628'))
        s = (1+D('.9525')**60)**-2
        physical_tail = D('1.00139')**120*(1+D('.00000025'))-1
        t = (1+physical_tail**2)**-2
        sharper = sequence(1-s, 1-t)
        spectral = sequence(D(".07584"), D(".059062"))
    print(json.dumps({
        'status': 'Exploration only; not part of the exact certificate',
        'meaning': 'Observed decay rates of this chosen coupled recurrence, not a mathematical limit on the method or the physical gap',
        'rounded_printed_seeds': rounded,
        'sharper_seed_expressions': sharper,
        'version_1_4_certified_seeds_diagnostic_sequence': spectral,
    }, indent=2))


if __name__ == '__main__':
    main()
