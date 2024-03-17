from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY, Gauge
import psycopg2
import redis
from dotenv import load_dotenv
import os
import time
import atexit

app = Flask(__name__)

load_dotenv()
service_up = Gauge('service_up', 'Whether the service is up or not')

# Initialisez le middleware PrometheusMetrics
metrics = PrometheusMetrics(app)

# Connexion à la base de données PostgreSQL
conn_postgres = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
conn_postgres.set_client_encoding('UNICODE')
cursor_postgres = conn_postgres.cursor()

cursor_postgres.execute("CREATE TABLE IF NOT EXISTS clients (client_id SERIAL PRIMARY KEY, client_url VARCHAR(255) NOT NULL)")

# Connexion à Redis
conn_redis = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'),password=os.getenv('REDIS_PASSWORD'), decode_responses=True)

@app.route('/api/visits', methods=['POST'])
@metrics.summary('request_processing_time', 'Processing time of requests')
@metrics.counter('number_https_calls', 'Number of http calls')
@metrics.counter('redis_connections', 'Number of redis connections')
def track_visit():
    data = request.json  # Récupérer les données JSON envoyées

    # Vérifier si le client est enregistré dans la base de données PostgreSQL
    client_url = data['tracker']['WINDOW_LOCATION_HREF']
    cursor_postgres.execute("SELECT * FROM clients;")
    client = cursor_postgres.fetchall()

    res = False
    for row in client:
        if row[1] in client_url:
            res = True

    if res:
        # Si le client est enregistré, incrémenter le compteur de visite dans Redis
        page_url = client_url
        conn_redis.incr(page_url)  # Incrémentation du compteur pour cette page
        return jsonify({'message': 'Visite enregistrée avec succès'})
    else:
        return jsonify({'message': 'Client non autorisé'}), 403  # Accès interdit

## do a route to fill the database with the clients
@app.route('/api/clients', methods=['POST'])
@metrics.counter('postgres_connections', 'Number of postgres connections')
def add_client():
    client_urls = [
        "https://polytech.univ-cotedazur.fr",
        "www.google.com",
        "https://www.youtube.com"
    ]

    for url in client_urls:
        # Check if the client URL already exists in the database
        cursor_postgres.execute("SELECT * FROM clients WHERE client_url = %s", (url,))
        existing_client = cursor_postgres.fetchone()

        if existing_client:
            continue  # URL already exists, skip adding

        # Insert the client URL into the PostgreSQL database
        cursor_postgres.execute("INSERT INTO clients (client_url) VALUES (%s)", (url,))
        conn_postgres.commit()  # Commit the changes to the database

    return jsonify({'message': 'Clients added successfully'})

@app.route('/api/fetch-db', methods=['GET'])
def fetch_db():
    cursor_postgres.execute("SELECT * FROM clients")
    clients = cursor_postgres.fetchall()

    return jsonify({'clients': clients})

@app.route('/api/fetch-redis', methods=['GET'])
def fetch_redis():
    ## print keys and values
    keys = conn_redis.keys()
    values = conn_redis.mget(keys)
    ## return a list of tuples (key, value)
    return jsonify({'visits': list(zip(keys, values))})

def shutdown_hook():
    service_up.set(0)

atexit.register(shutdown_hook)
if __name__ == '__main__':
    service_up.set(1)  # Set the 'up' metric to 1
    app.run(host='0.0.0.0', port=5000)
