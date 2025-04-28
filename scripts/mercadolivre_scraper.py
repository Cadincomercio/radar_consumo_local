import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_ml(cidades, categoria, palavra_chave):
    produtos = []
    estados_br = {
        'São Paulo': 'SP', 'Belo Horizonte': 'MG', 'Curitiba': 'PR',
        'Rio de Janeiro': 'RJ', 'Porto Alegre': 'RS', 'Salvador': 'BA'
    }
    estado = estados_br.get(cidades[0], 'SP')  # Assume SP se não encontrar

    query = palavra_chave if palavra_chave else 'produto'
    url = f"https://lista.mercadolivre.com.br/{query}_State_{estado}"

    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.select('li.ui-search-layout__item')
            for item in items:
                titulo_tag = item.select_one('h2.ui-search-item__title')
                if not titulo_tag:
                    titulo_tag = item.find('h2')  # fallback
                preco_tag = item.select_one('span.andes-money-amount__fraction')

                produtos.append({
                    'Produto': titulo_tag.text.strip() if titulo_tag else 'Produto sem nome',
                    'Cidade': cidades[0],
                    'Preço': preco_tag.text.strip() if preco_tag else 'Não informado',
                    'Origem': 'Mercado Livre'
                })
        time.sleep(2)
    except Exception as e:
        print(f"Erro Mercado Livre: {e}")

    return pd.DataFrame(produtos)
