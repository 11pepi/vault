'''
package installation
'''
import os
import shutil
import util

def do_copy(source, dest):
    '''
    copy a file
    '''
    print(f"[do_copy] Try to copy file... {source} -> {dest}...", end="   ")
    try:
        shutil.copy2(source, dest)
        print("Ok")
    except FileNotFoundError:
        print("Copy failed! Source file does not exist")
    except PermissionError:
        print("Copy failed! Permission error")
    except IsADirectoryError:
        print("source is a directory, use copytree... (this isn't an error)")
        shutil.copytree(source, dest, copy_function=do_copy)  # not tested
    except OSError as e:
        print(f"Unknown operating system error: {e}")

def copy_files(info, _):
    '''
    copy files needed for
    '''
    print("[copy_files] Ready to copy files needed...")
    for source, dest in info.copies.items():
        do_copy(source, dest)

def preform_build(info, config):
    '''
    execute build()
    '''
    package = config.build(info)
    return package

def start(path, prefix, config_file_name="config.py"):
    '''
    start package installation
    '''
    path = os.path.join(prefix, path)
    config_path = os.path.join(path, config_file_name)
    print(f"[start] Start package install for {path}...")

    config = util.load_config(config_path)
    print("[start] Gather information from package... config.information()")
    info = util.gather_information(path, config)

    print("[start] Begin installation... config.build()\n\n")
    build = preform_build(info, config)

    print("\n\n[start] Completed")
    copy_files(info, config)
    return build

#start("/mnt/sda1/vault/vaults/example", "/mnt/sda1/vault/vaults")
