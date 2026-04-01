import face_recognition
import cv2
import pickle
import csv
import os
from datetime import datetime, timedelta
from config import CLASS_SCHEDULE, ATTENDANCE_WINDOW_MINUTES

ENCODINGS_PATH = "encodings/face_encodings.pkl"
ATTENDANCE_DIR = "attendance"

os.makedirs(ATTENDANCE_DIR, exist_ok=True)

with open(ENCODINGS_PATH, "rb") as f:
    known_encodings, known_names = pickle.load(f)

today = datetime.now().strftime("%Y-%m-%d")
attendance_file = f"{ATTENDANCE_DIR}/attendance_{today}.csv"

if not os.path.exists(attendance_file):
    with open(attendance_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Period", "Status", "Time"])

marked = set()

cap = cv2.VideoCapture(0)
print("[INFO] AI Attendance System Started")

while True:
    now = datetime.now()
    current_time = now.time()

    for period, start, end in CLASS_SCHEDULE:
        if period == "Lunch":
            continue

        window_end = (datetime.combine(now.date(), start) +
                      timedelta(minutes=ATTENDANCE_WINDOW_MINUTES)).time()

        if start <= current_time <= window_end:
            ret, frame = cap.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            locations = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, locations)

            present_students = set()

            for encoding in encodings:
                matches = face_recognition.compare_faces(known_encodings, encoding)
                if True in matches:
                    name = known_names[matches.index(True)]
                    present_students.add(name)

            for student in set(known_names):
                key = (student, period)

                if key in marked:
                    continue

                status = "Present" if student in present_students else "Absent"

                with open(attendance_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([student, period, status, now.strftime("%H:%M:%S")])

                marked.add(key)
                print(f"[ATTENDANCE] {student} - {period} - {status}")

    cv2.imshow("AI Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
