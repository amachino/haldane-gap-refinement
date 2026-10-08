"""Recompute the nine exact totals, with independent small-chain checks.

Requires a C++17 compiler with OpenMP. --quick checks lengths 4..8 only.
The full run took about 6.5 minutes on the development machine (8 CPUs).
NumPy/SciPy are needed only for the independent odd-length cross-check.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial,isqrt
from pathlib import Path
import argparse,importlib.util,json,subprocess,tempfile

ROOT=Path(__file__).resolve().parent


def full_columns(n,coefficients):
    """All columns, no orbit reduction; two sparse integer coordinate matrices."""
    import numpy as np
    from scipy.sparse import csr_matrix
    total=0
    for M in range(n+1):
        words=[w for w in product((-1,0,1),repeat=n) if sum(w)==M]
        d=len(words);indices={w:i for i,w in enumerate(words)}
        A=np.zeros((d,d),dtype=np.int64);B=A.copy()
        for i,w in enumerate(words):
            A[i,i]=32-3*n-2*sum(w[j-1]*w[j] for j in range(n))
            for j in range(n):
                k=(j+1)%n
                for step in (-1,1):
                    v=list(w);v[j]-=step;v[k]+=step
                    if abs(v[j])>1 or abs(v[k])>1:continue
                    dest=indices[tuple(v)]
                    if k!=0:A[i,dest]-=2
                    elif step==1:B[i,dest]-=2
                    else:A[i,dest]+=2;B[i,dest]+=2
        A,B=csr_matrix(A),csr_matrix(B)
        X=np.zeros((d,d),dtype=np.int64);Y=X.copy()
        for c in reversed(coefficients):
            AX,AY,BX,BY=A@X,A@Y,B@X,B@Y
            X=(AX-BY)//32;Y=(BX+AY-BY)//32
            X[np.arange(d),np.arange(d)]+=c
        X,Y=X.astype(object),Y.astype(object)
        total+=(1 if M==0 else 2)*int((X*X-X*Y+Y*Y).sum())
    return total


def main():
    if not __debug__:raise RuntimeError('Assertions must be enabled.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--quick',action='store_true')
    parser.add_argument('--threads',type=int,default=8,choices=range(1,9))
    args=parser.parse_args()
    c=[Q(98)**j/factorial(j) for j in range(281)]
    coefficients=[int(2**55*x/sum(c)) for x in c]
    while coefficients[-1]==0:coefficients.pop()
    assert len(coefficients)==192
    spec=importlib.util.spec_from_file_location('packed_reference',
        ROOT/'source/verification/computations/source2/thermal.py')
    reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
    reference.probs=coefficients
    expected={r['n']:r for r in json.loads((ROOT/'independent_results/extended_cyclic_totals.json').read_text())}
    evidence=[]
    from thermal_error_bounds import errors
    with tempfile.TemporaryDirectory(prefix='haldane-cyclic-') as tmp:
        tmp=Path(tmp);binary=tmp/'thermal_engine';weights=tmp/'coefficients.txt'
        weights.write_text('\n'.join(map(str,coefficients))+'\n')
        subprocess.run(['g++','-O3','-std=c++17','-fopenmp',str(ROOT/'compute_thermal_moments.cpp'),'-o',str(binary)],check=True)
        def run(n,tw):
            result=subprocess.run([str(binary),str(n),str(tw),str(weights),str(args.threads)],check=True,capture_output=True,text=True)
            return json.loads(result.stdout)
        for tw in (0,1):
            rec=run(4,tw);assert int(rec['total'])==reference.part(4,tw)
            evidence.append({'n':4,'twist':tw,'packed_reference_exact_match':True})
        for n in range(4,9 if args.quick else 13):
            rec=run(n,2)
            assert all(rec[k]==expected[n][k] for k in rec)
            row={'n':n,'twist':2,'stored_integer_total_matches':True}
            if n in (4,6,8):
                assert int(rec['total'])==reference.part(n,2)
                row['packed_reference_exact_match']=True
            if n==5:
                direct=full_columns(n,coefficients);E,_,_=errors(n)
                assert abs(isqrt(direct)-isqrt(int(rec['total'])))<2*E+2
                row['all_column_integer_total']=str(direct)
                row['all_column_norm_intervals_overlap']=True
            evidence.append(row)
            print('PASS: exact extended cyclic total, n=',n,flush=True)
    if not args.quick:
        (ROOT/'independent_results/extended_engine_crosschecks.json').write_text(
            json.dumps({'entries':evidence,'success':True},indent=2)+'\n')


if __name__=='__main__':main()
