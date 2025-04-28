# scripts/mercadolivre_scraper.py
import pandas as pd
def scrape_ml(cidades, categoria, palavra_chave):
    return pd.DataFrame({'Produto': [], 'Cidade': [], 'Vendas': [], 'Preço': [], 'Origem': []})
