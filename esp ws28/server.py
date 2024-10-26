import socket

# Set the IP address and port of the ESP8266
esp_ip = '192.168.43.169'  # Replace with your ESP8266's IP address
esp_port = 8266  # Replace with the port number your ESP is listening on

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Example byte data to send
data = b'\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04'  # This is binary data in byte form

try:
    # Send the byte data to the ESP8266
    for i in range(10000):        
        sock.sendto(data, (esp_ip, esp_port))
    print(f"Sent {data} to {esp_ip}:{esp_port}")
finally:
    # Close the socket
    sock.close()
