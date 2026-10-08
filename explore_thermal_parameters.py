"""Floating-point candidate selection only. Nothing here is a proof."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import json,math
import numpy as np
from scipy.optimize import brentq,linprog
R=Path(__file__).parent
records=json.loads((R/'independent_results/exploratory_low_spectra.json').read_text())['entries']

def moments(beta,resolved=True):
    z={}
    tails={}
    for rec in records:
        if not resolved and rec['twist']==2:continue
        n=rec['n'];lo=hi=0.
        for b in rec['blocks']:
            e=np.array(b['energies'])+1.401482*n
            a=np.exp(-beta*e)
            mult=1 if b['M']==0 else 2
            lo+=mult*a.sum();hi+=mult*(b['dim']-len(e))*a[-1]
        z[n,rec['twist']]=lo;tails[n,rec['twist']]=hi
    ms={s:np.array([(z[n,0]+c*z[n,1])/4 for n in range(4,13)]) for s,c in [('J',3),('N',-1)]}
    if resolved:
        ms.update({s:np.array([sum(c[g]*z[n,g] for g in range(3))/12 for n in range(4,13)]) for s,c in [('I',(1,3,8)),('O',(1,3,-4))]})
    return ms,max(tails.values())

def support(ms):
    M=np.array([[ms[i+j] for j in range(5)] for i in range(5)])
    inv=np.linalg.inv(M)
    def score(x):
        p=x**np.arange(5)
        return x**4*(p@inv@p)-1
    caps=[]
    for sign in (-1,1):
        xx=np.linspace(0,3,3001);end=next(i for i in range(len(xx)-1,0,-1) if score(sign*xx[i])<=0)
        caps.append(brentq(lambda x:score(sign*x),xx[end],xx[end+1]))
    return caps

def flow(i,j,r,q,beta,steps=6):
    f=lambda x:x*x/(2*(1-x)**2)
    for k in range(steps):
        dd=2*r+r*r;dj=(dd+3*(2*j+j*j))/4;di=(dd+3*(2*j+j*j)+8*(2*i+i*i))/12
        if (1+dd)**2/2>=1-q:return 0.
        R=lambda h:max((dd+h)**2/3,(di+h)**2+(dd-di)**2/3,(di+h)**2+(dj-di)**2/2+(dd-dj)**2/3,(dj+h)**2/2+(dd-dj)**2/3)
        lo=0.;hi=q+dd*dd
        while 2*hi-hi*hi<=q+R(hi):
            hi*=2
            if hi>=(1-dd)/2:return 0.
        for _ in range(55):
            h=(lo+hi)/2
            if 2*h-h*h>q+R(h):hi=h
            else:lo=h
        h=hi;den=(1-h)**2
        i=(di+h)**2/den;j=max((dj+h)**2/2,(di+h)**2+(dj-di)**2/2)/den;r=R(h)/den
        p=r*(2+r)/(1+r)**2;q=f(2*q-q*q+p*(1-q)**2);beta*=2
        if not (0<q<1 and 0<p<1):return 0.
    return min(-math.log(2*q)/beta,-2*math.log(2*p)/beta)

def search(beta,use_lp=False,resolved=True):
    ms,tail=moments(beta,resolved)
    U=max(support(ms['I' if resolved else 'J']));v,w=support(ms['N']);V=max(v,w)
    ao,bo=support(ms['O']) if resolved else (0.,0.);W=max(ao,bo)
    lp={}
    if use_lp:
        for sector in (('I','O','N') if resolved else ('J','N')):
            x=np.linspace(-U,U,4001) if sector in ('I','J') else np.linspace(-ao,bo,4001) if sector=='O' else np.linspace(-v,w,4001)
            A=x[None,:]**np.arange(9)[:,None]
            for m in range(18,43,2):
                for direction in (('upper',) if sector in ('I','J') else ('upper','lower')):
                    sign=-1 if direction=='upper' else 1
                    y=ms[sector]
                    eps=1e-9*np.maximum(abs(y),1)
                    res=linprog(sign*x**(m-4),A_ub=np.r_[A,-A],b_ub=np.r_[y+eps,-y+eps],bounds=(0,None),method='highs')
                    if res.success:lp[sector,m,direction]=sign*res.fun
    def I(m):
        cap=U**m+max(0,ms['I'][-1]-U**12)**(m/12)
        return min(cap,lp.get(('I',m,'upper'),cap))
    def O(m):
        cap=W**m+max(0,ms['O'][-1]-W**12)**(m/12)
        return min(cap,lp.get(('O',m,'upper'),cap))
    def J(m):
        if resolved:return I(m)+2*O(m)
        cap=U**m+max(0,ms['J'][-1]-U**12)**(m/12)
        return min(cap,lp.get(('J',m,'upper'),cap))
    def N(m):
        cap=V**m+max(0,ms['N'][-1]-V**12)**(m/12)
        return min(cap,lp.get(('N',m,'upper'),cap))
    def Z(m):return J(m)+3*N(m)
    def residual(v0,rr,D,a,b):
        return max(x**rr+2*(y/2)**rr+3*((max(0,D-v0-x-y))/3)**rr for x,y in ((0,0),(a-v0,0),(a-v0,b-a),(0,b-v0)))
    best=(0,None)
    for n in range(30,81,2):
      for m in range(18,min(n,42)+1,2):
        for tick in range(20,71):
          t=tick/20
          mass=Z(m)**t;ep=(J(m)-lp.get(('N',m,'lower'),0.))**t;ec=((I(m)-lp.get(('O',m,'lower'),0.)) if resolved else J(m))**t
          a=(mass+3*ep+8*ec)/12;b=(mass+3*ep)/4
          lo,hi=mass/2,min(1.,a)
          if lo>=hi or 2*(mass/2)**(120/m)>=1:continue
          for _ in range(45):
              s=(lo+hi)/2
              if s**(120/m)+residual(s,120/m,mass,a,b)<1:lo=s
              else:hi=s
          rr=n/m;s=lo
          i=((a-s)/s)**rr
          j=max(2*((b-s)/2)**rr,(a-s)**rr+2*((b-a)/2)**rr)/s**rr
          r=residual(s,rr,mass,a,b)/s**rr
          z=Z(2*n)-1
          if z<=0:continue
          q=1-(1+z**t)**-2
          rate=flow(i,j,r,q,beta*t)
          if rate>best[0]:best=(rate,(n,m,t,i,j,r,q))
    result={'beta':beta,'caps':([U,ao,bo,v,w] if resolved else [U,v,w]),'resolved':resolved,'omitted_trace_upper_diagnostic':tail,'sampled_LP':use_lp,'best_rate':best[0],'best_seed':best[1]}
    print(json.dumps(result),flush=True)
    return result
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--lp',action='store_true');p.add_argument('--two-sectors',action='store_true');p.add_argument('beta',type=float,nargs='*',default=[10.5,12.25,13.,14.,15.,16.,18.,20.]);a=p.parse_args()
    out=[search(b,a.lp,not a.two_sectors) for b in a.beta]
    print('These diagnostics are not gap bounds or global optima.')
