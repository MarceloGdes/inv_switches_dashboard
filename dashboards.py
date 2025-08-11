# leitura de dados
import pandas as pd
#criação de gráficos
import plotly.express as px
# Para construção dos dashboards
import streamlit as st 
import sqlalchemy

# Cria a string de conexão no formato esperado pelo SQLAlchemy
# Usando o driver pymysql para MySQL
DATABASE_URL = "mysql+pymysql://root:admin@localhost:3306/unipar"

# Cria o engine de conexão
engine = sqlalchemy.create_engine(DATABASE_URL)

st.set_page_config(page_title="Dashboard - Inventário de Switches", page_icon=":bar_chart:", layout="wide")

# Lendo dados da tabela com pandas, usando o engine
df = pd.read_sql('SELECT * FROM table_inv_switches', engine)

print(df.head())

# Distribuição de marcas (quantos switches de cada fabricante)
figDistMarcas = px.bar(
    df['MARCA'].value_counts().reset_index(name='QUANTIDADE'),
    x='MARCA',
    y='QUANTIDADE',
    title='Distribuição de Switches por Fabricante'
)
st.plotly_chart(figDistMarcas, use_container_width=True)

figDistModelos = px.bar(
    df['MODELO'].value_counts().reset_index(name='QUANTIDADE'),
    x='MODELO',
    y='QUANTIDADE',
    title='Distribuição de Switches por Modelo'
)
st.plotly_chart(figDistModelos)

#Distribuição de modelos
#Quantidade por versão de firmware
#Quantidade de equipamentos com/sem número de imobilizado
# print(df.head())

