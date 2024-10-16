from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

# serial port bisa kondsional
port = '/dev/ttyS7'  

# Konfigurasi Modbus Client RS485
client = ModbusClient(
    method='rtu',
    port=port,
    baudrate=9600,       
    parity='N',          
    stopbits=1,          
    bytesize=8,          
    timeout=2            
)

# Membuka koneksi ke sensor
if not client.connect():
    print("Gagal terhubung ke sensor.")
else:
    print("Terhubung ke sensor.")

def baca_kelembaban():
    try:
        # Baca register dari sensor (sesuaikan dengan alamat register yang digunakan untuk kelembaban)
        alamat_register = 0x0001  # (alamat register sensor)
        jumlah_register = 2       # (umlah register yang perlu dibaca (16-bit))

        # Membaca register holding (03h)
        response = client.read_holding_registers(alamat_register, jumlah_register, unit=1)

        if not response.isError():
            # Konversi data register - nilai kelembabann
            kelembaban_raw = response.registers[0]
            kelembaban = kelembaban_raw / 10.0  # sesuaikan konversi (kondisional ajha)

            print(f"Kelembaban: {kelembaban}%")
        else:
            print("Error membaca data dari sensor")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

try:
    while True:
        baca_kelembaban()
        time.sleep(2)  
finally:
    # Menutup koneksi setelah selesai
    client.close()
    print("Koneksi ditutup.")
