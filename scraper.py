import requests
from bs4 import BeautifulSoup

def get_embed_link(url):
    try:
        # Website ko request bhejna
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return "No embed link found"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # AnimeSalt par aksar video link 'iframe' tag mein hota hai
        # Tu apne browser mein F12 daba kar check kar ki video link kahan hai
        iframe = soup.find('iframe')
        
        if iframe and 'src' in iframe.attrs:
            return iframe['src'] # Ye tera streaming link hoga
            
        return "No embed link found"
    except Exception:
        return "No embed link found"
