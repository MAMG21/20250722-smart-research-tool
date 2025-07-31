
import pandas as pd
import numpy as np
import datetime

def compute_bibliometric_indices(df, comparables=None):
    df['citations'] = pd.to_numeric(df['citations'], errors='coerce').fillna(0)
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    citations = sorted(df['citations'], reverse=True)
    total_citations = sum(citations)

    # H-index
    h = sum(1 for i, c in enumerate(citations) if c >= i + 1)

    # G-index
    g, cum = 0, 0
    for i, c in enumerate(citations):
        cum += c
        if cum >= (i + 1)**2:
            g = i + 1
        else:
            break

    # E-index
    e = np.sqrt(sum(c - h for c in citations[:h])) if h > 0 else 0.0

    # M-index
    years = df['year'].dropna()
    m = h / max(1, datetime.datetime.now().year - int(years.min())) if not years.empty else 0

    # B-index
    b = np.sqrt(sum(citations[:h])) if h > 0 else 0.0

    # V-index
    v = (h + g) / 2

    # H relativo
    h_max = max(comparables) if comparables else max([95, 82, 120, 135, 147, 168, 103])
    h_rel = h / h_max if h_max > 0 else 0

    # i10-index
    i10 = sum(1 for c in citations if c >= 10)

    # k-index (simplificado): raíz cuadrada del total de citas (a falta de definición específica)
    k = round(np.sqrt(total_citations), 2)

    # Índice H fraccional (suma 1/#autores por artículo con al menos h citas)
    df_h_core = df[df["citations"] >= h]
    fractional_h = 0
    for _, row in df_h_core.iterrows():
        num_authors = len(row["authors"].split(";")) if pd.notna(row["authors"]) else 1
        fractional_h += 1 / num_authors

    # Autorank (propuesto): promedio ponderado de h, g, i10, b y total citas
    autorank = round((h + g + i10 + b + total_citations / 100) / 5, 2)

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
