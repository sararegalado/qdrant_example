# Qdrant con Docker

Este proyecto incluye una guía rápida para ejecutar y administrar **Qdrant** dentro de un contenedor **Docker** con persistencia de datos.

---

## 🚀 1. Iniciar Qdrant con volumen persistente
El siguiente comando iniciará Qdrant en segundo plano y montará un volumen local (`./qdrant_data`) para almacenar los datos de manera persistente:

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v ./qdrant_data:/qdrant/storage \
  qdrant/qdrant:latest
