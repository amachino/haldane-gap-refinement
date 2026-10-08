"""Recompute supplemental exact totals at beta=49/4 with the upstream engine.

This takes a few minutes. It is separate from the standard-library scalar
certificates and is not needed to reproduce the main gap certificate.
"""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import importlib.util
import json
import time

ROOT=Path(__file__).resolve().parent


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled; do not use -O.')
    spec=importlib.util.spec_from_file_location('upstream_thermal',
        ROOT/'source/verification/computations/source2/thermal.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    c=[Q(98)**j/factorial(j) for j in range(257)]
    module.probs=[int(module.Q*x/sum(c)) for x in c]
    while module.probs[-1]==0:
        module.probs.pop()
    records=json.loads((ROOT/'independent_results/cyclic_thermal_totals.json').read_text())
    for record in records:
        begin=time.monotonic()
        total=module.part(record['n'],2)
        assert total==int(record['total'])
        print('PASS: n=',record['n'],'seconds=',round(time.monotonic()-begin,3),flush=True)


if __name__=='__main__':
    main()
