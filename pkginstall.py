import importlib.util
from vaultpkg import VaultPKG
import os

def start(path, config_file_name="config.py"):
    print(f"[start] Starting package install for {path}...")
    config_path = os.path.join(path, config_file_name)

    config = load_config(config_path)
    print(f"[start] Gathering information from package... config.information()")
    info = config.information(VaultPKG())

    print(f"[start] Ready to begin installation... config.build()")
    package = config.build(info)

def load_config(path, module_name="config"):
    print(f"[load_config] Generating spec for {path}...")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec == None:
        print("[load_config] Invalid spec, does the file exist? Quitting with code 1")
        quit(1)

    print(f"[load_config] Exchanging spec for module...")
    # Create a module from that spec
    module = importlib.util.module_from_spec(spec)

    print(f"[load_config] Executing module to create attributes...")
    # Load that module to create it's attributes
    spec.loader.exec_module(module)

    # Donner le module oui oui
    return module

# Change this path to the path of the test C project
start("./vaults/example/example.sh")