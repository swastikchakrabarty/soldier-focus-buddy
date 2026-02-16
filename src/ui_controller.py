import cv2
import pygame

class SoldierUI:
    def __init__(self, idle_video, yell_video, yell_sound):
        pygame.mixer.init()
        self.yell_sound = pygame.mixer.Sound(yell_sound)
        
        # Load the video captures
        self.idle_cap = cv2.VideoCapture(idle_video)
        self.yell_cap = cv2.VideoCapture(yell_video)
        
        self.is_yelling = False

    def play_frame(self, should_yell):
        target_cap = self.yell_cap if should_yell else self.idle_cap
        
        # Audio Trigger for transition
        if should_yell and not self.is_yelling:
            self.yell_sound.play() # Plays when distraction starts
            self.is_yelling = True
        elif not should_yell:
            self.is_yelling = False
            self.yell_sound.stop() # Stops yelling if you return

        ret, frame = target_cap.read()
        
        # If video ends (Looping)
        if not ret:
            target_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = target_cap.read()
            # If we are in 'yell' mode, restart the sound on video loop
            if should_yell:
                self.yell_sound.play()
            
        return frame

    def cleanup(self):
        self.idle_cap.release()
        self.yell_cap.release()
        pygame.mixer.quit()