# Modbus TCP Simulátor

Tento projekt obsahuje jednoduchý Modbus TCP server napsaný v Pythonu, který simuluje zařízení poskytující různé typy dat. Aplikace je připravena pro spuštění v Docker kontejneru.

## Funkce

- Spouští Modbus TCP server na portu `5020`.
- Periodicky (každou sekundu) aktualizuje různé typy registrů:
  - **Registry 0-9:** Deset 16-bitových celých čísel (`uint16`), které cyklují s hodnotami od 0 do 50.
  - **Registry 20-23:** Dvě 32-bitové float hodnoty (Big-Endian):
    - **Registry 20-21:** Hodnota **sinus**.
    - **Registry 22-23:** Hodnota **kosinus**.
  - **Registry 30-37:** Dvě 64-bitové float hodnoty (Big-Endian):
    - **Registry 30-33:** Hodnota **lineární rampy**.
    - **Registry 34-37:** Hodnota **trojúhelníkového průběhu**.

## Požadavky

- [Docker](https://www.docker.com/get-started)
- [Python 3](https://www.python.org/)

## Sestavení a spuštění

Všechny příkazy spouštějte z kořenového adresáře tohoto projektu (`/Users/miikue/Downloads/NOBACKUP/prace/simulator`).

### 1. Sestavení Docker image

Tento příkaz sestaví Docker image s názvem `modbus-simulator`.

```bash
docker build -t modbus-simulator .
```

### 2. Spuštění Docker kontejneru

Tento příkaz spustí kontejner na pozadí. Server bude dostupný na `localhost:5020`.

```bash
docker run -d -p 5020:5020 --rm --name modbus-sim modbus-simulator
```

### Parametry příkazu `docker run`

- `-d`: Spustí kontejner na pozadí (detached mode).
- `-p 5020:5020`: Mapuje port `5020` z kontejneru na port `5020` na vašem počítači.
- `--rm`: Automaticky odstraní kontejner po jeho zastavení.
- `--name modbus-sim`: Pojmenuje kontejner pro snazší správu.
- `modbus-simulator`: Název image, která se má spustit.

## Ověření

Po spuštění se můžete k Modbus serveru připojit pomocí jakéhokoliv Modbus TCP klienta.

### Ověření pomocí přiloženého skriptu

Součástí projektu je jednoduchý klient `modbus_client.py` pro rychlé ověření.

1.  **Vytvoření virtuálního prostředí** (doporučeno):
    ```bash
    python3 -m venv venv
    ```

2.  **Aktivace prostředí**:
    -   macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    -   Windows:
        ```bash
        venv\Scripts\activate
        ```

3.  **Instalace závislostí**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Spuštění klienta**:
    ```bash
    python modbus_client.py
    ```

    Pokud vše funguje, skript vypíše aktuální hodnoty `uint16`, `float32` (sinus a kosinus) a `float64` (rampa a trojúhelník) ze simulátoru.

## Testovací konfigurace (`config.json`)

Pro klienty, kteří vyžadují konfigurační soubor pro definici Modbus tagů (např. ThingsBoard Gateway), je k dispozici soubor `config.json`. Tento soubor definuje všechny simulované registry.

```json
[
  {
    "tag": "uint16_value_${address}",
    "type": "uint16",
    "functionCode": 3,
    "address": "0-9",
    "objectsCount": 1
  },
  {
    "tag": "float32_sine",
    "type": "32float",
    "functionCode": 3,
    "address": 20,
    "objectsCount": 2
  },
  {
    "tag": "float32_cosine",
    "type": "32float",
    "functionCode": 3,
    "address": 22,
    "objectsCount": 2
  },
  {
    "tag": "float64_ramp",
    "type": "64float",
    "functionCode": 3,
    "address": 30,
    "objectsCount": 4
  },
  {
    "tag": "float64_triangle",
    "type": "64float",
    "functionCode": 3,
    "address": 34,
    "objectsCount": 4
  }
]
```
