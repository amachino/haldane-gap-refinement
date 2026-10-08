"""Nonrigorous candidate screen with octahedral projection caps."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json,math,itertools
import numpy as np
from scipy.optimize import linprog
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from explore_quarter_parameters import moments,support
S=Path(__file__).parent
C=np.array([[1,0,0,0],[1,1,0,0],[1,1,2,0],[1,0,1,1],[1,4,5,3]],float)
M=np.r_[C,-np.eye(4)]
sets=[];inverses=[]
for ix in itertools.combinations(range(9),4):
 a=M[list(ix)]
 if abs(np.linalg.det(a))>1e-8:sets.append(ix);inverses.append(np.linalg.inv(a))
sets=np.array(sets);inverses=np.array(inverses)

def vertices(caps):
 scale=max(caps);rhs=np.r_[np.array(caps)/scale,np.zeros(4)]
 v=np.einsum('ijk,ik->ij',inverses,rhs[sets]);keep=(v@M.T<=rhs+1e-10).all(axis=1)
 return np.maximum(0,v[keep])*scale

def projected_powers(v,rr):return np.max(v**rr@C.T,axis=0)

def R2(v,rr,D,A):return max((D-v)**rr/3**(rr-1),(A-v)**rr+(D-A)**rr/3**(rr-1))

def flow(caps,q,beta,steps=6):
 caps=np.array(caps)
 for k in range(steps):
  verts=vertices(caps)
  p=max(verts @ np.array([1,0,1,-1]));c=max(verts @ np.array([1,1,-1,0]));d=max(verts @ np.array([1,-2,-1,1]))
  r=caps[-1];dz=2*r+r*r;dp=2*p+p*p;dc=2*c+c*c;dt=2*d+d*d
  diffs=np.array([(dz+9*dp+8*dc+6*dt)/24,(dz+3*dp+8*dc)/12,(dz+3*dp)/4,(dz+dp+2*dt)/4,dz])
  diffs[0]=min(diffs);diffs[1]=min(diffs[1],diffs[2],diffs[4]);diffs[2]=min(diffs[2],diffs[4]);diffs[3]=min(diffs[3],diffs[4])
  if (1+dz)**2/2>=1-q:return 0.
  lo=0.;hi=q+dz*dz
  test=lambda h:q+max((dz+h)**2/3,(diffs[0]+h)**2+(dz-diffs[0])**2/3)<2*h-h*h
  while not test(hi):
   hi*=2
   if hi>=(1-dz)/2:return 0.
  for _ in range(50):
   h=(lo+hi)/2
   if test(h):hi=h
   else:lo=h
  h=hi;caps=projected_powers(vertices(diffs+h),2)/(1-h)**2
  p=caps[-1]*(2+caps[-1])/(1+caps[-1])**2;u=2*q-q*q+p*(1-q)**2;q=u*u/(2*(1-u)**2);beta*=2
  if not (0<q<1 and 0<p<1):return 0.
 return min(-math.log(2*q)/beta,-2*math.log(2*p)/beta)

def search(beta):
 ms,tail=moments(beta);sup={s:support(ms[s]) for s in ms};lp={}
 for s in ms:
  a,b=sup[s];x=np.linspace(-a,b,7001);A=np.array([x**j for j in range(9)]);y=ms[s];eps=2e-9*np.maximum(abs(y),1)
  for m in range(20,35,2):
   for direction in ('upper','lower'):
    sign=-1 if direction=='upper' else 1
    res=linprog(sign*x**(m-4),A_ub=np.r_[A,-A],b_ub=np.r_[y+eps,-y+eps],bounds=(0,None),method='highs')
    if res.success:lp[s,m,direction]=sign*res.fun
 def component(s,m):
  U=max(sup[s]);h=U**12;mm=ms[s][-1];q=int(mm/h);cap=q*U**m+(mm-q*h)**(m/12)
  return min(cap,lp.get((s,m,'upper'),cap))
 def source_caps(m):
  a,b,e,v=[component(s,m) for s in ('A','B','E','V')]
  bl,el,vl=[lp.get((s,m,'lower'),0.) for s in ('B','E','V')]
  return np.array([a+4*b+5*e+3*v,a+e-vl,a+b-el,a-2*bl-el+v])
 best=(0,None)
 for n in (36,38,40,42,44,46,48,50,52,54,56,60):
  z=source_caps(2*n)[0]-1
  for m in range(20,min(n,34)+1,2):
   sc=source_caps(m)
   for tick in range(32,51):
    t=tick/20;Z,P,C0,T=sc**t
    caps=np.array([(Z+9*P+8*C0+6*T)/24,(Z+3*P+8*C0)/12,(Z+3*P)/4,(Z+P+2*T)/4,Z]);caps[0]=min(caps)
    lo,hi=Z/2,min(1.,caps[0]);rr=120/m
    if lo>=hi or 2*(Z/2)**rr>=1:continue
    for _ in range(48):
     v=(lo+hi)/2
     if v**rr+R2(v,rr,Z,caps[0])<1:lo=v
     else:hi=v
    v=lo;rcaps=projected_powers(vertices(caps-v),n/m)/v**(n/m)
    q=1-(1+z**t)**-2
    rate=flow(rcaps,q,beta*t)
    if rate>best[0]:
     best=(rate,{'n':n,'m':m,'t':t,'caps':rcaps.tolist(),'q':q,'v':v});print('BEST',best,flush=True)
 result={'beta':beta,'best_rate':best[0],'seed':best[1],'sup':sup,'tail_diagnostic':tail}
 print(json.dumps(result),flush=True)
if __name__=='__main__':search(12.25)
