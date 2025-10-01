from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import os
import uuid
from typing import List, Dict, Any


client = QdrantClient(url="http://localhost:6333")

# Sentence Transformers contains many embedding models. Choose one
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Get the embedding dimension for the model
embedding_dim = encoder.get_sentence_embedding_dimension()

def load_text_from_file(file_path: str) -> str:
    """Carga texto desde un archivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error al cargar el archivo {file_path}: {e}")
        return ""

def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Divide el texto en chunks más pequeños para mejor procesamiento."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
    return chunks

def text_to_embeddings(texts: List[str]) -> List[List[float]]:
    """Convierte una lista de textos a embeddings."""
    embeddings = encoder.encode(texts)
    return embeddings.tolist()

def create_text_collection(collection_name: str = "text_collection"):
    """Crea una colección optimizada para texto."""
    try:
        client.get_collection(collection_name)
        print(f"La colección '{collection_name}' ya existe.")
    except:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
        )
        print(f"Colección '{collection_name}' creada exitosamente.")

def text_exists_in_collection(text: str, collection_name: str = "text_collection") -> bool:
    """Verifica si un texto ya existe en la colección."""
    try:
        # Buscar textos exactos
        search_result = client.scroll(
            collection_name=collection_name,
            scroll_filter=Filter(
                must=[FieldCondition(key="text", match=MatchValue(value=text))]
            ),
            limit=1,
            with_payload=True
        )
        return len(search_result[0]) > 0
    except:
        return False

def add_texts_to_collection(texts: List[str], collection_name: str = "text_collection", metadata: List[Dict[str, Any]] = None):
    """Añade textos como embeddings a la colección, evitando duplicados."""
    if not texts:
        print("No hay textos para procesar.")
        return
    
    # Filtrar textos que ya existen
    new_texts = []
    new_metadata = []
    duplicates_count = 0
    
    for i, text in enumerate(texts):
        if not text_exists_in_collection(text, collection_name):
            new_texts.append(text)
            if metadata and i < len(metadata):
                new_metadata.append(metadata[i])
            else:
                new_metadata.append({})
        else:
            duplicates_count += 1
    
    if duplicates_count > 0:
        print(f"⚠️  Se encontraron {duplicates_count} textos duplicados, se omitieron.")
    
    if not new_texts:
        print("✅ Todos los textos ya existen en la colección.")
        return
    
    # Generar embeddings solo para textos nuevos
    embeddings = text_to_embeddings(new_texts)
    
    # Crear puntos
    points = []
    for i, (text, embedding) in enumerate(zip(new_texts, embeddings)):
        point_id = str(uuid.uuid4())
        payload = {
            "text": text,
            "chunk_id": i,
            "text_length": len(text)
        }
        
        # Añadir metadata adicional
        if new_metadata and i < len(new_metadata):
            payload.update(new_metadata[i])
        
        points.append(PointStruct(
            id=point_id,
            vector=embedding,
            payload=payload
        ))
    
    # Insertar en Qdrant
    operation_info = client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points,
    )
    
    print(f"✅ Se añadieron {len(points)} textos nuevos a la colección '{collection_name}'")
    return operation_info

def search_similar_texts(query_text: str, collection_name: str = "text_collection", limit: int = 5):
    """Busca textos similares al query proporcionado."""
    # Convertir query a embedding
    query_embedding = encoder.encode([query_text])[0].tolist()
    
    # Realizar búsqueda
    search_result = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        with_vectors=False,
        with_payload=True,
        limit=limit
    ).points
    
    return search_result

# Crear la colección para texto
create_text_collection()

# Ejemplos de texto para cargar
sample_texts = [
    "Qdrant es una base de datos vectorial de código abierto que permite búsquedas de similitud.",
    "Los embeddings son representaciones numéricas de texto que capturan el significado semántico.",
    "La búsqueda por similitud permite encontrar documentos relacionados basándose en el contenido.",
    "Machine Learning y Deep Learning utilizan vectores para representar información compleja.",
    "Python es un lenguaje de programación popular para ciencia de datos e inteligencia artificial."
]

# Cargar textos de ejemplo en la colección
metadata_examples = [
    {"source": "documentation", "topic": "database"},
    {"source": "documentation", "topic": "embeddings"},
    {"source": "documentation", "topic": "search"},
    {"source": "documentation", "topic": "ml"},
    {"source": "documentation", "topic": "programming"}
]

add_texts_to_collection(sample_texts, metadata=metadata_examples)

# Ejemplo de carga de texto desde archivo
# Si tienes archivos de texto en el directorio RAG_example
text_files_directory = "text_files"
if os.path.exists(text_files_directory):
    text_files = [f for f in os.listdir(text_files_directory) if f.endswith('.txt')]
    for text_file in text_files:
        file_path = os.path.join(text_files_directory, text_file)
        content = load_text_from_file(file_path)
        if content and len(content.strip()) > 10:  # Solo procesar si tiene contenido significativo
            chunks = split_text_into_chunks(content)
            file_metadata = [{"source": text_file, "file_path": file_path} for _ in chunks]
            add_texts_to_collection(chunks, metadata=file_metadata)
            print(f"Procesado archivo: {text_file}")

# Ejemplos de búsqueda
print("\n=== EJEMPLOS DE BÚSQUEDA ===")

# Buscar textos similares
query_1 = "¿Qué es una base de datos vectorial?"
print(f"\nBúsqueda para: '{query_1}'")
results_1 = search_similar_texts(query_1)

for i, result in enumerate(results_1, 1):
    print(f"\n{i}. Score: {result.score:.4f}")
    print(f"   Texto: {result.payload['text'][:100]}...")
    print(f"   Metadata: {result.payload.get('source', 'N/A')}")

query_2 = "¿Donde está Bilbao?"
print(f"\nBúsqueda para: '{query_2}'")
results_2 = search_similar_texts(query_2)

for i, result in enumerate(results_2, 1):
	print(f"\n{i}. Score: {result.score:.4f}")
	print(f"   Texto: {result.payload['text'][:100]}...")
	print(f"   Metadata: {result.payload.get('source', 'N/A')}")




# Búsqueda con filtros
print(f"\n=== BÚSQUEDA CON FILTROS ===")
filter_search = client.query_points(
    collection_name="text_collection",
    query=encoder.encode([query_1])[0].tolist(),
    query_filter=Filter(
        must=[FieldCondition(key="topic", match=MatchValue(value="database"))]
    ),
    with_payload=True,
    limit=3,
).points

print(f"Búsqueda filtrada por topic='database':")
for i, result in enumerate(filter_search, 1):
    print(f"{i}. {result.payload['text'][:100]}...")

print("\n=== FUNCIÓN PARA AÑADIR NUEVOS TEXTOS ===")
print("Para añadir nuevos textos, usa:")
print("add_texts_to_collection(['tu texto aquí'], metadata=[{'source': 'manual'}])")

print("\n=== FUNCIÓN PARA BUSCAR ===")
print("Para buscar textos similares, usa:")
print("results = search_similar_texts('tu consulta aquí')")
