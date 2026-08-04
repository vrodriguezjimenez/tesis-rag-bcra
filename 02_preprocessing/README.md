# 02. Exploración y preprocesamiento del Corpus

Este subdirectorio documenta la exploración de la estructura interna de los Textos Ordenados del BCRA y el desarrollo de la función de limpieza de texto, como paso previo a la implementación de la estrategia de chunking por secciones.

## Contexto

El corpus consiste en 103 archivos PDF correspondientes a los Textos Ordenados del BCRA, descargados en la etapa anterior (`01_corpus_extraction/`). El objetivo de esta etapa es comprender la estructura interna de los documentos para implementar una estrategia de chunking por secciones, tal como recomendó el director de tesis.

## Hallazgos principales

### Estructura del corpus

A partir del análisis de los 103 documentos se identificaron cuatro grupos con estructuras distintas:

| Grupo | Descripción | Cantidad aproximada |
|-------|-------------|-------------------|
| A | Secciones numeradas con pie de página estándar | ~75 documentos |
| B | Secciones numeradas con pie de página en formato distinto | ~10 documentos |
| C | Organizados por Anexos en lugar de Secciones | ~6 documentos |
| D | Numerados directamente sin la palabra "Sección", o con texto ruidoso | ~11 documentos |

Un documento (`t-capmin.pdf`) estaba corrupto por una descarga incompleta y fue descargado nuevamente.

### Pies de página

Los PDFs del BCRA repiten en cada página un pie de página que interfiere con el chunking. Se detectaron tres variantes de este patrón y se desarrolló una función de limpieza.

## Archivos

- `exploracion_corpus.ipynb` — notebook con el código de exploración y la función de limpieza (versión preliminar, sujeta a revisión)
  
