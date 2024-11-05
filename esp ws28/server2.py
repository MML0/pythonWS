import socket
import time
# Configure server IP and port
server_ip = "192.168.43.81"  # Use your server's IP
server_port = 8266
esp_ip = "192.168.43.222"  # ESP's static IP 8266
esp_ip = "192.168.43.232"  # ESP's static IP   32
CHUNK_SIZE = 300           # Size of each packet

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind((server_ip, server_port))

# Example data to send to ESP
led_data = b'\xFF\x00\x00' + b'\x00\x00\x00' * 1023  # Sync byte + RGB data for each LED
led_data = b'\xFF\x00\x00' * 1024  # Sync byte + RGB data for each LED
led_data = bytearray(300 * 3)

sync_byte = bytearray([0xAA]) 

i = 0
while True: 
    # Send data to ESP
    t = time.time()
    #print( led_data)
    #sock.sendto(bytearray([0xAA]) , (esp_ip, 8266))
    for j in range(0, len(led_data), CHUNK_SIZE):
        chunk = led_data[j:j + CHUNK_SIZE]
        if j == 0:
            sock.sendto(bytearray( b'\xBB'+chunk), (esp_ip, 8266))
        else:
            sock.sendto(bytearray( b'\xAA'+chunk), (esp_ip, 8266))

    #led_data = input().encode( encoding="utf-8")
    led_data = bytearray(300 * 3)
    led_data[(i*3)%100] = 255
    led_data[(i*3+1)%100] = 255
    led_data[(i*3+2)%100] = 255
   
    i += 1
    # Wait for the ESP's response
    #data, addr = sock.recvfrom(64)
    #print("Received from ESP:", data.decode())
    print(time.time()-t)
    time.sleep(0.05)

