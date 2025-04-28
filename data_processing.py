# scripts/data_processing.py
import pandas as pd
def process_data(df_olx, df_shopee, df_ml, df_trends):
    return pd.concat([df_olx, df_shopee, df_ml, df_trends]).head(50)
