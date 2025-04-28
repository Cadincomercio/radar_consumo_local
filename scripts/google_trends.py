from pytrends.request import TrendReq
import pandas as pd

def get_trends(cidades):
    pytrends = TrendReq(hl='pt-BR', tz=360)
    try:
        cidade = cidades[0] if cidades else 'Brazil'
        pytrends.build_payload(kw_list=['comprar', 'promoção', 'barato'], geo='BR')
        df = pytrends.trending_searches(pn='brazil')
        df.columns = ['Termo']
        df['Cidade'] = cidade
        df['Interesse'] = 100
        return df.head(10)
    except Exception as e:
        print(f"Erro Trends: {e}")
        return pd.DataFrame(columns=['Termo', 'Cidade', 'Interesse'])
