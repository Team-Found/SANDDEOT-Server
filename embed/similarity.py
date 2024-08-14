from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/LaBSE")

async def similarity(text,text2):
  return float(np.inner(text,text2))