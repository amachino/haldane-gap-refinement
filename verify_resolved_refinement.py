"""Exact certificate using all three thermal twists and tight purity extraction.

The analytic spatial-transfer premises remain conditional. All scalar
acceptance decisions, polynomial interval checks, and covering decisions
use rational arithmetic. See the note for the sector recurrence proof.
"""
from decimal import localcontext
from fractions import Fraction as Q
from math import comb, isqrt
from pathlib import Path
import json

from sector_bounds import (rounded, power, real_power, root, significant_upper,
                           decimal, defect, f, residual, nonnegative_on_interval)
from verify_gap_improvement import exp_upper as taylor_upper
from thermal_error_bounds import errors
from verify_local_energy import certificate
import sector_bounds as arithmetic

# The ninth recurrence step reaches defects below 10^-800. This setting
# affects this checker process only; retained certificates keep their grids.
arithmetic.GRID = 10**1000
arithmetic.ROOT_MARGIN = Q(1,10**450)


def exp_upper(x):
    """Exact Taylor upper bound, scaled and squared with upward rounding."""
    if x<0:raise ValueError('Expected a nonnegative exponent.')
    steps=0
    while x>1:
        x/=2;steps+=1
    value=significant_upper(taylor_upper(x),40)
    for _ in range(steps):
        value=significant_upper(value*value,40)
    return value

