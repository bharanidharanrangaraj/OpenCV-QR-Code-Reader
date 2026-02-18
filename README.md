# QR Code & Barcode Reader

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS%20|%20RaspberryPi-lightgrey)

A real-time QR code and barcode scanner built with Python, OpenCV, and pyzbar.
Runs on a live webcam feed with FPS, scan count HUD, duplicate-scan prevention, and multi-format barcode support.

## Features

* 📷 **Live webcam feed** (1280×720 request)
* 🔍 **20 barcode & QR formats supported**
* 🚫 **Duplicate scan prevention** per session
* 🎨 **Color-coded bounding boxes** per barcode type
* 📊 **HUD overlay** with FPS and total scans
* 🖥️ **Console logging** of each unique scan

## Supported Barcode Types

QR Code, EAN-8, EAN-13, UPC-A, UPC-E, Code128, Code39, Code93, Aztec, Codabar, DataBar, Interleaved 2-of-5, and more (via ZBar).

## Requirements

### Software

* Python **3.7 or higher**
* OpenCV
* NumPy
* pyzbar
* **ZBar system library** (mandatory)

> ⚠️ **Important**
> `pyzbar` is only a Python wrapper.
> The actual barcode engine is **ZBar**, which must be installed at the OS level.

## Installation (Correct Way)

### 1. Clone the repository

```bash
git clone https://github.com/bharanidharanrangaraj/OpenCV-QR-Code-Reader.git
cd OpenCV-QR-Code-Reader
```

### 2. Create and activate a virtual environment (mandatory)

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
```

Your terminal **must show `(venv)`** before continuing.

### 3. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install system dependencies (ZBar)

#### Linux (Ubuntu / Debian / Raspberry Pi OS)

```bash
sudo apt update
sudo apt install libzbar0 libzbar-dev -y
```

#### macOS (Homebrew)

```bash
brew install zbar
```

#### Windows

```bash
pip install pyzbar[scripts]
```

Or download the ZBar binary manually from:
[http://zbar.sourceforge.net/](http://zbar.sourceforge.net/)

## Usage

Run the application from inside the virtual environment:

```bash
python qrcode_and_barcode_detection.py
```

### Controls

* Point the webcam at any QR code or barcode
* Detected codes are outlined and labeled
* Each unique code is printed once in the console
* Press **`q`** to quit

On exit, the total number of unique scans is printed.

## Console Output Example

```
QR / Barcode Reader started. Press 'q' to quit.
Decoding 20 symbol types.

[001] [QRCODE]  https://example.com
[002] [CODE128] ABC-abc-1234
[003] [EAN13]   1234567890123

Session ended. Total unique codes scanned: 3
```

## How It Works (High-Level)

* OpenCV captures frames from the webcam
* pyzbar (via ZBar) scans each frame for supported symbols
* Each detected barcode returns:

  * Encoded data
  * Barcode type
  * Polygon corner points
* Duplicate `(type, data)` pairs are ignored
* Bounding boxes, labels, FPS, and scan count are drawn in real time

## Common Issues

### `ImportError: Unable to find zbar shared library`

ZBar is not installed on the system.
Install it using your OS package manager (see above).

### Camera does not open

* Check webcam permissions
* Try changing `VideoCapture(0)` to `VideoCapture(1)`
* Ensure no other application is using the camera

## License

MIT License
Free to use, modify, and distribute.