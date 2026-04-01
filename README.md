# AI-Based Face Recognition Attendance System

An AI-powered student attendance system that uses **face recognition** to automatically mark attendance through a webcam.

## 📌 Project Overview

This project is designed to reduce manual attendance work in classrooms by recognizing student faces and recording attendance automatically.

The system:
- Detects faces from a live webcam feed
- Matches them with pre-stored student face encodings
- Marks attendance automatically
- Supports **hour-wise attendance**
- Allows attendance only during the **first few minutes of each class**

---

## 🚀 Features

- Face detection and recognition using AI
- Automatic attendance marking
- Hour-wise attendance support
- Configurable attendance window (e.g., first 10 minutes)
- Attendance stored digitally in CSV format
- Easy to run and demo

---

## 🛠️ Technologies Used

- **Python**
- **OpenCV**
- **face_recognition**
- **NumPy**
- **Pickle**
- **CSV**

---

## 📂 Project Structure

```bash
AI_ML_std_attendance/
│
├── dataset/                     # Not uploaded (contains student face images)
│   ├── Student1/
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   └── ...
│
├── encodings/
│   ├── encode_face.py
│   └── face_encodings.pkl       # Generated after encoding
│
├── src/
│   └── mark_attendance_hourly.py
│
├── attendance/                  # Not uploaded (auto-generated attendance files)
│
├── requirements.txt
└── README.md
