import pygame
import sys

def page_2():
    # Initialize Pygame
    pygame.init()
    bg_page_2 = pygame.image.load(r'bg_page_2.JPG')
    # Set up display
    screen = pygame.display.set_mode((1280, 720))
    #pygame.display.set_caption('Game Menu')
    
    
    # Set up fonts
    font = pygame.font.SysFont('garamond', 74)
    #small_font = pygame.font.Font(None, 36)
    
    # Render text
    level_1 = font.render('Level 1', True, black)
    level_2 =font.render('Level 2', True, black)
    level_3 =font.render('Level 3', True, black)
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if level_1_b.collidepoint(mouse_pos):
                    print("Level 1 activated")

                if level_2_b.collidepoint(mouse_pos):
                    print('Level 2 activated')

                if level_3_b.collidepoint(mouse_pos):
                    print('Level 3 activated')
                    # Add code to start the game
    
        # Fill the screen with black
        #screen.fill(black)
        screen.blit(bg_page_2, (0, 0))
        
        level_1_b = screen.blit(level_1, (530, 200))
        level_2_b = screen.blit(level_2, (530, 325))
        level_3_b = screen.blit(level_3, (530, 450))
        # Update the display
        pygame.display.flip()
    
        # Cap the frame rate
        pygame.time.Clock().tick(60)
# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Game Menu')
white = (255, 255, 255)
black = (0, 0, 0)
# Set up fonts
font = pygame.font.SysFont('garamond', 74)
small_font = pygame.font.SysFont(None, 36)
bg_intro = pygame.image.load(r'bg_intro.JPG')
# Render text
#title_text = font.render('My Game', True, white)
start_text = font.render('Start Game', True, white)
#quit_text = font.render('Quit', True, (240,233,232))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if start_button.collidepoint(mouse_pos):
                print("Start Game pressed")
                page_2()

                # Add code to start the game
           # elif quit_button.collidepoint(mouse_pos):
           #     pygame.quit()
           #     sys.exit()

    
    screen.blit(bg_intro, (0, 0))
    # Blit the text to the screen
   # screen.blit(title_text, (500, 200))
    
    start_button = screen.blit(start_text, (512, 500))
    #quit_button = screen.blit(quit_text, (575, 650))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)


    