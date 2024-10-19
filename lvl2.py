import cv2
import mediapipe as mp
import math
import pygame
import random
import sys
import threading
import time

# Initialize Pygame and OpenCV
pygame.init()
dart_held = False
dart_released = False
score = 0
thrown_darts = []
missed_message = ""
turns = 3
current_turn = 0
bg_page_2 = pygame.image.load(r'bg_page_2.JPG')


# Wind variables
wind_speed = random.uniform(-10, 10)  # Increase wind speed range
wind_direction = random.choice(['Left', 'Right'])  # Random wind direction
wind_effect_multiplier = 20.0  # Increase the wind effect on dart movement

# Set up display for 1280x720 resolution with hardware acceleration
screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('Dart Game')

# Load dartboard and dart images
board = pygame.image.load(r'board.png')
dart = pygame.image.load(r'dart.png')  
dart = pygame.transform.scale(dart, (50, 50))

# Load home button image
home_button = pygame.Surface((150, 50))  
home_button.fill((255, 0, 0))  
button_font = pygame.font.SysFont(None, 35)
button_text = button_font.render("Home", True, (255, 255, 255))
home_button.blit(button_text, (45, 13))


# Initialize dartboard position
x = 200
y = 100

# Set random direction for the board
direction_x = random.choice([-1, 1])
direction_y = random.choice([-1, 1])
speed = 5

# Font for displaying score and wind info
font = pygame.font.SysFont(None, 36)

# Smoothing factors
HAND_SMOOTHING_ALPHA = 0.8
DART_SMOOTHING_ALPHA = 0.5

# Time-based hold variables
dart_hold_start_time = None
dart_release_wait_time = 0.2
movement_threshold = 50

# Function to display the score and turns on the screen
def display_score_and_turns(score, turns_left):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    turns_text = font.render(f"Turns Left: {turns_left}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(turns_text, (10, 50))

# Function to display wind information on the screen
def display_wind_info(wind_speed, wind_direction):
    wind_text = font.render(f"Wind: {wind_speed:.2f} m/s {wind_direction}", True, (255, 255, 255))
    screen.blit(wind_text, (10, 90))

# Function to calculate distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Function to calculate score based on distance from the center of the board
def calculate_score(dart_x, dart_y, board_x, board_y):
    board_center_x = board_x + board.get_width() // 2
    board_center_y = board_y + board.get_height() // 2
    distance = calculate_distance(dart_x, dart_y, board_center_x, board_center_y)
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
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Threading to handle OpenCV processing separately
frame = None
results = None

# Variables for storing previous positions for smooth movements
prev_landmarks = None
dart_pos = (0, 0)  # Initialize dart position

def smooth_landmarks(prev_landmarks, new_landmarks, alpha=HAND_SMOOTHING_ALPHA):
    if prev_landmarks is None:
        return new_landmarks
    smoothed_landmarks = []
    for prev, new in zip(prev_landmarks, new_landmarks):
        smoothed_x = prev[0] * alpha + new[0] * (1 - alpha)
        smoothed_y = prev[1] * alpha + new[1] * (1 - alpha)
        smoothed_landmarks.append((smoothed_x, smoothed_y))
    return smoothed_landmarks

def process_webcam():
    global frame, results
    frame_counter = 0
    while cap.isOpened():
        ret, new_frame = cap.read()
        if not ret:
            break
        
        frame_counter += 1
        if frame_counter % 2 != 0:
            continue
        
        new_frame = cv2.resize(new_frame, (640, 360))
        new_frame = cv2.flip(new_frame, 1)
        rgb_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        frame = new_frame

# Start the webcam processing in a separate thread
webcam_thread = threading.Thread(target=process_webcam)
webcam_thread.start()

# Main Pygame loop
while cap.isOpened():
    if frame is None:
        continue

    index_x, index_y = None, None
    x += direction_x * speed
    y += direction_y * speed

    if x <= 0 or x >= 1280 - board.get_width():
        direction_x *= -1
    if y <= 0 or y >= 720 - board.get_height():
        direction_y *= -1

    screen.blit(bg_page_2, (0, 0))
    dart_board(x, y)

    for dart_data in thrown_darts:
        stuck_dart_x, stuck_dart_y = dart_data
        screen.blit(dart, (stuck_dart_x - dart.get_width() // 2 + x, stuck_dart_y - dart.get_height() // 2 + y))

    if current_turn < turns:
        if results and results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                new_landmarks = []
                for lm in hand_landmarks.landmark:
                    lm_x = int(lm.x * 1280)
                    lm_y = int(lm.y * 720)
                    new_landmarks.append((lm_x, lm_y))

                smoothed_landmarks = smooth_landmarks(prev_landmarks, new_landmarks)
                prev_landmarks = smoothed_landmarks

                for connection in mp_hands.HAND_CONNECTIONS:
                    start_idx, end_idx = connection
                    start_pos = smoothed_landmarks[start_idx]
                    end_pos = smoothed_landmarks[end_idx]
                    pygame.draw.line(screen, (0, 255, 0), start_pos, end_pos, 2)

                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                thumb_x, thumb_y = int(thumb_tip.x * 1280), int(thumb_tip.y * 720)
                index_x, index_y = int(index_tip.x * 1280), int(index_tip.y * 720)

                distance = calculate_distance(thumb_x, thumb_y, index_x, index_y)

                if distance < movement_threshold:
                    if not dart_held:
                        dart_held = True
                        dart_hold_start_time = time.time()
                else:
                    if dart_held:
                        current_time = time.time()
                        if current_time - dart_hold_start_time >= dart_release_wait_time:
                            dart_released = True
                            dart_held = False
                            dart_offset_x = index_x - x + 1
                            dart_offset_y = index_y - y + 1

                            # Apply wind effects on dart's movement
                            dart_x_movement = dart_offset_x + (wind_speed * wind_effect_multiplier if wind_direction == 'Right' else -wind_speed * wind_effect_multiplier)
                            dart_y_movement = dart_offset_y  # No wind effect on vertical movement
                            
                            if (x <= index_x <= x + board.get_width()) and (y <= index_y <= y + board.get_height()):
                                thrown_darts.append((dart_x_movement, dart_y_movement))
                                score += calculate_score(index_x, index_y, x, y)
                                missed_message = ""
                            else:
                                missed_message = "Missed the board!"
                
                if dart_held:
                    dart_pos = (
                        index_x,  # Directly follow the index finger
                        index_y
                    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and current_turn >= turns:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (1120 <= mouse_x <= 1270) and (10 <= mouse_y <= 60):
                pygame.quit()
                sys.exit()

    if dart_held:
        screen.blit(dart, (dart_pos[0] - dart.get_width() // 2, dart_pos[1] - dart.get_height() // 2))

    if dart_released:
        current_turn += 1
        dart_released = False

    display_score_and_turns(score, turns - current_turn)
    display_wind_info(wind_speed, wind_direction)

    if current_turn >= turns:
        screen.blit(home_button, (1120, 10))
        screen.blit(home_button, (1120, 10))
        game_over_text = font.render("Game Over! Click Home to Exit!", True, (255, 255, 255))
        screen.blit(game_over_text, (10, 130))

    if missed_message:
        missed_text = font.render(missed_message, True, (255, 255, 255))
        screen.blit(missed_text, (10, 150))

    pygame.display.flip()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()
