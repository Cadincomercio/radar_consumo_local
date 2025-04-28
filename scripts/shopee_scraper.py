
import pandas as pd

def scrape_shopee(categoria, palavra_chave):
    # Shopee bloqueia scraping simples, então retornamos base simulada
    produtos = []
    if palavra_chave:
        produtos.append({
            'Produto': f"Exemplo Shopee {palavra_chave}",
            'Preço': "99",
            'Origem': 'Shopee'
        })
    return pd.DataFrame(produtos)
