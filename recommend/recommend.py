import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from embed.embedding import similarity, blobToNumpy
from embed.embedModel import embedModel

async def recommend(data, db, quantity):
  ebData = []
  exclude = []
  for index, articleID in enumerate(data):
    result = db.execute("""SELECT titleEb, descriptEb FROM article WHERE articleID = ?""",[articleID]).fetchone()
    ebData.append([articleID, result[0], result[1], 0])
    exclude.append(articleID)

  sumSimilar = 0

  titleEbList = []
  descriptEbList = []

  for index, (rssID, titleEb, descriptEb, weight) in enumerate(ebData):
    titleEbList.append(await blobToNumpy(titleEb))
    descriptEbList.append(await blobToNumpy(descriptEb))
    ebData[index].insert(4, index)
    del ebData[index][1]
    del ebData[index][1]

  for index, (rssID, weight, reference) in enumerate(ebData):
    for index2, (rssID2, weight2, reference2) in enumerate(ebData):
      if index != index2:
        recommend = await similarity(titleEbList[index],titleEbList[index2]) + await similarity(descriptEbList[index],descriptEbList[index2])
        sumSimilar += recommend
        ebData[index][1] += recommend
        ebData[index2][1] += recommend

  # 관계유사도 순으로 정렬 *관계유사도 : 각 데이터끼리 유사도를 돌린 각각의 합
  settingData = db.execute("""select articleID, titleEb, descriptEb from article""").fetchall()
  
  reference = ebData[0][2]

  ebData = sorted(ebData, key=lambda x: x[1],reverse=True)

  return await embedModel(db,titleEbList[reference],settingData,quantity,descriptEbList[reference], exclude=exclude)

  # return embedModel(titleEbList(ebData[0][2]))
  # for i in range(len(ebData)):
  #   ranged = int((ebData[i][2]/sumSimilar)*100) #관계유사도에 따른 피드수 
  #    ranged *= (len(ebData) - i) #가중치
  #   embedModel(ebData[i][1],settingData,ranged)

#TODO: 비율로 처리해야함
#      저장됨 가중치
#      % 이하 search X