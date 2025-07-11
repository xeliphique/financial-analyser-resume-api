# Utilisez une image Python officielle comme base
FROM python:3.9-slim-buster

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers de dépendances et installez-les
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiez le reste de votre code
COPY . .

# Commande pour démarrer l'application
CMD ["python", "appresume.py"]
