'''
Remove a package
'''
import os
import logging
import util
log = logging.getLogger(__name__)

def do_deletion(_, dest):
    '''
    Delete file
    '''
    log.info("Delete file... %s...", dest)
    try:
        os.remove(dest)
    except FileNotFoundError:
        log.error("Removal failed! file does not exist")
    except PermissionError as e:
        log.error("Removal failed! Permission error: %s", util.explain_permission_error(e))
    except IsADirectoryError:
        log.error("Removal failed! OS apparently can't wanna copy directories\
                  (this is probably a bug in the operating system kernel)")
    except OSError as e:
        log.error("Unknown operating system error: %s", e)

def delete_files(info, _):
    '''
    Delete ALL FILES (scary!)
    '''
    log.info("Delete files...")
    for source, dest in info.copies.items():
        do_deletion(source, dest)

def start(path, prefix, config_file_name="config.py", recursive=False):
    '''
    start package removal
    '''
    path = os.path.join(prefix, path)
    config_path = os.path.join(path, config_file_name)
    log.info("Start package uninstall for %s...", path)

    config = util.load_config(config_path)
    info = util.gather_information(path, config)

    log.info("Begin removal...")
    delete_files(info, config)
    if recursive:
        util.for_all_dependencies(info, config, prefix,
                                method=start,
                                action_name="Uninstall",
                                recursive=True)
    else:
        log.debug("Skip dependency install... `recursive == False`")

    log.info("Execute postremoval script...")
    config.endremoval(config)
