
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
    estado = estados_br.get(cidades[0], 'SP')  # assume SP se não achar
    query = palavra_chave if palavra_chave else 'produto'
    url = f"https://lista.mercadolivre.com.br/{query}_Desde_0_NoIndex_True_State_{estado}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.select('li.ui-search-layout__item')
            for item in items:
                titulo = item.find('h2')
                preco = item.select_one('span.andes-money-amount__fraction')
                produtos.append({
                    'Produto': titulo.text.strip() if titulo else 'Sem título',
                    'Cidade': cidades[0],
                    'Preço': preco.text.strip() if preco else 'Não informado',
                    'Origem': 'Mercado Livre'
                })
        time.sleep(2)
    except Exception as e:
        print(f"Erro Mercado Livre: {e}")
    return pd.DataFrame(produtos)
