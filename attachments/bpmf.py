from __future__ import absolute_import

import random

import numpy as np
import pandas as pd
from scipy import sparse

from model.matrix_utill import normal
from model.matrix_utill import inverse
from model.matrix_utill import cholesky
from model.matrix_utill import wishart
from model.matrix_utill import mean_latent
from model.matrix_utill import cov_latent
from model.matrix_utill import user_based_item_rating
from model.matrix_utill import item_based_user_rating

from sklearn.linear_model.base import BaseEstimator
from sklearn.linear_model.base import RegressorMixin

"""
paper from http://www.cs.toronto.edu/~rsalakhu/papers/bpmf.pdf
original matlab source code from http://www.utstat.toronto.edu/~rsalakhu/code_BPMF/bayespmf.m
also refering https://github.com/LoryPack/BPMF

refactored, reformulate and commented
"""

"""
capital letters are constant.

R is the ranking matrix (NxM, N=#users, M=#movies)
u matrices are NxD, while v matrices are MxD. (D is num of latent vector)

ALPHA and BETA is a explained as Gaussian observation noise (precision),
but fix them 2 because Normal-wishart hyperparam_update has denominator 2

mu0 is the average vector of latent matrix used in sampling the multivariate Normal variable

w0 is the DxD scale matrix in the Wishart sampling
nu0 is the number of degrees of freedom used in the Wishart sampling.
"""


