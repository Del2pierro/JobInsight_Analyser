FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
ENV PYTHONPATH=/code

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Téléchargement du modèle de langue spaCy
RUN python -m spacy download fr_core_news_sm

# Copie du code source (Important pour la prod !)
COPY . /code/

EXPOSE 8000

# Commande par défaut (Sera surchargée dans docker-compose.prod.yml)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
