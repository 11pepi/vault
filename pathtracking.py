import os
import util

def build_path_line(full_path):
    return f"export PATH=\"{full_path}:$PATH\"\n"

def generate_paths(pkg) -> list[str]:
    print(f"[generate_paths] generate paths for... {pkg.package_root}")
    lines = []
    for path in pkg.paths:
        full_path = os.path.join(
            pkg.package_root,
            path
        )
        line = build_path_line(full_path)
        print(f"[rebuild_path] Built line... {line}")
        lines.append(line)
    
    return lines

def rebuild_paths(pkg, filepath):
    print(f"[rebuild_paths] rebuild paths for... {pkg.package_root} ({pkg.paths_file})")
    with open(filepath, mode="w") as f:
        f.truncate(0)
        paths = generate_paths(pkg)
        f.writelines(paths)
    
    return paths

def rebuild_all_paths(filepath, vaults_dir, config_file_name="config.py", paths_file_name="paths.sh"):
    lines = []
    for package_dirname in os.listdir(vaults_dir):
        print(f"[rebuild_all_paths] Rebuild paths for... {package_dirname}")
        config_path = os.path.join(vaults_dir, package_dirname, config_file_name)
        config = util.load_config(config_path)

        info = util.gather_information(os.path.join(vaults_dir, package_dirname), config)
        paths = rebuild_paths(info, os.path.join(info.package_root, info.paths_file))
        lines.extend(paths)

    with open(filepath, mode="w") as f:
        f.truncate(0)
        f.writelines(lines)