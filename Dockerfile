# Utilisez une image Python officielle comme base
FROM python:3.9-slim-buster

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers de dépendances et installez-les
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiez le reste de votre code
COPY . .

# Exposez le port sur lequel l'application Flask écoute (Cloud Run utilise la variable d'environnement PORT)
ENV PORT 8080

# Commande pour démarrer l'application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]