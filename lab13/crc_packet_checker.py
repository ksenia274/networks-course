import random

CRC_POLY = 0x07
CRC_WIDTH = 8

def compute_crc(data: bytes) -> int:
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ CRC_POLY) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc

def encode_packet(payload: bytes) -> bytes:
    crc = compute_crc(payload)
    return payload + bytes([crc])

def introduce_error(packet: bytes, bit_indices: list[int]) -> bytes:
    mutable = bytearray(packet)
    for bit_index in bit_indices:
        byte_index = bit_index // 8
        bit_pos = bit_index % 8
        mutable[byte_index] ^= (1 << bit_pos)
    return bytes(mutable)

def check_packet(packet: bytes) -> bool:
    payload = packet[:-1]
    received_crc = packet[-1]
    return compute_crc(payload) == received_crc

def main():
    text = "Пример текста для проверки CRC-проверки на пакетах."
    data = text.encode("utf-8")
    packet_size = 5
    packets = [data[i:i+packet_size] for i in range(0, len(data), packet_size)]

    print("Результаты передачи:\n")
    error_indices = {1: [3], 4: [12], 6: [5]}  # искусственные ошибки: пакет -> бит

    for i, payload in enumerate(packets):
        encoded = encode_packet(payload)
        corrupted = introduce_error(encoded, error_indices[i]) if i in error_indices else encoded
        status = "ОШИБКА" if not check_packet(corrupted) else "OK"

        print(f"Пакет {i + 1}:")
        print(f"  Данные           : {payload}")
        print(f"  Кодированный     : {corrupted}")
        print(f"  CRC              : {corrupted[-1]:02X}")
        print(f"  Статус проверки  : {status}\n")

if __name__ == "__main__":
    main()