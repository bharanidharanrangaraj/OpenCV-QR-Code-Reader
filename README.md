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


## Complete Setup Guide (From Scratch)

### Step 1 — Install Python

#### Linux (Ubuntu / Debian / Raspberry Pi OS)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

Verify the installation:

```bash
python3 --version
pip3 --version
```

#### Windows

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest Python 3 installer
3. Run the installer — **check the box "Add Python to PATH"** before clicking Install
4. Open **Command Prompt** or **PowerShell** and verify:

```powershell
python --version
pip --version
```

#### macOS

```bash
brew install python
```

> If you don't have Homebrew, install it first from [https://brew.sh](https://brew.sh):
>
> ```bash
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> ```

Verify:

```bash
python3 --version
pip3 --version
```

### Step 2 — Install Git

#### Linux

```bash
sudo apt install git -y
```

#### Windows

Download and install from [https://git-scm.com/downloads](https://git-scm.com/downloads).
Use all default options during installation.

#### macOS

```bash
brew install git
```

Verify:

```bash
git --version
```

### Step 3 — Install the ZBar System Library

> ⚠️ **Important:** `pyzbar` is only a Python wrapper.
> The actual barcode engine is **ZBar**, which must be installed at the OS level.

#### Linux (Ubuntu / Debian / Raspberry Pi OS)

```bash
sudo apt install libzbar0 libzbar-dev -y
```

#### macOS

```bash
brew install zbar
```

#### Windows

```powershell
pip install pyzbar[scripts]
```

Or download the ZBar binary manually from:
[http://zbar.sourceforge.net/](http://zbar.sourceforge.net/)

### Step 4 — Clone the Repository

```bash
git clone https://github.com/bharanidharanrangaraj/OpenCV-QR-Code-Reader.git
cd OpenCV-QR-Code-Reader
```

### Step 5 — Create a Virtual Environment

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

### Step 6 — Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:

| Package         | Purpose                                      |
| --------------- | -------------------------------------------- |
| `opencv-python` | Camera feed, drawing overlays, display window |
| `pyzbar`        | Decodes QR codes and barcodes (ZBar wrapper)  |
| `numpy`         | Array operations for polygon handling         |

### Step 7 — Run the Application

```bash
python qrcode_and_barcode_detection.py
```

A window will open showing your webcam feed.

## Usage

* Point the webcam at any **QR code** or **barcode**
* Detected codes are **outlined and labeled** on screen
* Each unique code is **printed once** in the console
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

## How It Works

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
Install it using your OS package manager (see [Step 3](#step-3--install-the-zbar-system-library)).

### `python3: command not found` or `python: command not found`

Python is not installed or not added to PATH.
Revisit [Step 1](#step-1--install-python).

### `pip: command not found`

On Linux, install pip separately:

```bash
sudo apt install python3-pip -y
```

On Windows, reinstall Python and make sure **"Add Python to PATH"** is checked.

### Camera does not open

* Check webcam permissions
* Try changing `VideoCapture(0)` to `VideoCapture(1)` in the script
* Ensure no other application is using the camera

### `No module named 'venv'`

On Linux:

```bash
sudo apt install python3-venv -y
```

## License

MIT License
Free to use, modify, and distribute.