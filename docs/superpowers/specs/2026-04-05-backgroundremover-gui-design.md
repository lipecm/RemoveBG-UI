# BackgroundRemover GUI Design Spec

## Overview

A beautiful desktop application for removing backgrounds from images and videos, wrapping the `backgroundremover` CLI tool with a CustomTkinter UI. Packaged as a standalone Windows executable.

## Architecture

```
┌─────────────────────────────────────────────┐
│           BackgroundRemoverGUI.exe          │
├─────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────────────┐ │
│  │  CustomTkin │    │   Core Processor    │ │
│  │  ter UI     │───▶│   (subprocess calls)│ │
│  └─────────────┘    └─────────────────────┘ │
│         │                     │             │
│         ▼                     ▼             │
│  ┌─────────────┐    ┌─────────────────────┐ │
│  │  File       │    │  backgroundremover  │ │
│  │  Manager    │    │  CLI (pip package)  │ │
│  └─────────────┘    └─────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Tech Stack
- Python 3.10+
- CustomTkinter for UI (modern dark theme)
- backgroundremover (pip package) with PyTorch GPU
- PyInstaller for .exe packaging

## Features

### Core Features
1. **Image Processing** - Remove background from JPG, PNG, BMP, etc.
2. **Video Processing** - Remove background from MP4, MOV, etc.
3. **Batch Processing** - Process multiple files at once
4. **Preview** - Side-by-side input/output preview

### Advanced Features
1. **Model Selection** - Choose between u2net models (fast vs quality)
2. **Output Format** - PNG (transparent), JPG, WebP, GIF, JPEG
3. **Background Replacement**:
   - None (transparent)
   - Solid color (with color picker)
   - Custom image background

### Settings
- Model: u2net, u2netp, u2net_human_seg, u2net_cloth_seg
- Format: PNG, JPG, WebP
- Background: Transparent, Color, Image
- Output folder: Custom or same as source

## UI Components

### Main Window Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  ✨ Background Remover                                    _ □ × │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │      INPUT          │  │      OUTPUT         │              │
│  │     PREVIEW         │  │     PREVIEW         │              │
│  │   [Drag & Drop]     │  │    [Preview]        │              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 📁 + Add Files    📂 Add Folder    🗑️ Clear                 ││
│  │ 🖼️ photo1.jpg    🖼️ photo2.png    🎬 video.mp4            ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ⚙️ Settings                                                 ││
│  │ Model: [u2net (Fast) ▼]    Format: [PNG (Transparent) ▼]   ││
│  │ Background: ○ None  ○ Color  ○ Image                        ││
│  │ Color: [▮▮▮ Color Picker]                                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Output: [C:\...\output] [📂 Browse]  ☑ Same as source         │
│                                                                 │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░  52%                │
│  Processing: photo3.jpg (3 of 5)              [✕ Cancel]        │
│                                                                 │
│         [▶️ PROCESS]              [📂 OPEN OUTPUT]              │
└─────────────────────────────────────────────────────────────────┘
```

### Visual Design
- **Theme**: Dark mode (default), Light mode option
- **Colors**: Purple/blue gradient accents
- **Buttons**: Rounded corners, hover effects
- **Icons**: Unicode emoji icons throughout
- **Animations**: Smooth progress bar, hover transitions

## File Structure

```
RemoveBG/
├── main.py              # Entry point
├── app.py               # Main application class
├── ui/
│   ├── __init__.py
│   ├── main_window.py   # Main window layout
│   ├── preview_panel.py # Input/output preview
│   ├── file_list.py     # Batch file list
│   ├── settings_panel.py# Settings controls
│   └── progress_bar.py  # Progress indicator
├── core/
│   ├── __init__.py
│   ├── processor.py     # CLI subprocess wrapper
│   ├── file_manager.py  # File handling
│   └── config.py        # Settings management
├── assets/
│   └── icon.ico         # App icon
├── build/
│   └── build.spec        # PyInstaller spec
├── requirements.txt
└── README.md
```

## Data Flow

1. User adds files (drag-drop or buttons)
2. User configures settings (model, format, background)
3. User clicks Process
4. For each file:
   - Build CLI command with settings
   - Execute subprocess
   - Parse output for progress
   - Update progress bar
   - Update preview when complete
5. On completion, show output folder button

## CLI Command Mapping

```python
# Basic image
backgroundremover -i input.jpg -o output.png

# Video
backgroundremover -i video.mp4 -o output.mp4 -mk

# With model
backgroundremover -i input.jpg -o output.png -m u2net

# With background color (requires post-processing)
# backgroundremover outputs transparent PNG
# Then composite with color/image background
```

## Error Handling

- **Missing GPU**: Show warning, allow CPU processing
- **Invalid file**: Skip with error message in batch
- **Processing failure**: Show error, allow retry
- **Output folder not writable**: Prompt to select different folder

## Build/Packaging

Use PyInstaller to create standalone executable:

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico main.py
```

Bundle requirements:
- PyTorch (GPU version)
- backgroundremover
- CustomTkinter
- All dependencies

## Success Criteria

1. User can drag-drop or select files/folders
2. Processing works for both images and videos
3. Progress bar shows accurate progress
4. Preview shows input/output side-by-side
5. Batch processing completes all files
6. Background replacement (color/image) works
7. Executable runs without Python installation