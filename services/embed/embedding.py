from sentence_transformers import SentenceTransformer
import numpy as np
import io

model = None

import asyncio

def get_model():
  global model
  if model is None:
      model = SentenceTransformer("sentence-transformers/LaBSE")  # 모델을 여기서 로드
  return model

async def embedding(text):
  return get_model().encode(text)

async def blobToNumpy(blob):
  if type(blob) == "<class 'bytes'>":
    return blob
  return np.frombuffer(io.BytesIO(blob).getvalue(), dtype=np.float32)

async def similarity(text,text2):
  return float(np.inner(text,text2))