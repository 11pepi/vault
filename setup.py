#! /bin/python
import os
import sys
def set_up_vault(reset_i_think):
    '''
    set up vault for the first time
    '''
    os.system("mkdir /vault &> /dev/null")
    try:
        with open("/vault/pkglist","x") as f:
            f.write("vault")
        print("[vault] Completed setup of vault")
    except Exception:
        if not reset_i_think:
            print("[vault] Please don't run setup multiple times!")
        else:
            print("[vault] Resetting...")
            os.system("sudo rm -rf /vault")
            print("[vault] Finished!")
            set_up_vault(False)

if __name__ == "__main__":  # prevent running this code on module import
    try:
        set_up_vault(sys.argv[1] == "reset")
    except IndexError:
        set_up_vault(False)
