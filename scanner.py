from wia_scan import *
import pythoncom

pythoncom.CoInitialize()

device = prompt_choose_device_and_connect()
pillow_image = scan_side(device=device)
filename = f'scanned_image.jpeg'
pillow_image.save(filename, subsampling=0, optimize=True,
                          progressive=True, quality=80)