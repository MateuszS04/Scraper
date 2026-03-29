FROM python:3.12-slim

# Ustaw katalog roboczy
WORKDIR /app

# Kopiuj zaleznosci
COPY requirements.txt ./

# Zainstaluj zaleznosci
RUN pip install --no-cache-dir -r requirements.txt

# Zainstaluj przeglądarkę dla Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python -m playwright install chromium

# Skopiuj kod aplikacji do kontenera
COPY . .

# Expose (brak potrzebnych portów; scheduler i scraper działają w tle)

# Domyślne polecenie uruchomienia
CMD ["python", "main.py"]
