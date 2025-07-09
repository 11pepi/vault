from vaultpkg import VaultPKG
import importlib.util

def gather_information(path, config):
    print(f"[gather_information] Gather package information for... {path}... config.information()")
    pkg = VaultPKG(path)
    info = config.information(pkg)
    return info

def load_config(path, module_name="config"):
    print(f"[load_config] Generating spec for {path}...")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        print("[load_config] Invalid spec, does the file exist? Error 1")
        return 1

    print("[load_config] Exchanging spec for module...")
    # Create a module from that spec
    module = importlib.util.module_from_spec(spec)

    print("[load_config] Executing module to create attributes...")
    # Load that module to create it's attributes
    spec.loader.exec_module(module)

    # Donner le module oui oui
    return module
