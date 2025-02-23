#---------------------------------------- SCRIPT DE ETL -----------------------------------------#
print('Iniciando o ETL.')

import json
import pandas as pd

#-------------------------------------------- FUNÇÕES --------------------------------------------#

#Lendo os arquivos:

def ler_csv(caminho):
    df = pd.read_csv(caminho)
    return df

def ler_json(caminho, x):
    with open(caminho) as file:
        data_json = json.load(file)
    df = pd.json_normalize(data_json[x])
    return df

#Tratando os dados:

def tratamento(df):
    # Excluindo as linhas com dados nulos:
    df = df.dropna().copy()

    # Pegando o nome do cliente a partir do email:
    df['customer_name'] = df['customer_email'].apply(lambda x: x.split('@')[0].replace('.', ' ').title())

    # Trocando o _ por espaço e deixando com a primeira letra maiúscula no nome das categorias:
    df['product_category_name'] = df['product_category_name'].apply(lambda x: x.replace('_', ' ').title())
    
    # Mudança para int ou float
    float_to_int_cols = ['order_item_id', 'product_photos_qty', 'product_name_lenght', 'product_description_lenght']
    for col in float_to_int_cols:
        df[col] = df[col].astype('int64')

    # Alterando para o tipo datetime:
    date_columns = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_customer_date', 
                    'order_estimated_delivery_date', 'shipping_limit_date']
    for coluna in date_columns:
        df[coluna] = pd.to_datetime(df[coluna], format='%Y-%m-%d %H:%M:%S')

    return df

def criacao_colunas(df):
    #extraindo o ano, mês, dia e ano-mês do order_purchase_timestamp:
    df['order_purchase_year'] = df['order_purchase_timestamp'].dt.year
    df['order_purchase_month'] = df['order_purchase_timestamp'].dt.month
    df['order_purchase_day'] = df['order_purchase_timestamp'].dt.day
    df['order_purchase_year_month'] = df['order_purchase_timestamp'].astype('str').str[:7]

    #Criação do total_price
    df['total_price'] = df['price'] + df['freight_value']

    return df 

def juncao_dados(df1, customers_df, sellers_df):
    df1 = df1.merge(customers_df, on = 'customer_id', how = 'left')
    df1 = df1.merge(sellers_df, on = 'seller_id', how = 'left')
    return df1

#--------------------------------------- EXTRACT (EXTRAÇÃO) ---------------------------------------#

#Caminhos dos arquivos:
path = 'datasets/order_items.csv'
sellers_path = 'datasets/sellers.json'
customers_path = 'datasets/customers.json'

#Carregamento do CSV:
ordersDF = ler_csv(path)

#Carregamento dos JSON's:
sellers_df = ler_json(sellers_path, 'sellers')
customers_df = ler_json(customers_path, 'customers')

#------------------------------------ TRANSFORM (TRANSFORMAÇÃO) ------------------------------------#

if __name__ == '__main__':

    print('Iniciando o tratamento dos dados.')
    ordersDF = tratamento(ordersDF)

    print('Iniciando a criação de colunas.')
    ordersDF = criacao_colunas(ordersDF)

    print('Iniciando a junção dos dados.')
    ordersDF = juncao_dados(ordersDF, customers_df, sellers_df)

    print('Tratamento dos dados finalizado com sucesso.')

#---------------------------------- LOAD (CARREGAMENTO) --------------------------------------#

    print('Salvando o arquivo .csv')

    #Salvando o CSV:
    ordersDF.to_csv('datasets/orders_items_cleaned.csv', index = False)

    print('Arquivo salvo com sucesso. \nFIM.')

#------------------------------------------ FIM ----------------------------------------------#