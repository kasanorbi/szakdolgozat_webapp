import os
import tempfile
import win32com.client

from datetime import datetime
from PIL import Image as PILImage


WIA_ID_UNKNOWN = '{00000000-0000-0000-0000-000000000000}'

WIA_FORMAT_BMP = '{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}'
WIA_FORMAT_PNG = '{B96B3CAF-0728-11D3-9D7B-0000F81EF32E}'
WIA_FORMAT_GIF = '{B96B3CB0-0728-11D3-9D7B-0000F81EF32E}'
WIA_FORMAT_JPEG = '{B96B3CAE-0728-11D3-9D7B-0000F81EF32E}'
WIA_FORMAT_TIFF = '{B96B3CB1-0728-11D3-9D7B-0000F81EF32E}'

WIA_COMMAND_SYNCHRONIZE = "{AF933CAC-ACAD-11D2-A093-00C04F72DC3C}"
WIA_COMMAND_TAKE_PICTURE = "{AF933CAC-ACAD-11D2-A093-00C04F72DC3C}"
WIA_COMMAND_DELETE_ALL_ITEMS = "{E208C170-ACAD-11D2-A093-00C04F72DC3C}"
WIA_COMMAND_CHANGE_DOCUMENT = "{04E725B0-ACAE-11D2-A093-00C04F72DC3C}"
WIA_COMMAND_UNLOAD_DOCUMENT = "{1F3B3D8E-ACAE-11D2-A093-00C04F72DC3C}"

WIA_EXTENSION_TO_FORMAT = {
    'bmp': WIA_FORMAT_BMP,
    'png': WIA_FORMAT_PNG,
    'gif': WIA_FORMAT_GIF,
    'jpeg': WIA_FORMAT_JPEG,
    'tiff': WIA_FORMAT_TIFF,
}

NOT_VERBOSE_PRINT_DEVICE_PROPERTIES = [
    'Unique Device ID', 'Manufacturer', 'Description', 'Server', 'Port', 'Name']

class IndentPrinter:

    def __init__(self, indent):
        self.indent = indent
    
    def __call__(self, *args, **kwargs):
        total_indent = self.indent + kwargs.get('indent', 0)

        args_as_string = " ".join([str(x) for x in args])
        output = (' ' * total_indent) + args_as_string

def format_id_to_extension(wia_id):
    for name, value in WIA_EXTENSION_TO_FORMAT.items():
        if value == wia_id:
            return name
    return 'UNKNOW_WIA_FORMAT'

def get_device_manager():
    device_manager = win32com.client.Dispatch("WIA.DeviceManager")
    return device_manager

def choose_device_and_connect():
    device_manager=get_device_manager()
    device_uid = choose_device(device_manager)
    device = connect_device(device_manager=device_manager, device_uid=device_uid)
    
    return device


def connect_device(device_manager, device_uid):
    if not device_uid:
        raise ValueError('Nem létező/elérhető device_uid!')
    device_info = get_device_info_by_unique_id(device_manager, unique_id=device_uid)
    if device_info is None:
        raise ValueError('Nem található eszköz ilyen azonosítóval.')
    
    device = device_info.Connect()

    device = get_scan_source(device)

    return device

def choose_device(device_manager):
    if device_manager.DeviceInfos.Count == 0:
        raise ValueError("Nincs választható eszköz")
    
    device_ids = []
    for item_index in range(1, device_manager.DeviceInfos.Count+1):
        device_info = device_manager.DeviceInfos(item_index)
        device_ids.append(device_info.DeviceID)
    
    return device_ids[0]

def get_device_info_by_unique_id(device_manager, unique_id):
    assert isinstance(unique_id, str)
    return device_manager.DeviceInfos(unique_id)

def get_scan_source(device):
    if device.Items.Count == 1:
        device = device.Items(1)
    elif device.Items.Count == 0:
        pass
    else:
        raise NotImplementedError('Egyetlen forrás van implementálva csak jelenleg')

    return device

def connect_to_device_by_uid(device_uid):
    device_manager = get_device_manager()
    device = connect_device(device_manager=device_manager, device_uid=device_uid)

def scan_side(device, scan_profile=None, return_wia_image=False):

    if scan_profile is None:
        scan_profile = get_default_profile()

    device.Properties('Brightness').Value = scan_profile['brightness']
    device.Properties('Contrast').Value = scan_profile['contrast']
    device.Properties('Horizontal Resolution').Value = scan_profile['dpi']
    device.Properties('Vertical Resolution').Value = scan_profile['dpi']
    if scan_profile['mode'] == 'RGB':
        device.Properties('Data Type').Value = 3
    elif scan_profile['mode'] == 'L':
        device.Properties('Data Type').Value = 2
    else:
        raise ValueError('Nem támogatott beolvasási mód')
    
    for command in device.Commands:
        if command.CommandID == WIA_COMMAND_TAKE_PICTURE:
            device.ExecuteCommand(WIA_COMMAND_TAKE_PICTURE)

    wia_image = device.Transfer(WIA_FORMAT_BMP)

    if return_wia_image:
        return wia_image
    
    tmp_directory = tempfile.mkdtemp()
    tmp_file_name = os.path.join(tmp_directory, 'tmp.png')

    wia_image.SaveFile(tmp_file_name)

    pillow_image_file = PILImage.open(tmp_file_name)
    pillow_image = pillow_image_file.copy()
    pillow_image_file.close()

    os.remove(tmp_file_name)
    os.rmdir(tmp_directory)

    return pillow_image

