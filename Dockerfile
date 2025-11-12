# Použijeme oficiální Python image jako základ
FROM python:3.9-slim

# Nastavíme pracovní adresář v kontejneru
WORKDIR /app

# Zkopírujeme soubor se závislostmi
COPY requirements.txt .

# Nainstalujeme systémové závislosti potřebné pro kompilaci (např. pro numpy)
RUN apt-get update && apt-get install -y build-essential

# Nainstalujeme závislosti
RUN pip install --no-cache-dir -r requirements.txt

# Zkopírujeme skript simulátoru
COPY simulator.py .

# Vystavíme port, na kterém Modbus server naslouchá
EXPOSE 5020

# Spustíme simulátor při startu kontejneru
CMD ["python", "simulator.py"]
