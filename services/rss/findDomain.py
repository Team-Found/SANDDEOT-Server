import re
import asyncio

# 도메인만 깔끔히 추출하는 함수
async def findDomain(url):
    pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None
