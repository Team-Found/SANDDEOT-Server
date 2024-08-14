import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from embed.embedding import similarity, blobToNumpy

async def recommend(data, db, quantity):
  ebData = []
  for index, rssID in enumerate(data):
    result = db.execute("""SELECT titleEb, descriptEb FROM article WHERE articleID = ?""",[rssID]).fetchone()
    ebData.append([rssID, result[0], result[1], 0])

  for index, (rssID, titleEb, descriptEb, weight) in enumerate(ebData):
    for index2, (rssID2, titleEb2, descriptEb2, weight2) in enumerate(ebData):
      if index != index2:
        titleEb = await blobToNumpy(titleEb)
        titleEb2 = await blobToNumpy(titleEb2)
        descriptEb = await blobToNumpy(descriptEb)
        descriptEb2 = await blobToNumpy(descriptEb2)

        recommend = await similarity(titleEb,titleEb2) + await similarity(descriptEb,descriptEb2)
        ebData[index][3] += recommend
        ebData[index2][3] += recommend
  for i in range(len(ebData)):
    del ebData[i][1]
    del ebData[i][1]
  return sorted(ebData, key=lambda x: x[0],reverse=True)

#descript없으면 오류나는 거 고쳐야함