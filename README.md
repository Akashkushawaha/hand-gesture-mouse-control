# hand-gesture-mouse-control ✅

**AI-powered hand gesture recognition for mouse control**

---

## Overview

This project provides a simple, lightweight way to control the mouse using hand gestures detected via MediaPipe and OpenCV. It offers a starting point for building gesture-driven interactions such as pointer movement, clicks, and custom gesture mappings.

## Features

- Detects single-hand landmarks using MediaPipe
- Displays landmarks on an OpenCV window for live feedback
- Designed to integrate with `pyautogui` for mapping gestures to mouse actions

## Installation 🔧

Clone the repo and install runtime dependencies:

```bash
git clone https://github.com/Akashkushawaha/hand-gesture-mouse-control.git
cd hand-gesture-mouse-control
pip install -r requirements.txt
```

> Note: `requirements.txt` contains the runtime deps (OpenCV, MediaPipe, pyautogui, numpy, Pillow). See `setup.py` for package metadata.

## Usage ▶️

A minimal detection script is available in `src/core/gesture_detector.py`. Run it to open a camera window and visualize landmarks:

```bash
python -m src.core.gesture_detector
```

Press `q` to quit the live demo. For production usage, integrate gesture outputs with `pyautogui` to perform mouse moves/clicks.

## Development & Tests 🧪

This repository includes placeholders for unit tests under `tests/`. To run tests (once implemented):

```bash
pytest -q
```

## Contributing 🤝

Contributions are welcome. Please open an issue or a PR and follow project guidelines in `CONTRIBUTING.md`.

## License 📄

This project is licensed under the MIT License. See `LICENSE` for details.

---

**Quick tips:** If your camera does not open, ensure correct camera device id and permissions. Use a virtual environment for installs.
