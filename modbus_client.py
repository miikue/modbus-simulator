import struct
from pymodbus.client import ModbusTcpClient

def registers_to_float(regs, byte_order='>'):
    """
    Převádí list dvou 16-bitových Modbus registrů na float32.
    '>' = Big-Endian, '<' = Little-Endian
    """
    packed_int = struct.pack(byte_order + 'HH', *regs)
    f_val = struct.unpack(byte_order + 'f', packed_int)[0]
    return f_val

def registers_to_float64(regs, byte_order='>'):
    """
    Převádí list čtyř 16-bitových Modbus registrů na float64 (double).
    '>' = Big-Endian, '<' = Little-Endian
    """
    packed_int = struct.pack(byte_order + 'HHHH', *regs)
    d_val = struct.unpack(byte_order + 'd', packed_int)[0]
    return d_val

def main():
    client = ModbusTcpClient('localhost', port=5020)
    try:
        client.connect()
        # Přečteme jeden velký blok registrů od adresy 0 do 38
        # Celkem 38 registrů
        rr = client.read_holding_registers(0, count=38, device_id=1)

        if rr.isError():
            print(f"Chyba při čtení registrů: {rr}")
        elif not rr.registers or len(rr.registers) < 38:
            print("Nepodařilo se přečíst dostatečný počet registrů.")
        else:
            print("Úspěšně přečteno:")
            
            # 1. Zpracování uint16 hodnot (adresy 0-9)
            uint16_values = rr.registers[0:10]
            print("\n--- UINT16 (Adresy 0-9) ---")
            for i, val in enumerate(uint16_values):
                print(f"  Registr {i}: {val}")

            # 2. Zpracování float32 hodnot (adresy 20-23)
            print("\n--- FLOAT32 (Adresy 20-23) ---")
            sine_regs = rr.registers[20:22]
            sine_value = registers_to_float(sine_regs)
            print(f"  Sinus (registry 20-21): {sine_value:.4f}")

            cosine_regs = rr.registers[22:24]
            cosine_value = registers_to_float(cosine_regs)
            print(f"  Kosinus (registry 22-23): {cosine_value:.4f}")

            # 3. Zpracování float64 hodnot (adresy 30-37)
            print("\n--- FLOAT64 (Adresy 30-37) ---")
            ramp_regs = rr.registers[30:34]
            ramp_value = registers_to_float64(ramp_regs)
            print(f"  Rampa (registry 30-33): {ramp_value:.4f}")

            triangle_regs = rr.registers[34:38]
            triangle_value = registers_to_float64(triangle_regs)
            print(f"  Trojúhelník (registry 34-37): {triangle_value:.4f}")

    finally:
        client.close()

if __name__ == "__main__":
    main()
