import requests
from bs4 import BeautifulSoup

#github-blog에서 썸네일을 추출하는 코드
def findGithubThumbnail(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    element = soup.find(id='start-of-content')
    if element:
        element = element.find('img')

        if element and 'src' in element.attrs:
            return element['src']
        else:
            return None

    else:
        return None