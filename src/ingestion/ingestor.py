import requests
import json
import os

def fetch_market_data():
    # URL de la API de CoinGecko para obtener el precio de Bitcoin y Ethereum
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
        
        # Verifica si la respuesta fue exitosa (Status 200)
        response.raise_for_status()
        
        data = response.json()
        print("✅ Datos recibidos con éxito:")
        print(json.dumps(data, indent=4))
        
        return data

    except requests.exceptions.HTTPError as err:
        print(f"❌ Error HTTP: {err}")
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. Revisa tu internet.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    fetch_market_data()