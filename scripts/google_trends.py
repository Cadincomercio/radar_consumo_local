# scripts/google_trends.py
import pandas as pd
def get_trends(cidades):
    return pd.DataFrame({'Termo': [], 'Cidade': [], 'Interesse': []})
