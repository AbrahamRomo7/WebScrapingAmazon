import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.com/-/es/Oster-HeatSoft-Mezclador-talla-%C3%BAnica/dp/B07FMHHRWJ"
headers = {
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')

# Obtener el precio
try:
    price = soup.find("span",{"class":"a-price"}).find("span").text
except (AttributeError, TypeError):
    price = None

print("Precio:", price)
