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
url = "https://www.amazon.com/Adapter-Braided-Charging-Converter-Universal/dp/B0989JNGD7?crid=25QWEQ8JFSG41&dib=eyJ2IjoiMSJ9.cmr01SbQzsTGj1zE79Jz1N47Urygy-IdMPP2CsLC2lcAyMEAWi40B3bkLT-d5sYpi7pEPPZ_lAGB2Soz13EoAuDcF_WoL_Ba5FP-XpnS_5JGvmNNtUVofP2BNYIHa3H2OKT7ZGw5jf8R0yDrW4WCxSL8qgRCNZD5ZzFMuFG0DIx8H7yHdKhtdgLCDf0nJfy9wZL9eC0zDotTHsCxvzyVS3gv9IQ4QLXMtrn-T7Kb-28.15xIEc1ebFXTdV7WKDRrlxA9bLqInA5fFe3rGUuRUks&dib_tag=se&keywords=adapter+ups&qid=1732151388&sprefix=adapter+u%2Caps%2C303&sr=8-18"
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
            "producto_id": 13,
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

