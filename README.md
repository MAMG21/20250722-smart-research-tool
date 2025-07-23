# Evaluación de la producción científica de investigadores con métricas y altmétricas a partir de bases de datos bibliográficas dinámicas

Este proyecto de maestría busca diseñar y desarrollar una herramienta automatizada para analizar y clasificar la producción científica de investigadores en el área de la astronomía. Se integran métricas bibliométricas, altmétricas y aprendizaje automático, usando datos abiertos provenientes de bases como OpenAlex.

## 🎯 Objetivo General

Desarrollar un sistema que permita la extracción, análisis, clasificación y visualización de artículos científicos mediante un pipeline ETL, técnicas estadísticas, y un modelo de clasificación basado en machine learning.

## 📌 Características Principales

- Extracción automatizada de datos científicos desde OpenAlex (API REST)
- Cálculo de métricas bibliométricas y altmétricas (índice H, índice G, i10, etc.)
- Modelo de clasificación de autores por relevancia
- Visualización interactiva de resultados (dashboard web)
- Foco de estudio en el área de la astronomía

## 🧱 Estructura del Proyecto

```
proyecto-impacto-cientifico/
├── docs/             ← Documentación (propuesta, cronograma, referencias)
├── src/
│   ├── backend/      ← ETL, cálculos, API
│   └── frontend/     ← Dashboard interactivo (Streamlit / Dash)
├── data/             ← Datos de entrada y muestras
├── notebooks/        ← Prototipos y análisis exploratorio
├── tests/            ← Scripts de pruebas
├── models/           ← Modelos entrenados y serializados
├── results/          ← Visualizaciones y resultados generados
```

## ⚙️ Tecnologías y Herramientas

- Python (Pandas, NumPy, Scikit-learn, FastAPI, Streamlit/Dash)
- PostgreSQL o MongoDB (según requerimientos)
- OpenAlex API
- Git & GitHub para control de versiones

## 📈 Estado del Proyecto

🚧 En desarrollo — actualmente en fase de diseño del pipeline ETL y revisión de métricas bibliométricas.

## 👩‍💻 Autores

- María Alejandra Marín Galán  
- Nelson Julián Maya  

Dirección académica:
- Prof. Dr. Jorge Enrique García Farieta  
- Prof. Dr. Héctor Javier Hórtua

Maestría en Estadística Aplicada y Ciencia de Datos — Universidad El Bosque

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.
