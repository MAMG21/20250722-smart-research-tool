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


# ============================================================
# 1️⃣ Publicaciones por año
# ============================================================
def graficar_publicaciones_por_anio(df_master):
    """
    Grafica la cantidad de publicaciones por año (dinámica con Plotly).
    Acepta tanto 'Año' como 'publication_year' como nombre de columna.
    """

    if df_master is None or df_master.empty:
        st.warning("⚠️ No hay datos para graficar publicaciones por año.")
        return

    # Detectar nombre de columna correcto
    if "Año" in df_master.columns:
        year_col = "Año"
    elif "publication_year" in df_master.columns:
        year_col = "publication_year"
    else:
        st.warning("⚠️ No se encontró ninguna columna de año ('Año' o 'publication_year').")
        return

    # Eliminar filas sin año
    df_valid = df_master[df_master[year_col].notna()].copy()

    if df_valid.empty:
        st.warning("⚠️ No hay valores válidos de año para graficar.")
        return

    # Contar publicaciones por año
    df_counts = (
        df_valid.groupby(year_col)
        .size()
        .reset_index(name="Publicaciones")
        .sort_values(year_col)
    )

    # Crear gráfica interactiva
    fig = px.bar(
        df_counts,
        x=year_col,
        y="Publicaciones",
        text="Publicaciones",
        template="plotly_white"
    )

    # Ajustes visuales
    fig.update_traces(textposition="outside", marker_color="rgb(0, 102, 204)")
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Número de publicaciones",
        margin=dict(l=20, r=20, t=20, b=20),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)



# ============================================================
# 2️⃣ Citas por año
# ============================================================
def graficar_citas_por_anio(df_master, author_display_name):
    """
    Grafica la cantidad de citas por año (dinámica con Plotly).
    """

    if df_master is None or df_master.empty:
        st.warning("⚠️ El DataFrame maestro está vacío.")
        return

    df = df_master.copy()
    if "year" not in df.columns:
        if "publication_year" in df.columns:
            df["year"] = df["publication_year"]
        else:
            st.warning("⚠️ No se encontró columna de año ('year').")
            return

    if "citations" not in df.columns:
        if "cited_by_count" in df.columns:
            df["citations"] = df["cited_by_count"]
        else:
            df["citations"] = 0

    df_cit = df.groupby("year", as_index=False)["citations"].sum().sort_values("year")

    fig = px.bar(df_cit, x='year', y='citations', template='plotly_white')
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=400)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 3️⃣ Posición de autoría (solo barras)
# ============================================================
def red_colaboraciones(df_master, author_display_name):
    """
    Grafica la cantidad de colaboraciones que ha tenido un autor de acuerdo
    a la posicion de su firma en la autoria.
    """
    if df_master is None or df_master.empty:
        st.warning("⚠️ No hay datos para generar la gráfica de colaboraciones.")
        return

    if "authors" not in df_master.columns:
        st.warning("⚠️ No se encontró la columna 'authors'.")
        return

    pos_counts = Counter({'1er Autor': 0, '2do Autor': 0, '3er Autor': 0, '4to o más': 0})
    for authors_str in df_master['authors'].dropna():
        authors_list = [a.strip() for a in str(authors_str).split(';')]
        try:
            pos = authors_list.index(author_display_name) + 1
            if pos == 1:
                pos_counts['1er Autor'] += 1
            elif pos == 2:
                pos_counts['2do Autor'] += 1
            elif pos == 3:
                pos_counts['3er Autor'] += 1
            else:
                pos_counts['4to o más'] += 1
        except ValueError:
            continue

    df_pos = pd.DataFrame({
        "Posición": list(pos_counts.keys()),
        "Frecuencia": list(pos_counts.values())
    })

    fig = px.bar(df_pos, x="Posición", y="Frecuencia", text="Frecuencia", color="Posición",
                 color_discrete_sequence=px.colors.sequential.Magma)
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, template="plotly_white", height=400)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 4️⃣ Red de coautoría (mantiene nodos)
# ============================================================
def red_coautoria(df_master, author_display_name):
    """
    Grafica los 10 coautores con los que ha trabajado el autor que se 
    está analizando.
    """
    if df_master is None or df_master.empty:
        st.warning("⚠️ No hay datos para generar la red de coautoría.")
        return
    if 'authors' not in df_master.columns:
        st.warning("⚠️ No existe la columna 'authors'.")
        return

    autor_principal = author_display_name
    coauthor_counter = Counter()

    # Contar coautores
    for author_list_str in df_master['authors'].dropna():
        authors_in_paper = [a.strip() for a in author_list_str.split(';')]
        if autor_principal in authors_in_paper:
            authors_in_paper = [a for a in authors_in_paper if a != autor_principal]
            coauthor_counter.update(authors_in_paper)

    # ✅ Solo los 10 coautores más frecuentes
    top_coauthors = coauthor_counter.most_common(10)
    if not top_coauthors:
        st.warning("⚠️ No se encontraron coautores.")
        return

    G = nx.Graph()
    G.add_node(autor_principal)
    for co, w in top_coauthors:
        G.add_node(co)
        G.add_edge(autor_principal, co, weight=w)

    pos = nx.spring_layout(G, seed=42)

    # Aristas
    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='rgba(150,150,150,0.6)'),
        mode='lines',
        hoverinfo='none'
    )

    # Nodos
    node_x, node_y, text, size, color = [], [], [], [], []
    for n in G.nodes():
        x, y = pos[n]
        node_x.append(x)
        node_y.append(y)
        if n == autor_principal:
            size.append(40)
            color.append('blue')
        else:
            size.append(15 + coauthor_counter.get(n, 0) * 2)
            color.append('salmon')
        text.append(f"{n} ({coauthor_counter.get(n, 0)})")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[n for n in G.nodes()],
        hovertext=text,
        hoverinfo='text',
        textposition="bottom center",
        marker=dict(size=size, color=color, line=dict(width=1, color='white'))
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        template="plotly_white",
        height=450,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)



