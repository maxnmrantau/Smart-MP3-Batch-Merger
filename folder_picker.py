"""
folder_picker.py
Standalone subprocess script for native Windows folder dialog.
"""
import sys
import os

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import tkinter as tk
from tkinter import filedialog

def pick_folder(title="Pilih Folder"):
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    root.focus_force()
    folder = filedialog.askdirectory(title=title)
    root.destroy()
    if folder:
        # Standardize path with backslashes for Windows
        norm_path = os.path.normpath(folder)
        print(norm_path)

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "Pilih Folder"
    pick_folder(t)
