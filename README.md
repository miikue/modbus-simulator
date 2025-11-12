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

### 1. Sestavení Docker image

Tento příkaz sestaví Docker image s názvem `modbus-simulator`. Verze se automaticky generuje z posledního `git tagu`.

```bash
VERSION=$(git describe --tags --always)
docker build -t modbus-simulator --build-arg VERSION=$VERSION .
```


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

