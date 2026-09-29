"""Pure ranking fusion; candidate IDs always address an image/caption pair."""
from fractions import Fraction
import numpy as np


def rank_scores(scores):
    if scores.ndim != 2 or not np.isfinite(scores).all():
        raise ValueError('Expected a finite query-by-candidate score matrix')
    # Candidate columns are sorted by ID, so stable sorting fixes score ties.
    order = np.argsort(-scores, axis=1, kind='stable')
    ranks = np.empty(order.shape, dtype=np.int16)
    np.put_along_axis(ranks, order, np.arange(1, scores.shape[1] + 1)[None], axis=1)
    return ranks


def fuse(ranks, weights, c, window):
    ranks = np.asarray(ranks)
    weights = np.asarray(weights, dtype=np.float64)
    if ranks.ndim != 3 or ranks.shape[0] != len(weights):
        raise ValueError('Expected branch-by-query-by-candidate ranks')
    if np.any(weights < 0) or not np.isclose(weights.sum(), 1):
        raise ValueError('Nonnegative branch weights must sum to one')
    if not np.all(np.sort(ranks, axis=-1) == np.arange(1, ranks.shape[-1] + 1)):
        raise ValueError('Each rank row must be a permutation of 1..N')
    c = float(Fraction(str(c)))
    if c <= 0 or not 1 <= window <= ranks.shape[-1]:
        raise ValueError('Invalid C/window')
    votes = np.sum(weights[:, None, None] * (c + 1) / (c + ranks) * (ranks <= window), axis=0)
    mean_rank = np.sum(weights[:, None, None] * ranks, axis=0)
    ids = np.broadcast_to(np.arange(ranks.shape[-1]), votes.shape)
    # Round at 12 decimals only to remove floating arithmetic tie noise.
    order = np.lexsort((ids, mean_rank, -np.round(votes, 12)), axis=-1)
    return order, votes


def metrics(order, truth):
    truth = np.asarray(truth)
    if truth.shape != (len(order),):
        raise ValueError('One ground-truth candidate column required per query')
    return {f'top{k}': float(np.any(order[:, :k] == truth[:, None], axis=1).mean())
            for k in range(1, 11)}
