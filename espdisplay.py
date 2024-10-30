import pygame, sys ,time
import random
import math
import serial
import threading

class Display:
    def __init__(self, cols, rows, pixel_width=40,baudrate=2000000,com_port='COM8',connection_type='serial',esp_ip = '192.168.43.169',esp_port = 8266 ):
        """Initialize the Display class with specified columns, rows, pixel width, and baud rate.
        
        Args:
            cols (int): Number of columns in the display.
            rows (int): Number of rows in the display.
            pixel_width (int, optional): Width of each pixel block. Defaults to 40.
            baudrate (int, optional): Baud rate for serial communication. Defaults to 2000000.
        """
        pygame.init()
        self.drawing = False  # Clear drawing flag when mouse is released
        self.clicked_blocks = []  # List to store clicked blocks
        self.clicked_keys = []  # List to store clicked blocks

        # timer
        self.tasks = []
        # timer 

        self.cols = cols
        self.rows = rows

        self.pixel_width = pixel_width
        self.width = self.cols * self.pixel_width
        self.height = self.rows * self.pixel_width
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(f"{self.cols}x{self.rows} Pixel Game")

        #self.color = ColorPalette()

        self.color = {
            "red": (255, 0, 0),              # Bright red
            "green": (0, 240, 0),            # Vivid green
            "blue": (0, 50, 255),           # Bright blue
            "orange": (255, 145, 0),         # Bright orange
            "pink": (255, 80, 180),         # Bright pink
            "purple": (190, 0, 255),         # Vivid purple
            "yellow": (255, 255, 0),         # Bright yellow
            "black": (0, 0, 0),              # Black
            "white": (255, 255, 255),        # White
            "cyan": (0, 255, 255),           # Cyan
            "magenta": (255, 0, 255),        # Magenta
            "lime": (191, 255, 0),           # Lime
            "teal": (0, 128, 128),           # Teal
            "brown": (165, 42, 42),          # Brown
            "gray": (128, 128, 128),         # Gray
            "light_gray": (211, 211, 211),   # Light gray
            "dark_gray": (169, 169, 169),    # Dark gray
            "gold": (255, 215, 0),           # Gold
            "beige": (245, 245, 220),        # Beige
            "maroon": (128, 0, 0),           # Maroon
            "navy": (0, 0, 128),             # Navy
            "olive": (128, 128, 0)           # Olive
        }
        
        # Array to hold pixel data for the display
        self.pixels = [[(0, 0, 0) for _ in range(self.cols)] for _ in range(self.rows)]
        self.led_data = bytearray(self.cols*self.rows * 3)  # 512 LEDs, 3 bytes per LED
        self.ser = None

        self.connection_type = connection_type

        if connection_type=='wifi':
            import socket

            # Set the IP address and port of the ESP8266
            self.esp_ip = esp_ip  # Replace with your ESP8266's IP address
            self.esp_port = esp_port # Replace with the port number your ESP is listening on

            # Create a UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        try:
            self.ser = serial.Serial(com_port, baudrate)  # Adjust COM port
            self.serial_thread = threading.Thread(target=self.receive_data)
            self.serial_thread.daemon = True  # Thread exits when main program exits
            self.serial_thread.start()
        except Exception as er:
            print('no usb!')
            print(er)

    def send_led_data(self):
        """Send the LED data over the serial or wifi connection.
        
        This method sends a sync byte followed by the LED data to the ESP.
        """
        try:
            if self.connection_type == 'wifi':
                self.sock.sendto(b'\xAA'+self.led_data, (self.esp_ip, self.esp_port))
            else:
                self.ser.write(b'\xAA')  # Send sync byte first (0xAA)
                self.ser.write(self.led_data)     # Send the entire byte array to the ESP8266
        except Exception as er:
            pass

    def receive_data(self):
        """Receives data from the serial device in a background thread."""
        self.ser.flushInput() 
        while True:
            time.sleep(0.001)
            try:
                if self.ser and self.ser.in_waiting > 0:
                    # Read one byte at a time until sync byte is found
                    incoming_byte = self.ser.read(1)
                    print(2)
                    
                    # Check for the sync byte
                    if incoming_byte == bytes([0xAA]):

                        led_data = self.ser.read(self.cols*2)

                        if led_data !=  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                            print("Received LED data:", led_data)
                    else:
                        self.ser.flushInput() 

            except Exception as e:
                print("Error receiving data:", e)

    def fill(self, color):
        """Fill the display with a specified color.
        
        Args:
            color (tuple): RGB color value to fill the display.
        """
        self.screen.fill(color)
        for y in range(self.rows):
            for x in range(self.cols):
                self.pixels[y][x] = color

    def put(self, x, y, color):
        """Set the color of a specific pixel on the display.
        
        Args:
            x (int): The x-coordinate of the pixel.
            y (int): The y-coordinate of the pixel.
            color (tuple): RGB color value to set the pixel.
        """
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.pixels[y][x] = color

    def draw_grid(self):
        """Draw a grid overlay on the display. pc's display only"""
        for x in range(self.cols + 1):
            pygame.draw.line(self.screen, (20, 20, 20), (x * self.pixel_width, 0), (x * self.pixel_width, self.height), 5)
        for y in range(self.rows + 1):
            pygame.draw.line(self.screen, (20, 20, 20), (0, y * self.pixel_width), (self.width, y * self.pixel_width), 5)

    def draw_line(self, start:tuple, end, color, fill_percentage=1.0):
        """Draw a line between two points on the display.
        
        Args:
            start (tuple): Starting coordinates (x1, y1).
            end (tuple): Ending coordinates (x2, y2).
            color (tuple): RGB color value for the line.
            fill_percentage (float): 0~1
        """
        x1, y1 = start
        x2, y2 = end

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if random.random() < fill_percentage:
                self.put(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_rectangle(self, top_left, bottom_right, color, fill=False, fill_percentage=1.0):
        """
        Draw a rectangle on the display. Optionally fill the rectangle.

        Args:
            top_left (tuple): Top-left corner coordinates (x1, y1).
            bottom_right (tuple): Bottom-right corner coordinates (x2, y2).
            color (tuple): RGB color value for the rectangle's border.
            fill (bool): If True, the rectangle will be filled with the color.
            fill_percentage (float) : blure.
        """
        x1, y1 = top_left
        x2, y2 = bottom_right

        if fill:
            # Draw filled rectangle by filling each row from top to bottom.
            for y in range(y1, y2 + 1):
                self.draw_line((x1, y), (x2, y), color, fill_percentage)
        else:
            # Draw only the outline of the rectangle.
            self.draw_line((x1, y1), (x2, y1), color, fill_percentage)  # Top edge
            self.draw_line((x1, y2), (x2, y2), color, fill_percentage)  # Bottom edge
            self.draw_line((x1, y1), (x1, y2), color, fill_percentage)  # Left edge
            self.draw_line((x2, y1), (x2, y2), color, fill_percentage)  # Right edge

    def update(self):
        """Update the display with the current pixel data and send LED data.
        
        This method refreshes the display and updates the LED data for serial transmission.
        """
        self.update_timer()
        for y in range(self.rows):
            for x in range(self.cols):
                color = self.pixels[y][x]
                if y%2==0:
                    self.led_data[(self.cols-x-1+y*self.cols)*3] = self.pixels[y][x][0]
                    self.led_data[(self.cols-x-1+y*self.cols)*3+1] = self.pixels[y][x][1]
                    self.led_data[(self.cols-x-1+y*self.cols)*3+2] = self.pixels[y][x][2]
                else:
                    self.led_data[(x+y*self.cols)*3] = self.pixels[y][x][0]
                    self.led_data[(x+y*self.cols)*3+1] = self.pixels[y][x][1]
                    self.led_data[(x+y*self.cols)*3+2] = self.pixels[y][x][2]

                pygame.draw.rect(self.screen, color, pygame.Rect(x * self.pixel_width, y * self.pixel_width, self.pixel_width, self.pixel_width))
        self.draw_grid()
        pygame.display.flip()
        self.send_led_data()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drawing = True
                x, y = pygame.mouse.get_pos()
                grid_x = x // self.pixel_width
                grid_y = y // self.pixel_width
                self.clicked_blocks.append((grid_x, grid_y))  # Store clicked block
                print(f"Mouse clicked at grid position: ({grid_x}, {grid_y})")
                #self.put(grid_x, grid_y, ((self.pixels[grid_y][grid_x][0]+50) % 250, 0, 0))

            if event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False

            if event.type == pygame.MOUSEMOTION and self.drawing:
                x, y = pygame.mouse.get_pos()
                grid_x = x // self.pixel_width
                grid_y = y // self.pixel_width
                #self.clicked_blocks.append((grid_x, grid_y))  # Store dragged blocks
                #self.put(grid_x, grid_y, ((self.pixels[grid_y][grid_x][0]+50) % 250, 0, 0))

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.clicked_keys.append('up')
                elif event.key == pygame.K_DOWN:
                    self.clicked_keys.append('down')
                elif event.key == pygame.K_LEFT:
                    self.clicked_keys.append('left')
                elif event.key == pygame.K_RIGHT:
                    self.clicked_keys.append('right')

    # timer class        
    def set_timeout(self, callback, delay):
        """Schedule a function to be called once after a delay (in seconds)."""
        trigger_time = time.time() + delay
        self.tasks.append({"callback": callback, "trigger_time": trigger_time, "repeat": False})

    def set_interval(self, callback, interval):
        """Schedule a function to be called repeatedly at specified intervals."""
        trigger_time = time.time() + interval
        self.tasks.append({"callback": callback, "trigger_time": trigger_time, "repeat": True, "interval": interval})

    def update_timer(self):
        """Check tasks and run them if their time has come."""
        current_time = time.time()
        for task in self.tasks[:]:
            if current_time >= task["trigger_time"]:
                task["callback"]()
                if task["repeat"]:
                    task["trigger_time"] = current_time + task["interval"]  # Reschedule for interval tasks
                else:
                    self.tasks.remove(task)  # Remove one-time tasks

class ColorPalette:
    def __init__(self):
        self.red = (255, 0, 0)          # Bright red
        self.green = (0, 240, 0)        # Vivid green
        self.blue = (0, 123, 255)       # Bright blue
        self.orange = (255, 165, 0)     # Bright orange
        self.pink = (255, 105, 180)     # Bright pink
        self.purple = (150, 0, 255)     # Vivid purple
        self.yellow = (255, 255, 0)     # Bright yellow
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        # Primary colors

        self.cyan = (0, 255, 255)
        self.magenta = (255, 0, 255)

        # Secondary colors
        self.orange = (255, 165, 0)
        self.lime = (191, 255, 0)
        self.teal = (0, 128, 128)
        self.brown = (165, 42, 42)

        # Grayscale colors
        self.gray = (128, 128, 128)
        self.light_gray = (211, 211, 211)
        self.dark_gray = (169, 169, 169)

        # Some additional colors
        self.gold = (255, 215, 0)
        self.beige = (245, 245, 220)
        self.maroon = (128, 0, 0)
        self.navy = (0, 0, 128)
        self.olive = (128, 128, 0)

class Player:
    def __init__(self, color:str, score=0, health=0,pos=[0,0]):
        """Initialize the Player class with specified ... .
        
        Args:
            color (int): ...
        """

        self.color = color  
        self.health = health  
        self.score = score  
        self.pos = pos  
        self.is_alive = True  

        # timer
        self.tasks = []
        # timer 



    # timer class        
    def set_timeout(self, callback, delay):
        """Schedule a function to be called once after a delay (in seconds)."""
        trigger_time = time.time() + delay
        self.tasks.append({"callback": callback, "trigger_time": trigger_time, "repeat": False})

    def set_interval(self, callback, interval):
        """Schedule a function to be called repeatedly at specified intervals."""
        trigger_time = time.time() + interval
        self.tasks.append({"callback": callback, "trigger_time": trigger_time, "repeat": True, "interval": interval})

    def update_timer(self):
        """Check tasks and run them if their time has come."""
        current_time = time.time()
        for task in self.tasks[:]:
            if current_time >= task["trigger_time"]:
                task["callback"]()
                if task["repeat"]:
                    task["trigger_time"] = current_time + task["interval"]  # Reschedule for interval tasks
                else:
                    self.tasks.remove(task)  # Remove one-time tasks

# Example usage:
def main():

    #game_display = Display(32, 16)
    game_display = Display(32, 32, pixel_width=20,connection_type='wifi',esp_ip = '192.168.43.169',esp_port = 8266 ,)

    running = True
    r = 25
    g = 20
    b = 0
    game_display.fill((r%255, g%255, b%255))

    while running:
        game_display.fill((25, 20, 12))
        game_display.fill(game_display.color['black'])
        r +=1
        g +=6
        b +=12
        #game_display.fill((255-(r%205), g%205, b%25))
        game_display.put(32-(r%250)//15,0,((255-(r%205), g%205, b%25)))
        game_display.handle_events()
        # Process clicked blocks in the main loop
        if game_display.clicked_blocks:
            for block in game_display.clicked_blocks:
                x = block[0]
                y = block[1]
                if game_display.pixels[y][x][0] == 250:
                    game_display.put(x, y, (0, 0, 0))
                else:
                    game_display.put(x, y, (250, 0, 0))

            game_display.clicked_blocks.clear()

        # Blue background
        game_display.draw_line((2, 2), (31, 14), (50, 20, 0))
        game_display.draw_line((15, 0), (32, 0), (10, 200,100),(r%250)/230)
        game_display.draw_rectangle((1, 1), (7, 5), (50, 50, 20),True,(r%250)/230)
        game_display.draw_rectangle((8, 10), (12, 14), (15, 100, 0),False,(r%250)/200)
        game_display.put(x, y, (250, 0, 0))

        #game_display.put(x, y, (250, 0, 0))

        game_display.update()

        time.sleep(0.03)

# Run the game loop
if __name__ == "__main__":
    main()
