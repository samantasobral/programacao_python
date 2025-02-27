#--------------------------------- SCRIPT PÁGINA INICIAL (HOME) ---------------------------------------#

import gdown
import pandas as pd
import streamlit as st
from funcoes import filtro_checkbox_df, bignumbers, ler_df_drive, filtra_df

st.set_page_config(page_title = 'Dashboard - Análise das Vendas', layout = 'wide') 

with st.container():
    st.markdown('# Dashboard - Análise das Vendas')
    st.markdown('#### Navegue pelo menu à esquerda para visualizar as análises das vendas por: Categoria e Estado')

#Leitura dos dados:
#order_items_df = pd.read_csv('datasets/orders_items_cleaned.csv')

order_items_df = ler_df_drive('1OTzGaimK_k8ZJKmaSxrvevQH2KFmIL8e')

customers_df_filtred, sellers_df_filtred, estados_selecionados = filtra_df(order_items_df)

bignumbers(customers_df_filtred, sellers_df_filtred)

with st.container():
    st.markdown('#### Insights:')
    st.write('- O Estado que mais vendeu foi SP;')
    st.write('- SP também possui a maior quantidade de clientes e vendedores distintos;')
    st.write('- De setembro de 2016 a agosto de 2018, as vendas aumentaram;')
    st.write('- No mesmo período, a quantidade de clientes e vendedores também aumentou;')
    st.write('- O faturamento das categorias, incluindo frete, varia de 324.51 reais a  14 milhões de reais;')
    st.write('- A categoria com o maior faturamento foi Beleza e Saúde;')
    st.write('- A categoria com o menor faturamento foi Seguros e Serviços.')

with st.container():
    st.markdown('#### Sugestões:')
    st.write('- Criar algum programa de cashback/premiação para os clientes que mais compram;')
    st.write('- Prospectar novos vendedores no AM (só há apenas 1 desde 2017);')
    st.write('- Criar promoções, a fim de alavancar as vendas e aumentar o número de clientes.')

