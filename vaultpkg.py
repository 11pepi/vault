# pylint: disable=method-hidden
'''
The Vault package class (VaultPKG) is defined here.
This is passed to config.py files
'''
from os import chdir
import logging
log = logging.getLogger(__name__)

class VaultPKG:
    '''
    Represents a packge.

    # Methods

    name(n: _str_):
        this method replaces itself with the package's name `n`

    version(v: _str_):
        this method replaces itself with the pacakge's version `v`

    dependency(d: _str_):
        indicates a dependency on a remote package named `d`

    file(d: _str_):
        indicates a file must be copied for installation. Also used
        for removal
    '''
    def __init__(self, root: str):
        self.root: str = root
        self.name: str
        self.version: str
        self.requires: list[str] = []
        self.copies: dict[str, str] = {}
        chdir(root)

    def name(self, n:str):
        '''
        deletes THIS function and replaces it with the given package name.
        It's a good thing we overwrite, because you're only meant to call this
        once.
        '''
        log.debug("Name... %s", n)
        self.name = n
        return self

    def version(self, v:str):
        '''
        deletes THIS function and replaces it with the given package VERSION.
        It's a good thing we overwrite, because you're only meant to call this
        once.
        '''
        log.debug("Version... %s", v)
        self.version = v
        return self

    def dependency(self, d:str):
        '''
        Appends a dependency to the pkg's dependency list
        '''
        log.debug("Dependency... %s", d)
        self.requires.append(d)
        return self

    def file(self, src:str, dest:str):
        '''
        Appends a file copy to the package's copies dict.
        '''
        log.debug("Needs copy... %s -> %s", src, dest)
        self.copies[src] = dest
        return self
