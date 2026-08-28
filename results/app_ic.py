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
        st.error(f"'{arquivo}' não encontrado. Verifique o caminho do arquivo.")
        return pd.DataFrame()

df = carregar_dados()

if not df.empty:
    
    st.sidebar.header("Filtros de Análise")
    
    tipo_associacao = st.sidebar.radio(
        "Filtrar Associações:",
        ("Todas", "Apenas Novas Previsões (Desconhecidas)", "Apenas Conhecidas pela FDA")
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

    tab1, tab2 = st.tabs(["Dashboard Analítico", "Consulta de Dados"])

    with tab1:
        st.markdown("### Resumo das Métricas")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Associações", f"{len(df_filtrado):,}")
        with col2:
            st.metric("Vacinas", f"{df_filtrado['TRADE_NAME'].nunique():,}")
        with col3:
            st.metric("Reações Únicas (PT)", f"{df_filtrado['ADVERSE_REACTION_PT'].nunique():,}")
        with col4:
            st.metric("Categorias (HLGT)", f"{df_filtrado['HLGT_NAME'].nunique():,}")

        st.divider()
        
        col_donut, col_bar_hlgt = st.columns([1, 1.5])
        
        with col_donut:
            st.markdown("#### Proporção de Associações")
            if 'KNOWN_BY_FDA' in df_filtrado.columns:
                contagem_fda = df_filtrado['KNOWN_BY_FDA'].value_counts().reset_index()
                contagem_fda.columns = ['Status FDA', 'Contagem']
                contagem_fda['Status FDA'] = contagem_fda['Status FDA'].map({True: 'Conhecida (FDA)', False: 'Nova Previsão (NMF)'})

                fig_pie = px.pie(
                    contagem_fda, 
                    names='Status FDA', 
                    values='Contagem',
                    hole=0.4,
                    color='Status FDA',
                    color_discrete_map={'Conhecida (FDA)': '#2E86C1', 'Nova Previsão (NMF)': '#E74C3C'}
                )
                fig_pie.update_layout(
                    height=380, 
                    margin=dict(l=0, r=0, t=30, b=0),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        with col_bar_hlgt:
            st.markdown("#### Categorias com Mais Associações (HLGT)")
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
                labels={'TOTAL_ASSOCIACOES': 'Total de Associações', 'HLGT_NAME': ''},
                text='TOTAL_ASSOCIACOES' 
            )
            fig_hlgt.update_traces(textposition='outside') 
            fig_hlgt.update_layout(height=380, margin=dict(l=0, r=0, t=10, b=0), coloraxis_showscale=False)
            st.plotly_chart(fig_hlgt, use_container_width=True)

        st.divider()

        st.markdown("### Top 20 Associações Mais Fortes")
        top_20 = df_filtrado.nlargest(20, 'NORMALIZED_SCORE_0_100').sort_values(by='NORMALIZED_SCORE_0_100', ascending=True)
        top_20['PAR'] = top_20['TRADE_NAME'] + " + " + top_20['ADVERSE_REACTION_PT']

        fig_bar = px.bar(
            top_20,
            y='PAR', 
            x='NORMALIZED_SCORE_0_100', 
            orientation='h',
            color='NORMALIZED_SCORE_0_100',
            color_continuous_scale='Inferno', 
            labels={
                'NORMALIZED_SCORE_0_100': 'Score Normalizado', 
                'PAR': '',
                'HLGT_NAME': 'Categoria HLGT',
                'RAW_SCORE': 'Score Bruto',
                'KNOWN_BY_FDA': 'Conhecida pela FDA?'
            },
            hover_data={
                'HLGT_NAME': True, 
                'RAW_SCORE': ':.4f', # Limita o tooltip a 4 casas decimais
                'KNOWN_BY_FDA': True, 
                'PAR': False
            } 
        )
        
        fig_bar.update_layout(
            height=500, 
            margin=dict(l=0, r=0, t=30, b=0),
            coloraxis_colorbar=dict(title="Score")
        )
        st.plotly_chart(fig_bar, use_container_width=True)
            
        st.divider()

        st.markdown("### Mapa de Calor: Intensidade Latente (Top Vacinas x Top Categorias)")
        
        top_vacinas = df_filtrado['TRADE_NAME'].value_counts().nlargest(15).index
        top_categorias = top_15_hlgt.sort_values(by='TOTAL_ASSOCIACOES', ascending=False)['HLGT_NAME'].head(15).tolist()

        df_heatmap = df_filtrado[
            (df_filtrado['TRADE_NAME'].isin(top_vacinas)) & 
            (df_filtrado['HLGT_NAME'].isin(top_categorias))
        ]

        if not df_heatmap.empty:
            fig_heat = px.density_heatmap(
                df_heatmap, 
                x="HLGT_NAME", 
                y="TRADE_NAME", 
                z="NORMALIZED_SCORE_0_100", 
                histfunc="avg",
                color_continuous_scale="Viridis",
                labels={
                    "HLGT_NAME": "Categoria (HLGT)", 
                    "TRADE_NAME": "Vacina",
                    "NORMALIZED_SCORE_0_100": "Score Médio"
                }
            )
            
            fig_heat.update_traces(
                hovertemplate="<b>Categoria (HLGT):</b> %{x}<br><b>Vacina:</b> %{y}<br><b>Score Médio:</b> %{z:.4f}<extra></extra>"
            )
            
            fig_heat.update_layout(height=550, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.info("Os filtros atuais não possuem dados sobrepostos suficientes para gerar o heatmap.")

        st.divider()

        st.markdown("### Hierarquia de Reações Específicas (Treemap - PT)")
        st.caption("Navegue pelas categorias (HLGT) para ver as reações específicas (PT) e as vacinas associadas. O tamanho representa a força do Score Normalizado.")
        
        top_pt_df = df_filtrado.nlargest(100, 'NORMALIZED_SCORE_0_100').fillna("Desconhecido")
        
        if not top_pt_df.empty:
            fig_tree = px.treemap(
                top_pt_df,
                path=[px.Constant("Previsões NMF"), 'HLGT_NAME', 'ADVERSE_REACTION_PT', 'TRADE_NAME'],
                values='NORMALIZED_SCORE_0_100',
                color='NORMALIZED_SCORE_0_100',
                color_continuous_scale='Inferno',
                labels={'NORMALIZED_SCORE_0_100': 'Score'}
            )
            
            fig_tree.update_traces(
                hovertemplate="<b>%{label}</b><br>Score Normalizado: %{value:.2f}<extra></extra>"
            )
            
            fig_tree.update_layout(
                height=650, 
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_tree, use_container_width=True)
        else:
            st.info("Dados insuficientes para gerar o mapa de árvore.")

    with tab2:
        st.markdown("### Registro de Associações Preditivas (NMF vs. FDALabel)")
        st.dataframe(
            df_filtrado[['TRADE_NAME', 'ADVERSE_REACTION_PT', 'HLGT_NAME', 'KNOWN_BY_FDA', 'RAW_SCORE', 'NORMALIZED_SCORE_0_100']],
            column_config={
                "TRADE_NAME": "Nome da Vacina",
                "ADVERSE_REACTION_PT": "Reação Adversa (PT)",
                "HLGT_NAME": "Categoria HLGT",
                "KNOWN_BY_FDA": "Conhecida pela FDA?",
                "RAW_SCORE": st.column_config.NumberColumn(
                    "Score Bruto",
                    help="Valor original da reconstrução da matriz NMF",
                    format="%.4f" 
                ),
                "NORMALIZED_SCORE_0_100": st.column_config.NumberColumn(
                    "Score Normalizado",
                    help="Score de predição escalonado (0 a 100)",
                    format="%.2f" 
                )
            },
            use_container_width=True,
            hide_index=True
        )