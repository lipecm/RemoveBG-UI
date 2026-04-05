import customtkinter as ctk
from PIL import Image
import os

class PreviewPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Headers
        ctk.CTkLabel(self, text="INPUT PREVIEW", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(10, 5))
        ctk.CTkLabel(self, text="OUTPUT PREVIEW", font=("Arial", 14, "bold")).grid(row=0, column=1, pady=(10, 5))

        # Image placeholders
        self.input_label = ctk.CTkLabel(self, text="[Drag & Drop]\nor select file below.", width=300, height=300, fg_color=("gray85", "gray25"), corner_radius=10)
        self.input_label.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.output_label = ctk.CTkLabel(self, text="[Preview]\nOutput will appear here.", width=300, height=300, fg_color=("gray85", "gray25"), corner_radius=10)
        self.output_label.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        
        self._current_input_img = None
        self._current_output_img = None

    def _load_and_scale_image(self, path):
        try:
            img = Image.open(path)
            # Maintain aspect ratio to fit inside 300x300
            img.thumbnail((300, 300))
            return ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def set_input_image(self, path):
        if not path or not os.path.exists(path) or path.endswith(".mp4") or path.endswith(".mov"):
            self.input_label.configure(text=f"File: {os.path.basename(path) if path else ''}", image=None)
            self._current_input_img = None
            return

        img = self._load_and_scale_image(path)
        if img:
            self._current_input_img = img
            self.input_label.configure(text="", image=img)
        else:
            self.input_label.configure(text="Invalid Image", image=None)

    def set_output_image(self, path):
        if not path or not os.path.exists(path) or path.endswith(".mp4") or path.endswith(".mov"):
            self.output_label.configure(text=f"Output File: {os.path.basename(path) if path else ''}", image=None)
            self._current_output_img = None
            return

        img = self._load_and_scale_image(path)
        if img:
            self._current_output_img = img
            self.output_label.configure(text="", image=img)
        else:
            self.output_label.configure(text="Invalid Output", image=None)

    def clear(self):
        self.input_label.configure(text="[Drag & Drop]\nor select file below.", image="")
        self.output_label.configure(text="[Preview]\nOutput will appear here.", image="")
        self._current_input_img = None
        self._current_output_img = None
