'''
utilities for the whole program to use
'''
import importlib.util
import logging
import os
import errno
import concurrent.futures as cf
from vaultpkg import VaultPKG
log = logging.getLogger(__name__)

def gather_information(path, config):
    '''
    Gathers information about a given package
    by calling it's information() method
    '''
    log.debug("Gather package information for... %s... config.information()",
             path)
    pkg = VaultPKG(path)
    info = config.information(pkg)
    return info

def load_config(path, module_name="config"):
    '''
    load a config from a given path
    '''
    log.debug("Generate spec for %s...", path)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        log.error("Invalid spec, does the file exist?")
        return 1

    log.debug("Exchange spec for module...")
    # Create a module from that spec
    module = importlib.util.module_from_spec(spec)

    log.debug("Run module to create attributes...")
    # Load that module to create it's attributes
    spec.loader.exec_module(module)

    # Donner le module oui oui
    return module

def for_all_dependencies(info, _config, prefix: str,
                         method, action_name: str,
                         recursive=False):
    '''
    call start_method with parameters on a package's dependencies
    '''
    if len(info.requires) == 0:  # make sure it's not 0-length array
        log.debug("%s... has no dependencies", info.name)
        return

    log.info("%s dependencies for... %s", action_name, info.name)
    for pkgname in info.requires:
        log.info("%s dependency... %s", action_name, pkgname)
        method(
            pkgname,
            prefix,
            recursive=recursive
        )

def explain_permission_error(e: PermissionError) -> str:
    '''
    Outputs one of the following messages depending on error:
    EACCES: Not enough permission to access <filename>
    EPERM: Illigal operation attempted on <filename>
    '''
    match e.errno:
        case errno.EACCES:
            return "Not enough permission to access."
        case errno.EPERM:
            return "Illegal operation attempted."
        case _:
            return f"Unknown permission error: {e.strerror}."

def what_depends_on_this_pkg_worker(dep, prefix: str):
    '''
    The actual worker for what_depends_on_this_pkg
    '''
    import logging
    local_log = logging.getLogger(f"{dep}_worker_dep_query")
    found = []
    for path in os.listdir(prefix):
        full_path = os.path.join(dep, prefix)
        local_log.info("Check... %s", full_path)
        if not os.path.isdir(path):
            log.warning(
                "Found a non-directory inode %s in %s. It's best to remove it",
                path, prefix,
            )
            continue

        # path is ALWAYS a directory by this point
        config = load_config(full_path)
        info = gather_information(full_path, config)
        if dep in info.requires:
            local_log.info("Found! %s", full_path)
            found.append(path)  # use path here, not full_path

    return found

def what_depends_on_this_pkg(info, _config, prefix: str):
    '''
    figures out what depends on this pkg, it's in the name
    '''
    with cf.ThreadPoolExecutor() as tp:
        results = tp.map(
            lambda pkg: what_depends_on_this_pkg_worker(pkg, prefix),
            info.requires
        )
        for result in results:
            print("result", result)
