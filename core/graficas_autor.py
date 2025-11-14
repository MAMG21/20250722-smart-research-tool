# core/graficas_autor.py
# ============================================================
# 📚 MÓDULO DE ANÁLISIS Y VISUALIZACIÓN DE AUTORES (Plotly)
# ============================================================

import io
from collections import Counter
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import networkx as nx
from scipy.optimize import curve_fit
from wordcloud import WordCloud
from PIL import Image
import pycountry
from geopy.geocoders import Nominatim
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns

# Ruta para guardar imagen de la grafica
OUTPUT_DIR = "outputs"
# ============================================================
# 1️⃣ Publicaciones por año
# ============================================================
def graficar_publicaciones_por_anio(df_master, author_display_name):
    """
    Grafica la cantidad de publicaciones por año usando Plotly (para Streamlit).
    """

    # --- Validación del DataFrame ---
    if df_master is None or df_master.empty:
        st.warning("⚠️ No se pudo generar el gráfico: el DataFrame está vacío o no existe.")
        return

    if "publication_year" not in df_master.columns:
        st.warning("⚠️ El DataFrame no contiene la columna 'publication_year'.")
        return

    # --- Preparar los datos ---
    publications_by_year = df_master["publication_year"].value_counts().sort_index()
    publications_by_year = publications_by_year.loc[publications_by_year.index >= 1900]

    # Asegurar años continuos hasta 2025
    all_years = pd.Series(0, index=range(publications_by_year.index.min(), 2026))
    publications_by_year = all_years.add(publications_by_year, fill_value=0).astype(int)

    # Crear DataFrame resumido
    publications_df = pd.DataFrame({
        "year": publications_by_year.index,
        "count": publications_by_year.values
    })

    # Asegurar que el nombre del autor no cause errores
    if not author_display_name:
        author_display_name = ""

    # --- Crear gráfico interactivo ---
    fig = px.bar(
        publications_df,
        x="year",
        y="count",
        text="count",  # Etiquetas de datos
        labels={"year": "Año de publicación", "count": "Número de artículos"},
        color_discrete_sequence=["dodgerblue"]
    )

    # Configurar etiquetas y estilo
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        hovertemplate="Año: %{x}<br>Publicaciones: %{y}<extra></extra>"
    )

    fig.update_layout(
        title="",
        showlegend=False,
        plot_bgcolor="white",
        xaxis=dict(tickangle=45),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True
    )

    # --- Mostrar en Streamlit ---
    st.plotly_chart(fig, use_container_width=True)

    # --- Guardar PDF opcional ---
    safe_author_name = author_display_name.replace(' ', '_').replace('.', '').lower()
    file_publicaciones = f"{OUTPUT_DIR}/graficar_publicaciones_por_anio_{safe_author_name}.png"
    fig.write_image(file_publicaciones)

