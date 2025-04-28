# app.py
import streamlit as st
from scripts import olx_scraper, shopee_scraper, mercadolivre_scraper, google_trends, data_processing, visualizations
import pandas as pd
import time

st.set_page_config(page_title="Radar de Consumo Local", layout="wide")
st.title("📊 Radar de Consumo Local")
st.write("Descubra os produtos mais buscados, anunciados e vendidos em diferentes cidades do Brasil!")

st.sidebar.header("Filtros de Busca")

cidades_disponiveis = ['São Paulo', 'Belo Horizonte', 'Curitiba', 'Rio de Janeiro', 'Porto Alegre', 'Salvador']
grupos = {
    'Grande SP': ['São Paulo', 'Guarulhos', 'Santo André', 'São Bernardo do Campo'],
    'Grande BH': ['Belo Horizonte', 'Contagem', 'Betim', 'Nova Lima'],
    'Grande Curitiba': ['Curitiba', 'São José dos Pinhais', 'Colombo', 'Araucária']
}

cidades_selecionadas = st.sidebar.multiselect("Selecione as cidades:", cidades_disponiveis)
grupo_selecionado = st.sidebar.selectbox("Ou selecione um grupo:", ['Nenhum'] + list(grupos.keys()))
if grupo_selecionado != 'Nenhum':
    cidades_selecionadas = grupos[groupo_selecionado]

categorias = ['Eletrodomésticos', 'Moda', 'Automotivo', 'Beleza', 'Informática', 'Casa e Jardim', 'Brinquedos']
categoria_selecionada = st.sidebar.selectbox("Categoria:", ["Todos"] + categorias)

palavra_chave = st.sidebar.text_input("Pesquisa livre:")

if st.sidebar.button("🔍 Buscar Produtos"):
    if not cidades_selecionadas:
        st.warning("Por favor, selecione ao menos uma cidade.")
    else:
        with st.spinner("Coletando dados..."):
            start_time = time.time()
            
            df_olx = olx_scraper.scrape_olx(cidades_selecionadas, categoria_selecionada, palavra_chave)
            df_shopee = shopee_scraper.scrape_shopee(categoria_selecionada, palavra_chave)
            df_ml = mercadolivre_scraper.scrape_ml(cidades_selecionadas, categoria_selecionada, palavra_chave)
            df_trends = google_trends.get_trends(cidades_selecionadas)

            df_final = data_processing.process_data(df_olx, df_shopee, df_ml, df_trends)

            elapsed = time.time() - start_time
            st.success(f"Dados coletados em {round(elapsed, 2)} segundos.")

            st.header("Top 50 Produtos Mais Populares")
            st.dataframe(df_final)

            visualizations.show_graphs(df_final)

            st.download_button("📥 Baixar CSV", data=df_final.to_csv(index=False), file_name="radar_consumo.csv")
            st.download_button("📥 Baixar Excel", data=df_final.to_excel(index=False), file_name="radar_consumo.xlsx")
