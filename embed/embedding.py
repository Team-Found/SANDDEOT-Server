from sentence_transformers import SentenceTransformer
import numpy as np
import io

model = SentenceTransformer("sentence-transformers/LaBSE")

import asyncio

async def embedding(text):
  return (model.encode(text))

async def blobToNumpy(blob):
  if type(blob) == "<class 'bytes'>":
    return blob
  return np.frombuffer(io.BytesIO(blob).getvalue(), dtype=np.float32)

async def similarity(text,text2):
  return float(np.inner(text,text2))