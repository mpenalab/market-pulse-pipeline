# 🚀 Market Pulse: Data Engineering Pipeline

## 📝 Descripción del Proyecto
Este es un proyecto de simulación laboral enfocado en la ingeniería de datos. El objetivo es construir un pipeline automatizado que extrae precios de cripto-activos en tiempo real desde APIs públicas (CoinGecko), los almacena en una arquitectura de contenedores y los procesa para su posterior análisis.

## 🏗️ Arquitectura
El sistema utiliza un enfoque de **Data Lake** sencillo:
1. **Ingestión:** Script en Python que consume la API REST.
2. **Landing Zone:** Almacenamiento local en archivos JSON para trazabilidad (Raw Data).
3. **Storage:** Base de Datos NoSQL (**MongoDB**) corriendo en Docker para persistencia estructurada.
4. **Orquestación:** (En proceso...)

## 🛠️ Tecnologías utilizadas
* **Lenguaje:** Python 3.13
* **Base de Datos:** MongoDB
* **Contenedores:** Docker & Docker Compose
* **Entorno Virtual:** Conda / venv

## 🚀 Cómo ejecutar el proyecto

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/market-pulse-pipeline.git](https://github.com/TU_USUARIO/market-pulse-pipeline.git)
cd market-pulse-pipeline
```
### 2. Configurar el entorno virtual
```bash
# Si usas Conda
conda activate market-pulse
# O si usas venv
.\venv\Scripts\activate
```
### 3. Levantar la infraestructura (Docker)
Este comando iniciará MongoDB y la interfaz visual Mongo Express:
```bash
docker-compose up -d
```
### 4. Ejecutar el Ingestor
```bash
python src/ingestion/ingestor.py
```
## 📊 Visualización de Datos
* Una vez ejecutado el script, puedes ver los datos en:
* **Mongo Express (Web UI):** http://localhost:8081
* **Credenciales: Usuario:** admin | Contraseña: password123

## 📂 Estructura del Proyecto
* **src/ingestion/:* Scripts de extracción de datos.
* **data/raw/:* Archivos JSON históricos extraídos de la API.
* **docker-compose.yml:* Definición de los servicios de infraestructura.