from datetime import time

# CHANGE THESE ANYTIME (demo friendly)
CLASS_SCHEDULE = [
    ("Period 1", time(9, 30), time(10, 20)),
    ("Period 2", time(10, 20), time(11, 10)),
    ("Period 3", time(11, 10), time(12, 0)),
    ("Lunch",    time(12, 0),  time(12, 30)),
    ("Period 4", time(12, 30), time(13, 20)),
    ("Period 5", time(13, 20), time(14, 10)),
    ("Period 6", time(14, 10), time(15, 0)),
]

ATTENDANCE_WINDOW_MINUTES = 10   # first 10 minutes only
