"""Optional floating-point filter search; NOT part of the proof.

Requires NumPy and SciPy. This local search inspired the fixed integer
coefficients checked by verify_spectral_refinement.py. Neither optimizer
success nor numerical endpoint roots establish a spectral bound or an
optimality claim. Small variations in numerical libraries may change the
candidate; the exact checker never calls this file.
"""
import numpy as np
from scipy.optimize import minimize


def main():
    raw = np.array([(124885379,65757),(2925,2960742),(12870614,286599),
                    (54069,1920414),(4639283,510140),(195455,1514846),
                    (2654823,675419),(377629,1314544),(1900547,787405)],float)/1e6
    moments = (raw[:,0]+3*raw[:,1])/4
    target, eps = 1.00139, 30e-6

    def objective(p):
        coefficients = np.convolve(p,p)
        upper = coefficients@moments+eps*np.sum(np.abs(coefficients))
        return upper/(target**4*np.polynomial.polynomial.polyval(target,p)**2)

    old = np.array([7,17,-280,-185,1000],float)
    old /= np.polynomial.polynomial.polyval(target,old)
    rng = np.random.default_rng(12345)
    best = None
    for i in range(24):
        initial = old if i == 0 else old+rng.normal(0,.5,5)
        result = minimize(objective,initial,method='BFGS',
                          options={'gtol':1e-10,'maxiter':2000})
        if best is None or result.fun < best.fun:
            best = result
    p = best.x/np.polynomial.polynomial.polyval(target,best.x)
    print('Exploration only: no rigorous or global-optimality claim.')
    print('Candidate normalized quartic:',p)
    print('Rounded candidate at scale 10^6:',np.rint(1e6*p).astype(int).tolist())
    print('Objective at the former cap:',best.fun)
    print('Use verify_spectral_refinement.py for the fixed, exact certificate.')


if __name__ == '__main__':
    main()