# ============================================================
# 2️⃣ Citas por año
# ============================================================
def graficar_citas_por_anio(df_master, author_display_name):
    """
    Grafica la cantidad de citas por año usando Plotly (versión limpia para Streamlit).
    """

    if df_master is None or df_master.empty:
        st.warning("⚠️ No se pudo generar el gráfico: el DataFrame está vacío o no existe.")
        return

    # --- Funciones auxiliares ---
    def safe_split(x):
        """Convierte un string tipo '2025|2024|2023' en lista ['2025','2024','2023']"""
        if isinstance(x, str) and "|" in x:
            return x.split("|")
        elif isinstance(x, str):
            return [x]
        elif isinstance(x, list):
            return x
        else:
            return []

    def to_int_list(lst):
        out = []
        for val in lst:
            try:
                out.append(int(val))
            except:
                out.append(0)
        return out

    df_master["year_list"] = df_master["counts_by_year.year"].apply(safe_split)
    df_master["cited_list"] = df_master["counts_by_year.cited_by_count"].apply(safe_split)

    df_master["year_list"] = df_master["year_list"].apply(to_int_list)
    df_master["cited_list"] = df_master["cited_list"].apply(to_int_list)

    # --- Desanidar datos ---
    expanded_rows = []
    for _, row in df_master.iterrows():
        years = row["year_list"]
        cites = row["cited_list"]
        if len(years) == len(cites) and len(years) > 0:
            for y, c in zip(years, cites):
                expanded_rows.append({"year": y, "cited_by_count": c})

    if len(expanded_rows) == 0:
        st.warning("⚠️ No se pudieron expandir los datos: revisa las columnas 'counts_by_year.*'.")
        return

    citations_df = pd.DataFrame(expanded_rows)
    citations_summary = (
        citations_df.groupby("year", as_index=False)
        .agg({"cited_by_count": "sum"})
        .sort_values("year", ascending=True)
    )

    # --- Gráfico interactivo con Plotly ---
    fig = px.bar(
        citations_summary,
        x="year",
        y="cited_by_count",
        text="cited_by_count",
        labels={"year": "Año", "cited_by_count": "Número total de citas"},
        color_discrete_sequence=["dodgerblue"]
    )

    # Personalizar etiquetas
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",  # Muestra las etiquetas sobre las barras
        hovertemplate="Año: %{x}<br>Citas: %{y}<extra></extra>"
    )

    # Estilo visual
    fig.update_layout(
        title="",
        showlegend=False,
        plot_bgcolor="white",
        xaxis=dict(tickangle=45),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Guardar PDF opcional ---
    safe_author_name = author_display_name.replace(' ', '_').replace('.', '').lower()
    file_citas_ano = f"{OUTPUT_DIR}/graficar_citas_por_anio_{safe_author_name}.png"
    fig.write_image(file_citas_ano)

# ============================================================
# 3️⃣ Posición de autoría (solo barras)
# ============================================================
def graficar_posicion_autoria(df_master, author_display_name):
    """
    Grafica la frecuencia de aparición del autor según su posición en la lista de autores.
    Compatible con Streamlit y coherente con la paleta azul de las otras gráficas.
    """

    # --- Validaciones iniciales ---
    if df_master is None or df_master.empty:
        st.warning("⚠️ No se pudo generar el gráfico: el DataFrame está vacío o no existe.")
        return

    if "authors" not in df_master.columns:
        st.warning("⚠️ El DataFrame no contiene la columna 'authors'.")
        return

    if not author_display_name:
        st.warning("⚠️ Debes proporcionar un nombre de autor válido.")
        return

    # --- Calcular la frecuencia por posición ---
    pos_counts = {'1er Autor': 0, '2do Autor': 0, '3er Autor': 0, '4to o más': 0}

    for authors_str in df_master['authors'].dropna():
        authors_list = [author.strip() for author in authors_str.split(';')]
        try:
            position = authors_list.index(author_display_name) + 1
            if position == 1:
                pos_counts['1er Autor'] += 1
            elif position == 2:
                pos_counts['2do Autor'] += 1
            elif position == 3:
                pos_counts['3er Autor'] += 1
            else:
                pos_counts['4to o más'] += 1
        except ValueError:
            continue

    # --- Crear DataFrame para graficar ---
    plot_data = pd.DataFrame(list(pos_counts.items()), columns=['Posición', 'Frecuencia'])

    # Orden lógico de posiciones
    orden_posiciones = ['1er Autor', '2do Autor', '3er Autor', '4to o más']
    plot_data['Posición'] = pd.Categorical(plot_data['Posición'], categories=orden_posiciones, ordered=True)

    # --- Crear gráfico con Plotly ---
    fig = px.bar(
        plot_data,
        x="Posición",
        y="Frecuencia",
        text="Frecuencia",
        color="Frecuencia",
        color_continuous_scale="Blues"
    )

    # Etiquetas y formato
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        hovertemplate="Posición: %{x}<br>Frecuencia: %{y}<extra></extra>"
    )

    fig.update_layout(
        title="",
        showlegend=False,
        plot_bgcolor="white",
        coloraxis_showscale=False,
        xaxis_title="Posición en la lista de autores",
        yaxis_title="Número de veces en esa posición",
        height=350,
        margin=dict(l=2, r=2, t=2, b=2),
        autosize=True
    )

    # --- Mostrar en Streamlit ---
    st.plotly_chart(fig, use_container_width=True)

    # --- Guardar PDF ---
    safe_author_name = author_display_name.replace(' ', '_').replace('.', '').lower()
    file_autoria = f"{OUTPUT_DIR}/graficar_posicion_autoria_{safe_author_name}.png"
    fig.write_image(file_autoria)

