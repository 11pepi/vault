#! /bin/python
import os
import sys
def SetupVault(a):
    os.system("mkdir /vault &> /dev/null")
    try:
        with open("/vault/pkglist","x") as f:
            f.write("vault")
        print("Setup vault!")
    except:
        if not a:
            print("Please don't run setup multiple times!")
        else:
            print("Resetting...")
            os.system("sudo rm -rf /vault")
            print("Finished!")
            SetupVault(False)
try:
    SetupVault(sys.argv[1] == "reset")
except:
    SetupVault(False)