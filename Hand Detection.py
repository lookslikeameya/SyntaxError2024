import cv2
import mediapipe as mp
import math

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

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

    # If hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of the thumb tip (landmark 4) and index finger tip (landmark 8)
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]

            # Get pixel coordinates for both points
            height, width, _ = frame.shape
            thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
            index_x, index_y = int(index_tip.x * width), int(index_tip.y * height)

            # Calculate the distance between thumb tip and index tip
            distance = calculate_distance(thumb_x, thumb_y, index_x, index_y)

            # Define a threshold for when the fingers are considered "touching"
            touching_threshold = 30  # Adjust this value depending on your camera's resolution

            # Output the coordinates of the thumb and index finger
            print(f'Thumb: ({thumb_x}, {thumb_y}), Index: ({index_x}, {index_y})')

            # Check if fingers are connected
            if distance < touching_threshold:
                print("Fingers Connected!")
            else:
                print("Fingers Apart")

    # Show the output frame
    cv2.imshow("Hand Detection", frame)

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
