import cv2
import mediapipe as mp
import math
import pygame
import random
import sys

# Initialize Pygame and OpenCV
pygame.init()
dart_held = False  # True when dart is held by fingers
dart_released = False  # True when dart is released
score = 0  # Initialize the score
thrown_darts = []  # List to store all darts stuck to the board
missed_message = ""  # Message for missed throws
turns = 3  # Number of turns
current_turn = 0  # Keep track of the current turn

# Set up display for 1280x720 resolution
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Dart Game')

# Load dartboard and dart images
board = pygame.image.load(r'board.png')
dart = pygame.image.load(r'dart.png')  # Load your dart image here
dart = pygame.transform.scale(dart, (50, 50))  # Scale dart image if necessary

# Load home button image
home_button = pygame.Surface((150, 50))  # Create a surface for the home button
home_button.fill((255, 0, 0))  # Red color for the button
button_font = pygame.font.SysFont(None, 30)  # Font for button text
button_text = button_font.render("Home", True, (255, 255, 255))  # Text for the button
home_button.blit(button_text, (10, 10))  # Center text in the button surface

# Initialize dartboard position
x = 200
y = 100

# Set random direction for the board
direction_x = random.choice([-1, 1])
direction_y = random.choice([-1, 1])
speed = 3  # Speed of movement

# Font for displaying score
font = pygame.font.SysFont(None, 36)

# Function to display the score and turns on the screen
def display_score_and_turns(score, turns_left):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    turns_text = font.render(f"Turns Left: {turns_left}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(turns_text, (10, 50))

# Function to calculate distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Function to calculate score based on distance from the center of the board
def calculate_score(dart_x, dart_y, board_x, board_y):
    # Center of the dartboard
    board_center_x = board_x + board.get_width() // 2
    board_center_y = board_y + board.get_height() // 2

    # Calculate distance from dart to center of the board
    distance = calculate_distance(dart_x, dart_y, board_center_x, board_center_y)

    # Define score zones based on distance
    if distance < 20:
        return 100  # Bullseye
    elif distance < 50:
        return 50
    elif distance < 100:
        return 20
    else:
        return 10  # Further away

# Function to draw the dartboard
def dart_board(x, y):
    screen.blit(board, (x, y))

# Set up the clock
clock = pygame.time.Clock()

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Ignoring empty frame.")
        continue

    # Flip the frame horizontally for a selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands only if turns are left
    if current_turn < turns:
        results = hands.process(rgb_frame)
    else:
        results = None  # Disable hand detection

    # Initialize index finger coordinates to None
    index_x, index_y = None, None

    # Update dartboard position
    x += direction_x * speed
    y += direction_y * speed

    # Check for boundary collisions and reverse direction if it hits the screen edges
    if x <= 0 or x >= 1280 - board.get_width():
        direction_x *= -1
    if y <= 0 or y >= 720 - board.get_height():
        direction_y *= -1

    # Fill the screen with a color
    screen.fill((0, 0, 0))
    dart_board(x, y)

    # Draw all previously thrown darts stuck to the board
    for dart_data in thrown_darts:
        stuck_dart_x, stuck_dart_y = dart_data
        # Adjust dart position to move with the board
        screen.blit(dart, (stuck_dart_x - dart.get_width() // 2 + x, stuck_dart_y - dart.get_height() // 2 + y))

    # If hands are detected and dart hasn't been released
    if results and not dart_released:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get pixel coordinates for all landmarks
            height, width, _ = frame.shape
            landmarks = []

            for lm in hand_landmarks.landmark:
                lm_x = int(lm.x * 1280)
                lm_y = int(lm.y * 720)
                landmarks.append((lm_x, lm_y))

            # Draw the hand skeleton in Pygame
            for connection in mp_hands.HAND_CONNECTIONS:
                start_idx, end_idx = connection
                start_pos = landmarks[start_idx]
                end_pos = landmarks[end_idx]
                pygame.draw.line(screen, (0, 255, 0), start_pos, end_pos, 2)

            # Get coordinates of the thumb tip (landmark 4) and index finger tip (landmark 8)
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]

            # Scale the coordinates from the camera to the Pygame screen size (1280x720)
            thumb_x, thumb_y = int(thumb_tip.x * 1280), int(thumb_tip.y * 720)
            index_x, index_y = int(index_tip.x * 1280), int(index_tip.y * 720)

            # Calculate the distance between thumb tip and index tip
            distance = calculate_distance(thumb_x, thumb_y, index_x, index_y)

            # Define a threshold for when the fingers are considered "touching"
            touching_threshold = 30

            # Check if fingers are touching (hold dart when fingers touch)
            if distance < touching_threshold and not dart_released:
                dart_held = True
            else:
                if dart_held:  # If dart was being held and fingers separate, release it
                    dart_released = True
                    dart_held = False
                    # Dart is released, calculate its offset from the dartboard position
                    dart_offset_x = index_x - x
                    dart_offset_y = index_y - y

                    # Check if the dart hit the dartboard area
                    if (x <= index_x <= x + board.get_width()) and (y <= index_y <= y + board.get_height()):
                        # Dart hit the board, add it to the thrown darts list and calculate the score
                        thrown_darts.append((index_x - x, index_y - y))  # Store dart position relative to board
                        score += calculate_score(index_x, index_y, x, y)
                        missed_message = ""  # Clear any missed message
                    else:
                        # Dart missed the board
                        missed_message = "Missed the board!"

    # Pygame event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Check for mouse clicks on the home button
        if event.type == pygame.MOUSEBUTTONDOWN and current_turn >= turns:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (1120 <= mouse_x <= 1270) and (10 <= mouse_y <= 60):  # Home button dimensions
                # Quit the game
                pygame.quit()
                sys.exit()

    # If dart is being held, follow the index finger
    if index_x is not None and dart_held:
        # Display the dart at the index finger's position
        screen.blit(dart, (index_x - dart.get_width() // 2, index_y - dart.get_height() // 2))

    # After dart is released, check if turns are over
    if dart_released:
        current_turn += 1  # Increment the turn counter
        dart_released = False  # Allow for the next dart throw
        dart_held = False  # Reset dart hold status

    # Display score and turns left
    display_score_and_turns(score, turns - current_turn)

    # If turns are exhausted, draw the home button
    if current_turn >= turns:
        screen.blit(home_button, (1120, 10))  # Draw home button at top right
        # Optionally display a game over message
        game_over_text = font.render("Game Over! Click Home to Exit!", True, (255, 255, 255))
        screen.blit(game_over_text, (10, 130))  # Centered in the screen

    # Display missed message if applicable
    if missed_message:
        missed_text = font.render(missed_message, True, (255, 255, 255))
        screen.blit(missed_text, (10, 90))

    # Update the display
    pygame.display.flip()

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Cap the frame rate
    clock.tick(30)

# Release resources
cap.release()
cv2.destroyAllWindows()
