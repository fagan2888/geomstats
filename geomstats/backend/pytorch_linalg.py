"""Pytorch based linear algebra backend."""

import numpy as np
import scipy.linalg
import torch

import warnings
warnings.filterwarnings('ignore')  # NOQA


def sqrtm(sym_mat):
    # TODO(nina): This only works for symmetric real matrices.
    # Need to generalize to all matrices
    if sym_mat.dim() == 2:
        sym_mat = torch.unsqueeze(sym_mat, dim=0)
    assert sym_mat.dim() == 3
    n_sym_mats, mat_dim, _ = sym_mat.shape

    diag_log = torch.zeros((n_sym_mats, mat_dim, mat_dim))
    log = torch.zeros((n_sym_mats, mat_dim, mat_dim))
    for i in range(n_sym_mats):
        one_sym_mat = sym_mat[i]
        one_sym_mat = 0.5 * (one_sym_mat + one_sym_mat.t())
        eigenvalues, vectors = torch.symeig(one_sym_mat)
        diag_log = torch.diag(torch.log(eigenvalues))
        log_aux = torch.matmul(diag_log, vectors.t())
        log[i] = torch.matmul(vectors, log_aux)

    return log


def logm(x):
    np_logm = np.vectorize(
        scipy.linalg.logm, signature='(n,m)->(n,m)')(x)
    np_logm = np.real(np_logm)
    return torch.from_numpy(np_logm).float()


def expm(x):
    np_expm = np.vectorize(
        scipy.linalg.expm, signature='(n,m)->(n,m)')(x)
    return torch.from_numpy(np_expm)


def inv(*args, **kwargs):
    return torch.from_numpy(np.linalg.inv(*args, **kwargs))


def eigvalsh(*args, **kwargs):
    return torch.from_numpy(np.linalg.eigvalsh(*args, **kwargs))


def eigh(*args, **kwargs):
    eigs = np.linalg.eigh(*args, **kwargs)
    return torch.from_numpy(eigs[0]), torch.from_numpy(eigs[1])


def svd(*args, **kwargs):
    svds = np.linalg.svd(*args, **kwargs)
    return (torch.from_numpy(svds[0]),
            torch.from_numpy(svds[1]),
            torch.from_numpy(svds[2]))


def det(*args, **kwargs):
    return torch.from_numpy(np.linalg.det(*args, **kwargs))


def norm(x, ord=2, axis=None, keepdims=False):
    if axis is None:
        return torch.norm(x, p=ord)
    return torch.norm(x, p=ord, dim=axis)


def qr(*args, **kwargs):
    return torch.from_numpy(np.linalg.qr(*args, **kwargs))