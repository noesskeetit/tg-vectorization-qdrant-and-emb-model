import threading

from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import *
from tg_vector.service import qdrant_service
from tg_vector.service.rabbitmq_service import start_consuming
from tg_vector.service.emb_model_service import get_vector

app = FastAPI(
    title="Server for Bot"
)


class TextInput(BaseModel):
    text: str


class VectorSearchRequest(BaseModel):
    list_chat_id: List[int]
    message: str


@app.post("/get_similar")
async def send_message(request: VectorSearchRequest):
    print("send_message", request)
    vector = get_vector(request.message)
    # {
    #     "id": "0f99ae30-8230-4c3b-968e-1e94fd3240ad",
    #     "version": 12,
    #     "score": 0.44128925,
    #     "payload": {
    #         "chatId": -1002143354525,
    #         "messageId": -1002143354525,
    #         "messages": "ывап\nывап\nfsdfgsdfg\nsdfgsdfg\nПривет. Я сегодня пил персиковый сок"
    #     },
    #     "vector": null,
    #     "shard_key": null
    # }

    result_list = []

    for query_result in qdrant_service.search_similar_vectors(QDRANT_COLLECTION_NAME, vector, request.list_chat_id):
        result = dict()
        result['chatId'] = query_result.payload['chatId']
        result['messageId'] = query_result.payload['messageId']
        result['messages'] = query_result.payload['messages']
        result_list.append(result)

    print("send_message", result_list)
    return result_list


@app.post('/get_embeddings')
def get_embeddings(request: Request, input_data: TextInput):
    try:
        # Вычислить эмбеддинг текста
        print('/get_embeddings', request)
        # Создать словарь для возврата в формате JSON
        response_data = {"embedding": get_vector(input_data.text)}
        # Вернуть JSONResponse с кодом состояния 200 (ОК)
        return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        # В случае ошибки возвращать JSON с кодом состояния 500 (Внутренняя ошибка сервера)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/health")
def health_check():
    return {"status": "ok"}


rmq_thread = threading.Thread(target=start_consuming)
rmq_thread.daemon = True
rmq_thread.start()

uvicorn.run(app, host="0.0.0.0", port=8000)
