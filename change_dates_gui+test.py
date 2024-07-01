import os
import shutil
import random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time


def select_exiftool():
    global exiftool_path
    exiftool_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    exiftool_label.config(text=exiftool_path)


def select_source_folder():
    global source_folder
    source_folder = filedialog.askdirectory()
    source_label.config(text=source_folder)


def select_destination_folder():
    global destination_folder
    destination_folder = filedialog.askdirectory()
    destination_label.config(text=destination_folder)


def create_dummy_images(folder, num_images):
    os.makedirs(folder, exist_ok=True)
    for i in range(num_images):
        img = Image.new('RGB', (100, 100), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10, 10), f"Image {i + 1}", fill=(255, 255, 0))
        img_path = os.path.join(folder, f'image_{i + 1}.jpg')
        img.save(img_path)
    print(f"Created {num_images} images in {folder}")


def copy_images(source_folder, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    for filename in os.listdir(source_folder):
        full_file_name = os.path.join(source_folder, filename)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, destination_folder)
    print(f"Copied images from {source_folder} to {destination_folder}")


def create_test():
    try:
        num_images = int(num_images_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of images.")
        return

    if not source_folder or not destination_folder:
        messagebox.showerror("Error", "Please select source and destination folders.")
        return

    create_dummy_images(source_folder, num_images)
    copy_images(source_folder, destination_folder)

    # Change the dates randomly in the destination folder
    destination_files = os.listdir(destination_folder)
    for dest_file in destination_files:
        dest_file_path = os.path.join(destination_folder, dest_file)
        random_date = datetime.now() - timedelta(days=random.randint(0, 365))
        formatted_date = random_date.strftime('%Y:%m:%d %H:%M:%S')

        # Change the date using exiftool
        result = subprocess.run(
            [exiftool_path, f'-AllDates={formatted_date}', '-overwrite_original', dest_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW  # This suppresses the pop-up window
        )

        if result.returncode != 0:
            print(f"Error changing date for {dest_file}: {result.stderr.decode('utf-8')}")
        else:
            print(f"Changed date for {dest_file} to {formatted_date}")

    messagebox.showinfo("Success", f"Created, copied, and modified dates for {num_images} test images successfully.")


def change_dates():
    if not exiftool_path or not source_folder or not destination_folder:
        messagebox.showerror("Error", "Please select exiftool path, source folder, and destination folder.")
        return

    # Get the list of files in the source and destination folders
    source_files = os.listdir(source_folder)
    destination_files = os.listdir(destination_folder)

    total_files = len(source_files)

    # Confirmation dialog
    confirm = messagebox.askyesno("Confirmation",
                                  f"{total_files} files were chosen. Are you sure you want to change the dates?")
    if not confirm:
        return

    processed_files = 0
    start_time = time.time()

    for source_file in source_files:
        if source_file in destination_files:
            try:
                # Full paths to the files
                source_file_path = os.path.join(source_folder, source_file)
                dest_file_path = os.path.join(destination_folder, source_file)

                # Read the original date using exiftool
                source_date = subprocess.check_output(
                    [exiftool_path, '-CreateDate', '-d', '%Y:%m:%d %H:%M:%S', '-s3', source_file_path]
                ).strip().decode('utf-8')

                # Change the date in the destination file using exiftool
                result = subprocess.run(
                    [exiftool_path, f'-AllDates={source_date}', '-overwrite_original', dest_file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW  # This suppresses the pop-up window
                )

                if result.returncode != 0:
                    print(f"Error changing date for {dest_file_path}: {result.stderr.decode('utf-8')}")
                else:
                    print(f"Changed date for {dest_file_path} to {source_date}")

                processed_files += 1
                elapsed_time = time.time() - start_time
                avg_time_per_file = elapsed_time / processed_files
                remaining_time = avg_time_per_file * (total_files - processed_files)
                minutes, seconds = divmod(remaining_time, 60)
                time_remaining_str = f"Approx. time remaining: {int(minutes)}:{int(seconds):02d} minutes"

                progress_label.config(text=f"{processed_files}/{total_files} files processed\n{time_remaining_str}")
                progress_bar['value'] = (processed_files / total_files) * 100
                root.update_idletasks()
            except Exception as e:
                print(f"Error processing {source_file}: {e}")

    messagebox.showinfo("Success", "Process completed successfully.")


# Create the main window
root = tk.Tk()
root.title("Change Dates of Photos")

exiftool_path = ''
source_folder = ''
destination_folder = ''

# Button to select the exiftool path
exiftool_button = tk.Button(root, text="Select Exiftool Path", command=select_exiftool)
exiftool_button.pack(pady=5)
exiftool_label = tk.Label(root, text="No path selected")
exiftool_label.pack(pady=5)

# Button to select the source folder
source_button = tk.Button(root, text="Select Source Folder", command=select_source_folder)
source_button.pack(pady=5)
source_label = tk.Label(root, text="No folder selected")
source_label.pack(pady=5)

# Button to select the destination folder
destination_button = tk.Button(root, text="Select Destination Folder", command=select_destination_folder)
destination_button.pack(pady=5)
destination_label = tk.Label(root, text="No folder selected")
destination_label.pack(pady=5)

# Entry to input number of images for the test
num_images_label = tk.Label(root, text="Number of images for test:")
num_images_label.pack(pady=5)
num_images_entry = tk.Entry(root)
num_images_entry.pack(pady=5)

# Button to create test images
create_test_button = tk.Button(root, text="Create Test Images", command=create_test)
create_test_button.pack(pady=5)

# Progress label and bar
progress_label = tk.Label(root, text="0/0 files processed\nApprox. time remaining: 0:00 minutes")
progress_label.pack(pady=5)
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

# Button to start the process
process_button = tk.Button(root, text="Start Process", command=change_dates)
process_button.pack(pady=20)


# Link to download exiftool
def open_exiftool_link():
    import webbrowser
    webbrowser.open("https://exiftool.org/")


exiftool_link = tk.Label(root, text="Download exiftool", fg="blue", cursor="hand2")
exiftool_link.pack(pady=5)
exiftool_link.bind("<Button-1>", lambda e: open_exiftool_link())

root.mainloop()
