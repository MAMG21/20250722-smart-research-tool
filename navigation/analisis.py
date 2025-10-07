# Copyright (c) 2023 Minniti Julien

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of TFinder and associated documentation files, to deal
# in TFinder without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of TFinder, and to permit persons to whom TFinder is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of TFinder.

# TFINDER IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH TFINDER OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import streamlit as st
import matplotlib.pyplot as plt
import hydralit_components as hc

# Analiticias
import core.graficas_autor as graficas

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

    # Crear tarjetas en filas
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
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
                <h4 style="font-size:20px; color:#333333; font-weight:600;">H Relativo</h4>
                <p style=font-size:22px; font-weight:bold; margin: 0;">{format_metric(df_metricas['H Relativo'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown(
        "<h3 style='text-left: center; color: black;'>Perfil del investigador</h1>",
        unsafe_allow_html=True)
    
    # Colaboracion cientifica

    st.markdown(
        "<div style='text-align: left; color: gray; font-size: 20px;'>Colaboración Científica</div>",
        unsafe_allow_html=True
    )

    # Crear columnas
    col1, col2, col3 = st.columns(3)

    # Gráfica 1
    with col1:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Frecuencia de Firmas por Posición de Autoría</div>", unsafe_allow_html=True)
        fig1, ax1 = plt.subplots()
        ax1.plot([1, 2, 3], [4, 5, 6])
        st.pyplot(fig1)

    # Gráfica 2
    with col2:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Colaboraciones Globales</div>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots()
        ax2.bar([1, 2, 3], [3, 1, 2])
        st.pyplot(fig2)

    # Gráfica 3
    with col3:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Mapa de Colaboraciones</div>", unsafe_allow_html=True)
        fig3, ax3 = plt.subplots()
        ax3.scatter([1, 2, 3], [6, 4, 5])
        st.pyplot(fig3)

    # Analisis de Publicaciones

    st.markdown(
        "<div style='text-align: left; color: gray; font-size: 20px;'>Análisis de Publicaciones</div>",
        unsafe_allow_html=True
    )

    # Crear columnas
    col1, col2, col3 = st.columns(3)

    # Gráfica 1
    with col1:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Frecuencia de Publicación</div>", unsafe_allow_html=True)
        fig1, ax1 = plt.subplots()
        ax1.plot([1, 2, 3], [4, 5, 6])
        st.pyplot(fig1)

    # Gráfica 2
    with col2:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Crecimiento Acumulado de Articulos</div>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots()
        ax2.bar([1, 2, 3], [3, 1, 2])
        st.pyplot(fig2)

    # Gráfica 3
    with col3:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Crecimiento Acumulado de Citas</div>", unsafe_allow_html=True)
        fig3, ax3 = plt.subplots()
        ax3.scatter([1, 2, 3], [6, 4, 5])
        st.pyplot(fig3)

    # Analisis Avanzado

    st.markdown(
        "<div style='text-align: left; color: gray; font-size: 20px;'>Análisis</div>",
        unsafe_allow_html=True
    )

    # Crear columnas
    col1, col2 = st.columns(2)

    # Gráfica 1
    with col1:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Análisis de Interferencias</div>", unsafe_allow_html=True)
        fig1, ax1 = plt.subplots()
        ax1.plot([1, 2, 3], [4, 5, 6])
        st.pyplot(fig1)

    # Gráfica 2
    with col2:
        st.markdown("<div style='text-align: center; color: black; font-size: 15px;'>Análisis ML Supervisado y No Supervisado</div>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots()
        ax2.bar([1, 2, 3], [3, 1, 2])
        st.pyplot(fig2)

    st.info("📄 Para exportar esta visualización, presiona `Ctrl + P` / `Cmd + P` y elige 'Guardar como PDF'.")



        