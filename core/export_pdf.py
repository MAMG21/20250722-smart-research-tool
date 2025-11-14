# core/export_pdf.py
import io
import os
from datetime import datetime

import streamlit as st
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors


# ---------------------------
# UTIL: buscar imagen por palabras clave (robusto)
# ---------------------------
def _find_image(figuras, keywords):
    """
    Busca en la lista figuras (titulo, ruta) la primera ruta cuyo título
    contiene alguna de las palabras clave (case-insensitive).
    keywords puede ser string o list de strings.
    Retorna ruta o None.
    """
    if figuras is None:
        return None
    if isinstance(keywords, str):
        keywords = [keywords]
    keywords = [k.lower() for k in keywords]

    for titulo, ruta in figuras:
        t = (titulo or "").lower()
        for k in keywords:
            if k in t:
                if os.path.isfile(ruta):
                    return ruta
    # si no encontró por título, intentar encontrar por nombre de archivo
    for titulo, ruta in figuras:
        fname = os.path.basename(ruta).lower()
        for k in keywords:
            if k in fname and os.path.isfile(ruta):
                return ruta
    return None


# ---------------------------
# GENERAR PDF: estilo similar a Streamlit (landscape)
# ---------------------------
def generar_pdf_autor(df_metricas, author_name, total_public, figuras=None):
    """
    Construye el PDF en memoria (BytesIO) con estilo similar a la página de análisis.
    df_metricas: DataFrame de 1 fila con las métricas (o dict convertido a df previamente).
    figuras: lista de tuplas (titulo, ruta)
    """

    buffer = io.BytesIO()

    # Usamos orientación horizontal para parecer al dashboard
    pagesize = landscape(letter)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    story = []
    styles = getSampleStyleSheet()

    # Estilos
    titulo_style = ParagraphStyle(
        "TituloCustom",
        parent=styles["Heading1"],
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),  # gris oscuro
        spaceAfter=10
    )

    subtitulo_style = ParagraphStyle(
        "SubtituloCustom",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=6
    )

    card_title_style = ParagraphStyle(
        "CardTitle",
        parent=styles["Normal"],
        fontSize=12,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827")
    )

    card_value_style = ParagraphStyle(
        "CardValue",
        parent=styles["Normal"],
        fontSize=18,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0a2540")
    )

    small_label = ParagraphStyle(
        "SmallLabel",
        parent=styles["Normal"],
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#6b7280")
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["BodyText"],
        fontSize=11,
        leading=14
    )

    # -----------------------------------
    # Portada / Cabecera
    # -----------------------------------
    story.append(Paragraph(f"Reporte de Análisis — {author_name}", titulo_style))
    story.append(Paragraph(f"Resumen bibliométrico generado automáticamente", small_label))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", small_label))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="95%", thickness=1, color=colors.HexColor("#E5E7EB")))
    story.append(Spacer(1, 12))

    # -----------------------------------
    # Cards métricas: organizadas en 4 columnas x 3 filas
    # -----------------------------------
    story.append(Paragraph("Métricas de productividad e impacto", subtitulo_style))
    story.append(Spacer(1, 6))

    # Extraer métricas del DataFrame (primera fila)
    if hasattr(df_metricas, "values"):
        try:
            # df_metricas may be a 1-row DataFrame
            cols = df_metricas.columns.tolist()
            row = df_metricas.iloc[0].to_dict()
        except Exception:
            # fallback if df_metricas is a dict-like
            cols = list(df_metricas.columns) if hasattr(df_metricas, "columns") else []
            row = dict(df_metricas)
    else:
        # if somehow not a DataFrame, try dict
        row = dict(df_metricas)
        cols = list(row.keys())

    # Define the exact order requested
    cards_order = [
        ("Total Citas", "Total Citas"),
        ("H-index", "H-index"),
        ("G-index", "G-index"),
        ("E-index", "E-index"),
        ("M-index", "M-index"),
        ("B-index", "B-index"),
        ("V-index", "V-index"),
        ("i10-index", "i10-index"),
        ("K-index", "K-index"),
        ("H Fraccional", "H Fraccional"),
        ("Autorank", "Autorank"),
        ("H Relativo", "H Relativo"),
    ]

    # Build card table data: each cell will be a mini table (title + value)
    card_cells = []
    for display_name, key in cards_order:
        value = row.get(key, "") if isinstance(row, dict) else ""
        # format numbers nicely
        try:
            if isinstance(value, float):
                val_text = f"{value:,.2f}".replace(",", ".")
            else:
                val_text = str(value)
        except Exception:
            val_text = str(value)

        # Create a small table representing the card (title and value stacked)
        card_inner = [
            [Paragraph(f"<b>{display_name}</b>", card_title_style)],
            [Spacer(1, 4)],
            [Paragraph(val_text, card_value_style)]
        ]
        card_table = Table(card_inner, colWidths=[1.5 * inch])
        card_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7FA")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E6EEF9")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ]))
        card_cells.append(card_table)

    # Arrange into rows of 4
    rows = []
    row_cells = []
    for i, cell in enumerate(card_cells):
        row_cells.append(cell)
        if (i + 1) % 4 == 0:
            rows.append(row_cells)
            row_cells = []
    if row_cells:
        # pad the last row to 4
        while len(row_cells) < 4:
            row_cells.append('')
        rows.append(row_cells)

    # build master table
    card_master = Table(rows, colWidths=[1.8 * inch] * 4, hAlign="LEFT")
    card_master.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 8),
                                     ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                                     ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                                     ("TOPPADDING", (0, 0), (-1, -1), 8)]))
    story.append(card_master)
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="95%", thickness=0.6, color=colors.HexColor("#E5E7EB")))
    story.append(Spacer(1, 12))

    # -----------------------------------
    # Sección Colaboración Científica (2x2)
    # -----------------------------------
    story.append(Paragraph("Colaboración Científica", subtitulo_style))
    story.append(Spacer(1, 8))

    # map titles to search keywords
    collab_map = [
        ("Posición en autoría", ["posicion", "firma", "autoria"]),
        ("Mapa de Colaboraciones", ["mapa", "colaboraciones"]),
        ("Redes de Coautoria", ["coautor", "coautoria", "red de coautor"]),
        ("Redes de Instituciones", ["institucion", "instituciones", "red de instituci"])
    ]

    collab_imgs = []
    for title, keys in collab_map:
        ruta = _find_image(figuras, keys)
        collab_imgs.append((title, ruta))

    # Build 2x2 table with images (use placeholders if missing)
    collab_cells = []
    for title, ruta in collab_imgs:
        cell_parts = []
        cell_parts.append(Paragraph(f"<b>{title}</b>", small_label))
        cell_parts.append(Spacer(1, 6))
        if ruta and os.path.isfile(ruta):
            img = Image(ruta, width=3.6 * inch, height=2.5 * inch)
            img.hAlign = "CENTER"
            cell_parts.append(img)
        else:
            cell_parts.append(Paragraph("No disponible", normal_style))
        collab_cells.append(cell_parts)

    # Arrange into table rows (2 columns)
    collab_table_data = [
        [collab_cells[0], collab_cells[1]],
        [collab_cells[2], collab_cells[3]]
    ]
    # Wrap each cell content into a single cell using Table
    def _wrap_cell(content):
        return Table([[c] for c in content], colWidths=[3.6 * inch])

    collab_wrapped = [[_wrap_cell(collab_table_data[r][c]) for c in range(2)] for r in range(2)]
    collab_master = Table(collab_wrapped, colWidths=[3.8 * inch, 3.8 * inch])
    collab_master.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(collab_master)
    story.append(Spacer(1, 18))
    story.append(HRFlowable(width="95%", thickness=0.6, color=colors.HexColor("#E5E7EB")))
    story.append(Spacer(1, 12))

    # -----------------------------------
    # Análisis de Publicaciones: 3 en fila
    # -----------------------------------
    story.append(Paragraph("Análisis de Publicaciones", subtitulo_style))
    story.append(Spacer(1, 8))

    pub_map = [
        ("Publicaciones por Año", ["publicaciones", "publicado", "histograma", "numero de articulos"]),
        ("Citas por Año", ["citas por año", "citas", "cantidad de citas", "citas_recibidas", "citas"]),
        ("Modelos de Crecimiento de Citas", ["modelo", "crecimiento", "modelos", "acumuladas"])
    ]

    pub_imgs = []
    for title, keys in pub_map:
        ruta = _find_image(figuras, keys)
        pub_imgs.append((title, ruta))

    # create three columns table
    pub_cells = []
    for title, ruta in pub_imgs:
        parts = []
        parts.append(Paragraph(f"<b>{title}</b>", small_label))
        parts.append(Spacer(1, 6))
        if ruta and os.path.isfile(ruta):
            # model plot may be taller, we keep consistent height
            img = Image(ruta, width=6.0 * inch / 3.0 * 2.0, height=2.6 * inch)  # approx width per column
            img.hAlign = "CENTER"
            parts.append(img)
        else:
            parts.append(Paragraph("No disponible", normal_style))
        pub_cells.append(_wrap_cell(parts))

    pub_master = Table([pub_cells], colWidths=[3.6 * inch, 3.6 * inch, 3.6 * inch])
    pub_master.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(pub_master)
    story.append(Spacer(1, 18))
    story.append(HRFlowable(width="95%", thickness=0.6, color=colors.HexColor("#E5E7EB")))
    story.append(Spacer(1, 12))

    # -----------------------------------
    # Nubes de palabras (ancho completo)
    # -----------------------------------
    story.append(Paragraph("Nubes de Palabras", subtitulo_style))
    story.append(Spacer(1, 8))

    cloud_map = [
        ("Nube de Abstracts", ["abstract", "nube_abstract", "nube abstracts"]),
        ("Nube de Títulos", ["titulos", "nube_titulos", "nube titulos", "titulo"])
    ]

    for title, keys in cloud_map:
        ruta = _find_image(figuras, keys)
        story.append(Paragraph(f"<b>{title}</b>", small_label))
        story.append(Spacer(1, 6))
        if ruta and os.path.isfile(ruta):
            img = Image(ruta, width=11.5 * inch, height=3.6 * inch)
            img.hAlign = "CENTER"
            # put in card-like border
            img_table = Table([[img]], colWidths=[11.5 * inch])
            img_table.setStyle(TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E6EEF9")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(img_table)
            story.append(Spacer(1, 12))
        else:
            story.append(Paragraph("No disponible", normal_style))
            story.append(Spacer(1, 12))

    # -----------------------------------
    # Pie de página / nota
    # -----------------------------------
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="95%", thickness=0.6, color=colors.HexColor("#E5E7EB")))
    story.append(Spacer(1, 8))
    story.append(Paragraph("🧠 Este reporte fue generado automáticamente con Smart Research Tool.", small_label))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}", small_label))

    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


# ---------------------------
# FUNCIÓN PARA STREAMLIT -> BOTÓN
# ---------------------------
def exportar_pdf(df_metricas, author_name, total_public, figuras=None):
    """
    Genera el PDF en memoria y crea el botón de descarga en Streamlit.
    """
    try:
        pdf_buffer = generar_pdf_autor(df_metricas, author_name, total_public, figuras)
        st.download_button(
            label="⬇️ Descargar reporte en PDF",
            data=pdf_buffer,
            file_name=f"perfil_{author_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"No se pudo generar el PDF: {e}")
        raise
