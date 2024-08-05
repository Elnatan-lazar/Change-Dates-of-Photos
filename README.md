
# Change Dates of Photos

This project provides a simple GUI application to change the dates of photos in a destination folder to match the dates of photos in a source folder. The application uses exiftool to read and modify the EXIF metadata of image files.

## Features

- Select a source folder containing the original photos.
- Select a destination folder containing copies of the photos.
- Change the dates of the photos in the destination folder to match the dates of the corresponding photos in the source folder.
- Progress bar to display the progress and estimated time remaining.

## Getting Started

### Prerequisites

- Python 3.x
- exiftool (download from [ExifTool](https://exiftool.org/))

### Installation

1. Clone the repository or download the files.
2. Ensure you have the required dependencies:
   
bash
   pip install Pillow
Usage
Running the Script
Run the finalApp.py script using Python:

bash
Copy code
python finalApp.py
Use the GUI to select the path for exiftool, the source folder, and the destination folder.

Press the "Start Process" button to change the dates of the photos in the destination folder to match the source folder.

Executable Version
Download the finalApp.exe executable file.
Run the executable file.
Follow the same steps as above to select the paths and start the process.
Additional Script (With Test Option)
The change_dates_gui+test.py script includes an additional feature for testing. It can create dummy images in the source folder, copy them to the destination folder, and change their dates randomly for testing purposes.

Running the Test Script
Run the change_dates_gui+test.py script using Python:

bash
Copy code
python change_dates_gui+test.py
Use the GUI to select the path for exiftool, the source folder, and the destination folder.

Enter the number of images for the test and click "Create Test Images" to create, copy, and modify dates of test images.

Press the "Start Process" button to change the dates of the photos in the destination folder to match the source folder.

Executable Version
Download the change_dates_gui+test.exe executable file.
Run the executable file.
Follow the same steps as above to select the paths, create test images, and start the process.
Implementation Summary
finalApp.py
GUI Components: Tkinter is used to create a simple and user-friendly interface for selecting folders and starting the date change process.
EXIF Metadata Handling: The exiftool command-line utility is used to read and modify the EXIF metadata of image files.
Error Handling: The script includes error handling to ensure that the process runs smoothly and provides feedback in case of issues.
change_dates_gui+test.py
Additional Testing Features: This script includes functionality to create dummy images in the source folder, copy them to the destination folder, and change their dates randomly for testing purposes.
**
