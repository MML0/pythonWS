import socket
import time
# Configure server IP and port
server_ip = "192.168.43.81"  # Use your server's IP
server_port = 8266
esp_ip = "192.168.43.222"  # ESP's static IP

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip, server_port))

# Example data to send to ESP
led_data = b'\xFF\xAA\x12' * 1024  # Sync byte + RGB data for each LED

while True:
    # Send data to ESP
    sock.sendto(b'\xAA' + led_data, (esp_ip, 8266))
    led_data = input().encode( encoding="utf-8")
    # Wait for the ESP's response
    data, addr = sock.recvfrom(64)
    print("Received from ESP:", data.decode())
    time.sleep(0.05)

