
import streamlit as st
import pandas as pd
import time
import io

from scripts import olx_scraper, shopee_scraper, mercadolivre_scraper, google_trends, data_processing, visualizations

# Configuração inicial
st.set_page_config(page_title="Radar de Consumo Local", layout="wide")
st.title("📊 Radar de Consumo Local")
st.write("Descubra os produtos mais buscados, anunciados e vendidos em diferentes cidades do Brasil!")

st.sidebar.header("Filtros de Busca")

# Lista padrão de cidades sugeridas
cidades_sugeridas = ['São Paulo', 'Belo Horizonte', 'Curitiba', 'Rio de Janeiro', 'Porto Alegre', 'Salvador', 'Uberlândia', 'Montes Claros', 'Campinas', 'Ribeirão Preto']

# Seleção de cidades
cidade_selecionada = st.sidebar.selectbox("Selecione uma cidade:", [""] + cidades_sugeridas)

# Campo livre para digitação
cidade_personalizada = st.sidebar.text_input("Ou digite o nome da sua cidade:")

# Definição final da cidade
if cidade_personalizada:
    cidades_final = [cidade_personalizada]
elif cidade_selecionada:
    cidades_final = [cidade_selecionada]
else:
    cidades_final = []

# Seleção de categorias
categorias = ['Eletrodomésticos', 'Moda', 'Automotivo', 'Beleza', 'Informática', 'Casa e Jardim', 'Brinquedos']
categoria_selecionada = st.sidebar.selectbox("Categoria:", ["Todos"] + categorias)

# Campo de busca livre
palavra_chave = st.sidebar.text_input("Pesquisa livre:")

# Botão de buscar
buscar = st.sidebar.button("🔍 Buscar Produtos")

if buscar:
    if not cidades_final:
        st.warning("Por favor, selecione ou digite pelo menos uma cidade.")
    else:
        with st.spinner("Coletando dados..."):
            start_time = time.time()
            
            df_olx = olx_scraper.scrape_olx(cidades_final, categoria_selecionada, palavra_chave)
            df_shopee = shopee_scraper.scrape_shopee(categoria_selecionada, palavra_chave)
            df_ml = mercadolivre_scraper.scrape_ml(cidades_final, categoria_selecionada, palavra_chave)
            df_trends = google_trends.get_trends(cidades_final)

            df_final = data_processing.process_data(df_olx, df_shopee, df_ml, df_trends)

            elapsed = time.time() - start_time
            st.success(f"Dados coletados em {round(elapsed, 2)} segundos.")

            st.header("Top 50 Produtos Mais Populares")
            st.dataframe(df_final)

            visualizations.show_graphs(df_final)

            # Botões de exportação
            if not df_final.empty:
                # Baixar CSV
                st.download_button("📥 Baixar CSV", data=df_final.to_csv(index=False), file_name="radar_consumo.csv", mime="text/csv")

                # Baixar Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_final.to_excel(writer, index=False)
                data_xlsx = output.getvalue()

                st.download_button("📥 Baixar Excel", data=data_xlsx, file_name="radar_consumo.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
