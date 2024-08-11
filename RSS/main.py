import feedparser

from domain import findDomain

target_feeds = {
    "Apple": "https://www.apple.com/newsroom/rss-feed.rss",
    "Github Blog": "https://github.blog/feed/",
    # "Billboard": "https://www.billboard.com/feed/",
    # "The New York Times - The Daily": "http://rss.art19.com/the-daily",
    # "Mashable": "http://feeds.mashable.com/mashable",
    # "Lifehacker": "https://lifehacker.com/feed/rss",
    # "Cup of Jo": "https://feeds.feedburner.com/blogspot/bboSV",
    # "Fox News": "https://moxie.foxnews.com/google-publisher/latest.xml",
    # "france24": "https://www.france24.com/en/rss",
    # "TIME": "https://feeds.feedburner.com/time/world",
    # "The Verge": "https://www.theverge.com/rss/frontpage",
    # "kotteke.org": "https://feeds.kottke.org/main",
    # "NPR: National Public Radio": "https://feeds.npr.org/1004/rss.xml",
    # "RT": "https://www.rt.com/rss/news/",
    # "NDTV": "https://feeds.feedburner.com/ndtvnews-world-news",
    # "The Sun": "https://www.thesun.co.uk/news/worldnews/feed/",
    # "The Cipher Brief": "https://www.thecipherbrief.com/feed",
    # "Raw Story": "https://www.rawstory.com/feeds/world.rss",
    # "Daily Research Plot": "https://dailyresearchplot.com/feed/",
    # "The World Association of Newspapers": "https://wan-ifra.org/news/feed/",
    # "Small Wars Journal Blog": "https://smallwarsjournal.com/rss/blogs"
}

from bs4 import BeautifulSoup

def findThumbnail(entry):
    # 1. media_thumbnail에서 썸네일 추출
    if 'media_thumbnail' in entry and entry.media_thumbnail:
        return entry.media_thumbnail[0].get('url')
    
    # 2. media_content에서 썸네일 추출
    if 'media_content' in entry:
        for media in entry.media_content:
            if media.get('type') and 'image' in media['type']:
                return media.get('url')
    
    # 3. links에서 썸네일 추출
    if 'links' in entry:
        for link in entry.links:
            if link.rel == 'enclosure' and 'image' in link.type:
                return link.get('href')
    
    # 4. image에서 썸네일 추출
    if 'image' in entry:
        return entry.image.get('url') or entry.image.get('href')
    
    # 5. content에서 첫 번째 이미지 태그의 src 속성 추출
    if 'content' in entry:
        soup = BeautifulSoup(entry.content[0].value, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']
    
    return None


for index, (siteName, url) in enumerate(target_feeds.items()):
    rss_url = url
    feed = feedparser.parse(rss_url)

    #파비콘을 추출하는 코드
    if 'image' in feed.feed:
      print(feed.feed.image.href)
    else:
      print(findDomain(rss_url)+'favicon.ico')

    #사이트 이름 추출
    print(feed.feed.title)

    for entry in feed.entries:
        print("Title:", entry.title) #글이름
        print(entry.link) #글 주소
        print('썸네일 : ', findThumbnail(entry))
        # print(entry)
        print()
    
      # print(entry.id)
      # try:
      #   print("Published:", entry.published)
      # except:
      #   None

    #   # print(entry.description)
    #   # print("Content:", entry.content)
