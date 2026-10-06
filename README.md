# Smart Face Recognition Attendance System

A smart and automated attendance management system built using Python, OpenCV, YuNet, and SFace.

The system uses a webcam to detect and recognize registered students and automatically records their attendance with Student ID, name, date, and time.

---

## 📌 Project Overview

The **Smart Face Recognition Attendance System** is designed to automate the traditional attendance process using face detection and face recognition technology.

Instead of manually taking attendance, students can register their face through the camera. During attendance, the system detects faces, compares them with registered face features, identifies the student, and records attendance automatically.

The project also includes attendance search, filtering, analytics, student management, report export, and a graphical user interface.

---

## ✨ Features

### 👤 Student Registration
- Register students using a webcam.
- Enter Student ID and Student Name.
- Capture multiple face samples.
- Generate face features using SFace.
- Store registered face features in JSON format.

### 🔐 Duplicate Face Protection
- Prevents the same face from being registered with another Student ID.
- Compares the newly captured face with existing registered faces.
- Uses a recognition threshold to identify duplicate registrations.

### 📷 Face Detection
- Uses **YuNet** for real-time face detection.
- Detects faces through the computer webcam.
- Works with live camera input.

### 🧠 Face Recognition
- Uses **SFace** for face recognition.
- Compares detected faces with registered face features.
- Identifies registered students automatically.
- Displays an **UNKNOWN FACE** result when a face is not recognized.

### 📝 Automatic Attendance
- Records attendance automatically after successful recognition.
- Stores:
  - Student ID
  - Student Name
  - Date
  - Time
  - Attendance Status
- Prevents duplicate attendance for the same student on the same day.

### 📊 Dashboard
The system provides an attendance dashboard showing:

- Total registered students
- Students present today
- Students not marked today
- Attendance percentage
- System status
- Recognition engine
- Detection engine

### 🔎 Attendance Search & Filtering

Attendance records can be searched using:

- Student ID
- Student Name
- Date
- Date Range
- Show All Records

### 📈 Attendance Analytics

The system provides:

- Today's attendance percentage
- Overall attendance percentage
- Total attendance records
- Student-wise attendance information
- Top attending student
- Recent attendance records

### 👨‍🎓 Student Management

The system allows users to:

- View registered students
- View individual attendance summaries
- Remove registered students

### 📄 Attendance Reports

Attendance data can be exported as an attendance report for further use.

### 🖥️ Graphical User Interface

The project includes a graphical interface for easier interaction with the attendance system.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| OpenCV | Computer vision and camera processing |
| YuNet | Face detection |
| SFace | Face recognition |
| NumPy | Numerical and feature processing |
| JSON | Registered face feature storage |
| CSV | Attendance record storage |
| Tkinter | Graphical User Interface |
| Git | Version control |
| GitHub | Project hosting |

---

## 🧠 How the System Works

The system follows this general workflow:


             ┌───────────────────┐
             │      Webcam       │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │  YuNet Detection  │
             │   Detect Face     │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │  SFace Recognition│
             │ Extract Features  │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ Compare with      │
             │ Registered Faces  │
             └─────────┬─────────┘
                       │
                ┌──────┴──────┐
                │             │
                ▼             ▼
        ┌──────────────┐  ┌──────────────┐
        │   Recognized │  │    Unknown   │
        │    Student   │  │     Face     │
        └──────┬───────┘  └──────────────┘
               │
               ▼
        ┌──────────────┐
        │ Check Today's│
        │  Attendance  │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │ Record Name, │
        │ Date & Time  │
        └──────────────┘

🔄 Registration Process:
1. Start the application.
2. Select Register New Person.
3. Enter Student ID.
4. Enter Student Name.
5. The webcam starts.
6. The system detects the face.
7. Multiple face samples are captured.
8. SFace generates face features.
9. The system checks whether the face already exists.
10. If the face is new, the student is registered.
11. The face feature is stored in the JSON file.

