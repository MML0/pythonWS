import socket

# ESP32 configuration
ESP32_IP = "192.168.43.232"  # Static IP of ESP32
ESP32_PORT = 8266          # Port to match the ESP32's UDP server

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Data to send (example bytes)
data = bytearray([0xAA, 0x02, 0x03, 0x04])  # Replace with the bytes you want to send

# Send the data to the ESP32
sock.sendto(data, (ESP32_IP, ESP32_PORT))
print("Data sent to ESP32:", data)

sock.close()

