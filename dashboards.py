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

# Lendo dados da tabela com pandas, usando o engine
df = pd.read_sql('SELECT * FROM table_inv_switches', engine)

# Deixar com que cada switch apareça só uma vez no DataFrame
df = df.drop_duplicates(subset=['NUM_SERIE'])

st.set_page_config(page_title="Dashboard - Inventário de Switches", page_icon=":bar_chart:", layout="wide")

#Definindo as colunas do meu dashboard
col1, col2 = st.columns(2)

#Distribuição de marcas (quantos switches de cada fabricante)
fig_dist_marcas = px.pie(
    df['MARCA'].value_counts().reset_index(name='QUANTIDADE'),
    names='MARCA',
    values='QUANTIDADE',
    color='MARCA',
    title='Distribuição de Switches por Fabricante'
)

col1.plotly_chart(fig_dist_marcas, use_container_width=True)

#Distribuição por Imobilizado
#Substitui vazio por "Não vinculado"
df['IMOBILIZADO'] = df['IMOBILIZADO'].replace('', "Não vinculado")

fig_imobilizado = px.pie(
    df['IMOBILIZADO']
        .apply(lambda x: 'Com Imobilizado' if x != 'Não vinculado' else 'Sem Imobilizado')
        .value_counts()
        .reset_index(name='QUANTIDADE'),
    names='IMOBILIZADO',   # agora usa a coluna gerada pelo reset_index
    values='QUANTIDADE',
    title='Switch com ou sem imobilizados vinculados'
)

col2.plotly_chart(fig_imobilizado, use_container_width=True)


#Distribuição de modelos
figDistModelos = px.bar(
    df[['MODELO', 'MARCA']].value_counts().reset_index(name='QUANTIDADE'),
    x='MODELO',
    y='QUANTIDADE',
    color='MARCA',
    title='Distribuição de Switches por Modelo'
)
st.plotly_chart(figDistModelos, use_container_width=True)

st.title("Análise Detalhada de Switches por Modelo")
#Seleção do modelo. 
modelo_selecionado = st.selectbox(
    "Selecione o modelo",
    sorted(df['MODELO'].unique())
)
#Filtrando o DataFrame com base no modelo escolhido
df_filtrado = df[df['MODELO'] == modelo_selecionado]

st.subheader(f"Detalhes do switch do Switch{modelo_selecionado}")

col3, col4, col5 = st.columns(3)
col3.metric("Quantidade Total: ", len(df_filtrado))
col4.metric("Quantidade de imobilizados vinculados: ", df_filtrado['IMOBILIZADO'].count())
col5.metric("Versões de Firmware", df_filtrado['VERSAO'].nunique())

df_switches_modelos = df_filtrado[['HOSTNAME','IP_ADDRESS', 'MAC_ADDRESS', 'MARCA', 'NUM_SERIE', 'VERSAO', 'IMOBILIZADO']]
st.dataframe(df_switches_modelos, use_container_width=True)
