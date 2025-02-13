import socket
import time
import random
# Configure server IP and port
server_ip = "192.168.43.81"  # Use your server's IP
server_port = 8266
esp_ip = "192.168.43.222"  # ESP's static IP 8266
esp_ip = "192.168.43.232"  # ESP's static IP   32

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip, server_port))

# Example data to send to ESP
led_data = b'\xFF\x00\x00' + b'\x00\x00\x00' * 1023  # Sync byte + RGB data for each LED
led_data = b'\xFF\x00\x00' * 1024  # Sync byte + RGB data for each LED
led_data = bytearray(1024 * 3)
i = 0
led_data = bytearray(200 *  b'\x00\x00\x00')

while True: 
    # Send data to ESP
    t = time.time()
    #led_data = input().encode( encoding="utf-8")
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    # Insert new random color at the start of the array
    led_data[0:3] = bytes([r, g, b])
    
    # Shift all pixels to the right by 1
    led_data[3:] = led_data[:-3]

    #led_data = b'\xFF\xFF\xFF' * 200  # Sync byte + RGB data for each LED

    sock.sendto(bytearray(b'\xAA' + led_data), (esp_ip, 8266))

    i += 1
    # Wait for the ESP's response
    #data, addr = sock.recvfrom(64)
    #print("Received from ESP:", data.decode())
    print(time.time()-t)
    time.sleep(0.05)

