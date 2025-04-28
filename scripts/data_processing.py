
import pandas as pd

def process_data(df_olx, df_shopee, df_ml, df_trends):
    frames = []
    if not df_olx.empty:
        frames.append(df_olx)
    if not df_shopee.empty:
        frames.append(df_shopee)
    if not df_ml.empty:
        frames.append(df_ml)
    df_produtos = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=['Produto', 'Cidade', 'Preço', 'Origem'])

    if not df_trends.empty:
        df_trends['Preço'] = 'Não aplicável'
        df_trends['Origem'] = 'Google Trends'
        df_trends.rename(columns={'Termo': 'Produto'}, inplace=True)
        df_produtos = pd.concat([df_produtos, df_trends[['Produto', 'Cidade', 'Preço', 'Origem', 'Interesse']]], ignore_index=True)

    return df_produtos.head(50)
