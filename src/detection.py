import cv2
import numpy as np
import time

class FocusDetector:
    def __init__(self, cascade_path):
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.cap = cv2.VideoCapture(0)
        self.last_seen_time = time.time()
        self.is_distracted = False
        
        # Skin Color range in HSV
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    def is_talking(self, frame, face_rect):
        x, y, w, h = face_rect
        # ROI for the mouth (bottom 1/3 of the face)
        mouth_roi = frame[y + int(2*h/3):y + h, x:x + w]
        gray_mouth = cv2.cvtColor(mouth_roi, cv2.COLOR_BGR2GRAY)
        
        # Calculate Laplacian variance (measures 'sharpness' and movement)
        variance = cv2.Laplacian(gray_mouth, cv2.CV_64F).var()
        return variance # If this value jumps, the mouth is moving

    def detect_phone_motion(self, frame, face_rect):
        x, y, w, h = face_rect
        # Create an ROI around the face but slightly wider (to catch hands near ears)
        padding = 40
        roi_x = max(0, x - padding)
        roi_y = max(0, y - padding)
        roi_w = w + (padding * 2)
        roi_h = h + (padding * 2)
        
        roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Create a mask that only shows skin-colored pixels
        mask = cv2.inRange(hsv_roi, self.lower_skin, self.upper_skin)
        
        # Count skin pixels. If you bring your hand up, pixel count spikes.
        skin_pixel_count = cv2.countNonZero(mask)
        return skin_pixel_count

    def check_presence(self):
        ret, frame = self.cap.read()
        if not ret: return None, False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.2, 7, minSize=(50, 50))

        if len(faces) > 0:
            self.last_seen_time = time.time()
            
            # Check for phone/hand near face
            skin_count = self.detect_phone_motion(frame, faces[0])
            
            # Threshold: If skin pixels exceed a certain amount, 
            # it means a hand is likely near the face.
            # You might need to adjust '40000' based on your camera resolution.
            if skin_count > 45000: 
                self.is_distracted = True
                print(f"PHONE DETECTED! (Skin Count: {skin_count})", end="\r")
            else:
                self.is_distracted = False
                print(f"Focused... (Skin Count: {skin_count})   ", end="\r")
        else:
            if time.time() - self.last_seen_time > 3:
                self.is_distracted = True

        return frame, self.is_distracted

    def cleanup(self):
        self.cap.release()