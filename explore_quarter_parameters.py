"""Nonrigorous four-twist screening; no acceptance decisions."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import sys,json,math
import numpy as np
from scipy.optimize import linprog
R=Path(__file__).resolve().parent
from explore_thermal_parameters import support,flow
S=Path(__file__).parent
records=json.loads((R/'independent_results/exploratory_low_spectra.json').read_text())['entries']+json.loads((R/'independent_results/exploratory_quarter_spectra.json').read_text())['entries']

def moments(beta):
 z={};tails={}
 for rec in records:
  n=rec['n'];lo=tail=0.
  for b in rec['blocks']:
   e=np.array(b['energies'])+1.401482*n;a=np.exp(-beta*e);mult=1 if b['M']==0 else 2
   lo+=mult*a.sum();tail+=mult*(b['dim']-len(e))*a[-1]
  z[n,rec['twist']]=lo;tails[n,rec['twist']]=tail
 coeff={'A':(1,9,8,6),'B':(1,-3,8,-6),'E':(2,6,-8,0),'V':(3,-9,0,6)}
 ms={s:np.array([sum(c[g]*z[n,g] for g in range(4))/24 for n in range(4,13)]) for s,c in coeff.items()}
 return ms,max(tails.values())

def search(beta,lp_enabled=False):
 ms,tail=moments(beta);caps={s:support(ms[s]) for s in ms};lp={}
 print('caps',beta,caps,'tail',tail,flush=True)
 if lp_enabled:
  for s in ms:
   a,b=caps[s];x=np.linspace(-a,b,6001);A=np.array([x**j for j in range(9)])
   for m in range(16,43,2):
    for direction in ('upper','lower'):
     sign=-1 if direction=='upper' else 1
     y=ms[s];eps=2e-9*np.maximum(abs(y),1)
     res=linprog(sign*x**(m-4),A_ub=np.r_[A,-A],b_ub=np.r_[y+eps,-y+eps],bounds=(0,None),method='highs')
     if res.success:lp[s,m,direction]=sign*res.fun
 def component(s,m):
  U=max(caps[s]);h=U**12;mm=ms[s][-1];q=int(mm/h);cap=q*U**m+(mm-q*h)**(m/12)
  return min(cap,lp.get((s,m,'upper'),cap))
 def I(m):return component('A',m)+component('B',m)
 def O(m):return component('E',m)
 def J(m):return I(m)+2*O(m)
 def N(m):return component('B',m)+component('E',m)+component('V',m)
 def Z(m):return J(m)+3*N(m)
 def residual(v0,rr,D,a,b):
  return max(x**rr+2*(y/2)**rr+3*(max(0,D-v0-x-y)/3)**rr for x,y in ((0,0),(a-v0,0),(a-v0,b-a),(0,b-v0)))
 best=(0,None)
 for n in range(30,81,2):
  for m in range(16,min(n,42)+1,2):
   z=Z(2*n)-1
   if z<=0:continue
   for tick in range(20,81):
    t=tick/20;mass=Z(m)**t;ep=(J(m)-sum(lp.get((s,m,'lower'),0.) for s in ('B','E','V')))**t;ec=(I(m)-lp.get(('E',m,'lower'),0.))**t
    a=(mass+3*ep+8*ec)/12;b=(mass+3*ep)/4
    lo,hi=mass/2,min(1.,a)
    if lo>=hi or 2*(mass/2)**(120/m)>=1:continue
    for _ in range(45):
     v=(lo+hi)/2
     if v**(120/m)+residual(v,120/m,mass,a,b)<1:lo=v
     else:hi=v
    v=lo;rr=n/m
    i=((a-v)/v)**rr;j=max(2*((b-v)/2)**rr,(a-v)**rr+2*((b-a)/2)**rr)/v**rr;r=residual(v,rr,mass,a,b)/v**rr
    q=1-(1+z**t)**-2
    rate=flow(i,j,r,q,beta*t)
    if rate>best[0]:best=(rate,(n,m,t,i,j,r,q))
 result={'beta':beta,'caps':caps,'omitted_trace_diagnostic':tail,'LP':lp_enabled,'best_rate':best[0],'best_seed':best[1]}
 print(json.dumps(result),flush=True);return result
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--lp',action='store_true');p.add_argument('beta',type=float,nargs='*',default=[12.25]);a=p.parse_args()
 results=[search(b,a.lp) for b in a.beta]
 print('NON-RIGOROUS: neither gap bounds nor global optima.')
