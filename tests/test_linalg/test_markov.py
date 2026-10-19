import numpy as np
import pytest

from puremacro._linalg import markov_stationary_gth


def test_markov_stationary_gth_basic():
    # 2x2 ergodic chain
    P = np.array([[0.5, 0.5], [0.2, 0.8]])
    pi = markov_stationary_gth(P)
    np.testing.assert_allclose(pi, [0.28571429, 0.71428571], atol=1e-7)

    # 3x3 ergodic chain
    P = np.array([[0.1, 0.6, 0.3], [0.2, 0.5, 0.3], [0.4, 0.4, 0.2]])
    pi = markov_stationary_gth(P)
    # Check that it's a left eigenvector for eigenvalue 1
    np.testing.assert_allclose(pi @ P, pi, atol=1e-12)
    np.testing.assert_allclose(pi.sum(), 1.0)
    assert np.all(pi >= 0)


def test_markov_stationary_gth_single_closed_class():
    # State 1 is absorbing
    P = np.array([[0.5, 0.5, 0.0], [0.0, 1.0, 0.0], [0.0, 0.5, 0.5]])
    pi = markov_stationary_gth(P)
    np.testing.assert_allclose(pi, [0.0, 1.0, 0.0])

    # States 1 and 2 form a closed communicating class, state 0 is transient
    P = np.array([[0.5, 0.25, 0.25], [0.0, 0.6, 0.4], [0.0, 0.3, 0.7]])
    pi = markov_stationary_gth(P)
    assert pi[0] == 0.0
    np.testing.assert_allclose(pi @ P, pi, atol=1e-12)
    np.testing.assert_allclose(pi.sum(), 1.0)


def test_markov_stationary_gth_multiple_closed_classes():
    # Two closed classes: {0} and {1, 2}
    P = np.array([[1.0, 0.0, 0.0], [0.0, 0.5, 0.5], [0.0, 0.5, 0.5]])
    with pytest.raises(ValueError, match="stationary distribution is not unique"):
        markov_stationary_gth(P)

    # Two absorbing states
    P = np.array([[1.0, 0.0, 0.0], [0.5, 0.0, 0.5], [0.0, 0.0, 1.0]])
    with pytest.raises(
        ValueError,
        match="stationary distribution is not unique: the chain has 2 closed classes",
    ):
        markov_stationary_gth(P)


def test_markov_stationary_gth_extreme_probabilities():
    # Very small probabilities, testing robustness of GTH
    eps = 1e-15
    P = np.array([[1.0 - eps, eps], [eps, 1.0 - eps]])
    pi = markov_stationary_gth(P)
    np.testing.assert_allclose(pi, [0.5, 0.5], atol=1e-12)

    # Identity matrix has N closed classes
    P = np.eye(4)
    with pytest.raises(ValueError, match="stationary distribution is not unique"):
        markov_stationary_gth(P)
