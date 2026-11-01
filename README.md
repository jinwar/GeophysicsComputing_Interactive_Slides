# Geophysical Computing: Interactive Slides

Quarto + Quarto Live lectures for GPGN 436/536, Ge Jin, Colorado School of Mines.

## Regression

The initial module combines the 59-slide `09 Regression.pptx` teaching sequence with runnable Python examples. It covers linear and polynomial least squares, coefficient uncertainty, 2-D fitting, weighting, robust fitting, regularization, interpolation-based smoothing, nonlinear optimization, and posterior sampling. There are 50 content slides plus a title slide and 16 editable demonstrations.

The sequence for polynomial regression is explanation, fitting demonstration, coefficient uncertainty, then repeated-fit demonstration. All added measurement noise is Gaussian. Uniform random draws in search methods sample the parameter domain or make acceptance decisions; they are not measurement noise.

The three lab topics are preserved. The original slides supplied model equations and figures rather than downloadable numeric datasets, so the interactive labs use explicitly synthetic data and expanded prompts.

## Publish

In **Settings → Pages → Build and deployment**, choose **GitHub Actions**. The included workflow tests the Python examples, renders the presentation, and publishes `_site` on pushes to `main`. Pull requests build and test without deploying.

## Local preview

Install Quarto 1.10.20. From this directory:

```sh
quarto add r-wasm/quarto-live@12fb30a5dd5e1bbe6d8ace96795eb1c114c80447 --no-prompt
quarto preview
```

The presentation uses `engine: markdown`. Python execution happens in the browser through Pyodide, rather than during Quarto rendering. NumPy and Matplotlib download on first load. Internet access is expected; this is not a self-contained offline presentation.

To test the examples locally:

```sh
python -m pip install numpy matplotlib
MPLBACKEND=Agg python tests/check_examples.py
```

## Teaching and editing

Edit `regression.qmd` for slide text, equations, and live code. Each demonstration works after shared setup has loaded without requiring previous demonstrations to run. The hidden setup block contains a copy of `helpers.py`; keep them synchronized (the test checks this). Helpers contain plot formatting and numerical gradient/Hessian calculations. Core fitting and search loops remain visible in the demonstrations.

Students can change code and select Run Code, or restore original code with Start Over. Their edits affect their browser session only. Click outside an editor before using keyboard slide navigation. Long editors scroll. Reloading resets the runtime. GitHub/Canvas submissions remain separate from browser experimentation.

## Mathematical corrections during adaptation

- Normal-equation derivative signs and polynomial coefficient ordering are consistent.
- Coefficient uncertainty uses covariance propagation and repeated Gaussian-noise fits.
- Rank deficiency is distinguished from having more equations than unknowns.
- Regularization uses `lambda` in the objective and `sqrt(lambda)` in augmented rows.
- Grid search finds the best sampled grid point, not an exact continuous global minimum.
- The original improvement-only search labeled MCMC is replaced by a Metropolis sampler with stated Gaussian likelihood and bounded uniform prior. The short demonstration starts near the synthetic truth and does not establish global uncertainty.
- Newton's method includes the one-half factor in its quadratic expansion and explains its local convergence limitations.

## Sources

Ge Jin, `09 Regression.pptx`; course regression notebook co-developed by Ge Jin and Jeff Shragge; Menke (2018), *Geophysical Data Analysis: Discrete Inverse Theory*; Kreyszig, *Advanced Engineering Mathematics*, 10th edition. Quarto Live is pinned to commit `12fb30a5dd5e1bbe6d8ace96795eb1c114c80447` and installed by the build workflow under its upstream license.
