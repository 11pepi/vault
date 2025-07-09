'''
Remove a package
'''

import os
import util

def do_deletion(_, dest):
    '''
    Delete file
    '''
    print(f"[do_deletion] Try to delete file... {dest}...", end="   ")
    try:
        os.remove(dest)
        print("Ok")
    except OSError as e:
        print(f"Unknown OS error: {e}")

def delete_files(info, _):
    '''
    Delete ALL FILES (scary!)
    '''
    print("[do_deletion] Ready to delete files...")
    for source, dest in info.copies.items():
        do_deletion(source, dest)

def start(path, prefix, config_file_name="config.py"):
    '''
    start package removal
    '''
    path = os.path.join(prefix, path)
    config_path = os.path.join(path, config_file_name)
    print(f"[start] Start package install for {path}...")

    config = util.load_config(config_path)
    print("[start] Gather information from package... config.information()")
    info = util.gather_information(path, config)

    print("[start] Begin removal...\n\n")
    delete_files(info, config)
    print("\n\n[start] Completed")
