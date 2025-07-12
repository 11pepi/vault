'''
handles setting up and removing vault
'''
#!/bin/python
import os

def set_up_vault(reset_i_think):
    '''
    set up vault for the first time
    '''
    try:
        # safer than system()
        os.makedirs("/globals/vault/db")
    except Exception:
        if not reset_i_think:
            print("Please don't run setup multiple times!")
        else:
            print("Remove... /globals/vault/db")
            os.system("sudo rm -rf /globals/vault/db")
            print("Done!")
            set_up_vault(False)
