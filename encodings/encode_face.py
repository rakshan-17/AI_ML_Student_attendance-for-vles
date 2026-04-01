import face_recognition
import os
import pickle

DATASET_PATH = "dataset"
ENCODINGS_PATH = "encodings/face_encodings.pkl"

known_encodings = []
known_names = []

print("[INFO] Encoding faces...")

for student in os.listdir(DATASET_PATH):
    student_path = os.path.join(DATASET_PATH, student)

    if not os.path.isdir(student_path):
        continue

    for img in os.listdir(student_path):
        img_path = os.path.join(student_path, img)

        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(student)
        else:
            print(f"[WARNING] No face found in {img_path}")

os.makedirs("encodings", exist_ok=True)

with open(ENCODINGS_PATH, "wb") as f:
    pickle.dump((known_encodings, known_names), f)

print("[INFO] Face encodings saved successfully")