# ============================================================
# 4️⃣ Red de coautoría (mantiene nodos)
# ============================================================
def graficar_red_coautoria(df_master, author_display_name):
    """
    Grafica la red de coautoría del autor principal (interactiva con Plotly y Streamlit).
    Usa tonos azules (paleta 'Blues') y destaca al autor principal en color salmón.
    """

    # --- Validaciones ---
    if df_master is None or df_master.empty:
        st.warning("⚠️ No se pudo generar la red: el DataFrame está vacío o no existe.")
        return

    if "authors" not in df_master.columns:
        st.warning("⚠️ El DataFrame no contiene la columna 'authors'.")
        return

    if not author_display_name:
        st.warning("⚠️ Debes proporcionar un nombre de autor válido.")
        return

    autor_principal = author_display_name

    # --- Contar coautores ---
    coauthor_counter = Counter()
    for author_list_str in df_master["authors"].dropna():
        authors_in_paper = [name.strip() for name in author_list_str.split(";")]
        if autor_principal in authors_in_paper:
            authors_in_paper.remove(autor_principal)
            coauthor_counter.update(authors_in_paper)

    top_5_coauthors = coauthor_counter.most_common(5)
    if not top_5_coauthors:
        st.warning(f"⚠️ No se encontraron coautores para {autor_principal}.")
        return

    # --- Crear grafo ---
    G = nx.Graph()
    G.add_node(autor_principal)
    for coauthor, count in top_5_coauthors:
        G.add_node(coauthor)
        G.add_edge(autor_principal, coauthor, weight=count)

    # --- Layout y posiciones ---
    pos = nx.spring_layout(G, seed=42, k=0.8, iterations=150)

    # --- Extraer coordenadas ---
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1.5, color="gray"),
        hoverinfo="none",
        mode="lines"
    )

    # --- Nodos ---
    node_x, node_y, node_color, node_size, node_text = [], [], [], [], []
    max_weight = max([count for _, count in top_5_coauthors]) if top_5_coauthors else 1

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        if node == autor_principal:
            color = "salmon"
            size = 30
            text = f"{node} (Autor principal)"
        else:
            count = dict(top_5_coauthors).get(node, 1)
            intensity = 0.3 + 0.7 * (count / max_weight)
            color = f"rgba(30, 144, 255, {intensity})"  # Azul tipo 'dodgerblue' con transparencia
            size = 20 + (count / max_weight) * 10
            text = f"{node}<br>{count} publicaciones conjuntas"

        node_color.append(color)
        node_size.append(size)
        node_text.append(text)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        textposition="bottom center",
        hoverinfo="text",
        text=[n for n in G.nodes()],
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line_width=1.5
        )
    )

    # --- Crear figura ---
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        height=350,
        margin=dict(l=2, r=2, t=2, b=2),
        autosize=True,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    # --- Auto-zoom dinámico ---
    padding = 0.15
    x_min, x_max = min(node_x), max(node_x)
    y_min, y_max = min(node_y), max(node_y)

    fig.update_xaxes(
        visible=False,
        range=[x_min - padding, x_max + padding]
    )
    fig.update_yaxes(
        visible=False,
        scaleanchor="x",
        scaleratio=1,
        range=[y_min - padding, y_max + padding]
    )

    # --- Mostrar en Streamlit ---
    st.plotly_chart(fig, use_container_width=True)

    # --- Guardar PDF ---
    safe_author_name = author_display_name.replace(' ', '_').replace('.', '').lower()
    file_co_autoria = f"{OUTPUT_DIR}/graficar_red_coautoria_{safe_author_name}.png"
    fig.write_image(file_co_autoria)

# ============================================================
# 5️⃣ Red de colaboración entre instituciones (mantiene nodos)
# ============================================================
def graficar_red_instituciones(df_master, author_display_name):
    """
    Grafica la red de colaboración institucional del autor principal.
    - Muestra la institución principal en color salmón.
    - Colaboradoras en tonos de azul (paleta tipo 'Blues').
    - Gráfico interactivo con Plotly.
    """

    # --- Validaciones ---
    if df_master is None or df_master.empty:
        st.warning("⚠️ No se pudo generar la red: el DataFrame está vacío o no existe.")
        return

    if "institutions_list" not in df_master.columns:
        st.warning("⚠️ El DataFrame no contiene la columna 'institutions_list'.")
        return

    autor_objetivo = author_display_name
    df_autor = df_master.copy()

    # --- Construcción del grafo ---
    colaboraciones = Counter()
    G = nx.Graph()

    for _, row in df_autor.iterrows():
        if pd.isna(row["institutions_list"]):
            continue

        instituciones = set(inst.strip() for inst in str(row["institutions_list"]).split(";") if inst.strip())
        instituciones = list(instituciones)

        for i in range(len(instituciones)):
            for j in range(i + 1, len(instituciones)):
                inst1, inst2 = tuple(sorted((instituciones[i], instituciones[j])))
                colaboraciones[(inst1, inst2)] += 1
                G.add_edge(inst1, inst2, weight=colaboraciones[(inst1, inst2)])

    # --- Identificar institución principal ---
    todas_instituciones = [
        inst.strip()
        for sublist in df_autor["institutions_list"].dropna().str.split(";")
        for inst in sublist if inst.strip()
    ]
    if not todas_instituciones:
        st.warning("⚠️ No hay instituciones válidas en los datos.")
        return

    institucion_principal = Counter(todas_instituciones).most_common(1)[0][0]

    # --- Filtrar colaboraciones relevantes ---
    colaboraciones_principales = Counter()
    for (inst1, inst2), w in colaboraciones.items():
        if inst1 == institucion_principal:
            colaboraciones_principales[inst2] += w
        elif inst2 == institucion_principal:
            colaboraciones_principales[inst1] += w

    top_5 = dict(colaboraciones_principales.most_common(5))
    if not top_5:
        st.warning(f"⚠️ No se encontraron colaboraciones para '{institucion_principal}'.")
        return

    # --- Crear layout circular ---
    G_sub = nx.Graph()
    G_sub.add_node(institucion_principal)
    for nodo, w in top_5.items():
        G_sub.add_node(nodo)
        G_sub.add_edge(institucion_principal, nodo, weight=w)

    n = len(top_5)
    radius = 4.0
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pos = {institucion_principal: np.array([0, 0])}
    for i, nodo in enumerate(top_5.keys()):
        pos[nodo] = np.array([radius * np.cos(angles[i]), radius * np.sin(angles[i])])

    # --- Aristas (cada una con su propio grosor) ---
    edge_traces = []
    max_w = max(top_5.values()) if top_5 else 1

    for nodo, w in top_5.items():
        x0, y0 = pos[institucion_principal]
        x1, y1 = pos[nodo]

        edge_traces.append(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(width=1.5 + 3 * (w / max_w), color="gray"),
                hoverinfo="none"
            )
        )

    # --- Nodos ---
    node_x, node_y, node_color, node_size, node_text = [], [], [], [], []
    for node in G_sub.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        if node == institucion_principal:
            color = "salmon"
            size = 35
            text = f"{node} (Institución principal)"
        else:
            w = top_5[node]
            intensity = 0.3 + 0.7 * (w / max_w)
            color = f"rgba(30, 144, 255, {intensity})"  # Azul tipo 'Blues'
            size = 22 + (w / max_w) * 10
            text = f"{node}<br>{w} publicaciones conjuntas"

        node_color.append(color)
        node_size.append(size)
        node_text.append(text)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=[n for n in G_sub.nodes()],
        textposition="bottom center",
        hoverinfo="text",
        hovertext=node_text,
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line_width=1.5,
            line=dict(color="darkblue", width=1)
        )
    )

    # --- Crear figura ---
    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True
    )

    # --- Mostrar en Streamlit ---
    st.plotly_chart(fig, use_container_width=True)

    # --- Guardar PDF ---
    safe_author_name = author_display_name.replace(' ', '_').replace('.', '').lower()
    file_instituciones = f"{OUTPUT_DIR}/graficar_red_instituciones_{safe_author_name}.png"
    fig.write_image(file_instituciones)

