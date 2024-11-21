import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

# Configuración de MongoDB
client = MongoClient("mongodb+srv://Dev-User:Udla-Tita@cluster0.t7vkm.mongodb.net/")  # Cambia la URI si usas MongoDB Atlas
db = client['web']  # Nombre de la base de datos
collection = db['tesis']  # Nombre de la colección

# Configuración de scraping
url = "https://www.amazon.com/dp/B0CLM7YW6C?ref_=cm_sw_r_apin_ct_ET4TVJV9PZSERTYFTCXW_3&language=en_US&th=1"
headers = {
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

def scrape_and_store():
    attempts = 0
    max_attempts = 6

    while attempts < max_attempts:
        try:
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Obtener el título
            title = soup.find('span', {'id': 'productTitle'}).text.strip()

            # Obtener la calificación de estrellas y truncar a los primeros 3 caracteres
            rating = soup.find('span', {'id': 'acrPopover'})['title'][:3]

            # Obtener el precio y eliminar el signo de $
            price = soup.find("span", {"class": "a-price"}).find("span").text.replace('$', '')

            # Registrar la fecha y hora de la ejecución
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Guardar resultados en MongoDB
            product_data = {
                "producto_id": 7,  # Identificador para el mismo producto
                "title": title,
                "rating": rating,
                "price": price,
                "url": url,
                "timestamp": timestamp  # Fecha y hora de la ejecución
            }

            collection.insert_one(product_data)

            print("Ejecución exitosa: Datos guardados en MongoDB")
            print("Título:", title)
            print("Calificación:", rating)
            print("Precio:", price)
            print("Fecha y hora:", timestamp)
            return True  # Indica que la ejecución fue exitosa
        except (AttributeError, TypeError):
            attempts += 1
            print(f"Intento {attempts}: Ocurrió un error. Reintentando...")

    print("No se pudo obtener la información después de 6 intentos.")
    return False  # Indica que la ejecución falló

if __name__ == "__main__":
    max_executions = 6  # Número máximo de ejecuciones permitidas

    for execution_count in range(1, max_executions + 1):
        print(f"Iniciando ejecución {execution_count} de {max_executions}")
        success = scrape_and_store()
        if success:
            print("Ejecución completada con éxito. Terminando el programa.")
            break  # Detiene el programa si una ejecución es exitosa
