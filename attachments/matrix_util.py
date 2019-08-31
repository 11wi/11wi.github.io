import numpy as _np
from multiprocessing import RawArray as _RawArray
from multiprocessing import Pool as _Pool
from functools import partial as _partial
from numba import njit


def nonzero(array):
    index_array = _np.nonzero(array)[0]
    return index_array


def inverse(mat):
    return _np.ascontiguousarray(_np.linalg.inv(mat))


def cholesky(mat):
    return _np.linalg.cholesky(mat)


def normal(mu=0, sd=1, size=1):
    if isinstance(size, tuple):
        size = [int(i) for i in size]
    else:
        size = int(size)
    return _np.random.normal(loc=mu, scale=sd, size=size)


def wishart(nu, scale):
    """
    :param nu: df
    :param scale: scale matrix (must be positive definite)
    :return: covariance matrix (symmetric positive definite)
    referred from
    https://gist.github.com/jfrelinger/2638485
    http://thaines.com/content/misc/gaussian_conjugate_prior_cheat_sheet.pdf
    """
    dim = scale.shape[1]
    chol = cholesky(scale)
    Lambda = _np.zeros((dim, dim))

    for i in range(dim):
        for j in range(i + 1):
            if i == j:
                Lambda[i, j] = _np.random.chisquare(nu - (i + 1) + 1) ** .5
            else:
                Lambda[i, j] = normal(0, 1, 1).item()
    return chol @ Lambda @ Lambda.T @ chol.T


def mean_latent(latent_u):
    u_bar = _np.sum(latent_u, axis=0).reshape(-1, 1) / latent_u.shape[0]
    return u_bar


def cov_latent(latent_u):
    s_bar = _np.cov(latent_u, rowvar=False, bias=True)
    return s_bar


def user_based_item_rating(n, rating_matrix):
    items = nonzero(rating_matrix[n, :])
    rating = rating_matrix[n, :][items].reshape(-1, 1)
    return items, rating


def item_based_user_rating(n, rating_matrix):
    users = nonzero(rating_matrix[:, n])
    rating = rating_matrix[:, n][users].reshape(-1, 1)
    return users, rating


def update_hyperparam(latent_u, mu0, w0, b0):
    n_sample = latent_u.shape[0]
    u_bar = mean_latent(latent_u)
    s_bar = cov_latent(latent_u)

    mu0_star = ((b0 * mu0) + (n_sample * u_bar)) / (b0 + n_sample)

    w0_u_inv = inverse(w0)
    w0_star = inverse(w0_u_inv + n_sample * s_bar + (b0 * n_sample) / (b0 + n_sample) * (mu0 - u_bar) @ (mu0 - u_bar).T)

    return mu0_star, w0_star


def sampling_params(n_latent, n_sample, mu0_star, w0_star, b0):
    _sigma_u = wishart(nu=n_latent + n_sample, scale=w0_star)
    sigma_u = (_sigma_u + _sigma_u.T) / 2
    lambda_u = inverse(b0 + n_sample * sigma_u)
    mu_u = mu0_star + cholesky(lambda_u) @ normal(size=(n_latent, 1))
    return mu_u, lambda_u, sigma_u


def _sampling_latent(latent_v_i, mu_u, lambda_u, sigma_u, target_ratings, n_latent, b0):
    lambda_star_u = inverse(sigma_u + b0 * latent_v_i.T @ latent_v_i)
    mean_star_u = lambda_star_u @ (b0 * latent_v_i.T @ target_ratings + lambda_u @ mu_u)
    posterior_sample_u = mean_star_u + cholesky(lambda_star_u) @ normal(size=(n_latent, 1))
    return posterior_sample_u.reshape(-1)


def sampling_latent_user(each, mu_u, lambda_u, sigma_u, latent_v, rating_matrix, n_latent, b0):
    find_user = user_based_item_rating(each, rating_matrix)
    target_items, target_ratings = find_user[0], find_user[1]
    latent_v_i = latent_v[target_items]
    each_user_latent = _sampling_latent(latent_v_i, mu_u, lambda_u, sigma_u, target_ratings, n_latent, b0)
    return each_user_latent


def sampling_latent_item(each, mu_u, lambda_u, sigma_u, latent_v, rating_matrix, n_latent, b0):
    find_item = item_based_user_rating(each, rating_matrix)
    target_user, target_ratings = find_item[0], find_item[1]
    latent_v_i = latent_v[target_user]
    each_item_latent = _sampling_latent(latent_v_i, mu_u, lambda_u, sigma_u, target_ratings, n_latent, b0)
    return each_item_latent


_parallel_env = {}


def _init_parallel(shared_array, latent_shape):
    _parallel_env['latent'] = shared_array
    _parallel_env['shape'] = latent_shape


def _init_args(n_sample_u, n_latent):
    shape_latent = (n_sample_u, n_latent)
    shared_latent = _RawArray('d', int(n_sample_u * n_latent))
    return shape_latent, shared_latent


def _pool_map(n_core, parallel_function, n_sample_u, shape_latent, shared_latent):
    with _Pool(processes=n_core, initializer=_init_parallel, initargs=(shared_latent, shape_latent)) as pool:
        pool.map(parallel_function, iterable=_np.arange(n_sample_u))
        latent = _np.frombuffer(shared_latent, dtype=_np.float64).reshape(shape_latent)
    return latent


def parallel_sampling_latent_user(n_core, mu_u, lambda_u, sigma_u, latent_v, rating_matrix, n_sample_u,
                                  n_latent, b0):
    """
    https://research.wmz.ninja/articles/2018/03/on-sharing-large-arrays-when-using-pythons-multiprocessing.html
    """
    shape_latent, shared_latent = _init_args(n_sample_u, n_latent)
    f = _partial(_parallel_sampling_latent_user, mu_u=mu_u, lambda_u=lambda_u, sigma_u=sigma_u, latent_v=latent_v,
                 rating_matrix=rating_matrix, n_latent=n_latent, b0=b0)
    latent = _pool_map(n_core, f, n_sample_u, shape_latent, shared_latent)
    return latent


def parallel_sampling_latent_item(n_core, mu_v, lambda_v, sigma_v, latent_u, rating_matrix, n_sample_v,
                                  n_latent, b0):
    """
    https://research.wmz.ninja/articles/2018/03/on-sharing-large-arrays-when-using-pythons-multiprocessing.html
    """
    shape_latent, shared_latent = _init_args(n_sample_v, n_latent)
    f = _partial(_parallel_sampling_latent_item, mu_v=mu_v, lambda_v=lambda_v, sigma_v=sigma_v, latent_u=latent_u,
                 rating_matrix=rating_matrix, n_latent=n_latent, b0=b0)
    latent = _pool_map(n_core, f, n_sample_v, shape_latent, shared_latent)
    return latent


def _parallel_sampling_latent_user(each, mu_u, lambda_u, sigma_u, latent_v, rating_matrix, n_latent, b0):
    updated = sampling_latent_user(each, mu_u, lambda_u, sigma_u, latent_v, rating_matrix, n_latent, b0)
    latent = _np.frombuffer(_parallel_env['latent']).reshape(_parallel_env['shape'])
    latent[each, :] = updated


def _parallel_sampling_latent_item(each, mu_v, lambda_v, sigma_v, latent_u, rating_matrix, n_latent, b0):
    updated = sampling_latent_item(each, mu_v, lambda_v, sigma_v, latent_u, rating_matrix, n_latent, b0)
    latent = _np.frombuffer(_parallel_env['latent']).reshape(_parallel_env['shape'])
    latent[each, :] = updated
