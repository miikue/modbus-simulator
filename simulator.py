

import time
import math
import struct
import threading
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# --------------------------------------------------------------------------- #
# Konfigurace simulátoru
# --------------------------------------------------------------------------- #
MODBUS_ADDRESS = "0.0.0.0"
MODBUS_PORT = 5020
UPDATE_INTERVAL_S = 1

# Adresy pro uint16 (0-50 cyklus)
UINT16_START_REGISTER = 0
UINT16_COUNT = 10

# Adresy pro 32-bit float (sin/cos)
FLOAT32_START_REGISTER = 20
SINE_REGISTER = FLOAT32_START_REGISTER
COSINE_REGISTER = FLOAT32_START_REGISTER + 2

# Adresy pro 64-bit float (ramp/triangle)
FLOAT64_START_REGISTER = 30
RAMP_REGISTER = FLOAT64_START_REGISTER
TRIANGLE_REGISTER = FLOAT64_START_REGISTER + 4


def float_to_registers(f_val, byte_order='>'):
    """
    Převádí float32 na list dvou 16-bitových Modbus registrů.
    '>' = Big-Endian, '<' = Little-Endian
    """
    packed_float = struct.pack(byte_order + 'f', f_val)
    regs = struct.unpack(byte_order + 'HH', packed_float)
    return list(regs)

def float64_to_registers(d_val, byte_order='>'):
    """
    Převádí float64 (double) na list čtyř 16-bitových Modbus registrů.
    '>' = Big-Endian, '<' = Little-Endian
    """
    packed_double = struct.pack(byte_order + 'd', d_val)
    regs = struct.unpack(byte_order + 'HHHH', packed_double)
    return list(regs)

# --------------------------------------------------------------------------- #
# Vlastní datový blok pro detekci čtení
# --------------------------------------------------------------------------- #
class CustomDataBlock(ModbusSequentialDataBlock):
    def getValues(self, address, count=1):
        print("-" * 60)
        print(f"[POŽADAVEK] Přijato čtení z adresy: {address}, počet registrů: {count}")
        return super().getValues(address, count)


def run_updating_server(context):
    """
    Funkce pro periodickou aktualizaci Modbus registrů.
    """
    print("Spouštím periodickou aktualizaci registrů.")
    start_time = time.time()
    uint16_counter = 0

    while True:
        try:
            current_time = time.time()
            elapsed_time = current_time - start_time

            # 1. Aktualizace uint16 hodnot (cyklus 0-50)
            uint16_values = [(uint16_counter + i) % 51 for i in range(UINT16_COUNT)]
            context[0].setValues(3, UINT16_START_REGISTER, uint16_values)
            print(f"Aktualizováno: uint16 ({UINT16_START_REGISTER}-{UINT16_START_REGISTER + UINT16_COUNT - 1}) = {uint16_values}")
            uint16_counter = (uint16_counter + 1) % 51

            # 2. Aktualizace float32 hodnot (sin/cos)
            sine_value = math.sin(elapsed_time * 0.5)
            cosine_value = math.cos(elapsed_time * 0.5)
            payload_sin = float_to_registers(sine_value)
            payload_cos = float_to_registers(cosine_value)
            context[0].setValues(3, SINE_REGISTER, payload_sin)
            context[0].setValues(3, COSINE_REGISTER, payload_cos)
            print(f"Aktualizováno: Sin({SINE_REGISTER}) = {sine_value:.4f}, Cos({COSINE_REGISTER}) = {cosine_value:.4f}")

            # 3. Aktualizace float64 hodnot
            # Lineární rampa (0.0 to 100.0 a zpět)
            ramp_value = (elapsed_time % 100)
            # Trojúhelníkový průběh (-50.0 to 50.0)
            triangle_value = abs((elapsed_time % 20) - 10) * 10 - 50.0
            
            payload_ramp = float64_to_registers(ramp_value)
            payload_triangle = float64_to_registers(triangle_value)
            context[0].setValues(3, RAMP_REGISTER, payload_ramp)
            context[0].setValues(3, TRIANGLE_REGISTER, payload_triangle)
            print(f"Aktualizováno: Ramp64({RAMP_REGISTER}) = {ramp_value:.4f}, Triangle64({TRIANGLE_REGISTER}) = {triangle_value:.4f}")


            time.sleep(UPDATE_INTERVAL_S)

        except Exception as e:
            print(f"Chyba při aktualizaci registrů: {e}")
            time.sleep(5)


def main():
    """
    Hlavní funkce pro spuštění Modbus TCP serveru.
    """
    print("Konfiguruji Modbus TCP server.")
    datablock = CustomDataBlock(0, [0] * 100)
    slave_context = ModbusSlaveContext(hr=datablock)
    server_context = ModbusServerContext(slaves=slave_context, single=True)

    # Spuštění úlohy pro aktualizaci v pozadí
    update_thread = threading.Thread(target=run_updating_server, args=(server_context,))
    update_thread.daemon = True
    update_thread.start()

    print(f"Modbus TCP server spuštěn na {MODBUS_ADDRESS}:{MODBUS_PORT}")
    StartTcpServer(
        context=server_context,
        address=(MODBUS_ADDRESS, MODBUS_PORT),
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Server byl ukončen.")
