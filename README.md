# QR Code & Barcode Reader

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20RaspberryPi-lightgrey)

A real-time QR code and barcode scanner built with Python, OpenCV, and pyzbar. Supports 20 symbol types with a live HUD showing FPS and scan count.



## Features

- 📷 **Live webcam feed** at 1280×720
- 🔍 **Decodes 20 barcode/QR types** - QR Code, EAN-8/13, UPC-A/E, Code128, Code39, Code93, Aztec, DataBar, Codabar, Interleaved 2-of-5, and more
- 🚫 **Duplicate scan prevention** - same code is never counted twice in a session
- 🎨 **Color-coded bounding boxes** - each barcode type gets a unique color
- 📊 **HUD overlay** - live FPS (top-left) and scan count (top-right)
- 🖥️ **Console log** - every new scan is printed with an index and type label



## Requirements

- Python 3.7+
- OpenCV
- pyzbar
- NumPy

Install all dependencies with a single command:

```bash
pip install -r requirements.txt
```

> **Windows users:** pyzbar also requires the ZBar DLL. Install it via:
> ```bash
> pip install pyzbar[scripts]
> ```
> Or download the ZBar binary from [zbar.sourceforge.net](http://zbar.sourceforge.net/).

## Usage

```bash
python qrcode_and_barcode_detection.py
```

- Point your webcam at any QR code or barcode.
- Detected codes are highlighted with a polygon and labeled on screen.
- Each unique scan is printed to the console.
- Press **`q`** to quit. The total scan count is printed on exit.

## Supported Barcode Types

| Type | Description |
|------|-------------|
| `QRCODE` | QR Code (2D) |
| `EAN13` | EAN-13 (retail) |
| `EAN8` | EAN-8 (retail, compact) |
| `UPCA` | UPC-A (retail, US) |
| `UPCE` | UPC-E (retail, compact) |
| `CODE128` | Code 128 (logistics) |
| `CODE39` | Code 39 (industrial) |
| `CODE93` | Code 93 |
| `I25` | Interleaved 2-of-5 |
| `DATABAR` | GS1 DataBar |
| `AZTEC` | Aztec Code (2D) |
| `CODABAR` | Codabar |

## Console Output Example
The output of the code should look like this. 

```
QR / Barcode Reader started. Press 'q' to quit.
Decoding 20 symbol types.

[001] [QRCODE]  https://example.com
[002] [CODE128] ABC-abc-1234
[003] [EAN13]   1234567890123

Session ended. Total unique codes scanned: 3
```

## License

MIT License — free to use, modify, and distribute.
