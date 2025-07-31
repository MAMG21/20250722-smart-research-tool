
import requests
import time
import pandas as pd

def fetch_author_works(author_id, email):
    base_url = "https://api.openalex.org/works"
    all_rows, page = [], 1
    while True:
        params = {
            "filter": f"authorships.author.id:{author_id}",
            "per-page": 200,
            "page": page
        }
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            break
        for w in results:
            authors = [a["author"].get("display_name", "N/A") for a in w.get("authorships", [])]
            topics = [c.get("display_name", "N/A") for c in w.get("concepts", [])]
            all_rows.append({
                "id": w.get("id"),
                "doi": w.get("doi"),
                "title": w.get("display_name"),
                "type": w.get("type"),
                "year": w.get("publication_year"),
                "authors": "; ".join(authors),
                "topics": "; ".join(topics),
                "citations": w.get("cited_by_count", 0),
                "author_id": author_id
            })
        page += 1
        time.sleep(0.1)
    return pd.DataFrame(all_rows)
