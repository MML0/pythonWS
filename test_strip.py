import espdisplay , time , random

col = 32
row = 16
game_display = espdisplay.Display(col, row,pixel_width=20,baudrate=2000000)

running = True

# F

while running:
    game_display.handle_events()
    #game_display.fill((0, 0, 0))  # Blue background

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

    #game_display.put(0,0, (250, 0, 0))
    for i in range(10):
        game_display.put(random.randint(0,col),random.randint(0,row), (random.randint(0,50), random.randint(0,50), random.randint(0,50)))

    

    #game_display.draw_line((2, 2), (31, 14), (0, 255, 0))
    #game_display.put(x, y, (250, 0, 0))

    game_display.update()
    time.sleep(0.02)