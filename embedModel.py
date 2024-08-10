from sentence_transformers import SentenceTransformer
import numpy as np
sentences = ["car", "오토바이"]

model = SentenceTransformer('sentence-transformers/LaBSE')
embeddings = model.encode(sentences)
print(embeddings)

print(np.inner(embeddings[0],embeddings[1]))