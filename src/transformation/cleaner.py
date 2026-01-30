import pandas as pd
from pymongo import MongoClient
from datetime import datetime

def transform_data():
    try:
        # 1. Conexión a la base de datos
        client = MongoClient("mongodb://admin:password123@localhost:27017/")
        db = client['market_pulse']
        raw_col = db['raw_prices']
        clean_col = db['cleansed_prices']

        # 2. Extraer el último documento insertado
        last_entry = raw_col.find().sort("created_at", -1).limit(1)[0]
        extraction_date = last_entry.get('created_at')

        # 3. Transformación con Pandas
        # Eliminamos campos que no son de precios para procesar el resto
        price_data = {k: v for k, v in last_entry.items() if k not in ['_id', 'created_at']}
        
        # Convertimos a DataFrame y "limpiamos"
        df = pd.DataFrame(price_data).T # Transponemos para que las monedas sean filas
        df = df.reset_index().rename(columns={'index': 'coin'})
        
        # Añadimos la metadata de tiempo
        df['extraction_date'] = extraction_date
        
        # 4. Carga (Load) a la nueva colección
        # Convertimos el DataFrame a una lista de diccionarios para MongoDB
        clean_records = df.to_dict('records')
        clean_col.insert_many(clean_records)
        
        print(f"✨ Transformación completada. {len(clean_records)} registros procesados.")
        print(df.head()) # Ver una muestra en consola

    except Exception as e:
        print(f"❌ Error en la transformación: {e}")

if __name__ == "__main__":
    transform_data()