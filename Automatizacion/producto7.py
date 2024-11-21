import requests
from bs4 import BeautifulSoup
import time
import schedule
from pymongo import MongoClient

# Configuración de MongoDB
client = MongoClient("mongodb://localhost:27017")  # Cambia la URI si usas MongoDB Atlas
db = client['web']  # Nombre de la base de datos
collection = db['tesis']  # Nombre de la colección

# Configuración de scraping
url = "https://www.amazon.com/alimentaci%C3%B3n-universal-ventilador-auriculares-tel%C3%A9fonos/dp/B0CNNRP96W?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1UZFBW0EB1A7R&dib=eyJ2IjoiMSJ9.oBV30HieFqXE__d7sr_cANv7rjsg8TFqIrYAmweFGPT_0FwxdFi4FmdMZl_jcD06_2OFs9btmIFim3oK1jMuZpwUuDtwmZb4zxH2-NGy8bdZcoHFzw6SJVcSDL3dYYW8JYiA7n-Rfra50WlvfSpkdud67TjMc97tw74BAGw_FmluecxY7kl5J-HB4UZl-JbQVXA5soo8cqcHbSjbc4s3xEhBPg3hFkBNnutk8kqoNt4.L_9U1oCYkbCeNUoZJP4PH-cvfwoEA7jkqoSlJCjzbMI&dib_tag=se&keywords=usb%2Bto%2Bdc+12v&qid=1731086660&sprefix=usb%2Bto%2Bdc+12%2Caps%2C230&sr=8-22-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9idGY&psc=1"
headers = {
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

execution_count = 0
max_executions = 3

def scrape_and_store():
    global execution_count

    # Incrementar el contador de ejecuciones
    execution_count += 1

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
            price = soup.find("span", {"class": "a-price"}).find("span").text

            # Guardar resultados en MongoDB sin especificar _id y con producto_id=1
            product_data = {
                "producto_id": 7,  # Identificador para el mismo producto
                "title": title,
                "rating": rating,
                "price": price,
                "url": url
            }

            # Inserta un nuevo documento en la colección sin especificar _id
            collection.insert_one(product_data)

            print(f"Ejecución {execution_count}: Datos guardados en MongoDB")
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

    # Detener el programa después de 3 ejecuciones
    if execution_count >= max_executions:
        print("Se alcanzó el número máximo de ejecuciones. Deteniendo...")
        return schedule.CancelJob

# Programar el scraping cada 2 minutos
schedule.every(2).minutes.do(scrape_and_store)

# Ejecutar el ciclo principal de programación
while execution_count < max_executions:
    schedule.run_pending()
    time.sleep(1)  # Espera un segundo entre chequeos