# ============================================================
# 5️⃣ Red de colaboración entre instituciones (mantiene nodos)
# ============================================================
def red_colaboracion_instituciones(df_master, author_display_name):
    """
    Grafica las 10 instituciones con las que ha trabajado el autor que se 
    está analizando, mostrando una red basada en las coocurrencias
    institucionales dentro de sus publicaciones.
    """

    if df_master is None or df_master.empty:
        st.warning("⚠️ No hay datos para generar la red de instituciones.")
        return

    posibles_cols = ["institutions_list", "institutions", "institution", "affiliations", "author_institutions"]
    col_institutions = next((col for col in posibles_cols if col in df_master.columns), None)
    if not col_institutions:
        st.error("❌ No se encontró ninguna columna de instituciones.")
        return

    # Construir red completa
    G = nx.Graph()
    for _, row in df_master.iterrows():
        if pd.isna(row.get(col_institutions)):
            continue
        instituciones = [inst.strip() for inst in str(row[col_institutions]).split(";") if inst.strip()]
        for i in range(len(instituciones)):
            for j in range(i + 1, len(instituciones)):
                a, b = instituciones[i], instituciones[j]
                if G.has_edge(a, b):
                    G[a][b]['weight'] += 1
                else:
                    G.add_edge(a, b, weight=1)

    if G.number_of_nodes() == 0:
        st.warning("⚠️ No se encontraron instituciones para graficar.")
        return

    # ✅ Filtrar el top 10 instituciones con más conexiones (grado)
    top_institutions = sorted(G.degree, key=lambda x: x[1], reverse=True)[:10]
    top_nodes = [n for n, _ in top_institutions]
    G_sub = G.subgraph(top_nodes).copy()

    pos = nx.spring_layout(G_sub, seed=42)

    # --- Aristas ---
    edge_x, edge_y = [], []
    for u, v in G_sub.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='rgba(150,150,150,0.6)'),
        mode='lines',
        hoverinfo='none'
    )

    # --- Nodos ---
    node_x, node_y, size, color, text = [], [], [], [], []
    for n in G_sub.nodes():
        x, y = pos[n]
        node_x.append(x)
        node_y.append(y)
        degree = G_sub.degree[n]
        size.append(10 + degree * 3)
        color.append('salmon')
        text.append(f"{n} ({degree})")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[n for n in G_sub.nodes()],
        hovertext=text,
        hoverinfo='text',
        textposition="bottom center",
        marker=dict(size=size, color=color, line=dict(width=1, color='white'))
    )

    # --- Figura final ---
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        template="plotly_white",
        height=450,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 6️⃣ Mapa de colaboraciones internacionales
