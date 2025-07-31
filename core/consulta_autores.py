
import requests

def get_author_id(author_name, email):
    """Busca el ID de un autor en OpenAlex dado su nombre."""
    url = "https://api.openalex.org/authors"
    params = {"search": author_name, "mailto": email}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        raise ValueError("Autor no encontrado.")
    author = results[0]
    return author['id'].split('/')[-1], author['display_name']

def get_concept_id(field_name):
    url = "https://api.openalex.org/concepts"
    params = {"filter": f"display_name.search:{field_name}"}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        raise ValueError(f"No se encontró el campo: {field_name}")
    return results[0]["id"], results[0]["display_name"]

def get_top_authors_by_concept(concept_id, top_n=50, mailto="tucorreo@ejemplo.com"):
    url = "https://api.openalex.org/authors"
    params = {
        "filter": f"concepts.id:{concept_id}",
        "sort": "summary_stats.h_index:desc",
        "per-page": top_n,
        "mailto": mailto
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("results", [])
