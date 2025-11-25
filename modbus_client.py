import struct
from pymodbus.client.sync import ModbusTcpClient

def registers_to_float(regs, byte_order='>'):
    """
    Converts a list of two 16-bit Modbus registers to float32.
    '>' = Big-Endian, '<' = Little-Endian
    """
    packed_int = struct.pack(byte_order + 'HH', *regs)
    f_val = struct.unpack(byte_order + 'f', packed_int)[0]
    return f_val

def registers_to_float64(regs, byte_order='>'):
    """
    Converts a list of four 16-bit Modbus registers to float64 (double).
    '>' = Big-Endian, '<' = Little-Endian
    """
    packed_int = struct.pack(byte_order + 'HHHH', *regs)
    d_val = struct.unpack(byte_order + 'd', packed_int)[0]
    return d_val

def main():
    client = ModbusTcpClient('localhost', port=5020)
    try:
        client.connect()
        # Read a large block of registers from address 0 to 38
        # Total 38 registers
        rr = client.read_holding_registers(0, count=38, device_id=1)

        if rr.isError():
            print(f"Error reading registers: {rr}")
        elif not rr.registers or len(rr.registers) < 38:
            print("Failed to read enough registers.")
        else:
            print("Successfully read:")
            
            # 1. Process uint16 values (addresses 0-9)
            uint16_values = rr.registers[0:10]
            print("\n--- UINT16 (Addresses 0-9) ---")
            for i, val in enumerate(uint16_values):
                print(f"  Register {i}: {val}")

            # 2. Process float32 values (addresses 20-23)
            print("\n--- FLOAT32 (Addresses 20-23) ---")
            sine_regs = rr.registers[20:22]
            sine_value = registers_to_float(sine_regs)
            print(f"  Sine (registers 20-21): {sine_value:.4f}")

            cosine_regs = rr.registers[22:24]
            cosine_value = registers_to_float(cosine_regs)
            print(f"  Cosine (registers 22-23): {cosine_value:.4f}")

            # 3. Process float64 values (addresses 30-37)
            print("\n--- FLOAT64 (Addresses 30-37) ---")
            ramp_regs = rr.registers[30:34]
            ramp_value = registers_to_float64(ramp_regs)
            print(f"  Ramp (registers 30-33): {ramp_value:.4f}")

            triangle_regs = rr.registers[34:38]
            triangle_value = registers_to_float64(triangle_regs)
            print(f"  Triangle (registers 34-37): {triangle_value:.4f}")

    finally:
        client.close()

if __name__ == "__main__":
    main()
