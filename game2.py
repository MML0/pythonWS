import espdisplay , time ,random

col = 32
row = 16
game_display = espdisplay.Display(col, row)

running = True

def move_snake():
    global snake
    global direction
    new_head = [snake[-1][0] + direction[0], snake[-1][1] + direction[1]]
    if new_head in snake :
        snake = [[1,0],[1,1]]
        direction = [0,1]
        return

    snake.append(new_head)
    if new_head == food:
        food.clear()
    else:
        snake.pop(0)  # Remove the tail to simulate movement


game_display.set_interval(move_snake, 0.1)  # Move the snake every 0.5 seconds

def spawn_food():
    global food
    if not food :
        food = [random.randint(0, col-1), random.randint(0, row-1)]
        while food in snake:
            food = [random.randint(0, col-1), random.randint(0, row-1)]

game_display.set_interval(spawn_food, 2)  # Spawn food every 2 seconds

ball = [0,0]
while running:
    game_display.handle_events()
    game_display.fill((12, 18, 23))  

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

    if game_display.clicked_keys:
        for key in game_display.clicked_keys:
            if key == 'up' and not direction == [0, 1]:
                pass
            elif key == 'down' and not direction == [0, -1]:
                pass
            elif key == 'left' and not direction == [1, 0]:
                pass
            elif key == 'right' and not direction == [-1, 0]:
               pass
            break
        game_display.clicked_keys.clear()


    #game_display.draw_line((2, 2), (31, 14), (0, 255, 0))
    #game_display.put(x, y, (250, 0, 0))

    game_display.update()
    time.sleep(0.01)