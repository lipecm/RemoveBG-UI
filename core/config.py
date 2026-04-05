import os

class Config:
    def __init__(self):
        self.model = "u2net"
        self.format = "PNG"
        self.bg_type = "none" # none, color, image
        self.bg_color = "#FFFFFF"
        self.bg_image = ""
        self.output_path = os.path.join(os.path.expanduser("~"), "Desktop", "RemoveBG_Output")
        self.same_as_source = True

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path, exist_ok=True)

    def get_model(self): return self.model
    def set_model(self, model): self.model = model

    def get_format(self): return self.format
    def set_format(self, fmt): self.format = fmt

    def get_bg_type(self): return self.bg_type
    def set_bg_type(self, t): self.bg_type = t

    def get_bg_color(self): return self.bg_color
    def set_bg_color(self, c): self.bg_color = c

    def get_bg_image(self): return self.bg_image
    def set_bg_image(self, path): self.bg_image = path

    def get_output_path(self): return self.output_path
    def set_output_path(self, path): self.output_path = path

    def get_same_as_source(self): return self.same_as_source
    def set_same_as_source(self, val): self.same_as_source = val
