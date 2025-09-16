# graficas_autor.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# --- Cargar DF Master ---
def cargar_df_master(df):
    df = df.copy()
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df[df['year'].notnull()]
    return df

# --- Mostrar resumen del DF ---
def mostrar_info_dataframe(df):
    st.markdown("### 📌 Información general")
    st.write(f"**Número de publicaciones:** {len(df)}")
    st.write(f"**Años de publicación:** {int(df['year'].min())} - {int(df['year'].max())}")

# --- Gráfica de tipos de publicación ---
def graficar_tipos_publicacion(df, author_name):
    tipo_counts = df['type'].value_counts().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    tipo_counts.plot(kind='barh', ax=ax, color='#4a90e2')
    ax.set_title(f"Tipos de Publicaciones de {author_name}")
    ax.set_xlabel("Cantidad")
    ax.set_ylabel("Tipo")
    st.pyplot(fig)

# --- Gráfica de publicaciones por año ---
def graficar_publicaciones_por_anio(df, author_name):
    df_year = df.groupby('year').size().reset_index(name='conteo')
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df_year['year'], df_year['conteo'], color='#00a878')
    ax.set_title(f"Publicaciones por Año - {author_name}")
    ax.set_xlabel("Año")
    ax.set_ylabel("Número de publicaciones")
    st.pyplot(fig)

# --- Gráfica de citas por año ---
def graficar_citas_por_anio(df, author_name):
    df_year = df.groupby('year')['citations'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df_year['year'], df_year['citations'], marker='o', color='#f25f5c')
    ax.set_title(f"Citas por Año - {author_name}")
    ax.set_xlabel("Año")
    ax.set_ylabel("Citas")
    st.pyplot(fig)

# --- Gráfica de distribución de citas ---
def graficar_distribucion_citas(df, author_name):
    fig, ax = plt.subplots(figsize=(6, 4))
    df['citations'].hist(ax=ax, bins=30, color='#9b5de5')
    ax.set_title(f"Distribución de Citas - {author_name}")
    ax.set_xlabel("Citas")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)

# --- Gráfica de citas por publicación ---
def graficar_top_publicaciones_citadas(df, author_name, top_n=10):
    top_df = df.sort_values(by='citations', ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(top_df['title'], top_df['citations'], color='#ffb703')
    ax.invert_yaxis()
    ax.set_title(f"Top {top_n} Publicaciones más Citadas - {author_name}")
    ax.set_xlabel("Citas")
    ax.set_ylabel("Título")
    st.pyplot(fig)

# --- Gráfica de correlación año-citas ---
def graficar_citas_vs_ano(df, author_name):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df, x='year', y='citations', ax=ax, color='#7209b7')
    ax.set_title(f"Citas vs Año de Publicación - {author_name}")
    ax.set_xlabel("Año")
    ax.set_ylabel("Citas")
    st.pyplot(fig)

# --- Top 15 Campos de Investigación ---
def graficar_top_conceptos(df, author_name):
    conceptos = df['topics'].dropna().str.split('; ').explode()
    top_conceptos = conceptos.value_counts().head(15)
    fig, ax = plt.subplots(figsize=(6, 4))
    top_conceptos.sort_values().plot(kind='barh', ax=ax, color='#118ab2')
    ax.set_title(f"Top 15 Campos de Investigación - {author_name}")
    ax.set_xlabel("Frecuencia")
    ax.set_ylabel("Campo")
    st.pyplot(fig)

# --- Frecuencia de Autorías por Posición ---
def graficar_firmas_por_posicion(df, author_name):
    df['author_position'] = df['author_position'].fillna('desconocida')
    pos_counts = df['author_position'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    pos_counts.plot(kind='bar', ax=ax, color='#06d6a0')
    ax.set_title(f"Frecuencia de Firmas por Posición - {author_name}")
    ax.set_xlabel("Posición")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)

# --- Top 15 Instituciones Colaboradoras ---
def graficar_top_instituciones(df, author_name):
    instituciones = df['institutions'].dropna().str.split('; ').explode()
    top_inst = instituciones.value_counts().head(15)
    fig, ax = plt.subplots(figsize=(6, 4))
    top_inst.sort_values().plot(kind='barh', ax=ax, color='#ef476f')
    ax.set_title(f"Top 15 Instituciones Colaboradoras - {author_name}")
    ax.set_xlabel("Colaboraciones")
    ax.set_ylabel("Institución")
    st.pyplot(fig)

# --- Top 15 Países Colaboradores ---
def graficar_top_paises(df, author_name):
    paises = df['countries'].dropna().str.split('; ').explode()
    top_paises = paises.value_counts().head(15)
    fig, ax = plt.subplots(figsize=(6, 4))
    top_paises.sort_values().plot(kind='barh', ax=ax, color='#ffd166')
    ax.set_title(f"Top 15 Países Colaboradores - {author_name}")
    ax.set_xlabel("Colaboraciones")
    ax.set_ylabel("País")
    st.pyplot(fig)