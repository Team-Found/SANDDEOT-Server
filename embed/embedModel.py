from sentence_transformers import SentenceTransformer
import numpy as np
import json
import io

model = SentenceTransformer("sentence-transformers/LaBSE")


#target = 검색내용
#source = DB에 준비된 Data
#ranged = 검색내용 갯수
async def embedModel(target, source,ranged):
  ebData = []
  targetEb = model.encode(target)
  for index,(rssID, titleEb, descriptEb) in enumerate(source):
    titleEb = np.frombuffer(io.BytesIO(titleEb).getvalue(), dtype=np.float32)
    descriptEb = np.frombuffer(io.BytesIO(descriptEb).getvalue(), dtype=np.float32)
    ebData.append([rssID, float(np.inner(targetEb, titleEb))+ float(np.inner(targetEb, descriptEb))])
  return json.dumps(sorted(ebData, key=lambda x: x[0])[:ranged])