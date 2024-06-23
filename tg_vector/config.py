import os

from qdrant_client.http.models import Distance

QDRANT_DISTANCE = Distance.DOT

QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_COLLECTION_NAME = os.environ["QDRANT_COLLECTION_NAME"]
QDRANT_VECTOR_SIZE = os.environ["QDRANT_VECTOR_SIZE"]

RMQ_CONN_STR = os.environ["RMQ_CONN_STR"]
RMQ_QUEUE = os.environ["RMQ_QUEUE"]
RMQ_USERNAME = os.environ["RMQ_USERNAME"]
RMQ_PASSWORD = os.environ["RMQ_PASSWORD"]
SEARCH_LIMIT = os.environ["SEARCH_LIMIT"]

MODEL_PATH = os.environ["MODEL_PATH"]