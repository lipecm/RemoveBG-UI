import os

class FileManager:
    def __init__(self, config):
        self.config = config
        self.files = []

    def add_files(self, new_files):
        # Prevent duplicates
        for f in new_files:
            if f not in self.files and os.path.exists(f):
                self.files.append(f)

    def get_files(self):
        return self.files

    def clear(self):
        self.files = []

    def get_output_filepath(self, input_path):
        base_name = os.path.basename(input_path)
        name, _ = os.path.splitext(base_name)
        
        # Force extension based on user format setting
        ext = "." + self.config.get_format().lower()

        out_name = f"{name}_nobg{ext}"

        if self.config.get_same_as_source():
            out_dir = os.path.dirname(input_path)
        else:
            out_dir = self.config.get_output_path()

        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception:
                pass # Will likely fail during write

        return os.path.join(out_dir, out_name)
