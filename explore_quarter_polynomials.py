"""Optional floating-point search; its output is not a proof.

Example: python explore_quarter_polynomials.py --sector V --moment 27
Requires NumPy/SciPy. Run the exact certificate first to reconstruct moments.
Only fixed, independently certified rational polynomials enter the theorem.
"""
import argparse
from fractions import Fraction as Q
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sector',choices=['A','B','E','V'],default='V')
    parser.add_argument('--moment',type=int,default=26)
    parser.add_argument('--direction',choices=['upper','lower'],default='upper')
    parser.add_argument('--grid',type=int,default=12001)
    args=parser.parse_args()
    if args.moment<12 or args.grid<3:
        parser.error('Require moment >= 12 and grid >= 3.')
    root=Path(__file__).resolve().parent
    data=json.loads((root/'independent_results/quarter_refinement.json').read_text())
    rows=[data['moment_intervals'][str(k)] for k in range(4,13)]
    lo=np.array([float(Q(r[args.sector+'lo'])) for r in rows])
    hi=np.array([float(Q(r[args.sector+'hi'])) for r in rows])
    a,b=map(lambda v:float(Q(v)),data['supports'][args.sector])
    x=np.linspace(a,b,args.grid);A=np.array([x**j for j in range(9)])
    sign=-1 if args.direction=='upper' else 1
    result=linprog(sign*x**(args.moment-4),A_ub=np.r_[A,-A],b_ub=np.r_[hi,-lo],
                   bounds=(0,None),method='highs',options={
                       'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    if not result.success:
        raise RuntimeError(result.message)
    c=sign*(result.ineqlin.marginals[:9]-result.ineqlin.marginals[9:])
    print('NON-RIGOROUS sampled optimization objective:',sign*result.fun)
    print('Candidate degree-eight coefficients:',c.tolist())
    print('A continuum certificate and directed moment evaluation are still required.')


if __name__=='__main__':
    main()
