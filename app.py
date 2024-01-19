import streamlit as st
import cv2
import mediapipe as mp
import time
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Streamlit UI
st.set_page_config(
    page_title="Gym Trainer",
    page_icon="💪",
    layout="centered"
)

# Title
new_title = '<p style="font-size: 42px; color:white; font-weight: bold; text-align: center; line-height: 1.5;">Gym Posture Corrector</p>'
read_me_0 = st.markdown(new_title, unsafe_allow_html=True)

# Pose Selection Dropdown
selected_pose = st.selectbox("Select Pose", ["About", "Push-ups", "Leg Raises", "Dumbbell"])

# Webcam setup
cap = cv2.VideoCapture(0)

# Streamlit placeholders
image_placeholder = st.empty()
status_box = st.empty()

# Process frames function
def process_frames():
    global correct_posture_list  # Use global variable

    while True:
        # Read frame from webcam
        ret, frame = cap.read()

        # Pose Detection
        results = pose.process(frame)

        # Display developer information when "About" pose is selected
        if selected_pose == "About":
            status_box.markdown(
                f'<div style="background-color:gray;padding:10px;border-radius:10px;text-align:center">'
                f'<h3 style="color:#333333;font-weight:bold;">Welcome to our Gym Pose Detection project</h3>'
                f'<p>Crafted by Griffine Powered by MediaPipe</p>'
                f'<p>Our system offers real-time analysis of human poses during gym exercises. The integration of Streamlit ensures a seamless and user-friendly experience, allowing for quick deployment and easy sharing. Experience the benefits of instant feedback through positive and negative messages, guiding you towards impeccable form.Visual cues, represented by green lines for correct poses and red lines for errors, enhance your workout journey by fostering better posture and form. Elevate your fitness experience with our innovative Gym Pose Detection project</p>'
                f'</div>', 
                unsafe_allow_html=True)
        else:
            # Clear the status box in each iteration
            status_box.empty()
            status_box.text(process_frames.pose_status)  # Display pose status

            correct_posture = False

            # Pose-specific logic based on user selection
            if selected_pose == "Push-ups" and results.pose_landmarks:
                # Placeholder logic for push-ups
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
                right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]

                # Example: Check if elbows are close to the shoulders
                correct_posture = (abs(left_shoulder.x - left_elbow.x) < 0.1 and abs(right_shoulder.x - right_elbow.x) < 0.1)

            elif selected_pose == "Leg Raises" and results.pose_landmarks:
                # Placeholder logic for leg raises
                left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
                right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
                left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
                right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]

                # Example: Check if knees are close to the hips
                correct_posture = (abs(left_hip.y - left_knee.y) < 0.1 and abs(right_hip.y - right_knee.y) < 0.1)

            elif selected_pose == "Dumbbell" and results.pose_landmarks:
                 # Enhanced logic for dumbbell
                left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
                right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
                nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

    # Check if both wrists are above the nose (holding dumbbells)
                correct_posture = (
                    left_wrist.y < nose.y and
                    right_wrist.y < nose.y and
                    abs(left_wrist.x - right_wrist.x) < 0.1
                                                                 )

            # Draw landmarks based on correct posture
            annotated_frame = np.copy(frame)
            mp_drawing = mp.solutions.drawing_utils
            if correct_posture:
                mp_drawing.draw_landmarks(annotated_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
            else:
                mp_drawing.draw_landmarks(annotated_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

            # Display the annotated frame
            image_placeholder.image(annotated_frame, channels="BGR", use_column_width=True)

            # Update the pose status only when there is a change
            if correct_posture != process_frames.prev_posture:
                process_frames.pose_status = f"Correct {selected_pose} Posture" if correct_posture else f"Incorrect {selected_pose} Posture"
                process_frames.prev_posture = correct_posture

        # Introduce a sleep interval to control the frame rate
        time.sleep(0.5)

# Initialize variables within the function
process_frames.prev_posture = None
process_frames.pose_status = None

# Call the processing function
process_frames()