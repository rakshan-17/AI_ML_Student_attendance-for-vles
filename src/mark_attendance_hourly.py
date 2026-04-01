


import cv2
import face_recognition
import pickle
import os
from datetime import datetime, time

# ---------------- CONFIG ----------------
ENCODINGS_PATH = "encodings/face_encodings.pkl"
ATTENDANCE_DIR = "attendance"
ATTENDANCE_WINDOW_MINUTES = 10

CLASS_SCHEDULE = [
    ("09:30", "10:20", "Period 1"),
    ("10:20", "11:10", "Period 2"),
    ("11:10", "12:00", "Period 3"),
    ("12:30", "13:20", "Period 4"),
    ("13:20", "14:10", "Period 5"),
    ("14:10", "15:00", "Period 6"),
]

# ----------------------------------------
from datetime import datetime, timedelta

def str_to_time(t):
    return datetime.strptime(t, "%H:%M").time()

def get_current_period():
    now = datetime.now()

    for start, end, name in CLASS_SCHEDULE:
        start_t = datetime.combine(datetime.today(), str_to_time(start))

        attendance_end = start_t + timedelta(minutes=ATTENDANCE_WINDOW_MINUTES)

        if start_t <= now <= attendance_end:
            return name

    return None



# Load encodings
print("[INFO] Loading face encodings...")
with open(ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)

# Support both tuple and dict formats
if isinstance(data, tuple):
    known_encodings, known_names = data
elif isinstance(data, dict):
    known_encodings = data["encodings"]
    known_names = data["names"]
else:
    raise ValueError("Unknown encoding file format")

print(f"[INFO] Loaded {len(known_names)} face encodings")


# Attendance storage
today = datetime.now().strftime("%Y-%m-%d")
attendance_file = os.path.join(ATTENDANCE_DIR, f"{today}.csv")
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

attendance = {}

for _, _, period in CLASS_SCHEDULE:
    attendance[period] = {name: "Absent" for name in set(known_names)}

# Camera
cap = cv2.VideoCapture(0)
print("[INFO] AI Attendance System Started")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    current_period = get_current_period()

    if current_period:
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            if True in matches:
                best_match = face_distances.argmin()
                name = known_names[best_match]
                attendance[current_period][name] = "Present"
                print(f"[ATTENDANCE] {name} marked PRESENT for {current_period}")

        cv2.putText(
            frame,
            f"Marking Attendance: {current_period}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
    else:
        cv2.putText(
            frame,
            "Attendance Closed",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

    cv2.imshow("AI Hourly Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# Save attendance
with open(attendance_file, "w") as f:
    f.write("Name," + ",".join(attendance.keys()) + "\n")
    for name in set(known_names):
        row = [attendance[p][name] for p in attendance]
        f.write(name + "," + ",".join(row) + "\n")

print(f"[INFO] Attendance saved to {attendance_file}")
