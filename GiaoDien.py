import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg

root = tk.Tk()
root.title("🎬 MKV to MP4 Converter")

mkv_path_var = tk.StringVar()
output_dir_var = tk.StringVar()
batch_input_var = tk.StringVar()
batch_output_var = tk.StringVar()

def doanpython():
    filepath = filedialog.askopenfilename(
        title="Chọn tệp MKV",
        filetypes=[("Tệp MKV", "*.mkv")]
    )
    if filepath:
        mkv_path_var.set(filepath)
        check_ready()

def choose_output_folder():
    folder = filedialog.askdirectory(title="Chọn thư mục lưu file MP4")
    if folder:
        output_dir_var.set(folder)
        check_ready()

def choose_batch_input_folder():
    folder = filedialog.askdirectory(title="Chọn thư mục chứa các tệp MKV")
    if folder:
        batch_input_var.set(folder)
        check_batch_ready()

def choose_batch_output_folder():
    folder = filedialog.askdirectory(title="Chọn thư mục lưu các tệp MP4")
    if folder:
        batch_output_var.set(folder)
        check_batch_ready()

def check_ready():
    if mkv_path_var.get() and output_dir_var.get():
        ok_button.config(state="normal")
    else:
        ok_button.config(state="disabled")

def check_batch_ready():
    if batch_input_var.get() and batch_output_var.get():
        batch_button.config(state="normal")
    else:
        batch_button.config(state="disabled")

def convert():
    filepath = mkv_path_var.get()
    output_dir = output_dir_var.get()

    if not filepath or not output_dir:
        messagebox.showerror("Thiếu thông tin", "❌ Vui lòng chọn tệp và nơi lưu.")
        return

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(filepath))[0]
    output_path = os.path.join(output_dir, f"{filename}.mp4")

    try:
        ffmpeg.input(filepath).output(output_path, vcodec='copy', acodec='copy').run(overwrite_output=True)
        messagebox.showinfo("Thành công", f"✅ Đã chuyển thành công:\n{output_path}")
    except ffmpeg.Error as e:
        messagebox.showerror("Lỗi", f"❌ Lỗi:\n{e.stderr.decode()}")

def convert_all():
    input_folder = batch_input_var.get()
    output_folder = batch_output_var.get()

    if not input_folder or not output_folder:
        messagebox.showerror("Thiếu thông tin", "❌ Vui lòng chọn thư mục đầu vào và đầu ra.")
        return

    os.makedirs(output_folder, exist_ok=True)
    count = 0

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mkv"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".mp4")
            try:
                ffmpeg.input(input_path).output(output_path, vcodec='copy', acodec='copy').run(overwrite_output=True)
                count += 1
            except ffmpeg.Error as e:
                messagebox.showerror("Lỗi", f"❌ Không thể chuyển file: {filename}\n{e.stderr.decode()}")

    messagebox.showinfo("Hoàn tất", f"✅ Đã chuyển đổi {count} tệp thành công.")

def exit_app():
    root.destroy()

window_width = 620
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_pos = int((screen_width - window_width) / 2)
y_pos = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

bg_color = "#f0f0f0"
fg_color = "#000000"
entry_bg = "#ffffff"
btn_bg = "#e0e0e0"
btn_fg = "#000000"

root.configure(bg=bg_color)

header = tk.Label(root, text="Chuyển đổi tệp video MKV sang MP4", font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color)
header.pack(pady=(15, 10))

frame = tk.Frame(root, bg=bg_color)
frame.pack(padx=20, pady=5, fill="x")

tk.Button(frame, text="📂  Chọn tệp MKV", font=("Arial", 11), command=doanpython, bg=btn_bg, fg=btn_fg).grid(row=0, column=0, sticky="w")
tk.Entry(frame, textvariable=mkv_path_var, font=("Arial", 10), width=60, state="readonly", bg=entry_bg, fg=fg_color, insertbackground=fg_color).grid(row=0, column=1, padx=(10, 0))

tk.Button(frame, text="💾  Thư mục lưu file", font=("Arial", 11), command=choose_output_folder, bg=btn_bg, fg=btn_fg).grid(row=1, column=0, pady=10, sticky="w")
tk.Entry(frame, textvariable=output_dir_var, font=("Arial", 10), width=60, state="readonly", bg=entry_bg, fg=fg_color, insertbackground=fg_color).grid(row=1, column=1, padx=(10, 0))

ok_button = tk.Button(root, text="✅ OK - Chuyển tệp", font=("Arial", 12, "bold"), command=convert, state="disabled", bg="#4CAF50", fg="white")
ok_button.pack(pady=(5, 10))

batch_frame = tk.Frame(root, bg=bg_color)
batch_frame.pack(padx=20, pady=5, fill="x")

tk.Button(batch_frame, text="📁  Thư mục chứa các file MKV", font=("Arial", 11), command=choose_batch_input_folder, bg=btn_bg, fg=btn_fg).grid(row=0, column=0, sticky="w")
tk.Entry(batch_frame, textvariable=batch_input_var, font=("Arial", 10), width=60, state="readonly", bg=entry_bg, fg=fg_color, insertbackground=fg_color).grid(row=0, column=1, padx=(10, 0))

tk.Button(batch_frame, text="📁  Thư mục lưu các file MP4", font=("Arial", 11), command=choose_batch_output_folder, bg=btn_bg, fg=btn_fg).grid(row=1, column=0, pady=10, sticky="w")
tk.Entry(batch_frame, textvariable=batch_output_var, font=("Arial", 10), width=60, state="readonly", bg=entry_bg, fg=fg_color, insertbackground=fg_color).grid(row=1, column=1, padx=(10, 0))

batch_button = tk.Button(root, text="🔄 Chuyển tất cả tệp MKV trong thư mục", font=("Arial", 11), command=convert_all, state="disabled", bg="#2196F3", fg="white")
batch_button.pack(pady=(0, 10))

exit_button = tk.Button(root, text="❌ Thoát", font=("Arial", 11), command=exit_app, bg="#e74c3c", fg="white")
exit_button.pack(pady=(0, 15))

root.mainloop()