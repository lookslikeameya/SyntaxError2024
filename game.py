import pygame
import sys
#import lvl1
pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
home_button = pygame.Surface((150, 50))  # Create a surface for the home button
home_button.fill((255, 0, 0))  # Red color for the button
button_font = pygame.font.SysFont(None, 30)  # Font for button text
button_text = button_font.render("Home", True, (255, 255, 255))  # Text for the button
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
    
 #   def home():
#
 #       home_button.blit(button_text, (10, 10))  # Center text in the button surface
 #   # Check for mouse clicks on the home button
 #       if event.type == pygame.MOUSEBUTTONDOWN and current_turn >= turns:
 #           mouse_x, mouse_y = pygame.mouse.get_pos()
 #           if (1120 <= mouse_x <= 1270) and (10 <= mouse_y <= 60):
 #               main()
 #       if current_turn >= turns:
 #           screen.blit(home_button, (1120, 10))  # Draw home button at top right
 #           # Optionally display a game over message
 #           game_over_text = font.render("Game Over! Click Home to Exit!", True, (255, 255, 255))
 #           screen.blit(game_over_text, (10, 130))  # Centered in the screen
   
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
                    import lvl1

                if level_2_b.collidepoint(mouse_pos):
                    print('Level 2 activated')
                    import lvl2
                
                   # home()
                    # Add code to start the game
    
        # Fill the screen with black
        #screen.fill(black)
        screen.blit(bg_page_2, (0, 0))
        
        level_1_b = screen.blit(level_1, (530, 200))
        level_2_b = screen.blit(level_2, (530, 325))
        
        # Update the display
        pygame.display.flip()
    
        # Cap the frame rate
        pygame.time.Clock().tick(60)
# Initialize Pygame
def main():
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Game Menu')

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
    
    
        # Load home button image
    
       # if current_turn >= turns:
        #      screen.blit(home_button, (1120, 10))  # Draw home button at top right
        #      # Optionally display a game over message
        #      game_over_text = font.render("Game Over! Click Home to Exit!", True, (255, 255, 255))
        #      screen.blit(game_over_text, (10, 130))  # Centered in the screen
main()
