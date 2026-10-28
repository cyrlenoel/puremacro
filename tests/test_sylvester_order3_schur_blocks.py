"""Regression tests for the order-3 Real-Schur Sylvester solver.

Covers the mixed (1x1, 1x1, 2x2) Schur block, whose coefficient must be
T1[0,0] * T2[0,0] * T3, and the near-unit-root scalar blocks that rely on
iterative refinement in ``_solve_scalar_block``.
"""
import numpy as np
import pytest

from puremacro.dsge._sylvester import solve_order3_sylvester_schur


def _residual(A_hat, A_plus, h_x, K, X):
    hk = np.kron(np.kron(h_x, h_x), h_x)
    return np.max(np.abs(A_hat @ X + A_plus @ X @ hk + K))


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_mixed_real_and_complex_schur_blocks(seed):
    rng = np.random.default_rng(seed)
    N, n_x = 4, 3
    # h_x with one real eigenvalue and one complex pair -> 1x1 and 2x2 Schur blocks
    r, a, b = 0.6, 0.5, 0.3
    core = np.array([[r, 0.0, 0.0], [0.0, a, -b], [0.0, b, a]])
    Q, _ = np.linalg.qr(rng.standard_normal((n_x, n_x)))
    h_x = Q @ core @ Q.T
    A_hat = rng.standard_normal((N, N)) + 4.0 * np.eye(N)
    A_plus = 0.3 * rng.standard_normal((N, N))
    K = rng.standard_normal((N, n_x**3))
    X = solve_order3_sylvester_schur(A_hat, A_plus, h_x, K)
    assert _residual(A_hat, A_plus, h_x, K, X) < 1e-11


def test_near_unit_root_scalar_blocks_are_refined():
    rng = np.random.default_rng(7)
    N, n_x = 3, 2
    h_x = np.diag([0.999, 0.97])
    A_plus = rng.standard_normal((N, N))
    # A_hat + tau * A_plus nearly singular for tau close to 1
    A_hat = -A_plus + 1e-6 * rng.standard_normal((N, N))
    K = rng.standard_normal((N, n_x**3))
    X = solve_order3_sylvester_schur(A_hat, A_plus, h_x, K)
    scale = max(1.0, np.max(np.abs(X)))
    assert _residual(A_hat, A_plus, h_x, K, X) / scale < 1e-12
