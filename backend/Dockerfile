FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code
ENV PIP_NO_CACHE_DIR=1

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Installer PyTorch CPU explicitement
RUN pip install \
    --index-url https://download.pytorch.org/whl/cpu \
    torch

# Installer le reste
RUN pip install -r requirements.txt

# Télécharger le modèle spaCy
RUN python -m spacy download fr_core_news_sm

# Copier le projet après les dépendances
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]