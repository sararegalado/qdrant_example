
# 1. Ejecutar Qdrant con volumen persistente (crea carpeta automáticamente)
```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v ./qdrant_data:/qdrant/storage \
  qdrant/qdrant:latest


# 2. Para detener Qdrant
```bash
docker stop qdrant

# 3. Para reiniciar Qdrant (mantiene los datos)
```bash
docker start qdrant


# 4. Para eliminar el contenedor (los datos persisten en ~/qdrant_data)
```bash
docker rm qdrant

# 5. Para ver logs
```bash
docker logs qdrant
