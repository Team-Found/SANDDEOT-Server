from sentence_transformers import SentenceTransformer
import numpy as np
import json

model = SentenceTransformer("sentence-transformers/LaBSE")

#target = 검색내용
#source = DB에 준비된 Data
#ranged = 검색내용 갯수
async def embedModel(target, source,ranged):
  ebData = []
  targetEb = model.encode(target)
  for (rssID, titleEb, descriptEb) in enumerate(source):
    ebData.append([rssID, float(np.inner(targetEb, titleEb))+ float(np.inner(targetEb, descriptEb))])
  return json.dumps(sorted(ebData, key=lambda x: x[0])[:ranged], indent=4)