# scripts/olx_scraper.py
import pandas as pd
def scrape_olx(cidades, categoria, palavra_chave):
    return pd.DataFrame({'Produto': [], 'Cidade': [], 'Preço': [], 'Origem': []})
