
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def read_parquet(file_path):
    table = pq.read_table(file_path)
    df = table.to_pandas(split_blocks=True, self_destruct=True)
    # del table
    return df

def write_parquet(df, file_path):
    assert type(df) == pd.core.frame.DataFrame, "Can only write pandas df"
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path)
    # del table
    
