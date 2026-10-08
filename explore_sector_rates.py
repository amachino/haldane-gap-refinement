"""Non-rigorous seed/recurrence screening, independent of certificate acceptance.

The default compares three trial lengths already checked. --full-search also
screens hypothetical trial lengths; those candidates require new trial checks.
Decimal iteration mitigates underflow but does not provide enclosures.
"""
from decimal import Decimal as D,localcontext
from fractions import Fraction as Q
from pathlib import Path
import argparse,json,math


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full-search',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    data=json.loads((root/'independent_results/sector_refinement.json').read_text())
    lp={(r['sector'],r['moment'],r['direction']):float(Q(r['bound']))
        for r in data['polynomial_certificates']}
    U,V=1.0013391,.8710311
    mj=float(Q(data['moment_intervals']['12']['Jhi']))
    mn=float(Q(data['moment_intervals']['12']['Nhi']))
    def J(m):
        cap=U**m+(mj-U**12)**(m/12)
        return min(cap,lp.get(('J',m,'upper'),cap))
    def N(m):
        cap=V**m+(mn-V**12)**(m/12)
        return min(cap,lp.get(('N',m,'upper'),cap))
    def Z(m):return J(m)+3*N(m)
    def residual(v,r,mass,a,b):
        return max(x**r+2*(y/2)**r+3*((mass-v-x-y)/3)**r
                   for x,y in ((0,0),(a-v,0),(a-v,b-a),(0,b-v)))
    def diagnostic(n,m,t,sector=True):
        mass=Z(m)**t;ep=(J(m)-lp['N',m,'lower'])**t;ec=J(m)**t
        a=(mass+3*ep+8*ec)/12;b=(mass+3*ep)/4
        lo,hi=mass/2,min(1.,a)
        if lo>=hi or 2*(mass/2)**(120/m)>=1:return 0.
        for _ in range(65):
            v=(lo+hi)/2
            if v**(120/m)+residual(v,120/m,mass,a,b)<1:lo=v
            else:hi=v
        v=lo;rr=n/m
        i=((a-v)/v)**rr
        j=max(2*((b-v)/2)**rr,(a-v)**rr+2*((b-a)/2)**rr)/v**rr
        r=residual(v,rr,mass,a,b)/v**rr
        q=1-(1+(Z(2*n)-1)**t)**-2
        with localcontext() as ctx:
            ctx.prec=400
            i,j,r,q,beta=[D(str(x)) for x in (i,j,r,q,12.25*t)]
            f=lambda u:u*u/(2*(1-u)**2)
            defect=lambda r:r*(2+r)/(1+r)**2
            for _ in range(8):
                if not sector:
                    p=defect(r);ap=2*p-p*p+q*(1-p)**2
                    p=f(ap)
                    q=f(2*q-q*q+p*(1-q)**2)
                    if not 0<p<1 or not 0<q<1:return 0.
                    r=(1-p)**(-D('.5'))-1;beta*=2
                    continue
                dd=2*r+r*r;dj=(dd+3*(2*j+j*j))/4;di=(dd+3*(2*j+j*j)+8*(2*i+i*i))/12
                if (1+dd)**2/2>=1-q:return 0.
                R=lambda h:max((dd+h)**2/3,(di+h)**2+(dd-di)**2/3,
                               (di+h)**2+(dj-di)**2/2+(dd-dj)**2/3,
                               (dj+h)**2/2+(dd-dj)**2/3)
                low=D(0);high=q+dd*dd
                while 2*high-high*high<=q+R(high):
                    high*=2
                    if high>=(1-dd)/2:return 0.
                for _ in range(130):
                    h=(low+high)/2
                    if 2*h-h*h>q+R(h):high=h
                    else:low=h
                h=high;v2=(1-h)**2
                i=(di+h)**2/v2
                j=max((dj+h)**2/2,(di+h)**2+(dj-di)**2/2)/v2
                r=R(h)/v2;p=defect(r)
                q=f(2*q-q*q+p*(1-q)**2);beta*=2
            return float(min(-(2*q).ln()/beta,-2*(2*defect(r)).ln()/beta))
    print('NON-RIGOROUS diagnostics; not uniform gap certificates or optimality bounds.')
    if args.full_search:
        for n in (36,40,42,44,46,48,60):
            best=(0.,0,0.)
            for tick in range(40,131):
                t=tick/40
                for m in (22,24,26,28,30,32):
                    best=max(best,(diagnostic(n,m,t),m,t))
            print('reference',n,'best diagnostic, moment, multiplier:',best,flush=True)
    else:
        for n,m,t in ((36,24,1.775),(44,26,2.2),(60,26,3.1)):
            print('n,m,t=',n,m,t,'sector rate=',diagnostic(n,m,t),
                  'ordinary update=',diagnostic(n,m,t,False),flush=True)


if __name__=='__main__':
    main()
