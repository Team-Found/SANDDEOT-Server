from services.embed.embedding import similarity, blobToNumpy
from services.embed.embedModel import embedModel

async def recommend(data, db, quantity):
  ebData = []
  exclude = []

  titleEbList = []
  descriptEbList = []

  listScale = list(map(lambda x:x[1], data))
  maxScale = max(listScale)
  minScale = min(listScale)
  Normalization = lambda x : (x - minScale)/ ((maxScale - minScale)+0.1)

  for index, (articleID, tos) in enumerate(data): #tos = Time Of Stay
    result = db.execute("""SELECT titleEb, descriptEb FROM article WHERE articleID = ?""",[articleID]).fetchone()
    titleEbList.append(await blobToNumpy(result[0]))
    descriptEbList.append(await blobToNumpy(result[1]))
    print(Normalization(tos))
    ebData.append([articleID, Normalization(tos), index])
    exclude.append(articleID)
  
  sumSimilar = 0


  for index, (articleID, weight, reference) in enumerate(ebData):
    for index2, (articleID2, weight2, reference2) in enumerate(ebData):
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