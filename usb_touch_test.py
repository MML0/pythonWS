import serial
import time

# Replace with your ESP8266's serial port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
serial_port = 'COM8'
baud_rate = 115200  # Should match the baud rate in the ESP8266 code

# Initialize serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Allow time for the connection to establish
time.sleep(2)

try:
    while True:
        # Read data from the serial port
        if ser.in_waiting > 0:
            #line = ser.readline().decode('utf-8').strip()  # Read a line and decode it
            line = ser.readline().decode('utf-8', errors='replace').strip()  # Replace invalid characters
            if 'ouche' in line:
                print('!!!!!!!!')
            #print(f"Touch Status: {line}")
            
        #time.sleep(0.1)  # Add a small delay to avoid overwhelming the serial port

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()  # Close the serial connection
