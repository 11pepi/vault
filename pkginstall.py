'''
package installation
'''
import os
import shutil
import logging
import util
log = logging.getLogger(__name__)

def do_copy(source, dest):
    '''
    copy a file
    '''
    log.info("Copy file... %s -> %s...", source, dest)
    try:
        shutil.copy2(source, dest)
    except FileNotFoundError:
        log.error("Copy failed! Source file does not exist")
    except PermissionError as e:
        log.error("Removal failed! Permission error: %s", util.explain_permission_error(e))
    except IsADirectoryError:
        log.info("source is a directory, use copytree...")
        shutil.copytree(source, dest, copy_function=do_copy)  # not tested
    except OSError as e:
        log.error("Unknown operating system error: %s", e)

def copy_files(info, _):
    '''
    copy package files
    '''
    log.info("Ready to copy files...")
    for source, dest in info.copies.items():
        do_copy(source, dest)

def preform_build(info, config):
    '''
    execute build()
    '''
    log.info("Begin installation... config.build()")
    package = config.build(info)
    return package

def start(path: str, prefix: str, config_file_name="config.py", recursive=False):
    '''
    start package installation
    '''
    path = os.path.join(prefix, path)
    config_path = os.path.join(path, config_file_name)
    log.info("Start package install for %s...", path)

    config = util.load_config(config_path)
    info = util.gather_information(path, config)

    preform_build(info, config)

    copy_files(info, config)

    log.info("Install dependencies...")
    if recursive:
        util.for_all_dependencies(info, config, prefix,
                                method=start,
                                action_name="Install",
                                recursive=True)
    else:
        log.info("Skip dependency install... `recursive == False`")

    log.info("Execute postinstall script...")
    config.endinstall(info)

