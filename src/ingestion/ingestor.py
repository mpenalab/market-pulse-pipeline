import requests
import json
import os
from datetime import datetime

def save_to_json(data):
    # Crear la estructura de carpetas: data/raw/
    folder_path = os.path.join('data', 'raw')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📁 Carpeta creada: {folder_path}")

    # Nombre de archivo con timestamp (ej: 20240520_153005_market_data.json)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_market_data.json"
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"💾 Datos guardados en: {file_path}")

def fetch_market_data():
    API_URL = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum',
        'vs_currencies': 'usd',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true'
    }

    try:
        print("🚀 Iniciando extracción de datos...")
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print("✅ Datos recibidos con éxito.")
        
        # Guardar los datos en local
        save_to_json(data)
        
        return data

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_market_data()