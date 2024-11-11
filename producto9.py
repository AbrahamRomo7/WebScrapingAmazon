import requests
from bs4 import BeautifulSoup
import time

url = "https://www.amazon.com/-/es/Oster-HeatSoft-Mezclador-talla-%C3%BAnica/dp/B07FMHHRWJ"
headers = {
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

attempts = 0
max_attempts = 6

while attempts < max_attempts:
    try:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        
        # Obtener el título
        title = soup.find('span', {'id': 'productTitle'}).text.strip()
        
        # Obtener la calificación de estrellas
        rating = soup.find('span', {'id': 'acrPopover'})['title']
        
        # Obtener el precio
        price = soup.find("span",{"class":"a-price"}).find("span").text
        
        # Mostrar resultados y salir del bucle
        print("Título:", title)
        print("Calificación:", rating)
        print("Precio:", price)
        break
    except (AttributeError, TypeError):
        attempts += 1
        print(f"Intento {attempts}: Ocurrió un error. Reintentando...")
        time.sleep(2)  # Espera de 2 segundos entre intentos
else:
    print("No se pudo obtener la información después de 6 intentos.")
