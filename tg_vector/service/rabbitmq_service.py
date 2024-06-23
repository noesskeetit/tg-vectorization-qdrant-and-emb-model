import json
import uuid
import pika
from qdrant_client.http.models import PointStruct
from tg_vector.service import qdrant_service
from tg_vector.service.emb_model_service import get_vector
from tg_vector.config import *


def on_message(channel, method_frame, properties, body):
    try:
        # print("Received message:")
        message = json.loads(body.decode('utf-8'))
        # print("Message ID:", message['message_id'])
        # print("Message:", message['message'])
        # print("Chat ID:", message['chat_id'])

        vector = get_vector(message['message'])

        qdrant_service.update_collection(QDRANT_COLLECTION_NAME, points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "chatId": message['chat_id'],
                    "messageId": message['message_id'],
                    "messages": message['message']})])
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    except Exception as e:
        print("error on_message", e)
        print(e)


def start_consuming():
    rmq_parameters = pika.ConnectionParameters(host=RMQ_CONN_STR,
                                               credentials=pika.PlainCredentials(username=RMQ_USERNAME,
                                                                                 password=RMQ_PASSWORD))
    rmq_connection = pika.BlockingConnection(rmq_parameters)
    rmq_channel = rmq_connection.channel()
    rmq_channel.basic_consume(RMQ_QUEUE, on_message, auto_ack=False)
    rmq_channel.start_consuming()
    print('rabbit_mq service started')
