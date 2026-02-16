import cv2
from detection import FocusDetector
from ui_controller import SoldierUI
from logger import StudyLogger



def main():
    cascade_path = "data/haarcascades/haarcascade_frontalface_default.xml"
    # ... previous setup code ...
    logger = StudyLogger()
    distraction_start = None

    while True:
        cam_frame, distracted = detector.check_presence()
        
        # LOGGING LOGIC
        if distracted and distraction_start is None:
            # You just got distracted
            distraction_start = time.time()
            logger.log_event("DISTRACTION_STARTED")
        elif not distracted and distraction_start is not None:
            # You just came back
            duration = round(time.time() - distraction_start, 2)
            logger.log_event("RETURNED_TO_WORK", duration)
            distraction_start = None
    
    # ASSET PATHS (Make sure your filenames match these!)
    IDLE_VID = "assets/videos/idle_soldier.mp4"
    YELL_VID = "assets/videos/yelling_soldier.mp4"
    YELL_SND = "assets/sounds/drill_sergeant.mp3"

    detector = FocusDetector(cascade_path)
    
    try:
        ui = SoldierUI(IDLE_VID, YELL_VID, YELL_SND)
    except Exception as e:
        print(f"Error loading assets: {e}")
        return

    print("Soldier is on duty. Don't move!")

    while True:
        # 1. Check detection
        cam_frame, distracted = detector.check_presence()
        
        # 2. Get the correct soldier frame
        soldier_frame = ui.play_frame(distracted)

        # 3. Display the Soldier
        if soldier_frame is not None:
            # You can resize this to make the soldier window smaller/larger
            soldier_display = cv2.resize(soldier_frame, (640, 360))
            cv2.imshow("DRILL SERGEANT", soldier_display)

        # Optional: Hide the raw camera feed to save CPU/Focus
        # cv2.imshow("Your Feed", cam_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    detector.cleanup()
    ui.cleanup()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()