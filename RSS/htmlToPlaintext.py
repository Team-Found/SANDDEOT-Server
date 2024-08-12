from bs4 import BeautifulSoup

import asyncio

async def htmlToPlaintext(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    plaintext = soup.get_text()
    
    return plaintext

