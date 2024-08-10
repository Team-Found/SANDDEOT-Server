from sentence_transformers import SentenceTransformer
import numpy as np

def embedModel(source):
  sentences = ["car", source]

  model = SentenceTransformer('sentence-transformers/LaBSE')
  embeddings = model.encode(sentences)
  print(embeddings)

  predict = np.inner(embeddings[0],embeddings[1])
  print(predict)
  return float(predict)