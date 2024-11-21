import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

# Configuración de MongoDB
client = MongoClient("mongodb+srv://Dev-User:Udla-Tita@cluster0.t7vkm.mongodb.net/")  # Cambia la URI si usas MongoDB Atlas
db = client['web']  # Nombre de la base de datos
collection = db['tesis']  # Nombre de la colección

# Configuración de scraping
url = "https://www.amazon.com/-/es/GOBOBIOK-27000mAh-PowerBank-integrados-inteligente/dp/B0DG5K883J?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=15GYF4N7SWX8V&dib=eyJ2IjoiMSJ9.4x0hqbM2Km6obnsLR36SURVGmgxhkg65n0xcskojy4eEJFEcNeiTFTz72y4wwVVeh3YTznDOgF1gG25i4xHGxhmVU52-qx6mKJimz7YikWOMujtEG1wcnY7zbeIUaBLHmXk4GsOoA2tuQ8UvdZgmBSNM1zIKqZtWx2jki6Wvdwxw2NnejgY9cbdQYUfb1TSnV-szfvpF14DgPgMN5CnTmuZO63uO2TyMcC54zWrhPJs.VbS9vqr4vVubogmfzNa9q9VWNGKmmU4xxdVACFi6j34&dib_tag=se&keywords=power+bank+para+router&qid=1731081159&sprefix=power+bank+para+router%2Caps%2C157&sr=8-3"
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

            # Obtener el precio y eliminar el signo de $ y el prefijo 'US'
            price = soup.find("span", {"class": "a-price"}).find("span").text.replace('US', '').replace('$', '').strip()


            # Registrar la fecha y hora de la ejecución
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Guardar resultados en MongoDB
            product_data = {
                "producto_id": 3,  # Identificador para el mismo producto
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
