"""Shared plotting and numerical helpers for Module 09. All data are synthetic."""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.figsize': (8, 3), 'figure.dpi': 100,
                     'font.size': 11, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.grid': True,
                     'grid.alpha': .18})

def plot_fit(x, y, xp, prediction, truth=None):
    plt.close('all')
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=14, alpha=.65, label='Observations')
    ax.plot(xp, prediction, color='#c0502d', lw=2, label='Fit')
    if truth is not None:
        ax.plot(xp, truth, 'k--', lw=1.3, label='True relation')
    ax.set(xlabel='x', ylabel='y')
    ax.legend(loc='best', fontsize=9)
    fig.tight_layout()
    plt.show()

def poly_data(sigma=3., n=100, seed=42):
    x = np.linspace(-2, 2, n)
    c = np.array([1., 2., 3., 4., 5.])
    y = np.polyval(c, x) + np.random.default_rng(seed).normal(0, sigma, n)
    return x, y, c

def nonlinear_data():
    x = np.linspace(0, 1, 100)
    truth = np.array([1.21, 1.54])
    sigma = .2
    y = model(truth, x) + np.random.default_rng(42).normal(0, sigma, x.size)
    return x, y, truth, sigma

def model(p, x):
    return np.sin(20*p[0]*x) + p[0]*p[1]

def objective(p):
    objective.evaluations += 1
    x, y, _, _ = nonlinear_data()
    return np.sum((model(p, x)-y)**2)

objective.evaluations = 0

def gradient(p, h=1e-5):
    eye = np.eye(len(p))*h
    return np.array([(objective(p+d)-objective(p-d))/(2*h) for d in eye])

def hessian(p, h=1e-4):
    eye = np.eye(len(p))*h
    return np.column_stack([(gradient(p+d)-gradient(p-d))/(2*h) for d in eye])

def plot_search(points, best, history=None, connect=True):
    plt.close('all')
    x, y, truth, _ = nonlinear_data()
    a = np.linspace(0, 2, 85)
    aa, bb = np.meshgrid(a, a)
    z = np.sum((np.sin(20*aa[...,None]*x)+aa[...,None]*bb[...,None]-y)**2, axis=-1)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    axes[0].contourf(aa, bb, np.log10(z+1e-9), 24, cmap='viridis')
    points = np.asarray(points)
    axes[0].plot(points[:,0], points[:,1], marker='.', linestyle='-' if connect else 'None',
                 color='#f4ab55', ms=2, lw=.6)
    axes[0].plot(*truth, 'wx', ms=9)
    axes[0].plot(*best, 'ro', ms=5)
    axes[0].set(xlabel='alpha', ylabel='beta', title='log10 SSE and search points', xlim=(0,2), ylim=(0,2))
    axes[1].plot(x, y, '.', alpha=.5, label='Data')
    axes[1].plot(x, model(best,x), color='#c0502d', label='Estimated')
    axes[1].plot(x, model(truth,x), 'k--', label='True')
    axes[1].set(xlabel='x', ylabel='y', title=f'Best SSE = {np.sum((model(best, x)-y)**2):.2f}')
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    plt.show()

def interpolation_matrix(x, xc, kind="cubic"):
    from scipy.interpolate import interp1d
    A = np.zeros((len(x), len(xc)))
    for i in range(len(xc)):
        x0 = np.zeros(len(xc))
        x0[i] = 1
        f = interp1d(xc, x0, kind=kind)
        A[:, i] = f(x)
    return A
