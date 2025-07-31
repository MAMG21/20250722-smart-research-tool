
import streamlit as st
import pandas as pd
from core.consulta_autores import get_author_id
from core.consulta_publicaciones import fetch_author_works
from core.metricas import compute_bibliometric_indices

st.set_page_config(page_title="OpenAlex Analytics", layout="centered")

st.title("🔭 Análisis Bibliométrico con OpenAlex")
st.markdown("Introduce el nombre de un autor para obtener sus métricas bibliométricas usando OpenAlex.")

# Inputs
author_name = st.text_input("Nombre del autor", value="Yann LeCun")

if st.button("Analizar Autor"):
    try:
        # Buscar autor
        author_id, display_name = get_author_id(author_name, "")
        st.success(f"✅ Autor encontrado: {display_name}")

        # Descargar publicaciones
        with st.spinner("Descargando publicaciones..."):
            df = fetch_author_works(author_id, "")

        if df.empty:
            st.warning("⚠️ No se encontraron publicaciones para este autor.")
        else:
            # Calcular métricas
            indices = compute_bibliometric_indices(df)
            indices["Autor"] = display_name

            # Mostrar resultados
            st.subheader("📊 Métricas Bibliométricas")
            st.dataframe(pd.DataFrame([indices]))

            # Descargar CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Descargar publicaciones en CSV", csv, file_name=f"{author_id}_publicaciones.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Error: {e}")

