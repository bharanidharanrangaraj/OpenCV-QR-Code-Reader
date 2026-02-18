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

---

## Source Code Explanation

### Imports

```pythonv
import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode, ZBarSymbol
```

- **cv2**  - OpenCV library. Handles the camera, drawing shapes/text on frames, and showing the video window.
- **numpy**  - Used to convert barcode corner points into the array format OpenCV needs to draw polygons.
- **time**  - Measures how long each frame takes, which is used to calculate FPS.
- **decode, ZBarSymbol**  - From pyzbar. `decode()` scans an image for barcodes. `ZBarSymbol` is an enum listing every barcode type ZBar supports.

---

### Camera Setup

```python
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

`VideoCapture(0)` opens the default webcam. The `cap.set()` calls request HD resolution (1280×720) for clearer barcode scanning. If the camera doesn't support it, it silently falls back to its default.

---

### State Variables

```python
seen_codes = set()
scan_count = 0
prev_time  = time.time()
```

- **seen_codes**  - A Python set that stores `(type, data)` pairs of every code scanned. Sets only hold unique values, so the same code is never logged twice.
- **scan_count**  - Integer counter that goes up by 1 for each new unique scan. Displayed live on screen.
- **prev_time**  - Timestamp of the previous frame, used to compute FPS.

---

### Colour Palette

```python
TYPE_COLORS = {
    "QRCODE"  : (0, 255, 0),
    "EAN13"   : (255, 100, 0),
    ...
}
DEFAULT_COLOR = (0, 200, 255)
```

Each barcode type gets a unique colour for its bounding box. Colours are in **BGR** format (OpenCV uses Blue-Green-Red, not RGB). If a type isn't in the dictionary, `DEFAULT_COLOR` is used as a fallback.

---

### Symbol List

```python
ALL_SYMBOLS = [s for s in ZBarSymbol if s != ZBarSymbol.PDF417]
```

Builds a list of all 20 supported barcode types, excluding PDF417. The ZBar C library has a known bug in its PDF417 decoder that prints a `WARNING` message every frame even when no PDF417 barcode is present. Excluding it removes the noise. Add it back if you specifically need to scan PDF417 codes.

---

### Main Loop

```python
while True:
    success, img = cap.read()
    if not success:
        break
```

An infinite loop that runs until the user presses `q`. `cap.read()` grabs one frame from the camera. `success` is `False` if the camera disconnects, which breaks the loop cleanly.

---

### FPS Calculation

```python
curr_time = time.time()
fps       = 1.0 / max(curr_time - prev_time, 1e-6)
prev_time = curr_time
```

FPS = 1 ÷ time_per_frame. For example, if a frame takes 0.033 seconds, FPS ≈ 30. The `max(..., 1e-6)` prevents a division-by-zero on the very first frame.

---

### Decoding Barcodes

```python
decoded_objects = decode(img, symbols=ALL_SYMBOLS)
```

This is the core of the program. pyzbar scans the entire image and returns a list of all detected codes. Each object has:
- `.data`  - raw bytes of the encoded content
- `.type`  - string like `"QRCODE"` or `"CODE128"`
- `.polygon`  - corner points for drawing a tight outline
- `.rect`  - simple bounding rectangle `(x, y, width, height)`

---

### Processing Each Detected Code

**Decoding the data:**
```python
data = code.data.decode("utf-8", errors="replace")
```
Converts raw bytes to a readable string. `errors="replace"` substitutes unreadable characters with `?` instead of crashing.

**Duplicate prevention:**
```python
key = (code_type, data)
if key not in seen_codes:
    seen_codes.add(key)
    scan_count += 1
    print(f"[{scan_count:03d}] [{code_type}] {data}")
```
A `(type, data)` tuple is the unique key. If it's already in `seen_codes`, the code is silently skipped. If new, it's logged and counted.

**Bounding box:**
```python
pts = np.array(code.polygon, dtype=np.int32).reshape((-1, 1, 2))
cv2.polylines(img, [pts], isClosed=True, color=color, thickness=3)
```
Converts the polygon corner points into the 3D array shape OpenCV expects, then draws a closed polygon outline around the barcode.

**Label with background:**
```python
cv2.rectangle(img, (rx, ry - th - 10), (rx + tw + 6, ry), color, -1)
cv2.putText(img, label, (rx + 3, ry - 5), ...)
```
A filled rectangle (the `-1` thickness means filled) is drawn behind the text label so it's readable against any background. Black text is drawn on top.

---

### HUD Overlay

```python
overlay = img.copy()
cv2.rectangle(overlay, (0, 0), (w, 40), (20, 20, 20), -1)
cv2.addWeighted(overlay, 0.55, img, 0.45, 0, img)
```

To create a semi-transparent dark bar at the top:
1. Copy the frame into `overlay`.
2. Draw a solid dark rectangle on the copy.
3. Blend the copy (55%) with the original (45%) using `addWeighted`. This makes the bar look transparent rather than fully opaque.

FPS is shown on the left, scan count on the right.

---

### Display and Quit

```python
cv2.imshow("QR / Barcode Reader  [q = quit]", img)
if cv2.waitKey(1) & 0xFF == ord("q"):
    break
```

`imshow` displays the processed frame. `waitKey(1)` waits 1 ms for a key press — this is required for OpenCV to refresh the window. The `& 0xFF` bitmask ensures cross-platform compatibility. `ord("q")` is the ASCII code for `q` (113).

---

### Cleanup

```python
cap.release()
cv2.destroyAllWindows()
print(f"\nSession ended. Total unique codes scanned: {scan_count}")
```

- `cap.release()` — Frees the camera so other programs can use it.
- `destroyAllWindows()` — Closes all OpenCV windows.
- Final print shows the total unique codes scanned in the session.


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