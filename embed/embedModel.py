from embed.embedding import similarity, blobToNumpy, embedding
import json

#targetEb = 검색내용 (이미 임베딩된)
#source = DB에 준비된 Data
#ranged = 검색내용 갯수
async def embedModel(db, targetEb, source, ranged, targetDescriptEb = None):
  if targetDescriptEb is None:
    targetDescriptEb = targetEb

  ebData = []
  # targetEb = await embedding(target)
  for index,(rssID, titleEb, descriptEb) in enumerate(source):
    titleEb = await blobToNumpy(titleEb)
    descriptEb = await blobToNumpy(descriptEb)
    ebData.append([rssID, await similarity(targetEb, titleEb) + await similarity(targetDescriptEb, descriptEb)])
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


  return json.dumps(articles_json_list)