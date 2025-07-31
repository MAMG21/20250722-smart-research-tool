
import duckdb
import pandas as pd
from core.consulta_autores import get_concept_id, get_top_authors_by_concept
from core.consulta_publicaciones import fetch_author_works
from core.metricas import compute_bibliometric_indices

# Configuración
CAMPO = "astronomy"
TOP_N_AUTORES = 200

# Conectar o crear base de datos
con = duckdb.connect("outputs/openalex_metrics.duckdb")

# Crear tabla si no existe
con.execute("""
CREATE TABLE IF NOT EXISTS autor_metricas (
    autor TEXT,
    total_articulos INTEGER,
    total_citas INTEGER,
    h_index INTEGER,
    g_index INTEGER,
    e_index DOUBLE,
    m_index DOUBLE,
    b_index DOUBLE,
    v_index DOUBLE,
    i10_index INTEGER,
    k_index DOUBLE,
    h_fraccional DOUBLE,
    autorank DOUBLE,
    h_relativo DOUBLE
);
""")

# Obtener ID del campo
concept_id, concept_name = get_concept_id(CAMPO)  

# Obtener autores
autores = get_top_authors_by_concept(concept_id, top_n=TOP_N_AUTORES)

#test
#autor = autores[1] 

# Iterar sobre cada autor
for autor in autores:
    try:
        autor_id = autor["id"].split("/")[-1]
        autor_nombre = autor["display_name"]
        print(f"🔍 Procesando: {autor_nombre}")

        df_pub = fetch_author_works(autor_id, "")
        metricas = compute_bibliometric_indices(df_pub)
        metricas["autor"] = autor_nombre

        df_metricas = pd.DataFrame([metricas])
        df_metricas = df_metricas.rename(columns={
            "Total Artículos": "total_articulos",
            "Total Citas":      "total_citas",
            "H-index":          "h_index",
            "G-index":          "g_index",
            "E-index":          "e_index",
            "M-index":          "m_index",
            "B-index":          "b_index",
            "V-index":          "v_index",
            "i10-index":        "i10_index",
            "K-index":          "k_index",
            "H Fraccional":     "h_fraccional",
            "Autorank":         "autorank",
            "H Relativo":       "h_relativo"
        })
        

        # ahora sí insertamos todo
        con.execute("""
            INSERT INTO autor_metricas (
                autor,
                total_articulos,
                total_citas,
                h_index,
                g_index,
                e_index,
                m_index,
                b_index,
                v_index,
                i10_index,
                k_index,
                h_fraccional,
                autorank,
                h_relativo
            )
            SELECT
                autor,
                total_articulos,
                total_citas,
                h_index,
                g_index,
                e_index,
                m_index,
                b_index,
                v_index,
                i10_index,
                k_index,
                h_fraccional,
                autorank,
                h_relativo
            FROM df_metricas
            """)


    except Exception as e:
        print(f"❌ Error con {autor['display_name']}: {e}")

con.close()