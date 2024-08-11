from bs4 import BeautifulSoup

def htmlToPlaintext(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    plaintext = soup.get_text()
    
    return plaintext

