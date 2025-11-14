
import streamlit as st
import matplotlib.pyplot as plt
import hydralit_components as hc
import glob
import pandas as pd
import os

# Analiticias
import core.graficas_autor as graficas
# Renderizar pdf 
from core.export_pdf import exportar_pdf

def allapp_page():
    # Validador de que ya existe una 
    df_metricas = st.session_state.get("df_metricas")
    if df_metricas is not None:
        st.write(f"Mostrando métricas del autor: **{st.session_state.get('author_name', 'Autor desconocido')}**, con un total de **{st.session_state.get('total_public', '0')}** publicaciones.")
    else:
        st.warning("⚠️ Por favor, busca un autor en la página de introducción primero y luego regresa a esta página")


    # Barra lateral funcional donde se importan las metricas principales
    df_metricas = st.session_state.df_metricas
    df_trabajos = st.session_state.df_trabajos
    df_master = st.session_state.df_master

    # Formatear números
    def format_metric(value):
        if isinstance(value, float):
            return f"{value:.2f}"
        return f"{value:,}".replace(",", ".")
    
    # Titulo de la primera sección
    st.divider()
    st.markdown(
        "<h3 style='text-align: left; color: black;'>Métricas de productividad e impácto de investigación</h1>",
        unsafe_allow_html=True)
    
    # Formato tooltip 
    st.markdown("""
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>

    <style>
    /* Quitar icono de enlace de Streamlit */
    h4 a {text-decoration: none !important; pointer-events: none !important; color: inherit !important;}
    h4 svg {display: none !important;}
    .metric-card {
    position: relative;
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    }

    .tooltip-container {
    position: absolute;
    top: 8px;
    right: 8px;
    cursor: pointer;
    }

    .tooltip-icon {
    background-color: #d9d9d9;
    border-radius: 50%;
    width: 18px;
    height: 18px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: #333;
    transition: background 0.2s;
    }
    .tooltip-icon:hover {
    background-color: #bdbdbd;
    }

    .tooltip-text {
    visibility: hidden;
    opacity: 0;
    width: 280px;
    background-color: #333;
    color: #fff;
    text-align: left;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 1000;
    top: 25px;
    right: 0;
    transition: opacity 0.3s;
    font-size: 13px;
    line-height: 1.4;
    }

    .tooltip-text::after {
    content: "";
    position: absolute;
    bottom: 100%;
    right: 10px;
    border-width: 6px;
    border-style: solid;
    border-color: transparent transparent #333 transparent;
    }

    .tooltip-container:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

    # Crear tarjetas en filas
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Número de citas:</b> epresenta el total de referencias recibidas por los trabajos de un autor o por un artículo específico, funcionando como el indicador más directo de su impacto, influencia y visibilidad dentro de la comunidad científica (Garfield, 1979). 
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">Total Citas</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['Total Citas'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Índice H (h-index):</b> Propuesto por Hirsch (2005), mide simultáneamente la productividad y el impacto de un autor. Un investigador tiene un índice <i>h</i> si <i>h</i> de sus publicaciones tienen al menos <i>h</i> citas cada una.
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">H-index</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['H-index'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Índice G (g-index):</b> Propuesto por Egghe (2006), mejora el índice <i>h</i> al dar más peso a los artículos altamente citados.
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">G-index</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['G-index'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Índice E (e-index):</b> Desarrollado por Zhang (2009), complementa al índice <i>h</i> al cuantificar el excedente de citas en el núcleo <i>h</i>.
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">E-index</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['E-index'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Índice M (m-index):</b> introducido por Hirsch (2005), representa la productividad ajustada al tiempo de carrera investigadora
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">M-index</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['M-index'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col6:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Índice B (b-index):</b> Extiende el índice <i>h</i> considerando el volumen total de citas dentro del núcleo <i>h</i>, este índice refleja tanto la productividad como la profundidad del impacto científico del autor.
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">B-index</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['B-index'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    # Siguiente fila de tarjetas
    col7, col8, col9, col10, col11, col12 = st.columns(6)

    with col7:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Índice V (V-index):</b> Combina los índices <i>h</i> y <i>g</i> para generar una medida equilibrada entre productividad e impacto acumulado (Vinkler, 2010), 
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">V-index</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['V-index'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col8:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Índice i10 (i10-index):</b> Métrica propuesta por Google Scholar que indica el número de publicaciones que han recibido al menos 10 citas cada una.
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">i10-index</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['i10-index'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col9:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Índice K (k-index):</b> Métrica propuesta por Kinshuk et al. (2011) que analiza la distribución de citas y busca el punto de decaimiento que separa los artículos altamente influyentes del resto
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">K-index</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['K-index'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col10:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Índice H fraccional (fractional h-index):</b> Es un refinamiento del índice h que otorga crédito parcial a los artículos que contribuyen a alcanzar el siguiente nivel de citación (Pudovkin, 2022).
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">H Fraccional</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['H Fraccional'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col11:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Autorank:</b> Es una métrica propuesto por Radicchi et al. (2009), inspirado en el PageRank de Google, que mide la influencia de un investigador dentro de la red de citaciones ponderando la relevancia de los autores que lo citan.
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">Autorank</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['Autorank'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col12:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div class="tooltip-container">
                    <div class="tooltip-icon">?</div>
                    <div class="tooltip-text">
                        <b>Indice H-Relativo (h-rel):</b> es una métrica derivada del H-index que ajusta el valor según el tiempo desde la primera publicación del investigador, permitiendo comparar trayectorias de distinta duración.
                    </div>
                </div>
                <h4 style="font-size:20px; color:#333333; font-weight:600;">H Relativo</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['H Relativo'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    # *****************************************************************************************
    # GRAFICAS DEL PERFIL DEL INVESTIGADOR    
    # *****************************************************************************************

    st.divider()
    st.markdown(
        "<h3 style='text-left: center; color: black;'>Perfil del investigador</h1>",
        unsafe_allow_html=True)
    
    # Colaboracion cientifica

    st.markdown(
        "<div style='text-align: left; color: gray; font-size: 20px;'>Colaboración Científica</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    # Crear columnas
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    # Posicion de Firma Coautoria
    with col1:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Posición de Su Firma en Coautoría</div>", unsafe_allow_html=True)
        graficas.graficar_posicion_autoria(df_master, st.session_state.get('author_name', 'Autor desconocido'))

    # Mapa de Colaboracion
    with col2:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Mapa de Colaboraciones</div>", unsafe_allow_html=True)
        graficas.graficar_mapa_colaboraciones_internacionales(df_master, st.session_state.get('author_name', 'Autor desconocido'))

    # Redes de Coautoria
    with col3:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Redes de Coautoria</div>", unsafe_allow_html=True)
        graficas.graficar_red_coautoria(df_master, st.session_state.get('author_name', 'Autor desconocido'))

    # Redes de Instituciones
    with col4:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Redes de Instituciones", unsafe_allow_html=True)
        graficas.graficar_red_instituciones(df_master, st.session_state.get('author_name', 'Autor desconocido'))


    # *****************************************************************************************
    # Analisis de Citacion
    # *****************************************************************************************

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: left; color: gray; font-size: 20px;'>Análisis de Publicaciones</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
    # Crear columnas
    col1, col2, col3 = st.columns([1, 1, 1])

    # Gráfica 1
    with col1:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Número de artículos publicados</div>", unsafe_allow_html=True)
        graficas.graficar_publicaciones_por_anio(df_master, st.session_state.get('author_name', 'Autor desconocido'))

    # Gráfica 2
    with col2:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Cantidad de citas recibidas</div>", unsafe_allow_html=True)
        graficas.graficar_citas_por_anio(df_master, st.session_state.get('author_name', 'Autor desconocido'))

    # Gráfica 3
    with col3:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Modelo de Crecimiento Acumulado de Citas</div>", unsafe_allow_html=True)
        graficas.graficar_modelos_crecimiento_citas(df_master, st.session_state.get('author_name', 'Autor desconocido'))

    # *****************************************************************************************
    # Analisis de las Publicaciones
    # *****************************************************************************************

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: left; color: gray; font-size: 20px;'>Análisis de las Publicaciones</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    # Crear columnas
    col1, col2 = st.columns([1, 1])

    # Gráfica 1
    with col1:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Nube de Palabras de acuerdo a los Titulos</div>", unsafe_allow_html=True)
        graficas.graficar_nube_titulos(df_master, st.session_state.get('author_name', 'Autor desconocido'))

    # Gráfica 2
    with col2:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Nube de Palabras de acuerdo a los Abstracts</div>", unsafe_allow_html=True)
        graficas.graficar_nube_abstracts(df_master, st.session_state.get('author_name', 'Autor desconocido'))

    st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

    # ----------------------------
    # Proceso de Exportar reporte 
    # ----------------------------
    st.subheader("📥 Exportar reporte")

    OUTPUT_DIR = "outputs"

    def cargar_figuras_analisis(author_name):
        """
        Busca automáticamente todas las imágenes generadas en OUTPUT_DIR
        usando el nombre del autor como filtro.
        Devuelve la lista en el formato requerido por exportar_pdf().
        """

        safe_author = author_name.replace(" ", "_").replace(".", "").lower()

        # Lista final (titulo, ruta)
        figuras = []

        # Mapear prefijos a títulos bonitos
        TITULOS_MAP = {
            "graficar_citas_por_anio": "Citas por Año",
            "graficar_mapa": "Mapa de Colaboraciones",
            "graficar_modelo": "Modelos de Crecimiento de Citas",
            "graficar_nube_abstract": "Nube de Palabras — Abstracts",
            "graficar_nube_titulos": "Nube de Palabras — Títulos",
            "graficar_publicaciones_por_anio": "Publicaciones por Año",
            "graficar_red_coautoria": "Red de Coautoría",
            "graficar_red_instituciones": "Red de Instituciones",
            "graficar_posicion_autoria": "Posición de Autoría",
        }

        # Recorrer archivos del directorio
        for filename in os.listdir(OUTPUT_DIR):
            if safe_author in filename and filename.endswith(".png"):

                ruta = os.path.join(OUTPUT_DIR, filename)

                # Detectar el tipo por el prefijo
                for prefijo, titulo in TITULOS_MAP.items():
                    if filename.startswith(prefijo):
                        figuras.append((titulo, ruta))
                        break

        return figuras


    author_name = st.session_state.get("author_name", "Autor desconocido")
    total_public = st.session_state.get("total_public", "0")
    df_metricas = st.session_state.df_metricas    # ahora viene como dict
    figuras = cargar_figuras_analisis(author_name)

    # Convertir dict → DataFrame
    df_final = pd.DataFrame([df_metricas])

    exportar_pdf(df_final, author_name, total_public, figuras)

        