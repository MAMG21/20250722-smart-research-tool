import pandas as pd
import numpy as np
import datetime
import streamlit as st

def compute_bibliometric_indices(df, comparables=None):
    """
    Calcula varios índices bibliométricos (h, g, e, m, b, v, i10, k, h fraccional, etc.)
    Compatible con el DataFrame devuelto por fetch_author_works().
    """
    st.session_state.df_master = df

    # --- Verificación básica ---
    if df is None or len(df) == 0:
        print("⚠️ DataFrame vacío o no válido.")
        return {}

    df = df.copy()

    # --- Detección automática de columnas ---
    # Buscamos la columna de citas
    if "citations" in df.columns:
        citation_col = "citations"
    elif "cited_by_count" in df.columns:
        citation_col = "cited_by_count"
    else:
        df["citations"] = 0
        citation_col = "citations"

    # Buscamos la columna de año
    if "year" in df.columns:
        year_col = "year"
    elif "publication_year" in df.columns:
        year_col = "publication_year"
    else:
        df["year"] = np.nan
        year_col = "year"

    # --- Normalización de tipos ---
    df[citation_col] = pd.to_numeric(df[citation_col], errors="coerce").fillna(0).astype(int)
    df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
    if "authors" not in df.columns:
        df["authors"] = ""

    citations = sorted(df[citation_col], reverse=True)
    total_citations = int(sum(citations))

    # --- Cálculo de índices ---
    # H-index
    h = 0
    for i, c in enumerate(citations):
        if c >= i + 1:
            h = i + 1
        else:
            break

    # G-index
    g, cum = 0, 0
    for i, c in enumerate(citations):
        cum += c
        if cum >= (i + 1) ** 2:
            g = i + 1

    # E-index
    e = np.sqrt(sum((c - h) for c in citations[:h] if c > h)) if h > 0 else 0.0

    # M-index
    years = df[year_col].dropna()
    if not years.empty:
        first_year = int(years.min())
        active_years = max(1, datetime.datetime.now().year - first_year + 1)
        m = h / active_years
    else:
        m = 0.0

    # B-index
    b = np.sqrt(sum(citations[:h])) if h > 0 else 0.0

    # V-index
    v = (h + g) / 2

    # i10-index
    i10 = sum(1 for c in citations if c >= 10)

    # K-index
    k = round(np.sqrt(total_citations), 2)

    # H fraccional
    df_h_core = df[df[citation_col] >= h]
    fractional_h = 0.0
    for _, row in df_h_core.iterrows():
        authors = row.get("authors", "")
        n_authors = len([a for a in str(authors).split(";") if a.strip() != ""]) or 1
        fractional_h += 1 / n_authors

    # Autorank (promedio ponderado)
    autorank = round((h + g + i10 + b + total_citations / 100) / 5, 2)

    # H relativo
    if comparables and len(comparables) > 0:
        h_max = max(comparables)
    else:
        h_max = max([95, 82, 120, 135, 147, 168, 103])
    h_rel = h / h_max if h_max > 0 else 0

    # --- Resultado final ---
    return {
        "Total Artículos": len(citations),
        "Total Citas": total_citations,
        "H-index": h,
        "G-index": g,
        "E-index": round(e, 2),
        "M-index": round(m, 2),
        "B-index": round(b, 2),
        "V-index": round(v, 2),
        "i10-index": i10,
        "K-index": k,
        "H Fraccional": round(fractional_h, 2),
        "Autorank": autorank,
        "H Relativo": round(h_rel, 4)
    }
