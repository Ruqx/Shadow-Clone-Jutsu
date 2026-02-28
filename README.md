# 🥷 Naruto Shadow Clone Jutsu (Computer Vision Project)

A real-time computer vision project that recreates the **Shadow Clone Jutsu** effect inspired by Naruto.

When the user performs the Naruto hand sign (crossed index fingers), 6 live clones appear — 3 on the left and 3 on the right — making a total of 7 characters on screen.

All clones move in real-time and mimic the user's movements.

---

##  Demo Concept

Inspired by the Shadow Clone technique from the anime **Naruto**.

When activated:
- The background remains intact
- The original user stays in the center
- 3 clones appear on the left
- 3 clones appear on the right
- All clones move exactly like the user

---

## Features

- Real-time hand sign detection using MediaPipe Hands
- Real-time person segmentation using MediaPipe Selfie Segmentation
- Live animated clones (not frozen frames)
- Toggle activation using Naruto hand sign
- Symmetrical clone placement (3 left, 3 right)
- Runs entirely on CPU

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

---

```bash
git clone https://github.com/your-username/naruto-shadow-clone.git
cd naruto-shadow-clone
