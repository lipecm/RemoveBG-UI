from PIL import Image
import os

assets_dir = 'c:/Users/lfcma/Documents/Programaçao/RemoveBG/assets'
os.makedirs(assets_dir, exist_ok=True)
img = Image.new('RGB', (256, 256), color=(73, 109, 137))
img.save(os.path.join(assets_dir, 'icon.ico'))
