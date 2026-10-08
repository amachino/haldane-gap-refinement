"""Nonrigorous low-spectrum thermal screen; no gap certificate."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import importlib.util,itertools,json,time
import numpy as np
from scipy.sparse import eye,csr_matrix
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigvalsh
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('thermal',ROOT/'source/verification/computations/source1/thermal-definitions.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--refresh',action='store_true',help='Recompute rather than reuse the exploratory cache')
args=parser.parse_args()
out=ROOT/'independent_results/exploratory_low_spectra.json'
records=json.loads(out.read_text())['entries'] if out.exists() and not args.refresh else []
for n in range(4,13):
    basis={M:[] for M in range(n+1)}
    for w in itertools.product((-1,0,1),repeat=n):
        M=sum(w)
        if M>=0:basis[M].append(w)
    for tw in (0,1,2):
        if any(r['n']==n and r['twist']==tw for r in records):continue
        start=time.monotonic();blocks=[]
        for M,words in basis.items():
            d=len(words)
            if tw<2:
                A=t.dmat(words,tw)
                H=(16-1.5*n)*eye(d,format='csr')-.5*A
            else:
                lut={w:i for i,w in enumerate(words)};row=[];col=[];dat=[]
                for j,w in enumerate(words):
                    row.append(j);col.append(j);dat.append(sum(w[k-1]*w[k] for k in range(n)))
                    for k in range(n):
                        for delta in (-1,1):
                            z=list(w);z[k-1]+=delta;z[k]-=delta
                            if abs(z[k-1])<=1 and abs(z[k])<=1:
                                row.append(j);col.append(lut[tuple(z)]);dat.append(np.exp(2j*np.pi*delta/3) if k==0 else 1)
                H=csr_matrix((dat,(row,col)),shape=(d,d),dtype=complex)
            if d<=200:vals=eigvalsh(H.toarray());err=0.
            else:
                vals,V=eigsh(H,k=min(24,d-2),which='SA',tol=2e-12,ncv=min(d,96))
                err=float(np.max(np.linalg.norm(H@V-V*vals,axis=0)))
            blocks.append({'M':M,'dim':d,'energies':sorted(map(float,vals)),'max_residual':err})
        records.append({'n':n,'twist':tw,'blocks':blocks})
        out.write_text(json.dumps({'status':'NON-RIGOROUS; not a certificate','entries':records},indent=2)+'\n')
        print('NONRIGOROUS spectrum',n,tw,'seconds',round(time.monotonic()-start,2),flush=True)