# ============================================================
# 6️⃣ Mapa de colaboraciones internacionales
# ============================================================
def graficar_mapa_colaboraciones_internacionales(df_master, author_display_name):
    """
    Muestra un mapa mundial con las colaboraciones internacionales
    del autor especificado. Usa coordenadas fijas (sin geopy).
    """
    # --- VALIDACIÓN INICIAL ---
    if df_master is None or df_master.empty:
        st.warning("⚠️ No hay datos disponibles para generar el mapa de colaboración.")
        return

    df_autor = df_master.copy()

    # --- Coordenadas fijas por país (ISO-2) ---
    COORDS_BACKUP = {
        "AR": (-38.4161, -63.6167),   # Argentina
        "BR": (-14.2350, -51.9253),   # Brasil
        "CA": (56.1304, -106.3468),   # Canadá
        "CH": (46.8182, 8.2275),      # Suiza
        "CL": (-35.6751, -71.5430),   # Chile
        "CO": (4.5709, -74.2973),     # Colombia
        "DE": (51.1657, 10.4515),     # Alemania
        "ES": (40.4637, -3.7492),     # España
        "FR": (46.6034, 1.8883),      # Francia
        "GB": (55.3781, -3.4360),     # Reino Unido
        "IL": (31.0461, 34.8516),     # Israel
        "IT": (41.8719, 12.5674),     # Italia
        "JP": (36.2048, 138.2529),    # Japón
        "LB": (33.8547, 35.8623),     # Líbano
        "RU": (61.5240, 105.3188),    # Rusia
        "US": (37.0902, -95.7129),    # Estados Unidos

        # --- Continúo con más de 100 países ---
        "MX": (23.6345, -102.5528),   # México
        "PE": (-9.1899, -75.0152),    # Perú
        "EC": (-1.8312, -78.1834),    # Ecuador
        "BO": (-16.2902, -63.5887),   # Bolivia
        "PY": (-23.4425, -58.4438),   # Paraguay
        "UY": (-32.5228, -55.7658),   # Uruguay
        "VE": (6.4238, -66.5897),     # Venezuela
        "AU": (-25.2744, 133.7751),   # Australia
        "NZ": (-40.9006, 174.8860),   # Nueva Zelanda
        "CN": (35.8617, 104.1954),    # China
        "KR": (35.9078, 127.7669),     # Corea del Sur
        "IN": (20.5937, 78.9629),     # India
        "PK": (30.3753, 69.3451),     # Pakistán
        "BD": (23.6850, 90.3563),     # Bangladés
        "NP": (28.3949, 84.1240),     # Nepal
        "TH": (15.8700, 100.9925),    # Tailandia
        "VN": (14.0583, 108.2772),    # Vietnam
        "PH": (12.8797, 121.7740),    # Filipinas
        "ID": (-0.7893, 113.9213),    # Indonesia
        "MY": (4.2105, 101.9758),     # Malasia
        "SG": (1.3521, 103.8198),     # Singapur
        "SA": (23.8859, 45.0792),     # Arabia Saudita
        "AE": (23.4241, 53.8478),     # Emiratos Árabes Unidos
        "QA": (25.3548, 51.1839),     # Catar
        "KW": (29.3117, 47.4818),     # Kuwait
        "OM": (21.4735, 55.9754),     # Omán
        "IR": (32.4279, 53.6880),     # Irán
        "IQ": (33.2232, 43.6793),     # Irak
        "JO": (30.5852, 36.2384),     # Jordania
        "SY": (34.8021, 38.9968),     # Siria
        "TR": (38.9637, 35.2433),     # Turquía
        "GR": (39.0742, 21.8243),     # Grecia
        "PT": (39.3999, -8.2245),     # Portugal
        "NL": (52.1326, 5.2913),      # Países Bajos
        "BE": (50.5039, 4.4699),      # Bélgica
        "LU": (49.8153, 6.1296),      # Luxemburgo
        "AT": (47.5162, 14.5501),     # Austria
        "PL": (51.9194, 19.1451),     # Polonia
        "CZ": (49.8175, 15.4730),     # Chequia
        "SK": (48.6690, 19.6990),     # Eslovaquia
        "HU": (47.1625, 19.5033),     # Hungría
        "RO": (45.9432, 24.9668),     # Rumanía
        "BG": (42.7339, 25.4858),     # Bulgaria
        "DK": (56.2639, 9.5018),      # Dinamarca
        "NO": (60.4720, 8.4689),      # Noruega
        "SE": (60.1282, 18.6435),     # Suecia
        "FI": (61.9241, 25.7482),     # Finlandia
        "IE": (53.1424, -7.6921),     # Irlanda
        "IS": (64.9631, -19.0208),    # Islandia
        "UA": (48.3794, 31.1656),     # Ucrania
        "BY": (53.7098, 27.9534),     # Bielorrusia
        "GE": (42.3154, 43.3569),     # Georgia
        "AM": (40.0691, 45.0382),     # Armenia
        "AZ": (40.1431, 47.5769),     # Azerbaiyán

        # África (más de 30 países)
        "ZA": (-30.5595, 22.9375),    # Sudáfrica
        "EG": (26.8206, 30.8025),     # Egipto
        "NG": (9.0820, 8.6753),       # Nigeria
        "KE": (-0.0236, 37.9062),     # Kenia
        "TZ": (-6.3690, 34.8888),     # Tanzania
        "UG": (1.3733, 32.2903),      # Uganda
        "ET": (9.1450, 40.4897),      # Etiopía
        "SD": (12.8628, 30.2176),     # Sudán
        "SS": (6.8770, 31.3070),      # Sudán del Sur
        "MA": (31.7917, -7.0926),     # Marruecos
        "DZ": (28.0339, 1.6596),      # Argelia
        "TN": (33.8869, 9.5375),      # Túnez
        "LY": (26.3351, 17.2283),     # Libia
        "ML": (17.5707, -3.9962),     # Mali
        "NE": (17.6078, 8.0817),      # Níger
        "GH": (7.9465, -1.0232),      # Ghana
        "CI": (7.5399, -5.5471),      # Costa de Marfil
        "SN": (14.4974, -14.4524),    # Senegal
        "GM": (13.4432, -15.3101),    # Gambia
        "SL": (8.4606, -11.7799),     # Sierra Leona
        "LR": (6.4281, -9.4295),      # Liberia
        "CM": (7.3697, 12.3547),      # Camerún
        "GA": (-0.8037, 11.6094),     # Gabón
        "CG": (-0.2280, 15.8277),     # Congo
        "CD": (-4.0383, 21.7587),     # R. D. Congo
        "AO": (-11.2027, 17.8739),    # Angola
        "ZM": (-13.1339, 27.8493),    # Zambia
        "MW": (-13.2543, 34.3015),    # Malaui
        "ZW": (-19.0154, 29.1549),    # Zimbabue
        "BW": (-22.3285, 24.6849),    # Botsuana
        "NA": (-22.9576, 18.4904),    # Namibia
        "MG": (-18.7669, 46.8691),    # Madagascar

        # Caribe y otros
        "CU": (21.5218, -77.7812),    # Cuba
        "DO": (18.7357, -70.1627),    # Rep. Dominicana
        "HT": (18.9712, -72.2852),    # Haití
        "JM": (18.1096, -77.2975),    # Jamaica
        "BS": (25.0343, -77.3963),    # Bahamas
    }

    # --- Encontrar país principal ---
    all_countries = []
    for country_list in df_autor['countries_list'].dropna():
        countries = [c.strip() for c in country_list.split(';') if c.strip()]
        all_countries.extend(countries)

    if not all_countries:
        st.warning("❌ No se encontraron datos válidos de países en las publicaciones del autor.")
        return

    country_counter = Counter(all_countries)
    pais_principal_code = country_counter.most_common(1)[0][0]

    # --- Encontrar los 5 países más colaboradores ---
    collaboration_counter = Counter()
    for _, row in df_autor.iterrows():
        if pd.isna(row['countries_list']):
            continue
        countries = set(row['countries_list'].split(';'))
        countries = {c for c in countries if c.strip()}
        countries.discard(pais_principal_code)
        collaboration_counter.update(countries)

    top_collaborators = collaboration_counter.most_common(5)

    if not top_collaborators:
        st.warning("⚠️ No se encontraron colaboraciones internacionales registradas.")
        return

    # --- Obtener coordenadas ---
    all_country_codes = [pais_principal_code] + [c[0] for c in top_collaborators]
    country_coords = {}
    country_names = {}

    geolocator = Nominatim(user_agent="geo-app", timeout=8)

    with st.spinner("🌐 Obteniendo coordenadas de los países..."):
        for code in all_country_codes:
            try:
                country_obj = pycountry.countries.get(alpha_2=code)
                if country_obj:
                    country_names[code] = country_obj.name
                    # ✅ Primero usar backup si existe
                    if code in COORDS_BACKUP:
                        country_coords[code] = COORDS_BACKUP[code]
                    else:
                        # Intentar geolocalización
                        location = geolocator.geocode(country_obj.name)
                        if location:
                            country_coords[code] = (location.latitude, location.longitude)
                            
            except Exception as e:
                st.error(f"❌ Error obteniendo coordenadas para {code}: {e}")
                continue

    if pais_principal_code not in country_coords:
        st.error("❌ No se pudieron obtener coordenadas para el país principal.")
        return

    # --- Crear mapa interactivo ---
    fig = go.Figure()
    lat_principal, lon_principal = country_coords[pais_principal_code]
    max_collab = max([c[1] for c in top_collaborators]) if top_collaborators else 1

    # --- Dibujar líneas de colaboración ---
    for country_code, count in top_collaborators:
        if country_code in country_coords and country_code != pais_principal_code:
            lat_colab, lon_colab = country_coords[country_code]
            line_width = max(1, (count / max_collab) * 2)

            fig.add_trace(go.Scattergeo(
                lon=[lon_principal, lon_colab],
                lat=[lat_principal, lat_colab],
                mode='lines',
                line=dict(width=line_width, color='rgba(8, 81, 156, 0.6)'),  # azul consistente
                hoverinfo='text',
                text=f"{country_names.get(pais_principal_code, pais_principal_code)} → {country_names.get(country_code, country_code)}: {count} colaboraciones",
                showlegend=False
            ))

    # --- Nodo central (estrella azul oscuro) ---
    fig.add_trace(go.Scattergeo(
        lon=[lon_principal],
        lat=[lat_principal],
        mode='markers+text',
        marker=dict(
            size=18,
            color='darkblue',
            line=dict(width=2, color='white'),
            symbol='star'
        ),
        text=[pais_principal_code],
        textposition="top center",
        textfont=dict(size=14, color="black", family="Arial Black"),
        hoverinfo='text',
        hovertext=f"{country_names.get(pais_principal_code, pais_principal_code)} (Autor Principal)",
        showlegend=False
    ))

    # --- Países colaboradores (círculos celestes) ---
    for country_code, count in top_collaborators:
        if country_code in country_coords and country_code != pais_principal_code:
            lat_colab, lon_colab = country_coords[country_code]
            fig.add_trace(go.Scattergeo(
                lon=[lon_colab],
                lat=[lat_colab],
                mode='markers+text',
                marker=dict(
                    size=10 + (count / max_collab) * 5,
                    color='skyblue',
                    line=dict(width=1, color='gray'),
                    symbol='circle'
                ),
                text=[country_code],
                textposition="top center",
                textfont=dict(size=13, color="black"),
                hoverinfo='text',
                hovertext=f"{country_names.get(country_code, country_code)}: {count} colaboraciones",
                showlegend=False
            ))

    # --- Configuración visual ---
    fig.update_layout(
        showlegend=False,
        geo=dict(
            showland=True,
            landcolor='rgb(240, 240, 240)',
            countrycolor='rgb(200, 200, 200)',
            showcountries=True,
            projection_type='miller',
            bgcolor='rgba(255,255,255,1)',
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
            lataxis_showgrid=False,
            lonaxis_showgrid=False,
            fitbounds="locations",
        ),
        height=350,
        margin=dict(l=2, r=2, t=2, b=2),
        autosize=True,
        font=dict(size=15),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Exportar PDF ---
    safe_author_name = author_display_name.replace(' ', '_').replace('.', '').lower()
    file_mapa = f"{OUTPUT_DIR}/graficar_mapa_{safe_author_name}.png"
    fig.write_image(file_mapa)

# ============================================================
# 7️⃣ Modelo de Crecimiento de citas
# ============================================================
def graficar_modelos_crecimiento_citas(df_master, author_display_name):
    # --- VALIDACIÓN INICIAL ---
    if df_master is None or df_master.empty:
        st.warning("⚠️ No hay datos disponibles para generar la gráfica.")
        return

    # --- CONFIGURACIÓN GLOBAL DE ESTILO ---
    a = 18  # Tamaño base de fuente
    b = 2.0  # Grosor de líneas principales

    sns.set_theme(style="whitegrid", rc={
        'font.size': a,
        'axes.titlesize': a,
        'axes.labelsize': a,
        'xtick.labelsize': a,
        'ytick.labelsize': a,
        'legend.fontsize': a - 2,
        'legend.title_fontsize': a - 1
    })

    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': a,
        'axes.titlesize': a,
        'axes.labelsize': a,
        'xtick.labelsize': a - 1,
        'ytick.labelsize': a - 1,
        'legend.fontsize': a - 2,
        'legend.title_fontsize': a - 1
    })

    # ============================================================
    # 1️⃣ PREPARACIÓN DE DATOS
    # ============================================================

    def safe_split(x):
        if isinstance(x, str) and "|" in x:
            return x.split("|")
        elif isinstance(x, str):
            return [x]
        elif isinstance(x, list):
            return x
        else:
            return []

    def to_int_list(lst):
        out = []
        for val in lst:
            try:
                out.append(int(val))
            except:
                out.append(0)
        return out

    # --- PREPARAR COLUMNAS ---
    df_master["year_list"] = df_master["counts_by_year.year"].apply(safe_split).apply(to_int_list)
    df_master["cited_list"] = df_master["counts_by_year.cited_by_count"].apply(safe_split).apply(to_int_list)

    # --- DESANIDAR DATOS ---
    expanded_rows = []
    for _, row in df_master.iterrows():
        years = row["year_list"]
        cites = row["cited_list"]
        if len(years) == len(cites) and len(years) > 0:
            for y, c in zip(years, cites):
                expanded_rows.append({"year": y, "cited_by_count": c})

    if not expanded_rows:
        st.warning("⚠️ No se pudieron expandir los datos. Revisa las columnas 'counts_by_year.*'.")
        return

    citations_df = pd.DataFrame(expanded_rows)
    citations_summary = (
        citations_df.groupby("year", as_index=False)
        .agg({"cited_by_count": "sum"})
        .sort_values("year", ascending=True)
    )

    # ============================================================
    # 2️⃣ AJUSTE DE MODELOS SOBRE EL ACUMULADO DE CITAS
    # ============================================================

    first_year = citations_summary["year"].min()
    citations_summary["t"] = citations_summary["year"] - first_year
    cumulative_citations = citations_summary["cited_by_count"].cumsum()

    t_data = citations_summary["t"].values
    L_data = cumulative_citations.values

    # --- Modelos matemáticos ---
    def power_law_model(t, A, m): return A * (t ** m)
    def logistic_model(t, K, a, t0): return K / (1 + np.exp(-a * (t - t0)))
    def gompertz_model(t, K, b, c): return K * np.exp(-b * np.exp(-c * t))

    results = {}

    # Parámetros iniciales
    p0_logistic = [max(L_data), 1, np.median(t_data)]
    p0_gompertz = [max(L_data), 1, 0.5]

    try:
        params_power, _ = curve_fit(power_law_model, t_data, L_data)
        y_pred = power_law_model(t_data, *params_power)
        results['Ley de Potencia'] = {'R2': r2_score(L_data, y_pred), 'params': params_power, 'pred': y_pred}
    except RuntimeError:
        pass

    try:
        params_log, _ = curve_fit(logistic_model, t_data, L_data, p0=p0_logistic, maxfev=5000)
        y_pred = logistic_model(t_data, *params_log)
        results['Logístico'] = {'R2': r2_score(L_data, y_pred), 'params': params_log, 'pred': y_pred}
    except RuntimeError:
        pass

    try:
        params_gomp, _ = curve_fit(gompertz_model, t_data, L_data, p0=p0_gompertz, maxfev=5000)
        y_pred = gompertz_model(t_data, *params_gomp)
        results['Gompertz'] = {'R2': r2_score(L_data, y_pred), 'params': params_gomp, 'pred': y_pred}
    except RuntimeError:
        pass

    if not results:
        st.error("❌ No se pudieron ajustar los modelos.")
        return

    # ============================================================
    # 3️⃣ GRÁFICO FINAL (STREAMLIT)
    # ============================================================

    t_smooth = np.linspace(min(t_data), max(t_data), 300)
    year_smooth = t_smooth + first_year

    colors = {
        'Ley de Potencia': '#08306b',
        'Logístico': '#2171b5',
        'Gompertz': '#6baed6'
    }

    linestyles = {
        'Ley de Potencia': '--',
        'Logístico': ':',
        'Gompertz': '-.'
    }

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10),
                                   sharex=True,
                                   gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05})

    # --- PANEL SUPERIOR ---
    ax1.scatter(citations_summary["year"], L_data,
                label="Observaciones reales",
                color="black", zorder=5, s=50, alpha=0.8)

    for model, res in results.items():
        if model == 'Ley de Potencia':
            y_smooth = power_law_model(t_smooth, *res["params"])
        elif model == 'Logístico':
            y_smooth = logistic_model(t_smooth, *res["params"])
        else:
            y_smooth = gompertz_model(t_smooth, *res["params"])

        ax1.plot(year_smooth, y_smooth,
                 linestyles[model],
                 linewidth=b,
                 color=colors[model],
                 label=f"{model} (R²={res['R2']:.3f})")

    ax1.set_ylabel("Citas acumuladas", fontsize=a)
    ax1.legend(loc="best", frameon=False)
    ax1.grid(False)

    # --- PANEL INFERIOR (Error relativo) ---
    for model, res in results.items():
        rel_err = (res["pred"] / L_data) - 1
        ax2.plot(citations_summary["year"], rel_err,
                 linestyle=linestyles[model],
                 color=colors[model],
                 linewidth=b)

    ax2.axhline(0.0, color="black", linewidth=0.8)
    ax2.set_yticks(np.arange(-0.2, 0.21, 0.1))
    ax2.set_ylim(-0.2, 0.2)
    ax2.set_ylabel(r"$\frac{y_{modelo}}{y_{real}} - 1$", fontsize=a - 2)
    ax2.set_xlabel("Año", fontsize=a)
    ax2.grid(False)

    plt.tight_layout()

    # --- MOSTRAR EN STREAMLIT ---
    st.pyplot(fig)

    # --- DESCARGA PDF ---
    safe_author_name = author_display_name.replace(' ', '_').replace('.', '').lower()
    file_modelo = f"{OUTPUT_DIR}/graficar_modelo_{safe_author_name}.png"
    fig.savefig(file_modelo, dpi=300, bbox_inches="tight")