class bpmf(BaseEstimator, RegressorMixin):

    def __init__(self, n_user, n_item, max_value, min_value=0, n_latent=5, maxepoch=50, early_stop_step=3,
                 validatset=None, alpha=2, b0=2, verbose=False):
        self.n_user = n_user
        self.n_item = n_item
        self.n_latent = n_latent
        self.maxepoch = maxepoch
        self.early_stop_step = early_stop_step
        self.min_value = min_value
        self.max_value = max_value
        self.validatset = validatset
        self.alpha = alpha
        self.b0 = b0
        self.verbose = verbose

    def fit(self, X, y, seed=None):
        random.seed(seed)
        np.random.seed(seed)

        self.trainset = np.c_[X, y].astype(int)
        self.user = self.trainset[:, 0]
        self.item = self.trainset[:, 1]
        self.train_rating = self.trainset[:, 2]
        self.global_mu = np.mean(self.train_rating)
        self.unbiased_rating = self.train_rating - self.global_mu
        self.rating_matrix = (sparse.coo_matrix((self.train_rating - self.global_mu,  # mean 0 rating
                                                 (self.user, self.item)),
                                                shape=(self.n_user, self.n_item))
                              .toarray())  # scipy sparse matrix slow when slicing

        self.latent_u = normal(mu=1, size=(self.n_user, self.n_latent))
        self.latent_v = normal(mu=1, size=(self.n_item, self.n_latent))

        # initialize now the hierarchical priors:
        self.mu0_u, self.mu0_v = np.zeros((self.n_latent, 1)), np.zeros((self.n_latent, 1))
        self.w0_u, self.w0_v = np.eye(self.n_latent), np.eye(self.n_latent)

        self.error_log = pd.DataFrame(columns=['n_latent', 'epoch', 'train_rmse', 'test_rmse'])
        self.model_out = dict()

        self.U = np.zeros((self.n_user, self.n_latent))
        self.V = np.zeros((self.n_item, self.n_latent))

        for epoch in range(1, self.maxepoch + 1):
            """
            hyperparam_update/posterior함수는 user, item 동일하고
            대략적인 형태는 이렇다
            :latent matrix U (multivariate):
            p(U | mu_u, sigma_u) = pi(N(U | Ui, mu_u, sigma_u-1))
            :hyperparam_update of U: 
            p(mu_u, lamba_u| U, nu0, w0) = N(mu_u|mu_0, (BETA0, lamba_u)-1) W(sigma_u | w0, nu0)
            :posterior of U:
            p(U | R, V, mu_u, nu_u, w_u) = pi(p(Ui | R, V, mu_u, nu_u, w_u)
            """

            """
            user prior
            """
            u_bar = mean_latent(self.latent_u)
            s_bar = cov_latent(self.latent_u)

            mu0_star = ((self.b0 * self.mu0_u) + (self.n_user * u_bar)) / (self.b0 + self.n_user)

            w0_u_inv = inverse(self.w0_u)
            w0_star = inverse(
                w0_u_inv + self.n_user * s_bar + (self.b0 * self.n_user) / (self.b0 + self.n_user) * (
                        self.mu0_u - u_bar) @ (self.mu0_u - u_bar).T)

            _sigma_u = wishart(nu=self.n_latent + self.n_user, scale=w0_star)  # reduce mixing time
            sigma_u = (_sigma_u + _sigma_u.T) / 2
            lambda_u = inverse(self.b0 + self.n_user * sigma_u)
            mu_u = mu0_star + cholesky(lambda_u) @ normal(size=(self.n_latent, 1))

            """
            item prior
            """
            u_bar = mean_latent(self.latent_v)
            s_bar = cov_latent(self.latent_v)

            mu0_star = ((self.b0 * self.mu0_v) + (self.n_item * u_bar)) / (self.b0 + self.n_item)

            w0_v_inv = inverse(self.w0_v)
            w0_star = inverse(
                w0_v_inv + self.n_item * s_bar + (self.b0 * self.n_item) / (self.b0 + self.n_item) * (
                        self.mu0_v - u_bar) @ (self.mu0_v - u_bar).T)

            _sigma_v = wishart(nu=self.n_latent + self.n_item, scale=w0_star)
            sigma_v = (_sigma_v + _sigma_v.T) / 2
            lambda_v = inverse(self.b0 + self.n_item * sigma_v)
            mu_v = mu0_star + cholesky(lambda_v) @ normal(size=(self.n_latent, 1))

            for gibbs in [1]:
                """
                pseudo code
                * item 업데이트시
                item score를 가진 U만 subset -> U*
                rating - global_mu (Normal with mean 0)
                * hyperparam_update
                sigma_u = wishart random matrix
                lambda_star_u = inv(sigma_u + beta * U".T @ U")
                mu_star_u = lambda_star_u * (sigma_u * mu_u + beta * U" * rr)
                lambda = lower tri cholesky matrix
                * draw sample
                u_i = N(mu*, lambda*)
                """

                """SAMPLE THEN USER FEATURES (possibly in parallel):"""
                for each in np.arange(self.n_user):
                    find_user = user_based_item_rating(each, self.rating_matrix)
                    target_items, target_ratings = find_user[0], find_user[1]
                    latent_v_i = self.latent_v[target_items]
                    lambda_star = inverse(sigma_u + self.b0 * latent_v_i.T @ latent_v_i)
                    mean_star = lambda_star @ (self.b0 * latent_v_i.T @ target_ratings + lambda_u @ mu_u)
                    posterior_sample = mean_star + cholesky(lambda_star) @ normal(size=(self.n_latent, 1))
                    self.latent_u[each, :] = posterior_sample.reshape(-1)

                """SAMPLE THEN MOVIE FEATURES (possibly in parallel):"""

                for each in np.arange(self.n_item):
                    find_user = item_based_user_rating(each, self.rating_matrix)
                    target_items, target_ratings = find_user[0], find_user[1]
                    latent_u_i = self.latent_u[target_items]
                    lambda_star = inverse(sigma_v + self.b0 * latent_u_i.T @ latent_u_i)
                    mean_star = lambda_star @ (self.b0 * latent_u_i.T @ target_ratings + lambda_v @ mu_v)
                    posterior_sample = mean_star + cholesky(lambda_star) @ normal(size=(self.n_latent, 1))
                    self.latent_v[each, :] = posterior_sample.reshape(-1)

            """
            save snapshot
            """

            self.model_out[epoch] = (self.latent_u, self.latent_v)
            self.U = self.latent_u
            self.V = self.latent_v

            """get validation error"""

            if self.validatset is not None:
                val_X = self.validatset[:, [0, 1]]
                val_y = self.validatset[:, 2]
                validat_predict = self.predict(val_X)
                error_sqaure = (validat_predict - val_y) ** 2
                test_rmse = (sum(error_sqaure) / error_sqaure.size) ** .5
            else:
                test_rmse = 0

            """get train error"""

            train_predict = self.predict(X)
            error_sqaure = (train_predict - y) ** 2
            train_rmse = (sum(error_sqaure) / error_sqaure.size) ** .5

            self.error_log = self.error_log.append({'epoch': epoch,
                                                    'train_rmse': train_rmse,
                                                    'test_rmse': test_rmse,
                                                    'n_latent': self.n_latent},
                                                   ignore_index=True)
            if self.verbose:
                print('epoch %4i \t Train RMSE %6.4f \t  Test RMSE %6.4f' % (epoch, train_rmse, test_rmse))

            """early stop by test error"""

            if self.validatset is not None:
                if epoch > self.early_stop_step:
                    best_epoch = self.error_log['test_rmse'].idxmin() + 1
                    is_stop = abs(epoch - best_epoch) >= self.early_stop_step
                    if is_stop:
                        if self.verbose:
                            print('best recode:')
                            print(self.error_log.query('epoch == @best_epoch'))
                        self.U = self.model_out[best_epoch][0]
                        self.V = self.model_out[best_epoch][1]
                        return self

            else:
                """early stop by train error"""

                if epoch > self.early_stop_step:
                    best_epoch = self.error_log['train_rmse'].idxmin() + 1
                    is_stop = abs(epoch - best_epoch) >= self.early_stop_step
                    if is_stop:
                        if self.verbose:
                            print('best recode:')
                            print(self.error_log.query('epoch == @best_epoch'))
                        self.U = self.model_out[best_epoch][0]
                        self.V = self.model_out[best_epoch][1]
                        return self

    def predict(self, X):
        validat_user_index = X[:, 0].astype(int)
        validat_item_index = X[:, 1].astype(int)
        predict_value = self.global_mu + np.sum(
            self.U[validat_user_index] * self.V[validat_item_index], axis=1)
        predict_value = np.where(predict_value < self.min_value, self.min_value, predict_value)
        predict_value = np.where(predict_value > self.max_value, self.max_value, predict_value)
        predict_value = predict_value.round()
        return predict_value
