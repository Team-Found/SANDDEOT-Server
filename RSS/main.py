import feedparser
from bs4 import BeautifulSoup
from domain import findDomain
from githubImg import findGithubThumbnail


def findThumbnail(siteName, entry):
    if 'media_thumbnail' in entry and entry.media_thumbnail:
        return entry.media_thumbnail[0].get('url')

    if 'media_content' in entry:
        for media in entry.media_content:
            if media.get('type') and 'image' in media['type']:
                return media.get('url')

    if 'links' in entry:
        for link in entry.links:
            if link.rel == 'enclosure' and 'image' in link.type:
                return link.get('href')

    if 'image' in entry:
        return entry.image.get('url') or entry.image.get('href')

    if 'content' in entry:
        soup = BeautifulSoup(entry.content[0].value, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']

    return None


def htmlToPlaintext(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    plaintext = soup.get_text()
    
    return plaintext


target_feeds = {
    "Apple": "https://www.apple.com/newsroom/rss-feed.rss",
    "Github Blog": "https://github.blog/feed/",
    "Billboard": "https://www.billboard.com/feed/",
    "The New York Times - The Daily": "http://rss.art19.com/the-daily",
    "Mashable": "http://feeds.mashable.com/mashable",
    "Lifehacker": "https://lifehacker.com/feed/rss",
    "Cup of Jo": "https://feeds.feedburner.com/blogspot/bboSV",
    "Fox News": "https://moxie.foxnews.com/google-publisher/latest.xml",
    "france24": "https://www.france24.com/en/rss",
    "TIME": "https://feeds.feedburner.com/time/world",
    "The Verge": "https://www.theverge.com/rss/frontpage",
    "kotteke.org": "https://feeds.kottke.org/main",
    "NPR: National Public Radio": "https://feeds.npr.org/1004/rss.xml",
    "RT": "https://www.rt.com/rss/news/",
    "NDTV": "https://feeds.feedburner.com/ndtvnews-world-news",
    "The Sun": "https://www.thesun.co.uk/news/worldnews/feed/",
    "The Cipher Brief": "https://www.thecipherbrief.com/feed",
    "Raw Story": "https://www.rawstory.com/feeds/world.rss",
    "Daily Research Plot": "https://dailyresearchplot.com/feed/",
    "The World Association of Newspapers": "https://wan-ifra.org/news/feed/",
    "Small Wars Journal Blog": "https://smallwarsjournal.com/rss/blogs"
}


for index, (siteName, url) in enumerate(target_feeds.items()):
    rss_url = url
    feed = feedparser.parse(rss_url)

    # 파비콘을 추출하는 코드
    if 'image' in feed.feed:
      print(feed.feed.image.href)
    else:
      print(findDomain(rss_url)+'favicon.ico')

    # 사이트 이름 추출
    siteName = feed.feed.title
    print('사이트이름' + siteName)

    for entry in feed.entries:
      print(entry.guid) #RSSArticleID
      print("Title:", entry.title) #글이름

      if 'description' in entry:
        description = entry.description
      elif 'summary' in entry:
        description = entry.summary
      print("desc:", htmlToPlaintext(description))


      writingUrl = entry.link #글 링크
      print('글링크' +writingUrl)

      if siteName == 'The GitHub Blog': #github-blog만 특별히 썸네일 추출
        thumbnail = findGithubThumbnail(writingUrl)
      else:
        thumbnail =  findThumbnail(siteName,entry)
      
      published = entry.get('published', 'No publish date found')
      if published == 'No publish date found':
        published_parsed = entry.get('published_parsed', None)
      if published_parsed:
          from time import strftime
          published = strftime('%Y-%m-%d %H:%M:%S', published_parsed)
  
      print("Published Date:", published)
      # try:
      # print("Published:", entry.published)
      # except:
      #   None
      print()

    #   # print(entry.description)
    #   # print("Content:", entry.content)
