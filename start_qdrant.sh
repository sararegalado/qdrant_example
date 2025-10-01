#!/bin/bash

echo "🚀 Iniciando Qdrant con persistencia..."

# Crear carpeta de datos si no existe
mkdir -p ./qdrant_data

# Detener contenedor existente si está corriendo
docker stop qdrant 2>/dev/null
docker rm qdrant 2>/dev/null

# Iniciar Qdrant con volumen persistente
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v ./qdrant_data:/qdrant/storage \
  qdrant/qdrant:latest

echo "✅ Qdrant iniciado"
echo "📁 Los datos se guardan en: ./qdrant_data"
echo "🌐 Acceso en: http://localhost:6333"

# Esperar un poco para que inicie
sleep 3

# Verificar que esté corriendo
if curl -s http://localhost:6333/collections > /dev/null; then
    echo "✅ Qdrant está funcionando correctamente"
else
    echo "⚠️  Qdrant aún está iniciando, espera unos segundos..."
fi