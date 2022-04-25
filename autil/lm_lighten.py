
import linearmodels as lm


def lighten_lm_res(res, mode=1):
    """
    Lighten linearmodels result for the case of large sample regression
    If mode=0, remove all data except _resid and _fitted
    If mode=1, keep dependent so that res.nobs and res.rsquared_adj still work
    """
    res._cov_estimator = None
    res._wresid = None
    if mode == 0:
        res.model = None
    elif mode == 1:
        if type(res.model) == lm.iv.model._OLS:
            res.model.exog = None
            res.model.endog = None
            res.model.weights = None
            res.model.instruments = None  # if mute this display still work but not sure result
            res.model._index = None
            res.model._y = None
            res.model._wy = None
            res.model._x = None
            res.model._wx = None
            res.model._z = None
            res.model._wz = None

        if type(res.model) == lm.iv.absorbing.AbsorbingLS:
            res.model._exog = None
            res.model._absorb = None
            res.model._absorb_inter = None
            res.model._weight_data = None
            res.model._absorbed_dependent = None
            res.model._absorbed_exog = None
            res.model._index = None
            res.model._original_index = None
            res.model._regressors = None

    else:
        raise ValueError("mode should be either 0 or 1")
    return res
