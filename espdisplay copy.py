import pygame
import sys
import time
import serial
import random , math

class Display:
    def __init__(self, cols, rows, pixel_width=40, baudrate=2000000):
        pygame.init()
        self.drawing = False  # Clear drawing flag when mouse is released
        self.clicked_blocks = []  # List to store clicked blocks
        self.clicked_keys = []  # List to store clicked blocks

        # Timer
        self.tasks = []

        self.cols = cols
        self.rows = rows
        self.pixel_width = pixel_width
        self.width = self.cols * self.pixel_width
        self.height = self.rows * self.pixel_width
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"{self.cols}x{self.rows} Pixel Game")

        # Array to hold pixel data for the display
        self.pixels = [[(0, 0, 0) for _ in range(self.cols)] for _ in range(self.rows)]
        self.led_data = bytearray(self.cols * self.rows * 3)  # 512 LEDs, 3 bytes per LED
        try:
            self.ser = serial.Serial('COM8', baudrate)  # Adjust COM port
        except Exception as er:
            print('no usb!')
            print(er)

    def send_led_data(self):
        try:
            self.ser.write(b'\xAA')  # Send sync byte first (0xAA)
            self.ser.write(self.led_data)  # Send the entire byte array to the ESP8266
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

    def draw_line(self, start, end, color, fill_percentage=0, blurred=False, fade_out=False):
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
            if fade_out:
                self.put(x1, y1, self.fade_color(color))
            if blurred:
                self.blur_pixel(x1, y1, color)

            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_circle(self, center, radius, color, fill_percentage=0, blurred=False, fade_out=False):
        for angle in range(0, 360, 1):  # Draw in small increments
            x = int(center[0] + radius * math.cos(angle * math.pi / 180))
            y = int(center[1] + radius * math.sin(angle * math.pi / 180))

            if random.random() < fill_percentage:
                self.put(x, y, color)
            if fade_out:
                self.put(x, y, self.fade_color(color))
            if blurred:
                self.blur_pixel(x, y, color)

    def draw_rect(self, rect, color, fill_percentage=0, blurred=False, fade_out=False):
        x, y, width, height = rect
        for i in range(width):
            for j in range(height):
                if random.random() < fill_percentage:
                    self.put(x + i, y + j, color)
                if fade_out:
                    self.put(x + i, y + j, self.fade_color(color))
                if blurred:
                    self.blur_pixel(x + i, y + j, color)

    def blur_pixel(self, x, y, color):
        # Average the color with neighboring pixels
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < self.cols and 0 <= y + dy < self.rows:
                    neighbors.append(self.pixels[y + dy][x + dx])

        if neighbors:
            avg_color = tuple(sum(c) // len(neighbors) for c in zip(*neighbors))
            self.put(x, y, avg_color)

    def fade_color(self, color):
        # Create a fade effect by reducing the brightness of the color
        return tuple(max(0, c - 20) for c in color)

    def update(self):
        for y in range(self.rows):
            for x in range(self.cols):
                color = self.pixels[y][x]
                pygame.draw.rect(self.screen, color, (x * self.pixel_width, y * self.pixel_width, self.pixel_width, self.pixel_width))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main():
    game_display = Display(32, 16)

    running = True
    r = 250
    g = 250
    b = 0
    game_display.fill((r % 255, g % 255, b % 255))

    while running:
        r += 3
        g += 6
        b += 12
        game_display.fill((255 - (r % 205), g % 205, b % 25))

        # Drawing with options
        game_display.draw_circle((16, 8), 6, (255, 0, 0), fill_percentage=0.5, blurred=True, fade_out=True)
        game_display.draw_rect((10, 10, 12, 5), (0, 255, 0), fill_percentage=0.5, blurred=False, fade_out=False)
        game_display.draw_line((0, 0), (31, 15), (0, 0, 255), fill_percentage=0.5, blurred=False, fade_out=True)

        game_display.handle_events()
        game_display.update()

        time.sleep(0.01)

# Run the game loop
if __name__ == "__main__":
    main()
