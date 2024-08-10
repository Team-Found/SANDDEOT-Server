import feedparser

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
  print(feed.feed.title, siteName)

  for entry in feed.entries:
      print("Title:", entry.title)
      print("Link:", entry.link)

      try:
        print("Published:", entry.published)
      except:
        None
      
      print("Summary:", entry.summary)
      # print("Content:", entry.content)
      print()