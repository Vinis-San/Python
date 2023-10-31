import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(layout="wide")
# CSS personalizado para estilizar o aplicativo
st.write(
    f"""
    <style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #f3f3f3;
    }}
    .stApp {{
        max-width: 100%;
        margin: 0 auto;
    }}
    .stTable {{
        font-size: 25px;
    }}
    .st-expander {{
        font-size: 48px;
    }}
    .stPlotly {{
        font-size: 16px;
    }}
    .sidebar.accordion {{
        font-size: 40px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Carrega os dados
clientes = pd.read_csv("clientes.csv", sep=";", encoding='latin1')
estoque = pd.read_csv("estoque.csv", sep=";", encoding='utf-8')
fornecedores = pd.read_csv("fornecedores.csv", sep=";", encoding='utf-8')


# Conecta-se à planilha do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("total-handler-368820-b4d2291cd2a7.json", scope)
client = gspread.authorize(creds)

# Abre a planilha existente pelo link
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1PUvew10KRjNssO42zB9JJfh6Pa7TKN1VHDBzv97xIzw/edit?usp=sharing")

worksheet = spreadsheet.worksheet("forms")

# Carregue os dados da guia em um DataFrame
data = worksheet.get_all_values()
# O primeiro row é usado como cabeçalho
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)

# Configuração da página
st.title("Análise de Dados da All Parts Informática")
st.sidebar.header("Análise de Dados")

# Selecionar as abas
aba = st.sidebar.radio("Selecione uma aba:", ["Gráficos", "Pesquisa de Campo", "Tabelas Completas"])

if aba == "Gráficos":
    col1,col2 = st.columns(2)
    # Gráfico 1
    fig_faturamento_produto = px.bar(clientes, x="Produtos Comprados", y="Valor Venda", title="Análise de Faturamento por Produto")
    fig_faturamento_produto.update_traces(marker_color='#FFA500')
    fig_faturamento_produto.update_xaxes(title_text="Produtos", tickfont=dict(size=20))
    fig_faturamento_produto.update_yaxes(title_text="Valor Venda", tickfont=dict(size=20))
    fig_faturamento_produto.update_layout(width=2000, height=1200)
    col1.plotly_chart(fig_faturamento_produto, use_container_width=True)

    # Gráfico 2
    fig_grafico_3 = px.scatter(clientes, x="Produtos Comprados", y="Valor Venda", title="Exemplo de Gráfico 3")
    fig_grafico_3.update_xaxes(tickfont=dict(size=20))
    fig_grafico_3.update_yaxes(tickfont=dict(size=20))
    fig_grafico_3.update_layout(width=2000, height=1200)
    fig_grafico_3.update_layout(legend_title_text="Legendas", legend_title_font=dict(size=30))
    col2.plotly_chart(fig_grafico_3, use_container_width=True)
    
elif aba == "Pesquisa de Campo":
    col1,col2,col3 = st.columns(3)
    col4,col5 = st.columns(2)
    col6,col7 = st.columns(2)
    col8,col9,col10 = st.columns(3)
   
    # Define a cor principal
    cor_principal = "#FFA500"

    
    # Gráfico 1 - Distribuição de Idade por Gênero
    fig_grafico_1 = px.histogram(df, x="1. Qual é a sua faixa etária?", color="2. Qual o seu gênero?", title="Distribuição de Idade por Gênero")
    fig_grafico_1.update_xaxes(title_text="Faixa Etária", tickfont=dict(size=20))
    fig_grafico_1.update_yaxes(title_text="Contagem", tickfont=dict(size=20))
    fig_grafico_1.update_layout(width=1200, height=800)
    fig_grafico_1.update_traces(marker_color=cor_principal)
    col1.plotly_chart(fig_grafico_1, use_container_width=True)

    # Gráfico 2 - Nível de Experiência em Produtos Eletrônicos
    fig_grafico_2 = px.pie(df, names="Avalie seu nível de experiência com produtos eletrônicos:", title="Nível de Experiência em Produtos Eletrônicos")
    fig_grafico_2.update_layout(width=1200, height=800)
    fig_grafico_2.update_traces(marker_colors=[cor_principal] * len(df))
    col2.plotly_chart(fig_grafico_2, use_container_width=True)

    # Gráfico 3 - Dispositivo Preferido
    fig_grafico_3 = px.pie(df, names="Indique seu dispositivo preferido para atividades relacionadas a produtos eletrônicos:", title="Dispositivo Preferido para Atividades Eletrônicas")
    fig_grafico_3.update_layout(width=1200, height=800)
    fig_grafico_3.update_traces(marker_colors=[cor_principal] * len(df))
    col3.plotly_chart(fig_grafico_3, use_container_width=True)

    # Gráfico 4 - Finalidades de Uso de Produtos Eletrônicos
    finalidades = df.iloc[:, 7:14]
    finalidades_counts = finalidades.apply(pd.Series.value_counts)
    fig_grafico_4 = px.bar(finalidades_counts, x=finalidades_counts.index, y=finalidades_counts.sum(axis=1), title="Finalidades de Uso de Produtos Eletrônicos")
    fig_grafico_4.update_xaxes(title_text="Finalidades de Uso", tickfont=dict(size=20))
    fig_grafico_4.update_yaxes(title_text="Contagem", tickfont=dict(size=20))
    fig_grafico_4.update_layout(width=1200, height=800)
    fig_grafico_4.update_traces(marker_color=cor_principal)
    col4.plotly_chart(fig_grafico_4, use_container_width=True)

    # Gráfico 5 - Preferências de Produtos Eletrônicos
    marcas = df["Indique suas preferencias a produtos eletronicos:"].str.split(", ", expand=True).stack().reset_index(level=1, drop=True)
    fig_grafico_5 = px.bar(marcas.value_counts(), x=marcas.value_counts().index, y=marcas.value_counts(), title="Preferências de Produtos Eletrônicos")
    fig_grafico_5.update_xaxes(title_text="Marcas", tickfont=dict(size=20))
    fig_grafico_5.update_yaxes(title_text="Contagem", tickfont=dict(size=20))
    fig_grafico_5.update_layout(width=1200, height=800)
    fig_grafico_5.update_traces(marker_color=cor_principal)
    col5.plotly_chart(fig_grafico_5, use_container_width=True)

    
    # Gráfico 6 - Frequência de Compra
    fig_grafico_6 = px.histogram(df, x="Informe com que frequência costuma adquirir produtos eletrônicos:", title="Frequência de Compra de Produtos Eletrônicos")
    fig_grafico_6.update_xaxes(title_text="Frequência de Compra", tickfont=dict(size=20))
    fig_grafico_6.update_yaxes(title_text="Contagem", tickfont=dict(size=20))
    fig_grafico_6.update_layout(width=1200, height=800)
    st.subheader("Frequência de Compra de Produtos Eletrônicos")
    fig_grafico_6.update_traces(marker_color=cor_principal)
    col6.plotly_chart(fig_grafico_6, use_container_width=True)


    # Gráfico 7 - Gráfico de Dispersão com Cores
    fig_grafico_7 = px.scatter(df, x="1. Qual é a sua faixa etária?", y="Informe com que frequência costuma adquirir produtos eletrônicos:", color="Avalie seu nível de experiência com produtos eletrônicos:", title="Relação entre Idade, Frequência de Compra e Nível de Experiência")
    fig_grafico_7.update_xaxes(title_text="Faixa Etária", tickfont=dict(size=20))
    fig_grafico_7.update_yaxes(title_text="Frequência de Compra", tickfont=dict(size=20))
    fig_grafico_7.update_layout(width=1200, height=800)
    fig_grafico_7.update_traces(marker_colors=[cor_principal] * len(df))
    col7.plotly_chart(fig_grafico_7, use_container_width=True)


    # Gráfico 8 - Gráfico de Barra Empilhada
    finalidades_counts = finalidades.apply(pd.Series.value_counts).T
    fig_grafico_8 = px.bar(finalidades_counts, x=finalidades_counts.index, y=finalidades_counts.sum(axis=1), title="Finalidades de Uso de Produtos Eletrônicos por Faixa Etária")
    fig_grafico_8.update_xaxes(title_text="Finalidades de Uso", tickfont=dict(size=20))
    fig_grafico_8.update_yaxes(title_text="Contagem", tickfont=dict(size=20))
    fig_grafico_8.update_layout(width=1200, height=800)
    fig_grafico_8.update_traces(marker_color=cor_principal)
    col8.plotly_chart(fig_grafico_8, use_container_width=True)


    # Gráfico 9 - Gráfico de Donuts
    dispositivo_genero_counts = df.groupby(["2. Qual o seu gênero?", "Indique seu dispositivo preferido para atividades relacionadas a produtos eletrônicos:"]).size().reset_index(name="count")
    fig_grafico_9 = px.pie(dispositivo_genero_counts, names="Indique seu dispositivo preferido para atividades relacionadas a produtos eletrônicos:", hole=0.3)
    fig_grafico_9.update_layout(width=1200, height=800)
    fig_grafico_9.update_traces(marker_colors=[cor_principal] * len(dispositivo_genero_counts))
    col9.plotly_chart(fig_grafico_9, use_container_width=True)

    # Gráfico 10 - Gráfico de Radar
    marcas_counts = df["Indique suas preferências a produtos eletrônicos:"].str.split(", ", expand=True).stack().value_counts().reset_index()
    marcas_counts.columns = ["Marca", "Contagem"]
    fig_grafico_10 = px.line_polar(marcas_counts, r="Contagem", theta="Marca", line_close=True)
    fig_grafico_10.update_layout( polar=dict(radialaxis=dict(visible=True, showticklabels=False),),showlegend=False)
    fig_grafico_10.update_xaxes(categoryorder='total ascending')  
    fig_grafico_10.update_traces(marker_color=cor_principal)
    col10.plotly_chart(fig_grafico_10, use_container_width=True)

elif aba == "Tabelas Completas":
    # Tabelas Completas
    st.subheader("Tabelas Completas")
    
    with st.expander("Clientes", expanded=False):
        st.dataframe(clientes, width=0, height=0)
        
    with st.expander("Estoque", expanded=False):
        st.dataframe(estoque, width=0, height=0)
        
    with st.expander("Fornecedores", expanded=False):
        st.dataframe(fornecedores, width=0, height=0)

