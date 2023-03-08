import pygame
import random

# Initialize Pygame
pygame.init()

# Define game constants
WIDTH = 640
HEIGHT = 480
#WIDTH = 1920
#HEIGHT = 1080
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

#'Sdsd'


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
    food_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    food_surf = pygame.image.load('food.png').convert_alpha() # load the image for the food
    return food_surf, food_rect


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

    # Check if the snake has collided with the wall or itself
    # if snake[-1].left < 0 or snake[-1].right > WIDTH or snake[-1].top < 0 or snake[-1].bottom > HEIGHT:
    # game_over()

    # Check if the head has gone off the screen in any direction
    if head.left < 0:
        head.right = WIDTH
    elif head.right > WIDTH:
        head.left = 0
    elif head.top < 0:
        head.bottom = HEIGHT
    elif head.bottom > HEIGHT:
        head.top = 0

    snake.append(head)

    # Check if the snake has collided with the food
    if snake[-1].colliderect(food[1]):
        food = new_food()  # generate a new food
        #food.move_ip(random.choice(range(0, WIDTH, BLOCK_SIZE)), random.choice(range(0, HEIGHT, BLOCK_SIZE)))
    else:
        snake.pop(0)

        #######pygame.quit()
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
# Load the image for the snake head
#head_img2 = pygame.image.load('snake_head_2.png').convert_alpha()
head_img = {
    'right': pygame.image.load('snake_head_2.png').convert_alpha(),
    'left': pygame.transform.flip(pygame.image.load('snake_head_2.png').convert_alpha(), True, False),
    'up': pygame.transform.rotate(pygame.image.load('snake_head_2.png').convert_alpha(), 90),
    'down': pygame.transform.rotate(pygame.image.load('snake_head_2.png').convert_alpha(), -90)
}


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
            if direction == 'right':
                head_surf = head_img['right']
            elif direction == 'left':
                head_surf = head_img['left']
            elif direction == 'up':
                head_surf = head_img['up']
            else:
                head_surf = head_img['down']
            head_rect = head_surf.get_rect()
            head_rect.center = block.center
            screen.blit(head_surf, head_rect)
        else:
            pygame.draw.rect(screen, GREEN, block)
    screen.blit(food[0], food[1]) # draw the food image
    draw_text(screen, f'Score: {len(snake) - 3}', 18, WIDTH / 2, 10)

    # Update display
    pygame.display.flip()

    # Control game speed
    clock.tick(FPS)

# Quit the game
pygame.quit()

