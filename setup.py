'''
handles setting up and removing vault
'''
#!/bin/python
import os
from shutil import rmtree

def setup(dbpath="/global/vault/db"):
    '''
    set up vault for the first time
    '''
    try:
        # safer than system()
        print(f"Create... {dbpath}")
        os.makedirs(dbpath)
    except Exception as e:
        print(f"error {e}")

def arson(dbpath="/global/vault/db"):
    '''
    does arson on the DB
    いめ４４
    https://www.youtube.com/watch?v=F4REaTQgcXs
    '''
    try:
        print(f"Remove... {dbpath}")
        rmtree(dbpath)
    except Exception as e:
        print(f"error {e}")
