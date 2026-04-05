import customtkinter as ctk
import tkinter as tk
import os

class FileList(ctk.CTkFrame):
    def __init__(self, master, on_files_added_cb, **kwargs):
        super().__init__(master, **kwargs)
        self.on_files_added_cb = on_files_added_cb
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Toolbar
        self.toolbar = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        self.add_files_btn = ctk.CTkButton(self.toolbar, text="📄 + Add Files", command=self.add_files, width=100)
        self.add_files_btn.pack(side="left", padx=5)

        self.add_folder_btn = ctk.CTkButton(self.toolbar, text="📁 Add Folder", command=self.add_folder, width=100)
        self.add_folder_btn.pack(side="left", padx=5)

        self.clear_btn = ctk.CTkButton(self.toolbar, text="🗑️ Clear", command=self.clear_files, width=100, fg_color="#F44336", hover_color="#D32F2F")
        self.clear_btn.pack(side="right", padx=5)

        # Scrollable Frame for files
        self.scrollable_frame = ctk.CTkScrollableFrame(self, height=100)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.file_labels = []

    def add_files(self):
        files = tk.filedialog.askopenfilenames(
            title="Select Files",
            filetypes=[
                ("Image/Video Files", "*.png *.jpg *.jpeg *.bmp *.webp *.gif *.mp4 *.mov"),
                ("All Files", "*.*")
            ]
        )
        if files:
            self._update_ui_with_files(files)

    def add_folder(self):
        folder = tk.filedialog.askdirectory(title="Select Folder")
        if folder:
            valid_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.gif', '.mp4', '.mov'}
            files = []
            for f in os.listdir(folder):
                ext = os.path.splitext(f)[1].lower()
                if ext in valid_exts:
                    files.append(os.path.join(folder, f))
            if files:
                self._update_ui_with_files(files)

    def _update_ui_with_files(self, files):
        for f in files:
            icon = "🎬" if f.lower().endswith((".mp4", ".mov")) else "🖼️"
            lbl = ctk.CTkLabel(self.scrollable_frame, text=f"{icon} {os.path.basename(f)}", anchor="w")
            lbl.pack(fill="x", padx=5, pady=2)
            self.file_labels.append(lbl)
        
        if self.on_files_added_cb:
            self.on_files_added_cb(files)

    def clear_files(self):
        for lbl in self.file_labels:
            lbl.destroy()
        self.file_labels = []
        if self.on_files_added_cb:
            self.on_files_added_cb([]) # Clear signal
