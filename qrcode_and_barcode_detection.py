import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode, ZBarSymbol

# ── Camera setup ──────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ── State ─────────────────────────────────────────────────────────────────────
seen_codes   = set()          # Duplicate prevention
scan_count   = 0              # Live scan counter
prev_time    = time.time()    # For FPS calculation

# ── Colour palette (one per code type for visual variety) ─────────────────────
TYPE_COLORS = {
    "QRCODE"    : (0,   255,   0),
    "EAN13"     : (255, 100,   0),
    "EAN8"      : (255, 180,   0),
    "UPCA"      : (0,   180, 255),
    "UPCE"      : (0,   120, 255),
    "CODE128"   : (200,   0, 255),
    "CODE39"    : (255,   0, 200),
    "CODE93"    : (255,   0, 100),
    "I25"       : (0,   255, 200),
    "DATABAR"   : (255, 220,   0),
    "PDF417"    : (100, 100, 255),
    "AZTEC"     : (0,   200, 100),
    "CODABAR"   : (180, 255,   0),
}
DEFAULT_COLOR = (0, 200, 255)

ALL_SYMBOLS = [s for s in ZBarSymbol if s != ZBarSymbol.PDF417]

print("QR / Barcode Reader started. Press 'q' to quit.")
print(f"Decoding {len(ALL_SYMBOLS)} symbol types.\n")

# ── Main loop ─────────────────────────────────────────────────────────────────
while True:
    success, img = cap.read()
    if not success:
        break

    # ── FPS ───────────────────────────────────────────────────────────────────
    curr_time = time.time()
    fps       = 1.0 / max(curr_time - prev_time, 1e-6)
    prev_time = curr_time

    # ── Decode every supported symbol type ───────────────────────────────────
    decoded_objects = decode(img, symbols=ALL_SYMBOLS)

    for code in decoded_objects:
        data      = code.data.decode("utf-8", errors="replace")
        code_type = code.type          # e.g. "QRCODE", "EAN13", "CODE128" …
        color     = TYPE_COLORS.get(code_type, DEFAULT_COLOR)

        # ── Duplicate prevention ──────────────────────────────────────────────
        key = (code_type, data)
        if key not in seen_codes:
            seen_codes.add(key)
            scan_count += 1
            print(f"[{scan_count:03d}] [{code_type}] {data}")

        # ── Bounding box (tight polygon) ──────────────────────────────────────
        pts = np.array(code.polygon, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=color, thickness=3)

        # Filled rectangle behind text for readability
        rx, ry, rw, rh = code.rect
        label          = f"{code_type}: {data[:40]}"
        (tw, th), _    = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
        cv2.rectangle(img, (rx, ry - th - 10), (rx + tw + 6, ry), color, -1)
        cv2.putText(img, label, (rx + 3, ry - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)

    # ── HUD overlay ───────────────────────────────────────────────────────────
    h, w = img.shape[:2]

    # Semi-transparent dark bar at top
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (w, 40), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.55, img, 0.45, 0, img)

    cv2.putText(img, f"FPS: {fps:5.1f}",
                (10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 180), 2)
    cv2.putText(img, f"Scanned: {scan_count}",
                (w - 200, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 220, 255), 2)

    cv2.imshow("QR / Barcode Reader  [q = quit]", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ── Cleanup ───────────────────────────────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()
print(f"\nSession ended. Total unique codes scanned: {scan_count}")