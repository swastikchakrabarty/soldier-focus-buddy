import cv2
import time
from detection import FocusDetector
from ui_controller import SoldierUI

def main():
    cascade_path = "data/haarcascades/haarcascade_frontalface_default.xml"
    
    # ASSET PATHS
    IDLE_VID = "assets/videos/idle_soldier.mp4"
    YELL_VID = "assets/videos/yelling_soldier.mp4"
    YELL_SND = "assets/sounds/drill_sergeant.mp3"

    # Initialize components OUTSIDE the loop
    try:
        detector = FocusDetector(cascade_path)
        ui = SoldierUI(IDLE_VID, YELL_VID, YELL_SND)
    except Exception as e:
        print(f"Critical Error during initialization: {e}")
        return

    print("Soldier is on duty. Press 'q' to quit.")

    while True:
        # 1. Check detection
        cam_frame, distracted = detector.check_presence()
        
        if cam_frame is None:
            print("Camera feed lost.")
            break

        # 2. Get the correct soldier frame from the UI controller
        soldier_frame = ui.play_frame(distracted)

        # 3. Display the Soldier window
        if soldier_frame is not None:
            soldier_display = cv2.resize(soldier_frame, (640, 360))
            cv2.imshow("DRILL SERGEANT", soldier_display)

        # Press 'q' to exit safely
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up resources
    detector.cleanup()
    ui.cleanup()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()