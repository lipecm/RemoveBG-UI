import customtkinter as ctk
import tkinter as tk

class SettingsPanel(ctk.CTkFrame):
    def __init__(self, master, config, **kwargs):
        super().__init__(master, **kwargs)
        self.config = config
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        # Title
        ctk.CTkLabel(self, text="⚙️ Settings", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(10, 5))

        # Model Selector
        ctk.CTkLabel(self, text="Model:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.model_var = ctk.StringVar(value=config.get_model())
        self.model_menu = ctk.CTkOptionMenu(
            self, 
            values=["u2net", "u2netp", "u2net_human_seg", "u2net_cloth_seg"],
            variable=self.model_var,
            command=self.on_model_change
        )
        self.model_menu.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Format Selector
        ctk.CTkLabel(self, text="Format:").grid(row=1, column=2, sticky="e", padx=10, pady=5)
        self.format_var = ctk.StringVar(value=config.get_format())
        self.format_menu = ctk.CTkOptionMenu(
            self,
            values=["PNG", "JPG", "JPEG", "WEBP", "BMP", "GIF", "MP4", "MOV"],
            variable=self.format_var,
            command=self.on_format_change
        )
        self.format_menu.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # Background Selector
        ctk.CTkLabel(self, text="Background:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        
        self.bg_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bg_frame.grid(row=2, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        
        self.bg_type_var = ctk.StringVar(value=config.get_bg_type())
        
        self.rb_none = ctk.CTkRadioButton(self.bg_frame, text="None (Transparent)", variable=self.bg_type_var, value="none", command=self.on_bg_change)
        self.rb_none.pack(side="left", padx=(0, 10))
        
        self.rb_color = ctk.CTkRadioButton(self.bg_frame, text="Solid Color", variable=self.bg_type_var, value="color", command=self.on_bg_change)
        self.rb_color.pack(side="left", padx=10)
        
        self.rb_image = ctk.CTkRadioButton(self.bg_frame, text="Custom Image", variable=self.bg_type_var, value="image", command=self.on_bg_change)
        self.rb_image.pack(side="left", padx=10)

        # Background options (Color Picker / Image File)
        self.bg_options_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bg_options_frame.grid(row=3, column=1, columnspan=3, sticky="w", padx=10, pady=5)

        self.color_preview = ctk.CTkLabel(self.bg_options_frame, text="▮▮▮▮", text_color=config.get_bg_color(), font=("Arial", 20))
        self.color_btn = ctk.CTkButton(self.bg_options_frame, text="Pick Color", command=self.pick_color, width=100)
        
        self.image_path_var = ctk.StringVar(value=config.get_bg_image())
        self.image_entry = ctk.CTkEntry(self.bg_options_frame, textvariable=self.image_path_var, state="readonly", width=200)
        self.image_btn = ctk.CTkButton(self.bg_options_frame, text="Browse Image", command=self.pick_image, width=100)

        self.on_bg_change()

    def on_model_change(self, value):
        self.config.set_model(value)
        
    def on_format_change(self, value):
        self.config.set_format(value)

    def on_bg_change(self):
        val = self.bg_type_var.get()
        self.config.set_bg_type(val)
        
        # Hide all options first
        self.color_preview.pack_forget()
        self.color_btn.pack_forget()
        self.image_entry.pack_forget()
        self.image_btn.pack_forget()

        if val == "color":
            self.color_preview.pack(side="left", padx=(0, 10))
            self.color_btn.pack(side="left")
        elif val == "image":
            self.image_entry.pack(side="left", padx=(0, 10))
            self.image_btn.pack(side="left")

    def pick_color(self):
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Choose background color")
        if color[1]:
            self.color_preview.configure(text_color=color[1])
            self.config.set_bg_color(color[1])

    def pick_image(self):
        file = tk.filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")]
        )
        if file:
            self.image_path_var.set(file)
            self.config.set_bg_image(file)
