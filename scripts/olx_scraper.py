
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_olx(cidades, categoria, palavra_chave):
    produtos = []
    for cidade in cidades:
        cidade_formatada = cidade.lower().replace(" ", "")
        url = f"https://{cidade_formatada}.olx.com.br/"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                anuncios = soup.find_all('li', {'data-lurker-detail': True})
                for anuncio in anuncios:
                    titulo = anuncio.find('h2')
                    preco = anuncio.find('span', {'class': 'sc-ifAKCX'})
                    produtos.append({
                        'Produto': titulo.text.strip() if titulo else 'Sem título',
                        'Cidade': cidade,
                        'Preço': preco.text.strip() if preco else 'Não informado',
                        'Origem': 'OLX'
                    })
            time.sleep(2)  # respeitar boas práticas
        except Exception as e:
            print(f"Erro OLX: {e}")
    return pd.DataFrame(produtos)
