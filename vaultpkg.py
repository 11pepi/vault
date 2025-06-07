import os
import sys
import shutil

class PackagingError(BaseException):
    def __init__(self, package):
        self.package = package

class VaultPKG:
    package_root: str = "/mnt/sda1/vault/example"  # Hardcoded for my testing
    source_dir_name: str = "sources"
    output_dir_name: str = "binaries"
    src_root: str
    dest_root: str
    name: str
    def set_name(self, n:str):
        print(f"[information] Name is... {n}")
        self.name = n
        return self
    
    version: str
    def set_version(self, v:str):
        print(f"[information] Version is... {v}")
        self.version = v
        return self

    def copy_file(self, src, dest):
        print(f"[package] Copy file... {src} -> {dest}")
        shutil.copy2(
            src,
            dest
        )  # copy2 preserves file metadata
        return self

    def move_file(self, src, dest):
        print(f"[package] Move file... {src} -> {dest}")
        shutil.move(
            src,
            dest
        )  # copy2 preserves file metadata
        return self

    def copy_directory(self, src, dest):
        print(f"[package] Copy directory... {src} -> {dest}")
        shutil.copytree(
            src,
            dest,
            dirs_exist_ok=True
        )  # fuck
        return self

    def enter_directory(self, dir):
        path = os.path.join(self.package_root, dir)
        os.chdir(path)

        print(f"[package] Enter directory... {path}")
        return self
    
    def enter_package_root(self):
        print(f"[package] Enter package root... {self.package_root}")
        os.chdir(self.package_root)
        return self

    def enter_source_dir(self):
        path = os.path.join(self.package_root, self.source_dir_name)
        os.chdir(path)

        print(f"[package] Enter source dir... {path}")
        return self

    def enter_output_dir(self):
        path = os.path.join(self.package_root, self.output_dir_name)
        os.chdir(path)

        print(f"[package] Enter output dir... {path}")
        return self

    def command(self, cmd):
        os.system(cmd)   # Maybe dont put this one in prod tho

        print(f"[package] Execute... {cmd}")
        return self
    
    def gnu_make_target(self, targets, num_jobs=os.cpu_count()):
        # DO NOT USE THIS IN PROD, USE SUBPROCESS INSTEAD
        cmd = f"make {targets} -j {num_jobs}"
        os.system(cmd)

        print(f"[package] Build... {cmd}...")
        return self
    
    def python(self, src):
        exec(src, {"self": self, "os": os, "sys": sys})

        print(f"[package] Run python code... {src}")
        return self

    def _eval_python(self, src):
        return eval(src, {"self": self, "os": os, "sys": sys})

    def terminate_ok(self, msg:str = ""):
        print(f"[package] Terminate build proces... Build OK...")
        print(msg)
        return self

    def terminate_err(self, msg:str = ""):
        print(f"[package] Terminate build proces... Build ERROR...")
        print(msg)
        return PackagingError(package=self)
    
    def condition(self, condition, t, f):
        print(f"[package] Evaluate condition... {condition}")
        if self._eval_python(condition):
            if t == "":
                print("[package] Skipping empty truthy code...")
                return self

            print(f"[package] Execute truthy code... {t}... passing in self")
            return self.python(t)
        else:
            if f == "":
                print("[package] Skipping empty falsy code...")
                return self
            print(f"[package] Execute falsy code... {f}... passing in self")
            return self.python(f)
