def findThumbnail(entry):
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

    return None