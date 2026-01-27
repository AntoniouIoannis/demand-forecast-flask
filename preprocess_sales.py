import pandas as pd
import numpy as np
import os

def build_transactions(sales_files):
    all_data = []
    for year, path in sales_files.items():
        df = pd.read_excel(path, engine='openpyxl')
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)

def aggregate_item_month(df):
    # Χρήση των σωστών στηλών βάσει του check_columns.py
    date_col = 'shipped'
    item_col = 'product_id'
    qty_col = 'ordered_qty'
    
    df[date_col] = pd.to_datetime(df[date_col])
    df['month_year'] = df[date_col].dt.to_period('M').dt.to_timestamp()
    
    return df.groupby([item_col, 'month_year'])[qty_col].sum().reset_index()

def complete_panel(df):
    item_col = 'product_id'
    items = df[item_col].unique()
    dates = pd.date_range(start=df['month_year'].min(), end=df['month_year'].max(), freq='MS')
    full_idx = pd.MultiIndex.from_product([items, dates], names=[item_col, 'month_year'])
    full_df = pd.DataFrame(index=full_idx).reset_index()
    return pd.merge(full_df, df, on=[item_col, 'month_year'], how='left').fillna(0)

def add_ordered_rolling_features(df):
    item_col = 'product_id'
    qty_col = 'ordered_qty'
    df = df.sort_values([item_col, 'month_year'])
    for i in [1, 2, 3]:
        df[f'lag_{i}'] = df.groupby(item_col)[qty_col].shift(i)
    df['roll_mean_3'] = df.groupby(item_col)[qty_col].transform(lambda x: x.shift(1).rolling(3).mean())
    return df.fillna(0)

def run_preprocessing_pipeline(sales_files, outdir):
    os.makedirs(outdir, exist_ok=True)
    tx = build_transactions(sales_files)
    monthly = aggregate_item_month(tx)
    panel = complete_panel(monthly)
    final = add_ordered_rolling_features(panel)
    
    # Διαχωρισμός (Train: μέχρι τέλος 2018, Test: 2019)
    train_df = final[final['month_year'] < '2019-01-01']
    test_df = final[final['month_year'] >= '2019-01-01']
    
    train_path = os.path.join(outdir, "train_with_roll.csv")
    test_path = os.path.join(outdir, "test_with_roll.csv")
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    return train_path, test_path
    