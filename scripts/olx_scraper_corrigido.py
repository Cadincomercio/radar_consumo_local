
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_olx(cidades, categoria, palavra_chave):
    produtos = []

    estados = {
        'São Paulo': 'sp',
        'Belo Horizonte': 'mg',
        'Uberlândia': 'mg',
        'Montes Claros': 'mg',
        'Curitiba': 'pr',
        'Rio de Janeiro': 'rj',
        'Porto Alegre': 'rs',
        'Salvador': 'ba'
    }

    for cidade in cidades:
        estado_sigla = estados.get(cidade, 'mg')  # Padrão MG se não encontrar
        url = f"https://www.olx.com.br/estado-{estado_sigla}"

        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                anuncios = soup.select('li.sc-1fcmfeb-2')

                for anuncio in anuncios:
                    titulo_tag = anuncio.find('h2')
                    preco_tag = anuncio.find('span', {'data-testid': 'ad-price'})

                    if titulo_tag:
                        produtos.append({
                            'Produto': titulo_tag.text.strip(),
                            'Cidade': cidade,
                            'Preço': preco_tag.text.strip() if preco_tag else 'Não informado',
                            'Origem': 'OLX'
                        })
            time.sleep(2)  # respeitar boas práticas
        except Exception as e:
            print(f"Erro OLX: {e}")

    return pd.DataFrame(produtos)
