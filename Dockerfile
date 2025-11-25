# STEP 1: Build stage (Používá se pro instalaci závislostí a zkopírování compiled/binary files)
FROM python:3.9-alpine AS builder

# Nastaví pracovní adresář
WORKDIR /app

# Kopíruje soubor závislostí
COPY requirements.txt .

# Instaluje systémové závislosti potřebné pro kompilaci (pokud jsou potřeba)
# Mnoho knihoven to nepotřebuje, ale pro jistotu to ponecháme v této fázi
RUN apk add --no-cache build-base

# Instaluje potřebné balíčky Pythonu. Všimněte si, že zde máme build-essential, 
# což umožňuje instalaci balíčků s kompilovanými rozšířeními.
RUN pip install --no-cache-dir -r requirements.txt

# ---
# STEP 2: Final stage (Malý, finální image bez buildovacích závislostí)
FROM python:3.9-alpine

# Nastaví pracovní adresář
WORKDIR /app

# Zkopíruje nainstalované Python závislosti z build stage
# Tímto se přenáší pouze to, co je potřeba pro běh
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Zkopíruje skript simulátoru a soubor s verzí
COPY simulator.py .
COPY VERSION /app/version.txt

# Otevře port
EXPOSE 5020

# Spustí simulátor
CMD ["python", "simulator.py"]
