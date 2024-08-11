from bs4 import BeautifulSoup
from githubImg import findGithubThumbnail
from findThumbnail import findThumbnail

def findImgList(siteName, entry):
    if siteName == 'The GitHub Blog': #github-blog만 특별히 썸네일 추출
        thumbnail = findGithubThumbnail(entry.link)
    else:
        thumbnail = findThumbnail(entry)
    
    img_srcs = []
    if 'content' in entry:
        soup = BeautifulSoup(entry.content[0].value, 'html.parser')
        img_tags = soup.find_all('img')
        img_srcs = [img['src'] for img in img_tags if 'src' in img.attrs and img['src'] != thumbnail]


    return (thumbnail and [thumbnail] or []) + img_srcs

#배열의 0번째는 썸네일