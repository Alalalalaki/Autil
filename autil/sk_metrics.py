
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, balanced_accuracy_score, classification_report, r2_score, mean_squared_error

from mpl_set import set_style, set_size, save_fig


def scoring(y_true, y_pred, y_score=None, target_names=None):
    _as = accuracy_score(y_true, y_pred)
    print(f"accuracy_score: {_as}")
    bas = balanced_accuracy_score(y_true, y_pred)
    print(f"balanced_accuracy_score: {bas}")
    # ras = roc_auc_score(y_true, y_score)
    # print(f"roc_auc_score: {ras}")
    cr = classification_report(y_true, y_pred, target_names=target_names)
    print(f"classification_report: {cr}")


def plot_confusion(y_true, y_predict, ticklabels, normalize="true", only_wrong=False,
                   figsize=(22, 22), fmt='.4f', major_lines=None,
                   save_path=None
                   ):
    confusion = confusion_matrix(y_true, y_predict, normalize=normalize)
    if only_wrong:
        np.fill_diagonalgonal(confusion, 0)

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(confusion.T, ax=ax, square=True, cbar=False, cmap='rocket_r', annot=True,
                fmt=fmt,  # if count, fmt='d', if normalzie fmt='.2f'
                xticklabels=ticklabels, yticklabels=ticklabels)
    if major_lines is not None:
        ax.hlines(major_lines, *ax.get_xlim(), color="C1")
        ax.vlines(major_lines, *ax.get_xlim(), color="C1")
    plt.xlabel('true label')
    plt.ylabel('predicted label')

    if save_path is not None:
        save_fig(fig, save_path)


def bic_scorer(estimator, X, y):
    # ref: https://github.com/scikit-learn/scikit-learn/blob/844b4be24/sklearn/linear_model/_least_angle.py#L1952
    n = len(y)
    y_pred = estimator.predict(X)
    mse = np.average((y - y_pred) ** 2, axis=0)  # (y - Xβ) / N
    sigma2 = np.var(y)
    eps64 = np.finfo("float64").eps
    K = np.log(n)
    mask = np.abs(estimator.coef_) > np.finfo(estimator.coef_.dtype).eps
    df = np.sum(mask)

    score = (n * mse / (sigma2 + eps64) + K * df)
    return score


def bic_scorer_neg(estimator, X, y):
    return bic_scorer(estimator, X, y) * -1


def gic_scorer(estimator, X, y, K="lnlp"):
    # exactly the same as bic except K
    n = len(y)
    p = X.shape[1]
    y_pred = estimator.predict(X)
    mse = np.average((y - y_pred) ** 2, axis=0)
    sigma2 = np.var(y)
    eps64 = np.finfo("float64").eps
    if K == "lnlp":
        K = np.log(n) * np.log(p)
    elif K == "llnlp":
        K = np.log(np.log(n)) * np.log(p)
    elif K == "2ln":
        K = 2*np.log(n)
    else:
        raise ValueError("K should be lnlp or llnlp or 2ln")
    mask = np.abs(estimator.coef_) > np.finfo(estimator.coef_.dtype).eps
    df = np.sum(mask)

    score = (n * mse / (sigma2 + eps64) + K * df)
    return score


def best_alpha_index(results):
    # ref: https://github.com/scikit-learn-contrib/lightning/issues/84
    # ref: https://scikit-learn.org/stable/modules/model_evaluation.html#implementing-your-own-scoring-object
    K = len([x for x in list(results.keys()) if x.startswith('split')])
    alpha_range = results['param_ridge__alpha'].data

    mean_per_alpha = pd.Series(results['mean_test_score'], index=alpha_range)
    std_per_alpha = pd.Series(results['std_test_score'], index=alpha_range)
    sem_per_alpha = std_per_alpha / np.sqrt(K)

    max_score = mean_per_alpha.max()
    sem = sem_per_alpha[mean_per_alpha.idxmax()]
    best_alpha = mean_per_alpha[mean_per_alpha >= max_score - sem].index.max()

    best_alpha_index = int(np.argwhere(alpha_range == best_alpha)[0])

    return best_alpha_index


def plot_model_fit(y_test, y_test_predict, lim=(7, 12), figsize=(8, 5), label="Log Wage", save_path=None):
    r2 = r2_score(y_test, y_test_predict)
    string_score = f"R2: {r2:.3f}"
    mse = mean_squared_error(y_test, y_test_predict)
    string_score += f"\nMSE: {mse:.3f}"
    set_style(color_style="default")
    fig, ax = plt.subplots(figsize=figsize)
    # ax.scatter(y_test, y_test_predict, alpha=0.02, c="C0")
    ax.plot(y_test, y_test_predict, 'o', alpha=0.1, c="C0", rasterized=True)  # this reduce figure size
    ax.plot([0, 1], [0, 1], transform=ax.transAxes, ls="--", c="C1")
    ax.text(lim[0]*1.1, lim[1]*0.9, string_score)
    # plt.title(f"Lasso, α={model.alpha_:.4}")
    plt.ylabel(label+", Model Predictions")
    plt.xlabel(label+", Truths")
    plt.xlim(lim)
    plt.ylim(lim)

    if save_path is not None:
        save_fig(fig, save_path)
