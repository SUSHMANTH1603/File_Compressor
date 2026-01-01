import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

selected_file = None
selected_ext = None

# ---------------- FUNCTIONS ---------------- #


def set_status(msg):
    status_label.config(text=msg)
    status_label.update_idletasks()


def upload_file():
    global selected_file, selected_ext

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("Text Files", "*.txt"),
            ("PDF Files", "*.pdf")
        ]
    )

    if file_path:
        selected_ext = os.path.splitext(file_path)[1]
        selected_file = os.path.join(BASE_DIR, "input" + selected_ext)

        shutil.copy(file_path, selected_file)

        file_label.config(text=f"Selected File: {os.path.basename(file_path)}")
        compress_btn.config(state=tk.NORMAL)
        decompress_btn.config(state=tk.DISABLED)

        set_status("File uploaded successfully.")


def compress_file():
    if not selected_file:
        return

    try:
        set_status("Compressing file...")
        root.config(cursor="watch")

        subprocess.run(
            ["./compress", selected_file, "compressed.bin"],
            cwd=BASE_DIR,
            check=True
        )

        decompress_btn.config(state=tk.NORMAL)
        set_status("Compression completed. compressed.bin created.")

        messagebox.showinfo(
            "Success",
            "File compressed successfully!\n\ncompressed.bin is ready."
        )

    except Exception as e:
        messagebox.showerror("Error", f"Compression failed:\n{e}")
        set_status("Compression failed.")

    finally:
        root.config(cursor="")


def decompress_file():
    if not selected_ext:
        return

    output_file = os.path.join(BASE_DIR, "output" + selected_ext)

    try:
        set_status("Decompressing file...")
        root.config(cursor="watch")

        subprocess.run(
            ["./decompress", "compressed.bin", output_file],
            cwd=BASE_DIR,
            check=True
        )

        set_status("Decompression completed.")

        messagebox.showinfo(
            "Success",
            f"File decompressed successfully!\n\n{os.path.basename(output_file)} is ready."
        )

    except Exception as e:
        messagebox.showerror("Error", f"Decompression failed:\n{e}")
        set_status("Decompression failed.")

    finally:
        root.config(cursor="")


# ---------------- GUI LAYOUT ---------------- #

root = tk.Tk()
root.title("File Compressor (TXT / PDF)")
root.geometry("480x360")
root.resizable(False, False)

# Title
tk.Label(
    root,
    text="File Compressor",
    font=("Segoe UI", 20, "bold")
).pack(pady=15)

# File info
file_label = tk.Label(
    root,
    text="No file selected",
    font=("Segoe UI", 11),
    fg="gray"
)
file_label.pack(pady=5)

# Buttons Frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

upload_btn = tk.Button(
    btn_frame,
    text="Upload File (TXT / PDF)",
    width=30,
    command=upload_file
)
upload_btn.grid(row=0, column=0, pady=6)

compress_btn = tk.Button(
    btn_frame,
    text="Compress",
    width=30,
    state=tk.DISABLED,
    command=compress_file
)
compress_btn.grid(row=1, column=0, pady=6)

decompress_btn = tk.Button(
    btn_frame,
    text="Decompress",
    width=30,
    state=tk.DISABLED,
    command=decompress_file
)
decompress_btn.grid(row=2, column=0, pady=6)

# Separator
tk.Frame(root, height=1, bg="#cccccc").pack(fill="x", pady=15)

# Status Bar
status_label = tk.Label(
    root,
    text="Ready.",
    font=("Segoe UI", 10),
    fg="blue"
)
status_label.pack(pady=5)

# Footer
tk.Label(
    root,
    text="Supports lossless compression for Text & PDF files",
    font=("Segoe UI", 9),
    fg="gray"
).pack(side="bottom", pady=10)

root.mainloop()
