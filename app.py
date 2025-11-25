# Librerias principales
import hydralit_components as hc
import platform
import pandas as pd
import requests
import streamlit as st

# import streamlit_analytics
from streamlit_modal import Modal
import streamlit_lottie
import time
import json

# Funciones dentro de carpetas
# Visuales
from navigation.introduction import home_page
from navigation.analisis import allapp_page
from navigation.referencias import resource_page
from navigation.contacto import contact_page
from utils.components import footer_style, footer

# Analiticias
from core.consulta_autores import get_author_id
from core.consulta_autores import get_concept_id, get_top_authors_by_concept
from core.consulta_publicaciones import fetch_author_works
from core.metricas import compute_bibliometric_indices

try:
    from streamlit import rerun as rerun
except ImportError:
    # conditional import for streamlit version <1.27
    from streamlit import experimental_rerun as rerun

import os


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


st.set_page_config(
    page_title='Analisis Bibliometrico',
    page_icon="img/analisis.png",
    initial_sidebar_state="expanded",
    layout="wide"
)

if 'lottie' not in st.session_state:
    st.session_state.lottie = False


max_width_str = f"max-width: {75}%;"

st.markdown(f"""
        <style>
        .appview-container .main .block-container{{{max_width_str}}}
        </style>
        """,
            unsafe_allow_html=True,
            )

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;

                }
        </style>
        """, unsafe_allow_html=True)

# Footer

st.markdown(footer_style, unsafe_allow_html=True)

# NavBar

HOME = 'Introducción'
APPLICATION = 'Análisis'
RESOURCE = 'Referencias'
CONTACT = 'Contacto'

tabs = [
    HOME,
    APPLICATION,
    RESOURCE,
    CONTACT,
]

option_data = [
    {'icon': "🗂", 'label': HOME},
    {'icon': "✍", 'label': APPLICATION},
    {'icon': "📑", 'label': RESOURCE},
    {'icon': "✉️", 'label': CONTACT},
]

over_theme = {'txc_inactive': 'black', 'menu_background': '#D6E5FA', 'txc_active': 'white', 'option_active': '#749BC2'}
font_fmt = {'font-class': 'h3', 'font-size': '50%'}

chosen_tab = hc.option_bar(
    option_definition=option_data,
    title='',
    key='PrimaryOptionx',
    override_theme=over_theme,
    horizontal_orientation=True)

st.success("Bienvenido a la herramienta de análisis del impacto científico de investigadores. Aquí podrás explorar métricas bibliométricas y altmétricas integradas, visualizar resultados de forma interactiva y conocer el nivel de relevancia de los investigadores.")

if chosen_tab == HOME:
    home_page()

elif chosen_tab == APPLICATION:
    allapp_page()

elif chosen_tab == RESOURCE:
    resource_page()

elif chosen_tab == CONTACT:
    contact_page()

for i in range(4):
    st.markdown('#')
st.markdown(footer, unsafe_allow_html=True)

# Credit
st.logo("img/analisis.png")

# Help
def mostrar_sidebar():
    st.sidebar.image("img/cientifico.png")
    st.sidebar.title("Análisis Bibliométrico")
    author_name = st.sidebar.text_input("Nombre del autor", value="Viatcheslav Mukhanov")

    if st.sidebar.button("Analizar Autor"):
        with st.sidebar:
            try:
                with st.spinner("Descargando publicaciones..."):
                    author_id, display_name = get_author_id(author_name, "")
                    df = fetch_author_works(author_id, "")

                    if df.empty:
                        st.sidebar.warning("⚠️ No se encontraron publicaciones para este autor.")
                        st.session_state.clear()  # O elimina las claves necesarias
                    else:
                        indices = compute_bibliometric_indices(df)
                        indices["Autor"] = display_name
                        st.session_state.df_metricas = indices
                        st.session_state.df_trabajos = df

                        total_publicaciones_fmt = "{:,.0f}".format(indices["Total Artículos"]).replace(",", ".")
                        total_citas_fmt = "{:,.0f}".format(indices["Total Citas"]).replace(",", ".")

                        st.session_state.total_public = total_publicaciones_fmt

                        st.markdown('')

                        st.sidebar.markdown(f"""
                        <div style="background-color: #d4edda; padding: 10px; border-radius: 5px;">
                        <b>✅</b>
                        <b>Autor encontrado:</b> {display_name}<br>
                        <b>Total Publicaciones:</b> {total_publicaciones_fmt}<br>
                        <b>Total Citas:</b> {total_citas_fmt}
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown('')

                        csv = df.to_csv(index=False).encode('utf-8')
                        st.sidebar.download_button("Descargar publicaciones", csv, file_name=f"{author_id}_publicaciones.csv", mime="text/csv")

            except Exception as e:
                st.error(f"❌ Error: {e}")

    # Guardar el author_name para que esté disponible
    st.session_state.author_name = author_name

    return author_name  # opcional
    
mostrar_sidebar()
