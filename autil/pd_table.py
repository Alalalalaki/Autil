
import pandas as pd


def add_share_columns(df, base_line_idx, column_names=["Value", "Share"], formatting=True):
    dt = pd.DataFrame()
    for i, c in df.items():
        pct = c / c[base_line_idx]
        if formatting:
            pct = pct.map(lambda x: f'{abs(x):.3f}'.lstrip('0'))
        pct[base_line_idx] = "-"

        comb = pd.DataFrame({column_names[0]: c, column_names[1]: pct})
        comb.columns = [[i, i], comb.columns]
        dt = pd.concat([dt, comb], axis=1)
    return dt


def add_share_rows(df, base_line_idx, exp_lines_idx=None, row_name=" ", formatting=True):
    dt = pd.DataFrame()
    for i, r in df.iterrows():
        dt = dt.append(r)
        if i not in exp_lines_idx:
            pct = r/df.iloc[base_line_idx, :]
            if formatting:
                # pct = pct.map(lambda x: "("+str(int(x*100))+"%)")
                pct = pct.map(lambda x: "("+f'{abs(x):.2f}'.lstrip('0')+")")
            dt = dt.append(pct.rename(row_name))
    return dt
