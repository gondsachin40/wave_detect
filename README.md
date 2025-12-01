# wave_detect
This Python script detects the presence of a hand using your webcam. If a hand is continuously detected for 3 seconds, it triggers a custom action. OpenCV is used for video capture and display, while MediaPipe is used for hand landmark detection.



REQUIREMENTS

Python 3.7 or above
Install required packages:
pip install opencv-python mediapipe
Or if you use pip3:
pip3 install opencv-python mediapipe

HOW TO RUN
Save the script as:
wave_detect.py
Run the script:
python wave_detect.py

How it works:
Your webcam will turn on.
Hold your hand up and keep it visible for 3 seconds.
After 3 seconds of continuous hand detection, the script prints:
"🚨 Wave detected for 3 seconds! Triggering action..."
Stop the program:
Press the ESC key to exit the window.

CODE BEHAVIOR

The script does the following:
Opens the webcam using OpenCV.
Uses MediaPipe Hands to detect a hand.
Draws hand landmarks on the video feed.
Starts a timer when a hand is detected.
If the hand remains visible for 3 seconds:
-> trigger_action() is executed.

If the hand disappears, the timer resets.
