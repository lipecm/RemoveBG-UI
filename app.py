import tkinter as tk
import customtkinter as ctk
from PIL import Image
import os

from ui.preview_panel import PreviewPanel
from ui.file_list import FileList
from ui.settings_panel import SettingsPanel
from ui.progress_bar import ProgressBar
from core.config import Config
from core.processor import Processor
from core.file_manager import FileManager

class BackgroundRemoverApp(ctk.CTk):
    """
    Main Application Class connecting the UI components to the underlying processing logic.
    Inherits from CustomTkinter's main window class.
    """
    def __init__(self):
        super().__init__()

        # Rename to a generalized project name
        self.title("✨ Background Remover UI")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Initialize core components
        # Config holds all settings (format, output paths, colors)
        self.config = Config()
        # FileManager holds the queue of files chosen by the user
        self.file_manager = FileManager(self.config)
        # Processor handles the heavy asynchronous multithreading for CLI invocations
        self.processor = Processor(self.config)
        
        # Configure grid layout structure spanning 4 rows.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Row 0: Previews take maximum space
        self.grid_rowconfigure(1, weight=1)  # Row 1: File List
        self.grid_rowconfigure(2, weight=0)  # Row 2: Settings (static height)
        self.grid_rowconfigure(3, weight=0)  # Row 3: Output Path & Progress (static height)
        
        self.build_ui()

    def build_ui(self):
        """Builds all UI components and places them logically on the grid"""
        # 1. Preview Panel (Top side-by-side images)
        self.preview_panel = PreviewPanel(self)
        self.preview_panel.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")

        # 2. File List (Scrollable batch list)
        self.file_list = FileList(self, self.on_files_added)
        self.file_list.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # 3. Settings Panel (Model, Format, Color inputs)
        self.settings_panel = SettingsPanel(self, self.config)
        self.settings_panel.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # 4. Progress and Controls Panel (Bottom folder selection and Execute buttons)
        self.control_panel = ctk.CTkFrame(self)
        self.control_panel.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.control_panel.grid_columnconfigure(1, weight=1)

        # Output folder UI Frame
        self.output_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.output_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.output_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.output_frame, text="Output:").grid(row=0, column=0, padx=(0, 5))
        
        self.output_var = ctk.StringVar(value=self.config.get_output_path())
        self.output_entry = ctk.CTkEntry(self.output_frame, textvariable=self.output_var, state="readonly")
        self.output_entry.grid(row=0, column=1, sticky="ew", padx=5)

        self.browse_btn = ctk.CTkButton(self.output_frame, text="📂 Browse", width=80, command=self.browse_output_folder)
        self.browse_btn.grid(row=0, column=2, padx=5)

        # Checkbox for automatic destination mapping
        self.same_as_source_var = ctk.BooleanVar(value=self.config.get_same_as_source())
        self.same_as_source_cb = ctk.CTkCheckBox(
            self.output_frame, text="Same as source", variable=self.same_as_source_var, command=self.toggle_same_as_source
        )
        self.same_as_source_cb.grid(row=0, column=3, padx=(10, 0))
        self.toggle_same_as_source()

        # Progress bar (Indicates percentage state during subprocess execution)
        self.progress_bar = ProgressBar(self.control_panel)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        # Action Buttons Wrapper
        self.action_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Center align the two buttons
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(3, weight=1)

        self.process_btn = ctk.CTkButton(
            self.action_frame, text="▶️ PROCESS", font=("Arial", 16, "bold"), fg_color="#4CAF50", hover_color="#45a049",
            command=self.start_processing
        )
        self.process_btn.grid(row=0, column=1, padx=10, pady=10, ipadx=20, ipady=5)

        self.open_output_btn = ctk.CTkButton(
            self.action_frame, text="📂 OPEN OUTPUT", font=("Arial", 16, "bold"),
            command=self.open_output_folder, state="disabled"
        )
        self.open_output_btn.grid(row=0, column=2, padx=10, pady=10, ipadx=20, ipady=5)

    def on_files_added(self, files):
        """Callback: Updates the input preview when files are appended"""
        self.file_manager.add_files(files)
        if self.file_manager.get_files():
            first_file = self.file_manager.get_files()[0]
            self.preview_panel.set_input_image(first_file)

    def browse_output_folder(self):
        """Callback: Opens directory selector for explicit output routing"""
        folder = ctk.filedialog.askdirectory()
        if folder:
            self.config.set_output_path(folder)
            self.output_var.set(folder)

    def toggle_same_as_source(self):
        """Callback: Locks or unlocks output selector depending on automatic configuration"""
        val = self.same_as_source_var.get()
        self.config.set_same_as_source(val)
        if val:
            self.output_entry.configure(state="disabled")
            self.browse_btn.configure(state="disabled")
            self.output_var.set("Same as source directory")
        else:
            self.output_entry.configure(state="normal")
            self.browse_btn.configure(state="normal")
            self.output_var.set(self.config.get_output_path())
            self.output_entry.configure(state="readonly")

    def start_processing(self):
        """Callback: Primary execution node. Pushes files to the backend processor logic."""
        files = self.file_manager.get_files()
        if not files:
            tk.messagebox.showinfo("No Files", "Please add files to process.")
            return

        # Disable buttons to prevent duplicate runs
        self.process_btn.configure(state="disabled")
        self.open_output_btn.configure(state="disabled")
        self.progress_bar.start(len(files))

        # Begin threading the background execution
        self.processor.process_files(
            files,
            self.config,
            self.file_manager,
            on_progress=self.progress_bar.update_progress,
            on_file_complete=self.on_file_complete,
            on_batch_complete=self.on_batch_complete,
            on_error=self.on_processing_error
        )

    def on_file_complete(self, input_file, output_file, index):
        self.preview_panel.set_output_image(output_file)
        self.progress_bar.set_status(f"Completed {os.path.basename(input_file)}")

    def on_batch_complete(self):
        self.process_btn.configure(state="normal")
        self.open_output_btn.configure(state="normal")
        self.progress_bar.set_status("Processing complete!")
        tk.messagebox.showinfo("Complete", "Batch processing completed successfully.")

    def on_processing_error(self, message):
        self.process_btn.configure(state="normal")
        self.progress_bar.set_status("Error occurred.")
        tk.messagebox.showerror("Processing Error", message)

    def open_output_folder(self):
        path = self.config.get_output_path()
        if self.config.get_same_as_source() and self.file_manager.get_files():
            path = os.path.dirname(self.file_manager.get_files()[0])
        
        if os.path.exists(path):
            os.startfile(path)
