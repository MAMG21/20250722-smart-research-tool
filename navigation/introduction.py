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
from PIL import Image
import datetime


def home_page():
    st.divider()
    st.markdown(
        "<h3 style='text-align: center; color: black;'>📊 Evaluación del Impacto Científico de Investigadores</h1>",
        unsafe_allow_html=True)
    st.markdown('')
    st.markdown('**Introducción**')
    st.markdown(
        """
        <div style="text-align: justify;">
            <b>Esta herramienta está diseñada para facilitar el análisis, evaluación y visualización del impacto científico de investigadores en las áreas diferentes áreas del conocimiento.</b> 
            Combina métricas bibliométricas tradicionales (como el índice h) con altmétricas y técnicas de aprendizaje automático, utilizando datos abiertos provenientes de OpenAlex.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('')
    st.markdown(
        """
        <div style="text-align: justify;"> 
            A través de un proceso automatizado de extracción, análisis y clasificación de publicaciones científicas, la aplicación permite obtener una visión más completa, dinámica y actualizada de la productividad y relevancia de un investigador, tanto dentro como fuera del ámbito académico.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('')
    st.markdown(
        """
        <div style="text-align: justify;">
            Esta herramienta está especialmente pensada para apoyar procesos de evaluación científica, diseño de políticas públicas en ciencia y tecnología, y toma de decisiones en entornos académicos y gubernamentales.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()
    st.markdown('')
    st.markdown('**⚠️ Funcionamiento del aplicativo**')
    st.markdown(
    """
    <div style="text-align: justify;">
        Por favor antes de ingresar a la subpágina de <b>Análisis</b>, deberá utilizar la barra lateral para ingresar el <b>nombre del autor</b> que desea analizar. Es importante tener en cuenta que este autor debe pertenecer al campo de la <b>física</b> o la <b>astronomía</b> ya que este estudio está destinado a los autores de este campo.
        <br><br>
        Si el autor es encontrado en la base de datos, la aplicación mostrará un resumen con la siguiente información:
        <br><br>
        <div style="background-color: #d4edda; padding: 10px; border-radius: 5px;">
            <b>✅ Autor encontrado:</b> Jane Doe<br>
            <b>Total Publicaciones:</b> 154<br>
            <b>Total Citas:</b> 3.427
        </div>
        <br>
        En caso contrario, el sistema informará lo siguiente:
        <br><br>
        <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px;">
            ⚠️ No se encontraron publicaciones para este autor.
        </div>
        <br>
        Una vez identificado el autor, podrá navegar entre distintas secciones para consultar <b>métricas bibliométricas</b>, <b>altmétricas</b> y <b>visualizaciones interactivas</b> que le permitirán analizar de forma integral el impacto científico del investigador.
    </div>
    """,
    unsafe_allow_html=True
)