📸 Attendance Process:
1. Start the application.
2. Select Start Attendance.
3. The webcam starts.
4. YuNet detects the face.
5. SFace extracts the face feature.
6. The feature is compared with registered students.
7. If the student is recognized:
   - Student ID is identified.
   - Student name is identified.
   - Today's attendance is checked.
   - Attendance is recorded if not already marked.
8. If the face is not recognized:
   - The system displays UNKNOWN FACE.
   - Attendance is not recorded.

📁 Project Structure:
smart-face-attendance/
│
├── models/
│   ├── face_detection_yunet_2023mar.onnx
│   └── face_recognition_sface_2021dec.onnx
│
├── data/
│   └── registered_faces.json
│
├── smart_face_attendance.py
├── smart_face_attendance_v4_working.py
├── smart_face_attendance_before_gui.py
│
├── smart_face_attendance_gui.py
├── smart_face_attendance_gui_new.py
├── smart_face_attendance_gui_complete.py
├── smart_face_attendance_gui_final.py
│
├── attendance.csv
├── requirements.txt
└── README.md

⚙️ Requirements:
- Windows / Linux / macOS
- Python 3.x
- Webcam
- OpenCV
- NumPy
- Tkinter

The required Python packages are listed in:
   - requirements.txt
   
   🚀 Installation:
1. Clone the repository
   - git clone https://github.com/Mustak2005/smart-face-attendance.git
2. Open the project
   - cd smart-face-attendance
3. Install dependencies
   - pip install -r requirements.txt
4. Run the application
   - python smart_face_attendance_before_gui.py

🖥️ Application Menu:

The system provides the following options:

1. Dashboard
2. Register New Person
3. Start Attendance
4. View Today's Attendance
5. View Attendance History
6. Search Attendance History
7. Export Attendance Report
8. View Registered Students
9. Student Attendance Summary
10. Remove Registered Student
11. Attendance Statistics
12. Exit

💾 Data Storage:

The project uses local files for data storage.

Registered Students:
   - Registered face features are stored in:
         - data/registered_faces.json
Attendance Records:
   -Attendance records are stored in:
      - attendance.csv

The project does not require an online database for its basic operation.

🔒 Recognition & Attendance Logic:

The system uses a face recognition threshold to determine whether a detected face matches a registered student.

If the similarity score meets the required threshold:
   - Recognized Student

Otherwise:
   - UNKNOWN FACE

Unknown faces are not added to the attendance records.

The system also checks whether the student has already been marked present on the current date to prevent duplicate attendance entries.

🎯 Advantages:
- Automated attendance
- Reduces manual attendance work
- Real-time face detection
- Face recognition
- Duplicate registration protection
- Unknown face detection
- Duplicate attendance prevention
- Attendance analytics
- Search and filtering
- Student management
- Local data storage
- GUI-based interaction
 -Can work without an online database

🔮 Future Enhancements:

Possible future improvements include:
- Admin login and authentication
- Cloud database integration
- Web-based dashboard
- Mobile application
- Email/SMS attendance notifications
- Multiple camera support
- Advanced anti-spoofing/liveness detection
- Department and class management
- Monthly and semester reports
- Cloud backup
- Role-based access control

🎓 Learning Outcomes:

Through this project, the following concepts were practiced:
- Python programming
- Object-oriented programming concepts
- OpenCV
- Computer vision
- Face detection
- Face recognition
- NumPy
- JSON data handling
- CSV data handling
- File handling
- GUI development
- Data processing
- Git and GitHub
- Project structure and version control

👨‍💻 Author

Shaik Mohammed Mustak

Computer Science Student & Developer

GitHub:
https://github.com/Mustak2005

📌 Project Status

Status: Completed ✅

The core face detection, face recognition, registration, attendance management, analytics, search/filtering, student management, report export, and GUI functionality have been implemented.

⭐ If you find this project useful

Feel free to explore the repository and use the project as a learning reference.

Developed by Shaik Mohammed Mustak