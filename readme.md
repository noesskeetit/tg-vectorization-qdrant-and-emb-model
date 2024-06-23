
# HLD
![HLD](/img/HLD.png)

# Запуск qdrant

````
docker run -p 6333:6333 -p 6334:6334 -v C:/Users/alex/IdeaProjects/tg-vectorization-qdrant/qdrant_storage/qdrant_storage:/qdrant/storage qdrant/qdrant
````
````
sudo docker run -d -p 6333:6333 -e QDRANT__SERVICE__API_KEY='********' -p 6334:6334 -v /u01/qdrant:/qdrant/storage qdrant/qdrant 
````

# Создание коллекции
````
PUT /collections/messages
{
    "vectors": {
    "size": 384,
    "distance": "Cosine",
    "on_disk": true
    }
}
````


# Удаление коллекции
````
DELETE /collections/messages
````
