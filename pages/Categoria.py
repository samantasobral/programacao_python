#----------------------------- VISÃO POR CATEGORIAS -----------------------------------#

import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from funcoes import (definicao_parametros_graficos, filtra_df, ler_df_drive)

#------------------------------ CONFIGURAÇÃO -------------------------------------------#

st.set_page_config(page_title = 'Análise das Vendas por Categoria', layout = 'wide')
st.title('Análise das Vendas por Categoria')  #Título da página

definicao_parametros_graficos()

#Leitura dos dados:
order_items_df = ler_df_drive('1OTzGaimK_k8ZJKmaSxrvevQH2KFmIL8e')


#------------------------------------ FUNÇÕES ---------------------------------------------#

def filtro_faturamento(c_df):
    
    cat_faturamento  = (c_df[['product_category_name', 'total_price']]
                    .groupby('product_category_name').sum().
                    sort_values('total_price', ascending = False).reset_index())

    # Definindo o mínimo e máximo para o slider
    minimo = 300
    maximo = 1400000

    # Criando o slider para selecionar o intervalo de faturamento
    selected_range = st.slider("Selecione a faixa de Faturamento (R$)", 
                           minimo, maximo, (minimo, maximo), 
                           step=10000,  format="%d")

    # Filtrando os dados com base no intervalo de faturamento selecionado
    filtered_cat_faturamento = cat_faturamento[(cat_faturamento['total_price'] >= selected_range[0]) & 
                                           (cat_faturamento['total_price'] <= selected_range[1])]
    return filtered_cat_faturamento


def visao_categorias(cat_df):  

    plt.figure(figsize=(18,32))

    sns.barplot(cat_df, x = 'total_price', y = 'product_category_name')
    plt.title('Faturamento das Categorias', fontsize = 18)
    plt.xlabel('Faturamento (R$)')
    plt.ylabel('Categorias')

    st.pyplot(plt)

    return None

#------------------------------------- DASHBOARD ----------------------------------------#

if __name__ == '__main__':

    customers_df_filtred, sellers_df_filtred, estados_selecionados = filtra_df(order_items_df)

    filtered_cat_faturamento = filtro_faturamento(customers_df_filtred)

    visao_categorias(filtered_cat_faturamento)