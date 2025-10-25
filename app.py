import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av, cv2

st.set_page_config(page_title="Day 6 – Live Bot Control", page_icon="🤖", layout="centered")
st.title("🤖 Live Hand-Gesture Bot Control with Face Detection")
st.markdown("""
Allow camera access and show gestures in front of your webcam:  
✋ Stop ⬆️ Forward ⬇️ Backward ⬅️ Left ➡️ Right  
A command will appear in real-time.  
""")

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
fist_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "fist.xml") if cv2.data.haarcascades else None
palm_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "palm.xml") if cv2.data.haarcascades else None

class BotController(VideoTransformerBase):
    def __init__(self):
        self.last_command = "STOP"

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect face
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        driver_present = len(faces) > 0

        # Detect hand (simple area check)
        hands = []
        if palm_cascade and not palm_cascade.empty():
            hands = palm_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw face boxes
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Decide command (placeholder demo logic)
        command = "STOP"
        if not driver_present:
            command = "STOP (NO FACE)"
        elif len(hands) > 0:
            (x, y, w, h) = hands[0]
            center_x = x + w/2
            if center_x < img.shape[1]*0.33:
                command = "LEFT"
            elif center_x > img.shape[1]*0.66:
                command = "RIGHT"
            elif h > w:       # tall hand
                command
