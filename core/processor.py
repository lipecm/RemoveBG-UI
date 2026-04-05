import os
import subprocess
import threading
from PIL import Image

class Processor:
    """
    Handles the execution of the `backgroundremover` AI CLI engine.
    Runs tasks asynchronously in a background thread to prevent GUI freezing.
    """
    def __init__(self, config):
        self.config = config
        self.is_processing = False

    def process_files(self, files, config, file_manager, on_progress, on_file_complete, on_batch_complete, on_error):
        """
        Starts processing a list of files sequentially on a detached Daemon thread.
        Uses callbacks to continually update the GUI progress.
        """
        if self.is_processing:
            return

        self.is_processing = True

        def worker():
            total = len(files)
            for i, f in enumerate(files):
                try:
                    on_progress(i, total, os.path.basename(f))
                    out_path = file_manager.get_output_filepath(f)
                    
                    # Core subprocess execution
                    self._process_single_file(f, out_path, config)
                    
                    on_file_complete(f, out_path, i+1)
                except Exception as e:
                    on_error(str(e))
                    self.is_processing = False
                    return

            on_batch_complete()
            self.is_processing = False

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def _process_single_file(self, input_path, output_path, config):
        fmt = config.get_format().upper()
        is_video_input = input_path.lower().endswith((".mp4", ".mov", ".gif"))
        is_video_output = fmt in ["MP4", "MOV", "GIF"]
        
        # Temp output for transparent PNG before optional compositing
        # Only composite if output is a static image format like PNG/JPG/WEBP
        temp_out = output_path
        needs_compositing = not is_video_output and config.get_bg_type() in ["color", "image"]
        if needs_compositing:
            temp_out = output_path + ".temp.png"

        cmd = [
            "backgroundremover",
            "-i", input_path,
            "-o", temp_out,
            "-m", config.get_model()
        ]

        if is_video_input:
            if fmt == "GIF":
                cmd.append("-tg")
            elif fmt == "MOV":
                cmd.append("-tv")
            else:
                cmd.append("-mk")
            
        print(f"Executing: {' '.join(cmd)}")
        
        # Run subprocess, hide console window on Windows
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # This will block until the command completes
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            startupinfo=startupinfo
        )

        if result.returncode != 0:
            raise Exception(f"Process failed: {result.stderr}")

        if needs_compositing:
            self._apply_background(temp_out, output_path, config)
            if os.path.exists(temp_out):
                os.remove(temp_out)

    def _apply_background(self, fg_path, out_path, config):
        fg = Image.open(fg_path).convert("RGBA")
        
        if config.get_bg_type() == "color":
            bg = Image.new("RGBA", fg.size, config.get_bg_color())
            bg.paste(fg, (0, 0), fg)
        elif config.get_bg_type() == "image" and config.get_bg_image():
            try:
                custom_bg = Image.open(config.get_bg_image()).convert("RGBA")
                # Resize to fit fg
                bg = custom_bg.resize(fg.size, Image.Resampling.LANCZOS)
                bg.paste(fg, (0, 0), fg)
            except Exception as e:
                print(f"Failed to load background image: {e}")
                # Fallback to white or save transparent
                bg = Image.new("RGBA", fg.size, (255, 255, 255, 255))
                bg.paste(fg, (0, 0), fg)
        else:
            bg = fg # should not happen

        # convert appropriately based on format
        fmt = config.get_format().upper()
        if fmt == "JPG" or fmt == "JPEG":
            bg = bg.convert("RGB")
            bg.save(out_path, "JPEG", quality=95)
        elif fmt == "WEBP":
            bg.save(out_path, "WEBP")
        elif fmt == "BMP":
            bg = bg.convert("RGB")
            bg.save(out_path, "BMP")
        elif fmt == "GIF":
            # For static image saved as GIF
            bg.save(out_path, "GIF")
        else:
            bg.save(out_path, "PNG")

