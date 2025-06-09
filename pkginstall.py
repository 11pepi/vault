import importlib.util
from vaultpkg import VaultPKG
import pathtracking
import os
import util

def preform_build(info, config):
    package = config.build(info)
    return package

def start(path, vaults_dir, config_file_name="config.py", paths_file_name="paths.sh"):
    print(f"[start] Start package install for {path}...")
    config_path = os.path.join(path, config_file_name)

    config = util.load_config(config_path)
    print(f"[start] Gather information from package... config.information()")
    info = util.gather_information(path, config)

    print(f"[start] Begin installation... config.build()")
    build = preform_build(info, config)

    print(f"[start] Rebuild all paths... rebuild_all_paths()")
    #paths = pathtracking.rebuild_paths(build, "/mnt/sda1/vault/vaults/example/paths.sh")
    pathtracking.rebuild_all_paths(os.path.join(vaults_dir, paths_file_name), vaults_dir)

start("/mnt/sda1/vault/vaults/example", "/mnt/sda1/vault/vaults")
