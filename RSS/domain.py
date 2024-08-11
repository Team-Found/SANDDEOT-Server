# 도메인만 깔끔히 추출하는 함수
def findDomain(rss_url):
    header = rss_url[0:rss_url.index('.')]
    domain = rss_url[rss_url.index('.'):len(rss_url)]
    domain = domain[0:domain.index('/')]

    return (header+domain+'/')