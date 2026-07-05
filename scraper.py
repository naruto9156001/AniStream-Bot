import requests
from bs4 import BeautifulSoup

def get_embed_link(episode_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    try:
        # Anime Salt ke page ko request bhej rahe hain
        response = requests.get(episode_url, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 'responsiveIframe' ID wale iframe ko target kar rahe hain
        iframe = soup.find('iframe', id='responsiveIframe')
        
        if iframe and 'src' in iframe.attrs:
            return iframe['src']
        else:
            return "No embed link found"
            
    except Exception as e:
        print(f"Error aagaya bhai scraping mein: {e}")
        return None
