import pygame
import random

# Initialize Pygame
pygame.init()

# Define game constants
WIDTH = 640
HEIGHT = 480
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BLOCK_SIZE = 20
FPS = 10
FONT_NAME = pygame.font.match_font('arial')
HEAD_COLOR = (0, 0, 255) # change the color of the snake head here

# Define game colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Define game fonts
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# Define game functions
def new_food():
    x = random.randrange(0, WIDTH, BLOCK_SIZE)
    y = random.randrange(0, HEIGHT, BLOCK_SIZE)
    return pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)


def move_snake():
    global direction, food

    # Move the snake
    head = snake[-1].copy()
    if direction == 'up':
        head.move_ip(0, -BLOCK_SIZE)
    elif direction == 'down':
        head.move_ip(0, BLOCK_SIZE)
    elif direction == 'left':
        head.move_ip(-BLOCK_SIZE, 0)
    elif direction == 'right':
        head.move_ip(BLOCK_SIZE, 0)
    snake.append(head)

    # Check if the snake has collided with the food
    if snake[-1].colliderect(food):
        food = new_food()  # generate a new food
        #food.move_ip(random.choice(range(0, WIDTH, BLOCK_SIZE)), random.choice(range(0, HEIGHT, BLOCK_SIZE)))
    else:
        snake.pop(0)

    # Check if the snake has collided with the wall or itself
    if snake[-1].left < 0 or snake[-1].right > WIDTH or snake[-1].top < 0 or snake[-1].bottom > HEIGHT:
        pygame.quit()
    for block in snake[:-1]:
        if block == snake[-1]:
            game_over()



def game_over():
    global running

    draw_text(screen, 'GAME OVER', 48, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, 'Press any key to play again', 22, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                waiting = False


# Initialize game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
direction = 'right'
snake = [pygame.Rect(60, 80, BLOCK_SIZE, BLOCK_SIZE),
         pygame.Rect(40, 80, BLOCK_SIZE, BLOCK_SIZE),
         pygame.Rect(20, 80, BLOCK_SIZE, BLOCK_SIZE)]
food = new_food()
running = True



# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
            elif event.key== pygame.K_DOWN and direction != 'up':
                direction = 'down'
            elif event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
            elif event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'

    # Update game state
    move_snake()

    # Draw game objects
    screen.fill(BLACK)
    for i, block in enumerate(snake):
        if i == len(snake) - 1:  # if it's the last block, it's the head
            pygame.draw.rect(screen, HEAD_COLOR, block)
        else:
            pygame.draw.rect(screen, GREEN, block)
    pygame.draw.rect(screen, RED, food)
    draw_text(screen, f'Score: {len(snake) - 3}', 18, WIDTH / 2, 10)

    # Update display
    pygame.display.flip()

    # Control game speed
    clock.tick(FPS)

# Quit the game
pygame.quit()

