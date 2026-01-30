# 🚀 Market Pulse Pipeline

Pipeline automatizado de datos de mercado de criptomonedas construido con **Apache Airflow**, **MongoDB**, y **Python**. Este proyecto extrae datos de precios en tiempo real de criptomonedas, los procesa y los almacena en una base de datos MongoDB para análisis posterior.

## 📋 Descripción

Market Pulse Pipeline es un sistema ETL (Extract, Transform, Load) que:

- **Extrae** datos de precios de criptomonedas (Bitcoin, Ethereum) desde la API de CoinGecko
- **Transforma** los datos usando Pandas para limpiarlos y estructurarlos
- **Carga** los datos procesados en MongoDB para almacenamiento y análisis
- **Automatiza** el proceso completo usando Apache Airflow con ejecución programada cada hora

## 🏗️ Arquitectura

```
┌─────────────────┐
│   CoinGecko API │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Ingestion     │ (raw_prices)
│   Module        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Transformation │ (cleansed_prices)
│   Module        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    MongoDB      │
└─────────────────┘
```

## 🛠️ Stack Tecnológico

- **Orquestación**: Apache Airflow 2.7.1
- **Base de Datos**: MongoDB (última versión)
- **Base de Datos Metadata**: PostgreSQL 13 (para Airflow)
- **Lenguaje**: Python 3.x
- **Procesamiento de Datos**: Pandas
- **API**: CoinGecko API
- **Contenedorización**: Docker & Docker Compose
- **UI de MongoDB**: Mongo Express

## 📁 Estructura del Proyecto

```
market-pulse-pipeline/
│
├── airflow/
│   ├── dags/
│   │   └── market_pulse_dag.py      # DAG principal de Airflow
│   ├── logs/                         # Logs de Airflow
│   ├── plugins/                      # Plugins personalizados
│   └── airflow.cfg                   # Configuración de Airflow
│
├── data/
│   └── raw/                          # Datos JSON guardados localmente
│
├── src/
│   ├── ingestion/
│   │   └── ingestor.py              # Módulo de extracción de datos
│   └── transformation/
│       └── cleaner.py               # Módulo de transformación
│
├── docker-compose.yml               # Configuración de servicios
├── requirements.txt                 # Dependencias Python
├── .gitignore
└── README.md
```

## 🚦 Requisitos Previos

- Docker y Docker Compose instalados
- Puerto 8080 (Airflow UI), 27017 (MongoDB) y 8081 (Mongo Express) disponibles

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/market-pulse-pipeline.git
cd market-pulse-pipeline
```

### 2. Iniciar los servicios con Docker Compose

```bash
docker-compose up -d
```

Esto iniciará los siguientes servicios:

- **MongoDB** (puerto 27017)
- **PostgreSQL** (para metadatos de Airflow)
- **Airflow Init** (inicialización de base de datos y usuario admin)
- **Airflow Webserver** (puerto 8080)
- **Airflow Scheduler** (orquestador de tareas)
- **Mongo Express** (UI de MongoDB en puerto 8081)

### 3. Verificar que los servicios estén corriendo

```bash
docker-compose ps
```

Todos los servicios deberían estar en estado "running" (excepto `airflow-init` que completará su ejecución).

## 🎯 Uso

### Acceder a la interfaz de Airflow

1. Abre tu navegador en: http://localhost:8080
2. Credenciales:
   - **Usuario**: `airflow`
   - **Contraseña**: `airflow`

### Activar el DAG

1. En la interfaz de Airflow, busca el DAG `market_pulse_pipeline_v2`
2. Activa el toggle para habilitar el DAG
3. El pipeline se ejecutará automáticamente cada hora

### Acceder a MongoDB (Mongo Express)

1. Abre tu navegador en: http://localhost:8081
2. Credenciales:
   - **Usuario**: `admin`
   - **Contraseña**: `password123`

### Ver los datos

En Mongo Express:
- Base de datos: `market_pulse`
- Colecciones:
  - `raw_prices`: Datos crudos de la API
  - `cleansed_prices`: Datos procesados y limpios

## 📊 Pipeline de Datos

### Tarea 1: Ingestión (`ingest_raw_data`)

- Extrae datos de Bitcoin y Ethereum de CoinGecko API
- Incluye: precio USD, capitalización de mercado, volumen 24h
- Añade timestamp de creación
- Guarda en colección `raw_prices` de MongoDB

### Tarea 2: Transformación (`transform_and_load_clean_data`)

- Lee el último registro de `raw_prices`
- Limpia y estructura los datos con Pandas
- Crea un DataFrame con formato tabular
- Guarda registros limpios en colección `cleansed_prices`

### Dependencias

```
ingest_raw_data >> transform_and_load_clean_data
```

## 🔧 Configuración

### Variables de Entorno (MongoDB)

```
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password123
```

### Variables de Entorno (Airflow)

```
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__LOAD_EXAMPLES=False
```

### Programación del DAG

Por defecto, el DAG se ejecuta **cada hora** (`@hourly`). Para cambiar la frecuencia:

Edita `airflow/dags/market_pulse_dag.py`:

```python
schedule_interval='@hourly'  # Cambiar a '@daily', '@weekly', etc.
```

## 🧪 Ejecutar Scripts Manualmente

### Ingestión

```bash
python src/ingestion/ingestor.py
```

### Transformación

```bash
python src/transformation/cleaner.py
```

## 📦 Dependencias Principales

- `apache-airflow==2.7.1`
- `pymongo`
- `requests`
- `pandas`
- `psycopg2-binary`

Ver `requirements.txt` para la lista completa.

## 🛑 Detener los Servicios

```bash
docker-compose down
```

Para eliminar también los volúmenes de datos:

```bash
docker-compose down -v
```

## 🐛 Troubleshooting

### El DAG no aparece en Airflow

- Verifica que el archivo esté en `airflow/dags/`
- Revisa los logs: `docker-compose logs airflow-scheduler`
- Espera unos minutos (Airflow escanea DAGs periódicamente)

### Error de conexión a MongoDB

- Verifica que el contenedor MongoDB esté corriendo: `docker-compose ps`
- Verifica la conexión desde Airflow: los contenedores deben usar `mongodb` como hostname (no `localhost`)

### Airflow muestra errores de permisos

- El proyecto usa `AIRFLOW_UID=0` (root) para evitar problemas de permisos en Windows/Mac
- En Linux, considera ajustar los permisos de las carpetas `airflow/`

## 📈 Próximas Mejoras

- [ ] Añadir más criptomonedas al pipeline
- [ ] Implementar notificaciones por email en caso de fallos
- [ ] Crear dashboard de visualización con Grafana o Streamlit
- [ ] Añadir tests unitarios
- [ ] Implementar CI/CD con GitHub Actions
- [ ] Añadir soporte para otras APIs de mercado

## 👤 Autor

**MiguelPeña** - [GitHub](https://github.com/mpenalab)

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

⭐ Si este proyecto te resulta útil, ¡dale una estrella en GitHub!
