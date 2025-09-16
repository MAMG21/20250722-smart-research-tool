import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk
import networkx as nx
import plotly.express as px

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(
    page_title="OpenAlex Analytics - Demo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS GLOBALES ---
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #EBECF1;
        }
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #0771B6;
            margin-bottom: 5px;
        }
        .subtitle {
            text-align: center;
            font-size: 22px;
            font-weight: 500;
            color: #46566F;
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            color: black;
            margin-top: 25px;
            margin-bottom: 10px;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            font-size: 14px;
            color: black;
            font-weight: 500;
        }
        .profile-metrics-row {
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            gap: 30px;
            margin-bottom: 30px;
        }
        .author-box {
            width: 300px;
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .author-box img {
            border-radius: 50%;
            width: 120px;
            height: 120px;
            object-fit: cover;
            margin-bottom: 15px;
        }
        .author-name {
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 8px;
        }
        .author-affiliation {
            font-size: 14px;
            color: #46566F;
        }
        .metrics-box {
            flex: 1;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: flex-start;
        }
        .metric-card {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 10px 16px;
            text-align: center;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
            flex: 1 1 160px;
            min-width: 160px;
            max-width: 200px;
        }
        .metric-card h4 {
            margin: 0;
            font-size: 16px;
        }
        .metric-card p {
            font-size: 20px;
            font-weight: bold;
            margin: 5px 0 0 0;
        }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO Y SUBTÍTULO ---
st.markdown(
    """
    <div class="main-title">Evaluación de la producción científica de investigadores con métricas y altmétricas a partir de bases de datos bibliográficas dinámicas</div>
    <div class="subtitle">Maestría en Estadística Aplicada a Ciencia de Datos</div>
    """,
    unsafe_allow_html=True
)

# --- PERFIL DEL AUTOR + MÉTRICAS ---
st.markdown("""
<div class="profile-metrics-row">
    <div class="author-box">
        <img src="https://randomuser.me/api/portraits/men/75.jpg" alt="Foto autor">
        <div class="author-name">Nombre Autor</div>
        <div class="author-affiliation">Afiliación Autor</div>
    </div>
    <div class="metrics-box">
        <div class="metric-card"><h4>📄 Total Artículos</h4><p>100</p></div>
        <div class="metric-card"><h4>🧾 Total Citas</h4><p>2,000</p></div>
        <div class="metric-card"><h4>📗 H-index</h4><p>120</p></div>
        <div class="metric-card"><h4>📘 G-index</h4><p>150</p></div>
        <div class="metric-card"><h4>📙 E-index</h4><p>80</p></div>
        <div class="metric-card"><h4>📕 M-index</h4><p>10</p></div>
        <div class="metric-card"><h4>📒 B-index</h4><p>5</p></div>
        <div class="metric-card"><h4>📓 V-index</h4><p>20</p></div>
        <div class="metric-card"><h4>🔟 i10-index</h4><p>15</p></div>
        <div class="metric-card"><h4>🧮 K-index</h4><p>11</p></div>
        <div class="metric-card"><h4>📏 H Fraccional</h4><p>12</p></div>
        <div class="metric-card"><h4>🏅 Autorank</h4><p>200</p></div>
        <div class="metric-card"><h4>📊 H Relativo</h4><p>100</p></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- PERFIL DEL INVESTIGADOR ---
st.markdown('<div class="section-title">👤 Perfil del Investigador</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("🌍 Mapa de publicaciones")
    # Datos ficticios de publicaciones por país
    df_map = pd.DataFrame({
    "country": ["USA", "FRA", "JPN", "COL", "BRA"],  # ISO-3 codes
    "publications": [100, 50, 70, 30, 40]
    })

    fig_map = px.choropleth(
        df_map,
        locations="country",
        color="publications",
        hover_name="country",
        color_continuous_scale="Blues",
        projection="natural earth"
    )

    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.markdown("🤝 Colaboraciones entre autores")
    G = nx.Graph()
    G.add_edges_from([
        ("Yann LeCun", "Geoffrey Hinton"),
        ("Yann LeCun", "Yoshua Bengio"),
        ("Yann LeCun", "Jürgen Schmidhuber")
    ])

    fig, ax = plt.subplots(figsize=(4, 2))
    pos = nx.spring_layout(G, seed=20)
    nx.draw(G, pos, with_labels=True, node_size=200, node_color="lightblue", font_size=5, ax=ax)
    st.pyplot(fig)

# --- GRÁFICAS EN UNA SOLA FILA ---
st.markdown('<div class="section-title">📈 Evolución de Publicaciones y Citas</div>', unsafe_allow_html=True)

years = np.arange(2000, 2021)
pubs = np.random.randint(5, 30, size=len(years)).cumsum()
cites = np.random.randint(100, 1000, size=len(years)).cumsum()
freq_cites = np.random.randint(0, 200, size=len(years))
pubs_yearly = np.random.randint(1, 30, size=len(years))

col1, col2, col3, col4 = st.columns(4)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(years, pubs, marker="o")
    ax1.set_title("Artículos acumulados")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(years, cites, marker="o", color="red")
    ax2.set_title("Citas acumuladas")
    st.pyplot(fig2)

with col3:
    fig3, ax3 = plt.subplots()
    ax3.bar(years, freq_cites)
    ax3.set_title("Frecuencia de citas")
    st.pyplot(fig3)

with col4:
    fig4, ax4 = plt.subplots()
    ax4.bar(years, pubs_yearly, color="green")
    ax4.set_title("Publicaciones por año")
    st.pyplot(fig4)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        Universidad El Bosque - Facultad de Ciencias <br>
        Autores: Nelson Maya y Maria Alejandra Marin
    </div>
""", unsafe_allow_html=True)

