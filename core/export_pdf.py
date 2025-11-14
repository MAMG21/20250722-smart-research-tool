# core/export_pdf.py

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.units import inch
from io import BytesIO
import streamlit as st
import matplotlib.pyplot as plt
import tempfile
import base64

def generar_pdf_autor(df_metricas, author_name, total_public, figuras=None):
    """
    Genera un archivo PDF con las métricas principales del autor y opcionalmente imágenes de gráficas.

    Retorna: buffer (BytesIO) con el PDF generado.
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulo', fontSize=18, leading=22, spaceAfter=12, alignment=1))
    styles.add(ParagraphStyle(name='Subtitulo', fontSize=14, leading=18, spaceBefore=10, spaceAfter=8, textColor=colors.HexColor("#333333")))
    styles.add(ParagraphStyle(name='Texto', fontSize=11, leading=14))

    elementos = []

    # --- Título principal ---
    elementos.append(Paragraph(f"📊 Perfil de Investigación de {author_name}", styles['Titulo']))
    elementos.append(Spacer(1, 12))

    # --- Datos principales ---
    elementos.append(Paragraph(f"<b>Total de publicaciones:</b> {total_public}", styles['Texto']))
    elementos.append(Spacer(1, 8))

    # --- Tabla de métricas ---
    elementos.append(Paragraph("🧮 Métricas de Productividad e Impacto", styles['Subtitulo']))

    data = [["Métrica", "Valor"]]
    for col in df_metricas.index:
        data.append([col, str(df_metricas[col])])

    table = Table(data, colWidths=[200, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))
    elementos.append(table)
    elementos.append(Spacer(1, 16))

    # --- Gráficas si existen ---
    if figuras:
        elementos.append(Paragraph("📈 Gráficas del Perfil del Investigador", styles['Subtitulo']))
        for titulo, fig in figuras:
            elementos.append(Spacer(1, 10))
            elementos.append(Paragraph(f"<b>{titulo}</b>", styles['Texto']))

            tmpfile = BytesIO()
            fig.savefig(tmpfile, format="png", bbox_inches="tight", dpi=150)
            tmpfile.seek(0)
            elementos.append(Image(tmpfile, width=5.5*inch, height=3.2*inch))
            elementos.append(Spacer(1, 16))

    # --- Pie de página ---
    elementos.append(Spacer(1, 30))
    elementos.append(Paragraph(
        "🧠 Este reporte fue generado automáticamente con datos de OpenAlex y visualizado en la aplicación Streamlit.",
        styles['Texto']
    ))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


def exportar_pdf(df_metricas, author_name, total_public, figuras=None):
    """
    Genera el PDF y crea un botón de descarga en Streamlit.
    """
    pdf_buffer = generar_pdf_autor(df_metricas, author_name, total_public, figuras)

    st.download_button(
        label="⬇️ Descargar reporte en formato PDF",
        data=pdf_buffer,
        file_name=f"perfil_{author_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
