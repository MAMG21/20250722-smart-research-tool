import requests
import pandas as pd
import time
from collections import Counter

# --- FUNCIÓN AUXILIAR PARA RECONSTRUIR EL ABSTRACT ---
def reconstruct_abstract(inverted_index):
    """
    Reconstruye el texto del abstract a partir del formato de índice invertido de OpenAlex.
    """
    if not inverted_index:
        return ""
    max_index = max(max(positions) for positions in inverted_index.values())
    word_list = [""] * (max_index + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            word_list[pos] = word
    return " ".join(word_list)

# --- FUNCIÓN PRINCIPAL: fetch_author_works ---
def fetch_author_works(author_id, email):
    """
    Extrae todas las publicaciones de un autor en OpenAlex dado su ID.
    Incluye información detallada: autores, países, instituciones, conceptos, venue y abstract reconstruido.
    """
    base_url = "https://api.openalex.org/works"
    all_rows, page = [], 1

    while True:
        params = {
            "filter": f"authorships.author.id:{author_id}",
            "per-page": 200,
            "page": page,
            "mailto": email
        }

        print(f"📄 Descargando página {page} de publicaciones...")
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        results = resp.json().get("results", [])

        if not results:
            print("✅ No hay más resultados. Extracción completada.")
            break

        for w in results:
            try:
                # --- Autores, países e instituciones ---
                authorships = w.get("authorships", [])
                author_names = []
                countries_list = []
                institutions_list = []

                for authorship in authorships:
                    if not authorship:
                        continue
                    author_obj = authorship.get("author", {})
                    author_names.append(author_obj.get("display_name", "N/A"))

                    if authorship.get("countries"):
                        countries_list.extend(authorship["countries"])

                    if authorship.get("institutions"):
                        for inst in authorship["institutions"]:
                            if inst and inst.get("display_name"):
                                institutions_list.append(inst["display_name"])

                # --- Campos de investigación (concepts) ---
                concepts_list = [concept.get("display_name") for concept in w.get("concepts", []) if concept.get("display_name")]

                # --- Venue / Fuente de publicación ---
                primary_location = w.get("primary_location") or {}
                source = primary_location.get("source") or {}
                venue_name = source.get("display_name", "N/A")

                # --- Abstract reconstruido ---
                inverted_abstract = w.get("abstract_inverted_index")
                abstract_text = reconstruct_abstract(inverted_abstract)

                # --- Agregacion de los años ---
                counts_by_year = w.get("counts_by_year", [])
                counts_years = [c.get("year") for c in counts_by_year] if counts_by_year else []
                counts_citations = [c.get("cited_by_count") for c in counts_by_year] if counts_by_year else []

                # --- Fila de datos ---
                all_rows.append({
                    "id": w.get("id", "N/A"),
                    "DOI": w.get("doi", "N/A"),
                    "title": w.get("title", "N/A"),
                    "abstract": abstract_text,
                    "type": w.get("type", "N/A"),
                    "language": w.get("language", "N/A"),
                    "publication_year": w.get("publication_year"),
                    "cited_by_count": w.get("cited_by_count", 0),
                    "authors": "; ".join(author_names),
                    "author_count": len(author_names),
                    "countries_list": "; ".join(set(countries_list)),
                    "institutions_list": "; ".join(set(institutions_list)),
                    "research_fields": "; ".join(concepts_list),
                    "venue_name": venue_name,
                    "source_type": source.get("type", "N/A"),
                    "author_id": author_id,
                    "counts_by_year.year": counts_years,
                    "counts_by_year.cited_by_count": counts_citations
                })

            except Exception as e:
                work_id = w.get("id", "ID no encontrado")
                print(f"⚠️ Error procesando publicación {work_id}: {e}")
                continue

        page += 1
        time.sleep(0.1)
    
    if all_rows:
        df_master = pd.DataFrame(all_rows).dropna(subset=['publication_year', 'cited_by_count'])
        df_master['publication_year'] = df_master['publication_year'].astype(int)
        print(f"\n🚀 DataFrame Maestro creado con éxito. Contiene {len(df_master)} publicaciones.")
        df_master.info()
    else:
        print("No se encontraron publicaciones válidas para el autor.")
    
    df_master = df_master[
        (df_master['type'] == 'article') &
        (df_master['source_type'].isin(['journal']))
    ].copy()

    print(f"🚀 Extracción finalizada. Total de publicaciones: {len(all_rows)}")
    return pd.DataFrame(all_rows)