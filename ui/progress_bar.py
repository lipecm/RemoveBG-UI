import customtkinter as ctk

class ProgressBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(0, weight=1)

        self.progress = ctk.CTkProgressBar(self, height=15)
        self.progress.grid(row=0, column=0, sticky="ew", padx=10, pady=(5, 5))
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status_label.grid(row=1, column=0, sticky="ew", padx=10)
        
        self.total_files = 0
        self.completed_files = 0

    def start(self, total_files):
        self.total_files = total_files
        self.completed_files = 0
        self.progress.set(0)
        self.set_status(f"Starting processing of {total_files} file(s)...")

    def update_progress(self, index, total, filename):
        self.completed_files = index
        self.progress.set(self.completed_files / total)
        self.set_status(f"Processing: {filename} ({self.completed_files}/{total})")

    def set_status(self, text):
        self.status_label.configure(text=text)
        self.update_idletasks() # Force UI update during synchronous processing