# ============================================================
def graficar_mapa_colaboraciones_internacionales(df_master, author_display_name):
    """
    Muestra un mapa mundial con las colaboraciones internacionales
    del autor especificado. Usa coordenadas fijas (sin geopy).
    """

    # Coordenadas fijas por país (ISO-2)
    COORDS_BACKUP = {
        "US": (37.0902, -95.7129),
        "CA": (56.1304, -106.3468),
        "DE": (51.1657, 10.4515),
        "CH": (46.8182, 8.2275),
        "IL": (31.0461, 34.8516),
        "FR": (46.6034, 1.8883),
        "GB": (55.3781, -3.4360),
        "AR": (-38.4161, -63.6167),
        "CL": (-35.6751, -71.5430),
        "CO": (4.5709, -74.2973),
        "BR": (-14.2350, -51.9253),
        "ES": (40.4637, -3.7492),
        "IT": (41.8719, 12.5674),
        "JP": (36.2048, 138.2529),
    }

    # Validaciones iniciales
    if df_master is None or df_master.empty:
        st.warning("⚠️ El DataFrame maestro está vacío.")
        return
    if "countries" not in df_master.columns:
        st.warning("⚠️ No existe la columna 'countries' en el DataFrame.")
        return

    df_autor = df_master[df_master["countries"].notna()].copy()
    all_countries = (
        df_autor["countries"]
        .dropna()
        .str.split(";")
        .explode()
        .str.strip()
        .tolist()
    )

    if not all_countries:
        st.warning("⚠️ No se encontraron países asociados al autor.")
        return

    # Determinar país principal y colaboradores
    pais_principal = Counter(all_countries).most_common(1)[0][0]
    collaboration_counter = Counter()

    for countries_str in df_autor["countries"].dropna():
        countries = {c.strip() for c in countries_str.split(";")}
        countries.discard(pais_principal)
        collaboration_counter.update(countries)

    top_collaborators = collaboration_counter.most_common(10)
    if not top_collaborators:
        st.warning("⚠️ No se encontraron países colaboradores.")
        return

    # Resolver coordenadas solo desde el diccionario
    country_coords = {
        code: COORDS_BACKUP[code]
        for code in [pais_principal] + [c[0] for c in top_collaborators]
        if code in COORDS_BACKUP
    }

    if pais_principal not in country_coords:
        st.warning(f"⚠️ No se pudo determinar la ubicación del país principal: {pais_principal}")
        return

    lat0, lon0 = country_coords[pais_principal]
    fig = go.Figure()

    # Dibujar líneas entre el país principal y colaboradores
    for country_code, count in top_collaborators:
        if country_code in country_coords:
            latc, lonc = country_coords[country_code]
            fig.add_trace(go.Scattergeo(
                lon=[lon0, lonc],
                lat=[lat0, latc],
                mode="lines",
                line=dict(width=1.5, color="crimson"),
                hoverinfo="text",
                text=f"{pais_principal} → {country_code}: {count} colaboraciones"
            ))

    # Dibujar puntos
    lats = [coords[0] for coords in country_coords.values()]
    lons = [coords[1] for coords in country_coords.values()]
    codes = list(country_coords.keys())
    sizes = [18 if c == pais_principal else 10 for c in codes]
    colors = ["blue" if c == pais_principal else "rgb(0,51,102)" for c in codes]

    fig.add_trace(go.Scattergeo(
        lon=lons, lat=lats, mode="markers",
        marker=dict(size=sizes, color=colors, line=dict(width=1, color="white")),
        hoverinfo="text", text=codes
    ))

    # Configuración final del mapa
    fig.update_layout(
        showlegend=False,
        geo=dict(
            showland=True,
            landcolor="rgb(243,243,243)",
            countrycolor="rgb(204,204,204)",
            projection_type="natural earth"
        ),
        margin=dict(r=0, t=0, l=0, b=0),
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 📈 Modelos de Crecimiento de Citas (Power Law, Logistic, Gompertz)
# ============================================================
def graficar_modelos_crecimiento_citas(df_master, author_display_name):
    """
    Grafica los modelos de crecimiento de citas (Power Law, Logístico y Gompertz)
    para el autor que se está analizando. 

    La función calcula las citas acumuladas por año y ajusta distintos modelos
    de crecimiento para evaluar cuál describe mejor la evolución de las citas 
    del autor a lo largo del tiempo. 

    El gráfico muestra los datos reales junto con las curvas ajustadas y 
    sus respectivos valores de R², con la leyenda posicionada en la parte inferior.
    """

    if df_master is None or df_master.empty:
        st.warning("⚠️ No hay datos disponibles para generar la gráfica de crecimiento de citas.")
        return

    # Normalizar nombres de columnas
    if "year" not in df_master.columns:
        if "publication_year" in df_master.columns:
            df_master["year"] = df_master["publication_year"]
        else:
            st.warning("⚠️ No se encontró ninguna columna de año ('year' o 'publication_year').")
            return

    if "cited_by_count" not in df_master.columns:
        st.warning("⚠️ No se encontró la columna 'cited_by_count'.")
        return

    # --- 1️⃣ Preparar datos ---
    citations_df = (
        df_master.groupby("year", as_index=False)["cited_by_count"].sum().sort_values("year")
    )
    citations_df["t"] = citations_df["year"] - citations_df["year"].min()
    citations_df["cumulative_citations"] = citations_df["cited_by_count"].cumsum()

    t_data = citations_df["t"].values
    L_data = citations_df["cumulative_citations"].values

    # --- 2️⃣ Modelos ---
    def power_law_model(t, A, m): return A * (t**m)
    def logistic_model(t, K, a, t0): return K / (1 + np.exp(-a * (t - t0)))
    def gompertz_model(t, K, b, c): return K * np.exp(-b * np.exp(-c * t))

    # --- 3️⃣ Ajuste ---
    results = {}
    p0_logistic = [max(L_data), 1, np.median(t_data)]
    p0_gompertz = [max(L_data), 1, 0.5]

    try:
        params_power, _ = curve_fit(power_law_model, t_data, L_data)
        y_pred_power = power_law_model(t_data, *params_power)
        results["Power Law"] = {"params": params_power, "R2": r2_score(L_data, y_pred_power)}
    except:
        pass

    try:
        params_logistic, _ = curve_fit(logistic_model, t_data, L_data, p0=p0_logistic, maxfev=5000)
        y_pred_logistic = logistic_model(t_data, *params_logistic)
        results["Logistic"] = {"params": params_logistic, "R2": r2_score(L_data, y_pred_logistic)}
    except:
        pass

    try:
        params_gompertz, _ = curve_fit(gompertz_model, t_data, L_data, p0=p0_gompertz, maxfev=5000)
        y_pred_gompertz = gompertz_model(t_data, *params_gompertz)
        results["Gompertz"] = {"params": params_gompertz, "R2": r2_score(L_data, y_pred_gompertz)}
    except:
        pass

    if not results:
        st.warning("⚠️ No se pudieron ajustar los modelos de crecimiento.")
        return

    # --- 4️⃣ Gráfica Plotly ---
    t_smooth = np.linspace(min(t_data), max(t_data), 200)
    year_smooth = t_smooth + citations_df["year"].min()

    fig = go.Figure()

    # Datos reales
    fig.add_trace(go.Scatter(
        x=citations_df["year"],
        y=L_data,
        mode="markers+lines",
        name="Datos reales (acumulados)",
        line=dict(color="black", width=2)
    ))

    # Modelos ajustados
    colors = {"Power Law": "blue", "Logistic": "green", "Gompertz": "red"}

    for model_name, info in results.items():
        params = info["params"]
        r2 = info["R2"]

        if model_name == "Power Law":
            y_fit = power_law_model(t_smooth, *params)
        elif model_name == "Logistic":
            y_fit = logistic_model(t_smooth, *params)
        else:
            y_fit = gompertz_model(t_smooth, *params)

        fig.add_trace(go.Scatter(
            x=year_smooth,
            y=y_fit,
            mode="lines",
            name=f"{model_name} (R²={r2:.3f})",
            line=dict(color=colors[model_name], dash="dash")
        ))

    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Citas acumuladas",
        template="plotly_white",
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",   # horizontal
            yanchor="top",
            y=-0.25,           # mueve la leyenda debajo de la gráfica
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        margin=dict(l=20, r=20, t=20, b=60)
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ☁️ NUBE DE PALABRAS DE TÍTULOS
# ============================================================
def graficar_nube_titulos(df_master):
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
        collocations=False
    ).generate(all_text)

    # Mostrar con Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)



# ============================================================
# ☁️ NUBE DE PALABRAS DE ABSTRACTS
# ============================================================
def graficar_nube_abstracts(df_master):
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
        collocations=False
    ).generate(all_text)

    # Mostrar con Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
