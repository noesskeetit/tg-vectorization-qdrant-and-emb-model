from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Filter, FieldCondition, MatchAny

from ..config import *

_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


def create_collection(collection_name, distance, size_of_vectors):
    _client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=size_of_vectors, distance=distance))


def get_collection_info(collection_name):
    info = _client.get_collection(
        collection_name=collection_name)

    return info


def update_collection(collection_name, points):
    operation_info = _client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points,
    )

    if operation_info.status != "completed":
        raise Exception("Обновление коллекции не завершено")

    print(f"Коллекция с именем {collection_name} обновлена. Добавлена следующая информация: {', '.join(str(point) for point in points)}")


def search_similar_vectors(collection_name, points_of_vector, list_chat_id):
    similar_vectors = _client.search(
        collection_name=collection_name,
        query_vector=points_of_vector,
        with_payload=True,
        query_filter=Filter(
            must=[FieldCondition(key="chatId", match=MatchAny(any=list_chat_id))]
        ),
        limit=SEARCH_LIMIT,
    )

    print("Найдены векторы:")
    for scored_point in similar_vectors:
        print(f"ID: {scored_point.id}, Version: {scored_point.version}, Score: {scored_point.score}, Payload: {scored_point.payload}")

    return similar_vectors


def delete_collection(collection_name):
    operation_info = _client.delete_collection(
        collection_name=collection_name)

    if operation_info != True:
        raise Exception("Удаление коллекции не завершено успешно")

    print(f"Коллекция с именем {collection_name} удалена.")
