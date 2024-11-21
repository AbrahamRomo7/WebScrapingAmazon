import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import schedule
import time

# Configuración de MongoDB
client = MongoClient("mongodb+srv://Dev-User:Udla-Tita@cluster0.t7vkm.mongodb.net/")  # Cambia la URI si usas MongoDB Atlas
db = client['web']  # Nombre de la base de datos
collection = db['tesis']  # Nombre de la colección

# Configuración de scraping
url = "https://www.amazon.com/Rechargeable-Operated-Magnetic-Dimmable-Wireless/dp/B0BDF8CVBN/143-3200881-3752903?pd_rd_w=ap8b3&content-id=amzn1.sym.31346ea4-6dbc-4ac4-b4f3-cbf5f8cab4b9&pf_rd_p=31346ea4-6dbc-4ac4-b4f3-cbf5f8cab4b9&pf_rd_r=W7BTBBMS7T9J6WBYFF1J&pd_rd_wg=glxNz&pd_rd_r=312b74d2-0a2a-4fe3-93c0-980e6e7c9f00&pd_rd_i=B0BDF8CVBN&th=1"
headers = {
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

def scrape_and_store():
    try:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Obtener el título
        title = soup.find('span', {'id': 'productTitle'}).text.strip()

        # Obtener la calificación de estrellas y truncar a los primeros 3 caracteres
        rating = soup.find('span', {'id': 'acrPopover'})['title'][:3]

        # Obtener el precio y eliminar el signo de $ y el prefijo 'US'
        price = soup.find("span", {"class": "a-price"}).find("span").text.replace('US', '').replace('$', '').strip()


        # Registrar la fecha y hora de la ejecución
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Guardar resultados en MongoDB
        product_data = {
            "producto_id": 4,
            "title": title,
            "rating": rating,
            "price": price,
            "url": url,
            "timestamp": timestamp
        }

        collection.insert_one(product_data)

        print("Ejecución exitosa: Datos guardados en MongoDB")
        print("Título:", title)
        print("Calificación:", rating)
        print("Precio:", price)
        print("Fecha y hora:", timestamp)

    except Exception as e:
        print("Ocurrió un error:", str(e))

# Programar las ejecuciones
schedule.every().day.at("08:00").do(scrape_and_store)
schedule.every().day.at("20:00").do(scrape_and_store)

if __name__ == "__main__":
    print("Iniciando programador...")
    while True:
        schedule.run_pending()
        time.sleep(1)
