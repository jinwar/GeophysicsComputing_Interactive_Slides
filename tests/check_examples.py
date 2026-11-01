"""Execute every live Python block and check the central uncertainty calculation."""
from pathlib import Path
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
source = Path('regression.qmd').read_text()
blocks = re.findall(r'```\{pyodide\}\n(.*?)\n```', source, re.S)
setup = blocks[0]
assert setup.removeprefix("#| include: false\n").strip() == Path("helpers.py").read_text().strip()
# Every demo must work after setup, without running previous demos.
for i, block in enumerate(blocks[1:], 1):
    scope = {}
    exec(setup, scope)
    exec(block, scope)
    plt.close('all')
    print(f'PASS demo {i}')
x=np.linspace(-2,2,100); A=np.vander(x,5); G=np.linalg.pinv(A)
sigma=3.; rng=np.random.default_rng(42)
noise=rng.normal(0,sigma,(100,5000))
C=np.linalg.lstsq(A,noise,rcond=None)[0]
predicted=sigma*np.sqrt(np.sum(G**2,axis=1))
assert np.allclose(C.std(axis=1,ddof=1),predicted,rtol=.06)
L=np.diff(np.eye(5),axis=0); lam=2.3
As=np.vstack([A,np.sqrt(lam)*L])
assert np.allclose(As.T@As,A.T@A+lam*L.T@L)
print(f'PASS: {len(blocks)-1} independent demos, coefficient uncertainty and regularization scaling')
