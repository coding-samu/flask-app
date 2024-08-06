# Usa un'immagine di base Python
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file delle dipendenze
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice
COPY . .

# Imposta la variabile di ambiente
ENV FLASK_APP=app.py

# Avvia l'app Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
