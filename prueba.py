import requests
from bs4 import BeautifulSoup
import time

url = "https://www.amazon.com/alimentaci%C3%B3n-universal-ventilador-auriculares-tel%C3%A9fonos/dp/B0CNNRP96W?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1UZFBW0EB1A7R&dib=eyJ2IjoiMSJ9.oBV30HieFqXE__d7sr_cANv7rjsg8TFqIrYAmweFGPT_0FwxdFi4FmdMZl_jcD06_2OFs9btmIFim3oK1jMuZpwUuDtwmZb4zxH2-NGy8bdZcoHFzw6SJVcSDL3dYYW8JYiA7n-Rfra50WlvfSpkdud67TjMc97tw74BAGw_FmluecxY7kl5J-HB4UZl-JbQVXA5soo8cqcHbSjbc4s3xEhBPg3hFkBNnutk8kqoNt4.L_9U1oCYkbCeNUoZJP4PH-cvfwoEA7jkqoSlJCjzbMI&dib_tag=se&keywords=usb%2Bto%2Bdc+12v&qid=1731086660&sprefix=usb%2Bto%2Bdc+12%2Caps%2C230&sr=8-22-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9idGY&psc=1"
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
        
        # Mostrar resultados y salir del bucle
        print("Título:", title)
        print("Calificación:", rating)
        break
    except (AttributeError, TypeError):
        attempts += 1
        print(f"Intento {attempts}: Ocurrió un error. Reintentando...")
        time.sleep(2)  # Espera de 2 segundos entre intentos
else:
    print("No se pudo obtener la información después de 6 intentos.")
