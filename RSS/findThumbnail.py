from bs4 import BeautifulSoup

def findImgList(siteName, entry):
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