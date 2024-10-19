import pygame
import sys
import os
# os.system("C:\SyntaxError2024\Hand Detection.py")

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))


# Set up the clock
clock = pygame.time.Clock()
pygame.display.set_caption('Dart Game')
board = pygame.image.load(r'board.JPG')
x = 200
y = 100
def dart_board(x, y):
    screen.blit(board, (x, y))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
       # if  b == 0:
            #x = 0

    # Fill the screen with a color
    screen.fill((0, 0, 0))
    dart_board(x, y)
    pygame.draw.rect(screen, (200, 0, 0), (10, 100, 50, 50))
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    