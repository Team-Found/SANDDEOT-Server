from embed.embedding import similarity, blobToNumpy, embedding
import json

#target = 검색내용
#source = DB에 준비된 Data
#ranged = 검색내용 갯수
async def embedModel(target, source,ranged):
  ebData = []
  targetEb = await embedding(target)
  for index,(rssID, titleEb, descriptEb) in enumerate(source):
    titleEb = await blobToNumpy(titleEb)
    descriptEb = await blobToNumpy(descriptEb)
    ebData.append([rssID, await similarity(targetEb, titleEb) + await similarity(targetEb, descriptEb)])
  return sorted(ebData, key=lambda x: x[1],reverse=True)[:ranged]