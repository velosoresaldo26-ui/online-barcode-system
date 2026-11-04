"""
AUTO-GENERATE BARCODE SYSTEM (Code 128)

Paano gamitin:
  1. I-install muna (isang beses lang):
         pip install python-barcode pillow
     Sa Google Colab / online Python, ilagay sa unang cell:
         !pip install python-barcode pillow

  2. I-run:
         python barcode_generator.py

Ano ang ginagawa nito:
  - Awtomatikong gumagawa ng bagong barcode number (hal. PRD-000001, PRD-000002...)
  - Hindi nauulit ang number kahit i-close at i-run ulit (naka-save sa counter.txt)
  - Nagse-save ng barcode image (PNG) sa folder na "barcodes/"
  - Nagse-save ng talaan ng lahat ng barcode sa "barcode_log.csv"
"""

import csv
import os
from datetime import datetime

import barcode
from barcode.writer import ImageWriter

# ---------------- SETTINGS (pwede mong palitan) ----------------
PREFIX = "PRD"            # unahan ng barcode, hal. PRD, ITEM, SKU
DIGITS = 6                # ilang digit ang number (000001)
OUTPUT_FOLDER = "barcodes"
COUNTER_FILE = "counter.txt"
LOG_FILE = "barcode_log.csv"
# ---------------------------------------------------------------


def get_next_number():
    """Kunin ang susunod na number at i-save agad para hindi maulit."""
    current = 0
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            text = f.read().strip()
            if text.isdigit():
                current = int(text)
    current += 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(current))
    return current


def generate_code():
    """Gumawa ng bagong unique code, hal. PRD-000001."""
    number = get_next_number()
    return f"{PREFIX}-{str(number).zfill(DIGITS)}"


def make_barcode_image(code):
    """Gumawa ng barcode PNG at ibalik ang path ng file."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    barcode_class = barcode.get_barcode_class("code128")
    bc = barcode_class(code, writer=ImageWriter())
    path_without_ext = os.path.join(OUTPUT_FOLDER, code)
    return bc.save(path_without_ext)  # nagdadagdag ng .png


def write_log(code, item_name, image_path):
    """I-save sa CSV ang code, pangalan ng item, at oras."""
    new_file = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["barcode", "item_name", "image_file", "created_at"])
        writer.writerow([
            code,
            item_name,
            image_path,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ])


def create_barcode(item_name=""):
    """Isang function na gumagawa ng lahat: code + image + log."""
    code = generate_code()
    image_path = make_barcode_image(code)
    write_log(code, item_name, image_path)
    return code, image_path


def main():
    print("=== AUTO BARCODE GENERATOR ===")
    print("I-type ang pangalan ng item para gumawa ng barcode.")
    print("Pindutin lang ang Enter (walang tinype) para huminto.\n")

    while True:
        item = input("Pangalan ng item: ").strip()
        if not item:
            break
        code, path = create_barcode(item)
        print(f"  Barcode: {code}")
        print(f"  Na-save sa: {path}\n")

    print("Tapos na. Tingnan ang folder 'barcodes' at ang file na 'barcode_log.csv'.")


if __name__ == "__main__":
    main()
