"""Recompute the new 84-site trial from the published integer matrix recipe.

Requires NumPy and SciPy (through the independent reconstruction module).
Arbitrary-precision integer matrix products determine every acceptance result.
The floating energy display and timings are diagnostic only.
"""
from pathlib import Path
import sys,json,time
import numpy as np
from itertools import product
from fractions import Fraction as F
root=Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('Assertions must be enabled; do not use -O.')
from independent_audit import trial_matrices,physical_block
start=time.monotonic();labels,A=trial_matrices()
B={(s,t):A[s]@A[t] for s,t in product((-1,0,1),repeat=2)}
T=sum(np.kron(m,m) for m in A.values());pairs=list(product((-1,0,1),repeat=2));h=np.zeros((9,9),dtype=int)
for j,(s,t) in enumerate(pairs):
 h[j,j]=s*t
 for step in (-1,1):
  if -1<=s+step<=1 and -1<=t-step<=1:h[pairs.index((s+step,t-step)),j]=1
O=sum(int(h[i,j])*np.kron(B[x],B[y]) for i,x in enumerate(pairs) for j,y in enumerate(pairs) if h[i,j])
diffs=np.array([d-e for a,d in labels for b,e in labels]);totals={n:[0,0] for n in (4,84)}
assert all(T[i,j]==0 and O[i,j]==0 for i,j in zip(*np.where(diffs[:,None]!=diffs[None,:])))
dim=[]
for diff in sorted(set(diffs)):
 idx=np.flatnonzero(diffs==diff);x=T[np.ix_(idx,idx)];o=O[np.ix_(idx,idx)];x2=x@x;dim.append(len(idx))
 for n in totals:
  xp=np.linalg.matrix_power(x,n-2)
  energy=int((xp*o.T).sum());norm=int((xp*x2.T).sum())
  totals[n][0]+=energy;totals[n][1]+=norm
 print('block',int(diff),'dim',len(idx),'seconds',time.monotonic()-start,flush=True)
words,H=physical_block(4,0);psi=np.array([int(np.trace(A[w[0]]@A[w[1]]@A[w[2]]@A[w[3]])) for w in words],dtype=object)
assert sum(v*v for v in psi)==totals[4][1]
assert sum(psi[i]*int(H[i,j])*psi[j] for i in range(len(words)) for j in range(len(words)))==4*totals[4][0]
U,V=totals[84];assert V>0 and 500000*U+700741*V<0
record={'length':84,'one_bond_numerator':str(U),'norm':str(V),'shift_comparison_integer':str(500000*U+700741*V),'energy_per_bond_display':float(F(U,V)),'block_dimensions':dim,'four_site_direct_check':True,'success':True}
expected=json.loads((root/'independent_results/trial84.json').read_text())
assert record==expected
print('PASS: exact 84-site trial and direct four-site cross-check; seconds',time.monotonic()-start,flush=True)
