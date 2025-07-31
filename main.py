
import pandas as pd
from consulta_autores import get_concept_id, get_top_authors_by_concept
from consulta_publicaciones import fetch_author_works
from metricas import compute_bibliometric_indices

# Configuración
EMAIL = "tu_email@ejemplo.com"
CAMPO_ESTUDIO = "astronomy"
TOP_N_AUTORES = 30

# Paso 1: Obtener ID del campo
concept_id, concept_name = get_concept_id(CAMPO_ESTUDIO, EMAIL)

# Paso 2: Obtener autores top
autores = get_top_authors_by_concept(concept_id, EMAIL, top_n=TOP_N_AUTORES)

# Paso 3: Recopilar publicaciones y métricas
tabla_resultados = []

for autor in autores:
    autor_id = autor["id"].split("/")[-1]
    autor_nombre = autor["display_name"]
    try:
        print(f"🔍 Procesando autor: {autor_nombre}")
        df_pub = fetch_author_works(autor_id, EMAIL)
        if df_pub.empty:
            print(f"⚠️ Sin publicaciones para {autor_nombre}")
            continue
        metricas = compute_bibliometric_indices(df_pub)
        metricas["Autor"] = autor_nombre
        tabla_resultados.append(metricas)
    except Exception as e:
        print(f"❌ Error con {autor_nombre}: {e}")

# Paso 4: Guardar resultados
df_final = pd.DataFrame(tabla_resultados)
df_final.to_csv("metricas_astronomia.csv", index=False)
print("✅ Archivo 'metricas_astronomia.csv' generado.")
