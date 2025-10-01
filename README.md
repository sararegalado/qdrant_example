# Qdrant Example - Base de Datos Vectorial

🚀 **Proyecto de ejemplo usando Qdrant como base de datos vectorial para búsquedas semánticas**

## 📋 Descripción

Este proyecto demuestra cómo usar Qdrant (base de datos vectorial) para:
- Almacenar textos como embeddings
- Realizar búsquedas por similitud semántica
- Mantener persistencia de datos
- Evitar duplicados automáticamente

## 🛠️ Requisitos

- **Docker** (para ejecutar Qdrant)
- **Python 3.8+**
- **Librerías Python**:
  ```bash
  # Instalar desde requirements.txt
  pip install -r requirements.txt
  
  # O instalar manualmente
  pip install qdrant-client sentence-transformers
  ```

## 🚀 Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone https://github.com/sararegalado/qdrant_example.git
cd qdrant_example
```

### 2. Iniciar Qdrant (Método Simple)
```bash
# Hacer el script ejecutable
chmod +x start_qdrant.sh

# Ejecutar Qdrant con persistencia
./start_qdrant.sh
```

### 3. Ejecutar el ejemplo
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
qdrant_example/
├── main.py              # Script principal con ejemplos
├── start_qdrant.sh      # Script para iniciar Qdrant
├── requirements.txt     # Dependencias de Python
├── text_files/          # Carpeta para archivos de texto
│   └── bilbao.txt       # Archivo de ejemplo
├── qdrant_data/         # Datos persistentes (se crea automáticamente)
├── .gitignore           # Archivos a ignorar en git
└── README.md            # Este archivo
```

## 🔧 Uso Detallado

### Iniciar Qdrant Manualmente
Si prefieres no usar el script:

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v ./qdrant_data:/qdrant/storage \
  qdrant/qdrant:latest
```

### Comandos Útiles

```bash
# Ver estado del contenedor
docker ps

# Ver logs de Qdrant
docker logs qdrant

# Detener Qdrant
docker stop qdrant

# Reiniciar Qdrant (mantiene datos)
docker start qdrant

# Eliminar contenedor (datos persisten)
docker rm qdrant
```

## 📊 Funcionalidades del Código

### 1. **Creación de Colección**
```python
create_text_collection()  # Crea colección si no existe
```

### 2. **Agregar Textos (sin duplicados)**
```python
add_texts_to_collection([
    "Tu texto aquí",
    "Otro texto"
], metadata=[
    {"source": "manual", "topic": "ejemplo"}
])
```

### 3. **Búsqueda Semántica**
```python
results = search_similar_texts("¿Qué es Qdrant?")
for result in results:
    print(f"Score: {result.score}")
    print(f"Texto: {result.payload['text']}")
```

## 🗄️ Persistencia de Datos

- **Los datos se guardan en**: `./qdrant_data/`
- **Supervive a reinicios**: ✅
- **No se pierden al eliminar el contenedor**: ✅
- **Detección de duplicados**: ✅

## 📝 Archivos de Texto

Coloca archivos `.txt` en la carpeta `text_files/` y se procesarán automáticamente:

```
text_files/
├── documento1.txt
├── documento2.txt
└── bilbao.txt
```

## 🔍 Ejemplos de Búsqueda

El script incluye ejemplos de:
- Búsqueda básica por similitud
- Búsqueda con filtros por metadata
- Procesamiento de archivos de texto

## 🚨 Solución de Problemas

### Qdrant no inicia
```bash
# Verificar Docker
docker --version

# Verificar puertos
lsof -i :6333
```

### Error de conexión
```bash
# Verificar que Qdrant esté corriendo
curl http://localhost:6333/collections
```

### Permisos en el script
```bash
chmod +x start_qdrant.sh
```

## 🤝 Contribuir

1. Fork del proyecto
2. Crear rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🔗 Enlaces Útiles

- [Documentación de Qdrant](https://qdrant.tech/documentation/)
- [Qdrant Python Client](https://github.com/qdrant/qdrant-client)
- [Sentence Transformers](https://www.sbert.net/)

---

**Desarrollado por**: [Sara Regalado](https://github.com/sararegalado)