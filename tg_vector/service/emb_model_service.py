from sentence_transformers import SentenceTransformer
from typing import List
from transformers import AutoTokenizer

from tg_vector.config import MODEL_PATH

model = SentenceTransformer(MODEL_PATH)
print("Максимальная длина входной последовательности:",
      AutoTokenizer.from_pretrained(MODEL_PATH).model_max_length)


def get_vector(message: str) -> List[float]:
    # message = 'query: ' + message
    embeddings = model.encode(message, convert_to_tensor=False, normalize_embeddings=True)

    return embeddings.tolist()