import secrets

#TODO: implementar hash para convertir texto a cadena de 256 bits

def bits_to_float(bits, n_bits):
    return sum(bits[i] * 2 ** -(i + 1) for i in range(n_bits))

def bits_to_int(bits, n_bits):
    return sum(bits[i] * 2 ** (i) for i in range(n_bits))

def generate_key():

    key = secrets.token_bytes(32)

    bit_stream = [int(bit) for byte in key for bit in format(byte, '08b')]

    x0 = bits_to_float(bit_stream[:52], 52)
    r = bits_to_float(bit_stream[52:104], 52)

    d1 = bits_to_int(bit_stream[104:128], 24)
    d2 = bits_to_int(bit_stream[128:152], 24)

    r1 = bits_to_float(bit_stream[152:204], 52)
    r2 = bits_to_float(bit_stream[204:256], 52)

    return x0, r, d1, d2, r1, r2

def generate_round_keys():

    x0, r, d1, d2, r1, r2 = generate_key()
   
    x0_1 = (d1 * (x0 + r1)) % 1
    r_1 = (d1 * (r + r1)) % 4

    x0_2 = (d2 * (x0 + r2)) % 1
    r_2 = (d2 * (r + r2)) % 4

    return (x0_1, r_1), (x0_2, r_2)