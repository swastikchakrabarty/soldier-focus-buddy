# 🎖️ AI-Powered Soldier "Focus" Buddy

A digital Drill Sergeant that uses Computer Vision to ensure you stay productive. This isn't just a timer; it's an interactive enforcer that monitors your presence and behavior in real-time.

## 🚀 Features
- **Presence Detection:** Uses Haar Cascades to detect if you've left your post (AWOL).
- **Phone Distraction Check:** Monitors Skin-Tone HSV clusters to detect hands/phones near the face.
- **Dynamic Drill Sergeant:** Features a soldier that "lives" on your screen, yelling audio/video cues when you slack off.
- **Low-End Optimized:** Designed for Debian 12, running efficiently on older hardware without heavy Neural Networks.

## 🛠️ Tech Stack
- **Language:** Python 3.11+
- **Vision:** OpenCV (Haar Cascades, HSV Filtering)
- **Audio/UI:** Pygame, OpenCV Multi-threading
- **OS:** Debian 12 (Bookworm)

## 📦 Installation
1. Clone the repo:
   ```bash
   git clone [https://github.com/swastikchakrabarty/soldier-focus-buddy.git](https://github.com/swastikchakrabarty/soldier-focus-buddy.git)
   cd soldier-focus-buddy