# ============================================================
# ☁️ NUBE DE PALABRAS DE TÍTULOS
# ============================================================
def graficar_nube_titulos(df_master, author_display_name):
    """
    Genera y muestra una nube de palabras basada en los títulos de las publicaciones 
    del autor analizado. Si no hay suficientes datos, muestra una advertencia.
    """
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    if df_master is None or df_master.empty:
        st.warning("⚠️ El DataFrame maestro está vacío.")
        return

    if "title" not in df_master.columns:
        st.warning("⚠️ No se encontró la columna 'title' en el DataFrame.")
        return

    # Filtrar títulos válidos
    titles = df_master["title"].dropna().astype(str)
    all_text = " ".join(titles)

    if not all_text.strip():
        st.warning("⚠️ No se encontraron títulos para generar la nube de palabras.")
        return
    else:
        st.success(f"✅ Se generó la nube de palabras con {len(all_text.split())} palabras totales.")

    # Crear nube
    wordcloud = WordCloud(
        width=1000, 
        height=500, 
        background_color="white",
        max_words=200, 
        collocations=False,
        colormap="Blues"
    ).generate(all_text)

    # Mostrar con Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Guardar figura
    safe_author_name = author_display_name.replace(' ', '_').replace('.', '').lower()
    file_nube_titulos= f"{OUTPUT_DIR}/graficar_nube_titulos_{safe_author_name}.png"
    fig.savefig(file_nube_titulos, dpi=300, bbox_inches='tight')

