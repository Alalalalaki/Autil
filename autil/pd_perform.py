import pandas as pd
from tqdm import tqdm


def chunk_apply(df, func, args=(), n=10_000):

    m = df.shape[0]//n + 1
    list_dfjb = (df[i:i+n] for i in range(0, df.shape[0], n))

    listr_res = []

    for i in tqdm(list_dfjb, total=m):
        _res = i.pipe(func, *args)
        listr_res.append(_res)

    res = pd.concat(listr_res, axis=0)
    return res