def run_calibration_process(start_range, end_range, num_runs, device_uid, output_folder):
    assert num_runs > 1

    device = connect_to_device_by_uid(device_uid=device_uid)

    for i in range(num_runs):
        lam_ = i / float(num_runs - 1)
        brightness = (1.0 - lam_) * start_range + lam_ * end_range
        scan_profile = {
            'brightness' : brightness,
            'contrast' : 0,
            'dpi' : 100,
            'mode' : 'RGB'
        }
        
        pillow_image = scan_side(device=device, scan_profile=scan_profile)
        filepath = os.path.join(
            output_folder, f'run={i+1}_brightness={brightness}.jpg')
        pillow_image.save(filepath, subsampling=0, optimize=True, progressive=True, quality=80)

def combine_images_vertically(image_list, mode):
    assert len(image_list) > 0
    if len(image_list) == 1:
        return image_list[0]

    combined_image_width = 0
    combined_image_height = 0
    for pillow_image in image_list:
        combined_image_width = max(combined_image_width, pillow_image.size[0])
        combined_image_height = combined_image_height + pillow_image.size[1]

    pillow_image_combined = PILImage.new(mode,
                                         (combined_image_width, combined_image_height))

    y_offset = 0
    for pillow_image in image_list:
        pillow_image_combined.paste(pillow_image, (0, y_offset))
        y_offset = y_offset + pillow_image.size[1]

    return pillow_image_combined


def save_image_list(image_list, filepath, profile):
    file_extension = filepath.split(os.extsep)[-1].lower()

    if file_extension in ['jpg', 'jpeg', 'png', 'bmp', 'tga', 'tiff']:
        pillow_image_combined = combine_images_vertically(image_list,
                                                          mode=profile['mode'])
        pillow_image_combined.save(filepath, subsampling=0, optimize=True,
                                   progressive=True, quality=profile['jpeg_quality'])
    elif file_extension == 'pdf':
        image_list[0].save(filepath, save_all=True, append_images=image_list[1:],
                           resolution=profile['dpi'], subsampling=0, optimize=True,
                           progressive=True, quality=profile['jpeg_quality'])
    else:
        raise ValueError("Nem várt kiterjesztés")


def get_profiles():
    profiles = {
        'm': {
            'name': 'Medium Quality',
            'file_extension': 'png',
            'mode': 'RGB',
            'dpi': 300,
            'jpeg_quality': 100,
            'brightness': 0,
            'contrast': 0,
        },
        'c': {
            'name': 'Colored',
            'file_extension': 'jpg',
            'mode': 'RGB',
            'dpi': 200,
            'jpeg_quality': 75,
            'brightness': 0,
            'contrast': 0,
        },
        'g': {
            'name': 'Grayscale',
            'file_extension': 'jpg',
            'mode': 'L',
            'dpi': 200,
            'jpeg_quality': 75,
            'brightness': 0,
            'contrast': 0,
        },
        'pm': {
            'name': 'PDF-Medium Quality',
            'file_extension': 'pdf',
            'mode': 'RGB',
            'dpi': 300,
            'jpeg_quality': 90,
            'brightness': 0,
            'contrast': 0,
        },
        'pc': {
            'name': 'PDF-Colored',
            'file_extension': 'pdf',
            'mode': 'RGB',
            'dpi': 200,
            'jpeg_quality': 75,
            'brightness': 0,
            'contrast': 0,
        },
        'pg': {
            'name': 'PDF-Grayscale',
            'file_extension': 'pdf',
            'mode': 'L',
            'dpi': 200,
            'jpeg_quality': 75,
            'brightness': 0,
            'contrast': 0,
        }
    }
    return profiles

def get_default_profile():
    return get_profiles()['m']


def scan_single_side_main(scan_profile=None, device_uid=None, output_file=None):
    if scan_profile is None:
        scan_profile = get_default_profile()

    device = connect_to_device_by_uid(device_uid=device_uid)

    pillow_image = scan_side(device=device, scan_profile=scan_profile, return_wia_image=False)

    if not output_file:
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        file_extension = scan_profile['file_extension']
        output_file = f'scan_{date_string}.{file_extension}'

    save_image_list([pillow_image], filepath=output_file, profile=scan_profile)

def scan():
    device = choose_device_and_connect()

    pillow_image = scan_side(device=device)
    filename = f'temp.jpeg'
    pillow_image.save(filename, subsampling=0, optimize=True, progressive=True, quality=80)