# ============================================================
# ☁️ NUBE DE PALABRAS DE ABSTRACTS
# ============================================================
def graficar_nube_abstracts(df_master, author_display_name):
    """
    Genera y muestra una nube de palabras basada en los abstracts de las publicaciones 
    del autor analizado. Si no hay suficientes datos, muestra una advertencia.
    """
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    if df_master is None or df_master.empty:
        st.warning("⚠️ El DataFrame maestro está vacío.")
        return

    if "abstract" not in df_master.columns:
        st.warning("⚠️ No se encontró la columna 'abstract' en el DataFrame.")
        return

    # Filtrar abstracts válidos
    abstracts = df_master["abstract"].dropna().astype(str)
    all_text = " ".join(abstracts)

    if not all_text.strip():
        st.warning("⚠️ No se encontraron abstracts para generar la nube de palabras.")
        return
    else:
        st.success(f"✅ Se generó la nube de palabras con {len(all_text.split())} palabras totales.")

    # Crear nube
    wordcloud = WordCloud(
        width=1000, 
        height=500, 
        background_color="white",
        max_words=200, 
        collocations=False,
        colormap="Blues"
    ).generate(all_text)

    # Mostrar con Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Guardar imagen
    safe_author_name = author_display_name.replace(' ', '_').replace('.', '').lower()
    file_nube_abstract= f"{OUTPUT_DIR}/graficar_nube_abstract_{safe_author_name}.png"
    fig.savefig(file_nube_abstract, dpi=300, bbox_inches='tight')
    
