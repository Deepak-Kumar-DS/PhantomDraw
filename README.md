# ✦ PhantomDraw AI

### Gesture-Controlled Air Drawing & Digital Creative Workspace

PhantomDraw AI is a Python-based creative project that explores gesture-controlled digital drawing using computer vision and hand tracking technology.

The project aims to make digital creativity more interactive by allowing users to draw and interact with drawing tools using hand gestures in front of a webcam.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [Gesture Controls](#-gesture-controls)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Current Development Status](#-current-development-status)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)

---

## 🚀 Overview

PhantomDraw AI is designed to explore the possibilities of touch-free digital drawing.

Using a webcam and hand-tracking technology, the system detects hand landmarks and interprets gestures to perform drawing operations.

The project combines computer vision, gesture recognition, drawing algorithms, and a Python-based graphical interface.

The long-term vision is to develop an advanced digital creative environment where users can interact with drawing tools naturally without depending entirely on traditional mouse input.

---

## ✨ Features

### Air Drawing
- Draw in the air using hand movements.
- Real-time hand tracking.
- Webcam-based interaction.
- Index-finger-based drawing interaction.

### Gesture Interaction
- Hand landmark detection.
- Support for tracking multiple hands.
- Gesture-based interaction.
- Hand movement tracking.

### Drawing Tools
- Multiple brush presets.
- Color selection.
- Brush size adjustment.
- Eraser.
- Undo and Redo.
- Canvas clearing.
- Drawing export as PNG.

### Layer Management
- Multiple drawing layers.
- Add and delete layers.
- Switch between layers.
- Layer visibility control.
- Layer opacity adjustment.

### Desktop Interface
- Python-based graphical interface.
- Dashboard layout.
- Creative workspace navigation.
- Dedicated workspace sections.

*Note: Feature availability depends on the currently implemented module. Some workspace sections are still under development.*

---

## 🛠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Computer vision and webcam processing |
| MediaPipe | Hand tracking and landmark detection |
| NumPy | Numerical and array operations |
| PySide6 | Desktop graphical interface |
| Git | Version control |
| GitHub | Source code hosting |

---

## 💻 System Requirements

Recommended environment:

- Operating System: Windows 10 / Windows 11
- Python: Python 3.11 or 3.12 recommended
- RAM: 8 GB or more recommended
- Webcam: Required for air drawing
- Internet Connection: Required for initial dependency installation
- VS Code or another Python IDE (optional)

A working webcam and compatible Python packages are required for gesture-controlled drawing.

---

## 📥 Installation

Follow these steps to download and set up PhantomDraw AI.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Deepak-Kumar-DS/PhantomDraw.git
```

### Step 2: Open the Project Directory

```bash
cd PhantomDraw
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### Step 5: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 6: Install Dependencies

```bash
pip install opencv-python mediapipe numpy PySide6
```

---

## ▶️ How to Run

PhantomDraw AI currently contains multiple Python entry points.

Run the required module from the root project directory.

### 1. Launch the Desktop Interface

```bash
python main.py
```

This launches the PhantomDraw AI desktop interface.

### 2. Launch Gesture-Controlled Air Drawing

```bash
python test_gesture_drawing.py
```

This launches the webcam-based gesture drawing application.

The application uses hand tracking to detect gestures and control drawing operations.

### 3. Run the Air Drawing Test

```bash
python test_air_drawing.py
```

### 4. Run the Hand Tracking Test

```bash
python test_hand_tracking.py
```

### 5. Run the Basic Drawing Prototype

```bash
python PhantomDraw.py
```

**Important:** Run these commands from the main `PhantomDraw` project directory, not from inside the `core` or `vision` folders.

---

## ✋ Gesture Controls

The gesture drawing module uses hand tracking for drawing and interaction.

Current interaction design:

| Hand | Function |
|---|---|
| First Hand | Air drawing |
| Second Hand | Interface selection |
| Thumb Up | Selection interaction |
| Index Finger | Drawing interaction |

The exact interaction behavior depends on the active gesture-drawing implementation.

---

## 📁 Project Structure

```text
PhantomDraw/
│
├── ai/
│   └── __init__.py
│
├── assets/
│   └── __init__.py
│
├── core/
│   ├── PhantomDraw/
│   ├── drawing_engine.py
│   ├── history_manager.py
│   └── layer_manager.py
│
├── database/
│   └── __init__.py
│
├── exports/
│   ├── __init__.py
│   └── phantomdraw.png
│
├── projects/
│   └── __init__.py
│
├── tests/
│   └── __init__.py
│
├── tools/
│   ├── __init__.py
│   └── brush.py
│
├── ui/
│   ├── __init__.py
│   └── main_window.py
│
├── vision/
│   ├── __init__.py
│   ├── camera.py
│   ├── gesture_detection.py
│   ├── hand_tracking.py
│   └── interaction_controller.py
│
├── voice/
│   └── __init__.py
│
├── PhantomDraw.py
├── config,py
├── layer_manager.py
├── main.py
├── test_air_drawing.py
├── test_gesture_drawing.py
├── test_hand_tracking.py
│
├── .gitignore
└── README.md
```

---

## ⚠️ Troubleshooting

### 1. Camera Not Detected

- Make sure your webcam is connected.
- Check Windows camera permissions.
- Close other applications that may be using the webcam.
- Verify that the correct camera index is being used.

### 2. Module Not Found Error

Install the required packages:

```bash
pip install opencv-python mediapipe numpy PySide6
```

Make sure your virtual environment is activated.

### 3. MediaPipe Installation Error

Check your Python version:

```bash
python --version
```

Use a Python version supported by the installed MediaPipe release.

### 4. Application Does Not Start

Make sure you are running the command from the project root directory.

For example:

```powershell
cd PhantomDraw
python test_gesture_drawing.py
```

---

## 🚧 Current Development Status

PhantomDraw AI is an actively developing project.

The current codebase includes:

- Hand tracking modules.
- Gesture detection.
- Air drawing implementation.
- Drawing engine.
- Brush management.
- Layer management.
- Drawing history operations.
- Desktop interface foundation.

Additional creative tools and workspace modules are planned for future development.

---

## 🔮 Future Improvements

Planned development areas include:

- Advanced gesture recognition.
- Improved multi-hand interaction.
- More drawing tools and brush effects.
- Advanced layer management.
- AI-assisted drawing.
- Smart shape recognition.
- Voice-controlled interaction.
- Animation tools.
- Advanced 3D creative tools.
- Improved desktop experience.

---

## 🤝 Contributing

Contributions, suggestions, and feedback are welcome.

If you want to contribute:

1. Fork this repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Submit a Pull Request.

Please describe your changes clearly when submitting a contribution.

---

## 👨‍💻 Author

**Deepak Kumar Sharma**

GitHub: [@Deepak-Kumar-DS](https://github.com/Deepak-Kumar-DS)

Project: [PhantomDraw AI](https://github.com/Deepak-Kumar-DS/PhantomDraw)

---

## 📄 License

No license has currently been specified for this repository.

Unless a license is added, all rights are reserved by the copyright holder. Public visibility does not automatically grant permission to reuse, modify, or distribute the code.

---

### ⭐ Support

If you find this project interesting, consider giving the repository a Star on GitHub.

Your support and feedback are appreciated!

**Developed by Deepak Kumar Sharma**
