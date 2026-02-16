import csv
from datetime import datetime
import os

class StudyLogger:
    def __init__(self, filename="data/study_log.csv"):
        self.filename = filename
        # Create data folder if it doesn't exist
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        # Initialize CSV with headers if it's new
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Event", "Duration_Seconds"])

    def log_event(self, event_type, duration=0):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                event_type,
                duration
            ])