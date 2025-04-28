# scripts/visualizations.py
import streamlit as st
import plotly.express as px
def show_graphs(df):
    if not df.empty:
        fig = px.bar(df, x='Produto', y='Preço', title='Preço Médio por Produto')
        st.plotly_chart(fig)
