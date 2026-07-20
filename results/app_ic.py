import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Painel de Predições - Vacinas", layout="wide", page_icon="🔬")
st.title("🔬 Análise Preditiva de Associações Vacina-Reação (NMF)")
st.markdown("""
Ferramenta analítica desenvolvida para a exploração de padrões latentes em dados de farmacovigilância. 
O dashboard exibe a força de associação entre vacinas e reações adversas, padronizadas pelo dicionário **MedDRA** e
utilizando a Fatoração de Matrizes Não-Negativas (NMF), destacando potenciais eventos adversos que ainda não possuem documentação oficial na base da FDA.
""")

st.header("🔍 Explorador de Previsões")

@st.cache_data
def carregar_dados():
    arquivo = "results/all_associations_predictions.csv"
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    else:
        st.error(f"'{arquivo}' não encontrado.")
        return pd.DataFrame()

df = carregar_dados()

if not df.empty:

    st.sidebar.header("Filtros de Análise")
    
    tipo_associacao = st.sidebar.radio(
        "Filtrar Associações:",
        ("Apenas Novas Previsões (Desconhecidas)", "Apenas Conhecidas pela FDA", "Todas")
    )
    
    if tipo_associacao == "Apenas Novas Previsões (Desconhecidas)":
        df_filtrado = df[df['KNOWN_BY_FDA'] == False]
    elif tipo_associacao == "Apenas Conhecidas pela FDA":
        df_filtrado = df[df['KNOWN_BY_FDA'] == True]
    else:
        df_filtrado = df

    categorias = ["Todas"] + df_filtrado['HLGT_NAME'].dropna().unique().tolist()
    categoria_selecionada = st.sidebar.selectbox("Filtrar por Categoria (HLGT):", categorias)
    
    if categoria_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['HLGT_NAME'] == categoria_selecionada]

    vacinas = ["Todas"] + df_filtrado['TRADE_NAME'].dropna().unique().tolist()
    vacina_selecionada = st.sidebar.selectbox("Filtrar por Vacina:", vacinas)
    
    if vacina_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['TRADE_NAME'] == vacina_selecionada]


    st.markdown("### Resumo das Métricas")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Associações", f"{len(df_filtrado):,}")
    with col2:
        st.metric("Vacinas", f"{df_filtrado['TRADE_NAME'].nunique():,}")
    with col3:
        st.metric("Reações Únicas", f"{df_filtrado['ADVERSE_REACTION_PT'].nunique():,}")
    with col4:
        st.metric("Categorias (HLGT)", f"{df_filtrado['HLGT_NAME'].nunique():,}")

    st.divider()

    st.markdown("### Top 20 Associações Mais Fortes")
    
    top_20 = df_filtrado.nlargest(20, 'NORMALIZED_SCORE_0_100').sort_values(by='NORMALIZED_SCORE_0_100', ascending=True)
    
    top_20['PAR'] = top_20['TRADE_NAME'] + " + " + top_20['ADVERSE_REACTION_PT']

    fig = px.bar(
        top_20,
        y='PAR', 
        x='NORMALIZED_SCORE_0_100', 
        orientation='h',
        color='NORMALIZED_SCORE_0_100',
        color_continuous_scale='Inferno', 
        labels={
            'NORMALIZED_SCORE_0_100': 'Score Normalizado', 
            'PAR': '' 
        },
        hover_data={'HLGT_NAME': True, 'RAW_SCORE': True, 'PAR': False} 
    )
    
    fig.update_layout(
        height=600, 
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_colorbar=dict(title="Score")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Categorias com Mais Associações (HLGT)")
    
    contagem_hlgt = df_filtrado['HLGT_NAME'].value_counts().reset_index()
    contagem_hlgt.columns = ['HLGT_NAME', 'TOTAL_ASSOCIACOES']
    
    top_15_hlgt = contagem_hlgt.head(15).sort_values(by='TOTAL_ASSOCIACOES', ascending=True)

    fig_hlgt = px.bar(
        top_15_hlgt,
        x='TOTAL_ASSOCIACOES',
        y='HLGT_NAME',
        orientation='h',
        color='TOTAL_ASSOCIACOES', 
        color_continuous_scale='Blues', 
        labels={
            'TOTAL_ASSOCIACOES': 'Total de Associações', 
            'HLGT_NAME': ''
        },
        text='TOTAL_ASSOCIACOES' 
    )
    
    fig_hlgt.update_traces(textposition='outside') 
    fig_hlgt.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_showscale=False 
    )

    st.plotly_chart(fig_hlgt, use_container_width=True)
    st.divider() 
    
    st.markdown("### Tabela Detalhada")
    st.dataframe(
        df_filtrado[['TRADE_NAME', 'ADVERSE_REACTION_PT', 'HLGT_NAME', 'KNOWN_BY_FDA', 'NORMALIZED_SCORE_0_100']],
        column_config={
            "TRADE_NAME": "Nome da Vacina",
            "ADVERSE_REACTION_PT": "Reação Adversa",
            "HLGT_NAME": "Categoria da Doença (HLGT)",
            "KNOWN_BY_FDA": "Conhecida pela FDA?",
            "NORMALIZED_SCORE_0_100": st.column_config.NumberColumn(
                "Score Normalizado",
                help="Score de predição do modelo NMF (0 a 100)",
                format="%.2f" 
            )
        },
        use_container_width=True,
        hide_index=True
    )