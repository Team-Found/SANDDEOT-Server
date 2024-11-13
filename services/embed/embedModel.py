from services.embed.embedding import similarity, blobToNumpy, embedding
import json

#targetEb = 검색내용 (이미 임베딩된)
#source = DB에 준비된 Data
#ranged = 검색내용 갯수

#타겟Eb와 유사한 range개의 값을 반환하는 함수
async def embedModel(db, targetEb, source, ranged, targetDescriptEb = None, accuracy = 0, exclude = []):
  if targetDescriptEb is None: targetDescriptEb = targetEb

  ebData = []
  for index,(articleID, titleEb, descriptEb) in enumerate(source):
    if articleID in exclude:
      continue
    titleEb = await blobToNumpy(titleEb)
    descriptEb = await blobToNumpy(descriptEb)

    resultEb = await similarity(targetEb, titleEb) + await similarity(targetDescriptEb, descriptEb)

    if resultEb >= accuracy*2:
      ebData.append([articleID, resultEb])
  result = sorted(ebData, key=lambda x: x[1],reverse=True)[:ranged]

  articleData = db.execute(f"""select  r.rssID, r.rssName, rssUrl, favicon, articleID ,title, descript, date, thumbnail, imgList, content, link 
                from article a, rss r where articleID in ({','.join(map(str,[item[0] for item in result]))}) and r.rssID = a.rssID""")
  articles_json_list = []
  for article in articleData:
    rssID, rssName, rssUrl, favicon, articleID, title, descript, date, thumbnail, imgList, content, articleUrl = article

    imgList = json.loads(imgList)

    article_data = {
        "rssID": rssID,
        "rssName": rssName,
        "rssUrl": rssUrl,
        "favicon": favicon,
        "articleID": articleID,
        "title": title,
        "descript": descript,
        "date": date,
        "thumbnail": thumbnail,
        "imgList": imgList,
        "content": content,
        "articleUrl": articleUrl
    }
    # JSON 리스트에 추가
    articles_json_list.append(article_data)


  return articles_json_list