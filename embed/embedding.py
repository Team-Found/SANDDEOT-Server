from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/LaBSE")

def embedding(text):
  return model.encode(text)