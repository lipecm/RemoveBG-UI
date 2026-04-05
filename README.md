# Background Remover UI

A modern, highly-polished desktop application for removing backgrounds from images and videos. 
This application provides a beautiful graphical interface (CustomTkinter) wrapped around the powerful **[backgroundremover](https://github.com/nadermx/backgroundremover)** AI engine.

## Acknowledgements 🏆

This project serves as a GUI wrapper and would not be possible without the incredible **backgroundremover** engine. 
All AI processing and background segmentation capabilities are powered entirely by:
- **[backgroundremover](https://github.com/nadermx/backgroundremover)** (Created by nadermx)
- **U^2-Net** (Created by xuebinqin)

## Features 🚀

- **Image & Video Processing**: Seamlessly remove backgrounds from images (PNG, JPG, WEBP, BMP, GIF) and videos (MP4, MOV).
- **Batch Processing**: Drag and drop multiple files to process them sequentially automatically.
- **Model Selection**: Switch between lightweight vs. high-accuracy U-2-Net AI models.
- **Background Replacement**: Choose between a transparent background, a custom solid color, or completely replace the background with a custom PNG/JPG image.
- **Modern UI**: A responsive, dark-themed UI created with CustomTkinter.

## Requirements 🛠️

- Python 3.10+
- The dependencies listed in `requirements.txt`
- (Recommended) CUDA Toolkit installed for GPU acceleration, making AI processing drastically faster.

## Quick Start (Running via Python) 🐍

To run the application from source code:

1. Clone or download this repository.
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Creating the Executable (Standalone App) 📦

You can build a standalone executable that you can run without opening Python or CMD.

1. Install PyInstaller (it is included in `requirements.txt`).
2. Run the build script located in the `build/` folder:
   ```bash
   cd build
   build.bat
   ```
3. After the build finishes (it may take 5 minutes), navigate to the `build/dist/` directory. You will find `BackgroundRemoverUI.exe`. 
4. You can drag this file to your Desktop or pin it to your Start menu to use it freely!

## Step-by-Step Usage 📖

1. **Add Files**: Use the "Add Files", "Add Folder" buttons or simply drag and drop files into the app. They will appear in the queue at the bottom.
2. **Settings**:
   - **Model**: Choose `u2net` for standard balanced processing, `u2netp` for extremely fast low-res processing, or human/cloth segmentations.
   - **Format**: Select your desired output file format (e.g., MP4 for videos, PNG for transparent images).
   - **Background**: Leave it as Transparent, click "Solid Color" to pick a background color, or select a Custom Image to place the remaining subject on top of a new background.
3. **Output Destination**: Next to the *Output* label, choose where the files will be saved. By default, they save directly next to the original file ("Same as source").
4. **Process!**: Click **▶️ PROCESS** and wait for the progress bar to finish.
5. You can see a Before/After preview at the top of the app as files complete!

## License
Feel free to fork, customize, and use this GUI. Please refer to the [backgroundremover license](https://github.com/nadermx/backgroundremover/blob/main/LICENSE) for rules regarding the AI engine usage.
