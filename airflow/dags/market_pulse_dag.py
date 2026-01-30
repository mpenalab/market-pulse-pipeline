from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
from pymongo import MongoClient

# --- TAREA 1: INGESTIÓN ---
def run_ingestion():
    API_URL = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum',
        'vs_currencies': 'usd',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true'
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    
    client = MongoClient("mongodb://admin:password123@mongodb:27017/")
    db = client['market_pulse']
    data['created_at'] = datetime.now()
    db['raw_prices'].insert_one(data)
    print("✅ Ingestión RAW completada.")

# --- TAREA 2: TRANSFORMACIÓN ---
def run_transformation():
    client = MongoClient("mongodb://admin:password123@mongodb:27017/")
    db = client['market_pulse']
    
    # Extraer el último
    last_entry = db['raw_prices'].find().sort("created_at", -1).limit(1)[0]
    extraction_date = last_entry.get('created_at')
    
    # Limpiar con Pandas
    price_data = {k: v for k, v in last_entry.items() if k not in ['_id', 'created_at']}
    df = pd.DataFrame(price_data).T.reset_index().rename(columns={'index': 'coin'})
    df['extraction_date'] = extraction_date
    
    # Cargar a la nueva colección
    db['cleansed_prices'].insert_many(df.to_dict('records'))
    print(f"✨ Transformación y Carga de {len(df)} registros completada.")

# --- CONFIGURACIÓN DEL DAG ---
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'market_pulse_pipeline_v2',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False
) as dag:

    ingest_task = PythonOperator(
        task_id='ingest_raw_data',
        python_callable=run_ingestion,
    )

    transform_task = PythonOperator(
        task_id='transform_and_load_clean_data',
        python_callable=run_transformation,
    )

    # ESTABLECER LA DEPENDENCIA (El flujo de trabajo)
    ingest_task >> transform_task