import feedparser

from domain import findDomain

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


def findThumbnail(entry):
  thumbnail_url = None
  
  if 'media_thumbnail' in entry:
      thumbnail_url = entry.media_thumbnail[0]['url']
  
  elif 'media_content' in entry:
      for media in entry.media_content:
          if 'image' in media['type']:
              thumbnail_url = media['url']
              break
  
  elif 'links' in entry:
      for link in entry.links:
          if link.rel == 'enclosure' and 'image' in link.type:
              thumbnail_url = link.href
              break

  elif 'image' in entry:
      thumbnail_url = entry.image.get('url') or entry.image.get('href')

  return thumbnail_url


for index, (siteName, url) in enumerate(target_feeds.items()):
    rss_url = url
    print(findDomain(rss_url)+'favicon.ico')
  
'''
    feed = feedparser.parse(rss_url)
    print(rss_url+'/favicon.ico');
    # print(feed.feed.image) #파비콘 추출
    print(feed.feed.title) #사이트 이름 추출
    # print(feed.entries[1].enclosures

    for entry in feed.entries:
        print("Title:", entry.title) #글이름
        print(entry.media_thumbnail)
        # print(entry.content)
        # print(findThumbnail(entry))
        print(entry.link) #글 주소
        print()
    
      # print(entry.id)
      # try:
      #   print("Published:", entry.published)
      # except:
      #   None

    #   # print(entry.description)
    #   # print("Content:", entry.content)
'''