ROOT = Path(__file__).resolve().parent
TARGET = Q(29,200)
BETA = Q(49,4)
U, IU, OMAX, OMIN, V, W = map(Q, ('1.0008406','.59564','.699301','.577508','.8710233','.7502156'))
FILTERS = {'I+': [6831635, 13499843, -279426488, -155886938, 1000000000], 'I-': [-5619123, 149061130, 22763472, -1163237573, 1000000000], 'O+': [5534399, -1316911, -254754756, -42837950, 1000000000], 'O-': [2147995, 63138739, -163432436, -534422804, 1000000000], 'N-': [11995164, 14443993, -394383730, -41386229, 1000000000], 'N+': [7663895, -105278780, -311690898, 577215505, 1000000000]}


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled; do not run Python with -O.')
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError('Failed exact check: '+name)
        checks.append({'name':name,'passed':True})

    check('five-site energy certificate',certificate()['success'])

    # Re-enclose the two original twist tables using the geometric error.
    # The separately computed cyclic-twist totals are incorporated below.
    source = ROOT/'source/verification/computations/evidence/source1'
    totals = json.loads((source/'thermal-run/interval-summary.json').read_text())['entries']
    bounds = json.loads((source/'error-bounds.json').read_text())
    check('source thermal precision and truncation', bounds['Q']==2**55 and bounds['J']==280)
    moments = {}
    for rec in bounds['bounds']:
        n, d, E = rec['n'],rec['d'],rec['frobenius_error_Q_units']
        x = (Q(3,2)-Q(700741,500000))*BETA*n
        check(f'thermal {n}: enclosure parameters', 4 <= n <= 12 and
              d*d > 3**n and E == d*(281*(d+1)+1) and
              Q(rec['scale_exponent']) == x and 0 < x < 15)
        E,_,_=errors(n)
        term = s = Q(1)
        for k in range(1,101):
            term *= x/k
            s += term
        # Omitted tail <= term*x/(101-x) < term.
        check(f'thermal {n}: exponential tail', x/(101-x) < 1)
        z = []
        for tw in (0,1):
            total = int(next(e['W'] for e in totals if e['n']==n and e['tw']==tw))
            r = isqrt(total)
            check(f'thermal {n},{tw}: integer square root', r*r <= total < (r+1)**2 and r>E)
            z.append((s*(r-E)**2/2**110, (s+term)*(r+1+E)**2/2**110))
        moments[n] = {'Jlo':(z[0][0]+3*z[1][0])/4,
                      'Jhi':(z[0][1]+3*z[1][1])/4,
                      'Nlo':(z[0][0]-z[1][1])/4,
                      'Nhi':(z[0][1]-z[1][0])/4}

    from verify_extended_cyclic import enclosures
    cyclic = enclosures()
    for rec in cyclic:
        n=rec['n'];clo,chi=Q(rec['lower']),Q(rec['upper'])
        jlo,jhi=moments[n]['Jlo'],moments[n]['Jhi']
        moments[n].update({'Ilo':(jlo+2*clo)/3,'Ihi':(jhi+2*chi)/3,
                          'Olo':(jlo-chi)/3,'Ohi':(jhi-clo)/3})
    supports={'I':(-IU,U),'O':(-OMIN,OMAX),'N':(-V,W)}

    filter_records = []
    for name,p in FILTERS.items():
        c = [sum(p[i]*p[k-i] for i in range(5) if 0<=k-i<5) for k in range(9)]
        upper = sum(a*moments[k+4][name[0]+('hi' if a>=0 else 'lo')] for k,a in enumerate(c))
        rays = [(-1,-supports[name[0]][0])] if name[1]=='-' else [(1,supports[name[0]][1])]
        for sign,cap in rays:
            shifted = [sum(comb(i,j)*a*sign**i*cap**(i-j)
                           for i,a in enumerate(p) if i>=j) for j in range(5)]
            check(f'{name}, sign {sign}: entire exterior ray', all(x>0 for x in shifted)
                  and cap**4*shifted[0]**2 > upper)
        filter_records.append({'name':name,'quartic':p,'moment_sum_upper':str(upper)})

    # Polynomial duals are fixed rational inputs. Bernstein subdivision
    # proves their sign at every point in the support, including contacts.
    lp = {}
    polynomial_records = []
    for rec in json.loads((ROOT/'independent_results/resolved_moment_polynomials.json').read_text()):
        m, direction, sector = rec['moment'],rec['direction'],rec['sector']
        c = list(map(Q,rec['coefficients']))
        check(f'polynomial {sector},{m},{direction}: degree and moment domain',
              m>=12 and len(c)==9 and direction in ('upper','lower') and sector in ('I','O','N'))
        g = c+[Q(0)]*(m-3-len(c))
        g[-1] -= 1
        if direction=='lower':
            g = [-x for x in g]
        proof = nonnegative_on_interval(g,*supports[sector])
        value = sum(a*moments[k+4][sector+('hi' if (a>=0)==(direction=='upper') else 'lo')]
                    for k,a in enumerate(c))
        check(f'polynomial {sector},{m},{direction}: stored bound reproduced', value==Q(rec['bound']))
        lp[sector,m,direction] = (rounded(value,direction=='upper') if value>=0
                                     else -rounded(-value,direction!='upper'))
        polynomial_records.append({'sector':sector,'moment':m,'direction':direction,'bound':str(value),**proof})

    mI, mO, mN = [rounded(moments[12][s+'hi']) for s in ('I','O','N')]
    check('twelfth-moment cap domains', 0<U**12<mI<2*U**12 and
          0<OMAX**12<mO<2*OMAX**12 and 0<V**12<mN<2*V**12)

    def I(m):
        capped=power(U,m)+real_power(mI-U**12,Q(m,12))
        return min(capped,lp.get(('I',m,'upper'),capped))

    def O(m):
        capped=power(OMAX,m)+real_power(mO-OMAX**12,Q(m,12))
        return min(capped,lp.get(('O',m,'upper'),capped))

    def J(m):
        return I(m)+2*O(m)

    def N(m):
        capped = power(V,m)+real_power(mN-V**12,Q(m,12))
        return min(capped,lp.get(('N',m,'upper'),capped))

    def Z(m):
        return J(m)+3*N(m)

    trial = json.loads((ROOT/'independent_results/trial88.json').read_text())
    tu,tv = int(trial['one_bond_numerator']),int(trial['norm'])
    check('trial88: negative shifted Rayleigh quotient', trial['length']==88 and tv>0
          and 500000*tu+700741*tv==int(trial['shift_comparison_integer'])<0)

    def seed(m,t,n):
        D = significant_upper(real_power(Z(m),t))
        EP = significant_upper(real_power(J(m)-lp['N',m,'lower'],t))
        EC = significant_upper(real_power(I(m)-lp.get(('O',m,'lower'),Q(0)),t))
        Icap, Jcap = (D+3*EP+8*EC)/12, (D+3*EP)/4
        exponent = Q(120,m)
        check(f'seed {m},{t}: unique modulus dominance',
              m%2==0 and 12<=m<=n and t>=1 and
              0<Icap<=Jcap<=D and 2*real_power(D/2,exponent)<1)
        # Decimal bisection proposes v; the rational comparison below proves it.
        with localcontext() as ctx:
            ctx.prec=80
            dd,ii,jj,rr=map(decimal,(D,Icap,Jcap,exponent))
            zero=decimal(Q(0))
            lo,hi=dd/2,min(decimal(Q(1)),ii)
            for _ in range(200):
                s=(lo+hi)/2
                values=[x**rr+2*(y/2)**rr+3*((dd-s-x-y)/3)**rr
                        for x,y in [(zero,zero),(ii-s,zero),(ii-s,jj-ii),(zero,jj-s)]]
                if s**rr+max(values)<1:
                    lo=s
                else:
                    hi=s
            v=Q(int(lo*10**24)-1,10**24)
        check(f'seed {m},{t}: leading moment from trial120',
              D/2<v<=min(1,Icap) and real_power(v,exponent)+residual(v,exponent,D,Icap,Jcap)<1)
        exponent=Q(n,m)
        denominator=real_power(v,exponent,False)
        i=significant_upper(real_power(Icap-v,exponent)/denominator)
        j=significant_upper(max(2*real_power((Jcap-v)/2,exponent),
                              real_power(Icap-v,exponent)+2*real_power((Jcap-Icap)/2,exponent))/denominator)
        r=significant_upper(residual(v,exponent,D,Icap,Jcap)/denominator)
        q=significant_upper(defect(real_power(Z(2*n)-1,t)))
        check(f'seed {m},{t}: sector and purity domains', 0<i<=j<=r<1 and 0<q<1)
        return {'m':m,'t':t,'n':n,'beta':BETA*t,'D':D,'I':Icap,'J':Jcap,
                'v':v,'i':i,'j':j,'r':r,'q':q}

    initial = seed(28,Q(41,20),44)
    short_seeds = {m:seed(m,Q(2),60) for m in (18,20,22,24,26,28,30,32)}
    rows, levels = [], []
    i,j,r,q = [initial[k] for k in ('i','j','r','q')]
    for k in range(10):
        n,beta=44*2**k,BETA*Q(41,20)*2**k
        row={'k':k,'n':n,'beta':beta,'i':i,'j':j,'r':r,'p':defect(r),'q':q}
        rows.append(row)
        if k==9:
            break
        dd=2*r+r*r
        dj=(dd+3*(2*j+j*j))/4
        di=(dd+3*(2*j+j*j)+8*(2*i+i*i))/12
        check(f'row {k}: doubled-temperature dominance', (1+dd)**2/2<1-q)

        def R(h):
            return max((dd+h)**2/3,
                       (di+h)**2+(dd-di)**2/3,
                       (di+h)**2+(dj-di)**2/2+(dd-dj)**2/3,
                       (dj+h)**2/2+(dd-dj)**2/3)

        with localcontext() as ctx:
            ctx.prec=560
            dd0,di0,dj0,qq=map(decimal,(dd,di,dj,q))
            def rd(h):
                return max((dd0+h)**2/3,(di0+h)**2+(dd0-di0)**2/3,
                           (di0+h)**2+(dj0-di0)**2/2+(dd0-dj0)**2/3,
                           (dj0+h)**2/2+(dd0-dj0)**2/3)
            lo,hi=decimal(Q(0)),qq+dd0*dd0
            while 2*hi-hi*hi<=qq+rd(hi):
                hi*=2
                if hi>=(1-dd0)/2:
                    raise ArithmeticError('No leading-moment proposal.')
            for _ in range(160):
                mid=(lo+hi)/2
                if 2*mid-mid*mid>qq+rd(mid):
                    hi=mid
                else:
                    lo=mid
            h=significant_upper(Q(hi)*Q(1000000000001,1000000000000))
        v=1-h
        check(f'row {k}: sector-resolved leading lower bound',
              (1+dd)/2<v<1 and q+R(h)<2*h-h*h)
        inext=significant_upper((di+h)**2/v**2)
        jnext=significant_upper(max((dj+h)**2/2,(di+h)**2+(dj-di)**2/2)/v**2)
        rnext=significant_upper(R(h)/v**2)
        pnext=defect(rnext)
        qnext=significant_upper(f(2*q-q*q+pnext*(1-q)**2))
        check(f'row {k}: propagated sector domains', 0<inext<=jnext<=rnext<1 and 0<qnext<1)
        row.update({'h':h,'dD':dd,'dI':di,'dJ':dj})
        s=(dd+h)/v
        c,rho0,rho1=root(v,n,False),root(r,n),root(s,n)
        check(f'level {k}: interpolation domains', 0<c<1 and 0<rho0<1 and 0<rho1<1)
        levels.append({'name':str(k),'n':n,'beta':beta,'c':c,'r':r,'s':s,'rho0':rho0,'rho1':rho1})
        i,j,r,q=inext,jnext,rnext,qnext
        print(f'row {k}: certified',flush=True)

    def interval_lower(level,A,B):
        if not level['n']<=A<=B:
            return Q(0)
        a=rounded(level['r']*power(level['rho0'],A-level['n']))
        b=rounded(level['s']*power(level['rho1'],A-level['n']))
        if b>=1:
            return Q(0)
        return rounded(power(level['c'],B,False)*(1-b)/(1+a)**2,False)

    thresholds={l['name']:exp_upper(l['beta']*TARGET) for l in levels}
    thresholds={k:(1+x*x)/(1+x)**2 for k,x in thresholds.items()}

    def short_lower(L):
        denominator=(Z(L) if L%2==0 else
                     J(L)+3*min(mN*power(W,L-12),lp.get(('N',L,'upper'),mN*power(W,L-12))))
        if denominator<=0:
            raise ArithmeticError('Nonpositive partition-function upper bound.')
        candidates=[]
        for m,ss in short_seeds.items():
            if m>L:
                continue
            rr=Q(L,m)
            numerator=real_power(ss['v'],rr,False)
            if L%2:
                numerator-=residual(ss['v'],rr,ss['D'],ss['I'],ss['J'])
            candidates.append((rounded(max(Q(0),numerator)/denominator**2,False),m))
        return max(candidates)

    # Explicit checks for the short-length ladder. Larger lengths will be
    # supplied by the strongest bound; no unchecked monotonicity in L is used.
    short=[]
    for start,target in [(18,Q(1,50)),(20,Q(9,100)),(22,Q(3,25))]:
        for L in (start,start+1):
            value,m=short_lower(L)
            check(f'short L={L}: gap > {target}', value>Q(1,2) and (1+exp_upper(BETA*target)**2)/(1+exp_upper(BETA*target))**2<value)
            short.append({'L':L,'target':target,'m':m,'purity_lower':value})

    value,m=short_lower(18)
    check('short L=18: gap > 2/25', value>Q(1,2) and (1+exp_upper(BETA*Q(2,25))**2)/(1+exp_upper(BETA*Q(2,25)))**2<value)
    short.append({'L':18,'target':Q(2,25),'m':m,'purity_lower':value})

    tail_start=3*rows[-1]['n']//2
    A,intervals=24,[]
    short_threshold=exp_upper(BETA*TARGET)
    short_threshold=(1+short_threshold**2)/(1+short_threshold)**2
    while A<tail_start:
        candidates=[]
        for level in levels:
            threshold=thresholds[level['name']]
            if interval_lower(level,A,A)<=threshold:
                continue
            low,high=A,tail_start-1
            while low<high:
                mid=(low+high+1)//2
                if interval_lower(level,A,mid)>threshold:
                    low=mid
                else:
                    high=mid-1
            candidates.append((low,level))
        if not candidates:
            if A>150:
                raise ArithmeticError(f'Uncovered length {A}.')
            value,m=short_lower(A)
            check(f'short L={A}: gap > {TARGET}', Q(1,2)<value<1 and value>short_threshold)
            short.append({'L':A,'target':TARGET,'m':m,'purity_lower':value})
            A+=1
            continue
        B,level=max(candidates,key=lambda item:item[0])
        value=interval_lower(level,A,B)
        check(f'interval {A}..{B}: gap > {TARGET}', Q(1,2)<value<1 and value>thresholds[level['name']])
        intervals.append({'first':A,'last':B,'level':level['name'],'beta':level['beta'],'purity_lower':value})
        A=B+1
    lengths={x['L'] for x in short if x['target']==TARGET}
    for interval in intervals:
        lengths.update(range(interval['first'],interval['last']+1))
    check('every finite integer length covered', lengths==set(range(24,tail_start)))

    tail=rows[-1]
    w0=significant_upper(tail['q']*Q(101,100))
    C,B,xmax=Q(6),Q(15,2),Q(1,100)
    check('tail starting invariant', tail['p']**3<=w0**2 and tail['q']<=w0 and 0<w0<=xmax**3)
    ac,qc=2+xmax,2+3*xmax
    check('tail invariant propagates', ac**2/(2*(1-ac*xmax**2)**2)<=3 and
          qc**2/(2*(1-qc*xmax**3)**2)<=3 and 3**3<C**2 and 3<=C)
    check('tail interpolation coefficients', xmax**2<=Q(1,3) and ac*xmax**2<=Q(1,3)
          and ac**3<9 and 2*(1+3*xmax)+3+2<B and B*xmax**3<Q(1,2))
    E=exp_upper(tail['beta']*TARGET)
    check('tail exponential comparisons', E*C*w0<1 and E*B*w0/(1-B*w0)<1)
    check('tail all-integer cover', tail['n']%2==0 and tail_start==3*tail['n']//2)

    def serialize(x):
        if isinstance(x,Q):
            return str(x)
        if isinstance(x,dict):
            return {str(k):serialize(v) for k,v in x.items()}
        if isinstance(x,list):
            return list(map(serialize,x))
        return x
    result={'source_commit':'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
            'statement':'Conditional on the cited premises: unique ground state and gamma_L > 29/200 for every integer L >= 24, J=1',
            'additional_bounds':[{'gap':'.02','minimum_length':18},{'gap':'.09','minimum_length':20},
                                 {'gap':'.12','minimum_length':22}],
            'isolated_short_bound':'gamma_18 > .08, unique ground state',
            'cyclic_trace_enclosures':cyclic,'moment_intervals':moments,'filters':filter_records,'polynomial_certificates':polynomial_records,
            'caps':{'I_negative_modulus':IU,'I_positive':U,'O_negative_modulus':OMIN,'O_positive':OMAX,'N_negative_modulus':V,'N_positive':W},
            'seed':initial,'short_seeds':list(short_seeds.values()),'rows':rows,'levels':levels,
            'short_lengths':short,'finite_intervals':intervals,
            'tail':{'start':tail_start,'n0':tail['n'],'beta0':tail['beta'],'w0':w0,'C':C,'B':B},
            'root_directions':'Every Decimal proposal is accepted by directed rational integer-power comparisons',
            'exponential_bounds':'Rational Taylor upper bound after halving, followed by 40-digit upward-rounded squaring',
            'product_rounding':'Outward on a 10^-1000 grid; recurrence bounds rounded upward to 15 significant digits',
            'checks':checks,'success':True}
    (ROOT/'independent_results/resolved_refinement.json').write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(f'PASS: {len(checks)} exact checks; {len(intervals)} finite intervals; tail starts at {tail_start}.')
    print('gamma_L > 0.145 for every integer L >= 24; unique ground state; conditional on cited premises.')
    print('Finite intervals:',[(x['first'],x['last'],x['level']) for x in intervals])
    print('Short main lengths:',sorted(x['L'] for x in short if x['target']==TARGET))


if __name__=='__main__':
    main()
