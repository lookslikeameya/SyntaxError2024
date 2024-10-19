import cv2
import mediapipe as mp
import math
import pygame
import random

# Initialize Pygame and OpenCV
pygame.init()
dart_held = False  # True when dart is held by fingers
dart_released = False  # True when dart is released and stuck to board
score = 0  # Initialize the score

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Dart Game')

# Load dartboard and dart images
board = pygame.image.load(r'board.png')
dart = pygame.image.load(r'dart.png')  # Load your dart image here
dart = pygame.transform.scale(dart, (50, 50))  # Scale dart image if necessary

# Initialize dartboard position
x = 200
y = 100

# Dart position relative to dartboard after release
dart_offset_x = 0
dart_offset_y = 0

# Set random direction for the board
direction_x = random.choice([-1, 1])
direction_y = random.choice([-1, 1])
speed = 3  # Speed of movement

# Font for displaying score
font = pygame.font.SysFont(None, 36)

# Function to display the score on the screen
def display_score(score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

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

    # Define score zones based on distance (adjust these thresholds as needed)
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

    # Process the frame to detect hands
    results = hands.process(rgb_frame)

    # Initialize index finger coordinates to None
    index_x, index_y = None, None

    # Update dartboard position
    x += direction_x * speed
    y += direction_y * speed

    # Check for boundary collisions and reverse direction if it hits the screen edges
    if x <= 0 or x >= 800 - board.get_width():
        direction_x *= -1
    if y <= 0 or y >= 600 - board.get_height():
        direction_y *= -1

    # Fill the screen with a color
    screen.fill((0, 0, 0))
    dart_board(x, y)

    # If hands are detected and dart hasn't been released
    if results.multi_hand_landmarks and not dart_released:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get pixel coordinates for all landmarks
            height, width, _ = frame.shape
            landmarks = []

            for lm in hand_landmarks.landmark:
                lm_x = int(lm.x * 800)
                lm_y = int(lm.y * 600)
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

            # Get pixel coordinates for both points
            thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
            index_x, index_y = int(index_tip.x * width), int(index_tip.y * height)

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

                    # Calculate score when dart is released
                    score += calculate_score(index_x, index_y, x, y)

    # Pygame event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # If dart is being held, follow the index finger
    if index_x is not None and dart_held:
        # Convert index finger coordinates to match Pygame's resolution
        pygame_index_x = int(index_x * (800 / width))
        pygame_index_y = int(index_y * (600 / height))

        # Display the dart at the index finger's position
        screen.blit(dart, (pygame_index_x - dart.get_width() // 2, pygame_index_y - dart.get_height() // 2))

    # After dart is released, make it stick to the dartboard and move with it
    if dart_released:
        dart_pos_x = x + dart_offset_x
        dart_pos_y = y + dart_offset_y
        screen.blit(dart, (dart_pos_x - dart.get_width() // 2, dart_pos_y - dart.get_height() // 2))

    # Display the score
    display_score(score)

    # Update the display
    pygame.display.flip()

    # Show the output frame in OpenCV
   

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Cap the frame rate
    clock.tick(30)

# Release resources
cap.release()
cv2.destroyAllWindows()
