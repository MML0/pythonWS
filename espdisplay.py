import pygame, sys ,time
import serial

class Display:
    def __init__(self, cols, rows, pixel_width=40,baudrate=2000000):
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

        # Array to hold pixel data for the display
        self.pixels = [[(0, 0, 0) for _ in range(self.cols)] for _ in range(self.rows)]
        self.led_data = bytearray(self.cols*self.rows * 3)  # 512 LEDs, 3 bytes per LED
        try:
            self.ser = serial.Serial('COM8', baudrate)  # Adjust COM port
        except Exception as er:
            print('no usb!')
            print(er)

    def send_led_data(self):
        try:
            self.ser.write(b'\xAA')  # Send sync byte first (0xAA)
            self.ser.write(self.led_data)     # Send the entire byte array to the ESP8266
        except Exception as er:
            pass

    def fill(self, color):
        self.screen.fill(color)
        for y in range(self.rows):
            for x in range(self.cols):
                self.pixels[y][x] = color

    def put(self, x, y, color):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.pixels[y][x] = color

    def draw_grid(self):
        for x in range(self.cols + 1):
            pygame.draw.line(self.screen, (20, 20, 20), (x * self.pixel_width, 0), (x * self.pixel_width, self.height), 5)
        for y in range(self.rows + 1):
            pygame.draw.line(self.screen, (20, 20, 20), (0, y * self.pixel_width), (self.width, y * self.pixel_width), 5)

    def draw_line(self, start, end, color):
        x1, y1 = start
        x2, y2 = end

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
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

    def update(self):
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


# Example usage:
def main():
    game_display = Display(32, 16)

    running = True
    r = 250
    g = 250
    b = 0
    game_display.fill((r%255, g%255, b%255))
    while running:
        r +=3
        g +=6
        b +=12
        game_display.fill((255-(r%205), g%205, b%25))

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
        #game_display.draw_line((2, 2), (31, 14), (0, 255, 0))
        #game_display.put(x, y, (250, 0, 0))

        game_display.update()

        time.sleep(0.01)

# Run the game loop
if __name__ == "__main__":
    main()
