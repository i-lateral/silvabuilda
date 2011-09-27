__author__="morven"
__date__ ="$07-Jul-2011 23:40:00$"

import os
from silvabuilda.filesystem import rm_existing,fix_path

class LocalManager:
    def __init__(self,path = None):
        if not path:
            raise ValueError("You must set a path for your working copy")
        else:
            self._base_path = path
        
        self._ignores = []
        self._out_path = None
    
    def execute(self):
        if not self._out_path:
            set_out_path(self._base_path)
        
        for root, dirs, files in os.walk(self._base_path):
            for item in self._ignores:
                self._remove_from_list(dirs,item)
                self._remove_from_list(files,item)
                
            # Create all required directories
            for d in dirs:
                root = fix_path(root)
                
                old = root + d
                new = self._out_path + old.replace(self._base_path,'')

                if rm_existing(new):
                    print 'Directory removed: ' + new

                if not os.path.isdir(new):
                    os.mkdir(new)
                    print 'Directory created at: ' + new
    
            #loop through all files in the directory
            for f in files:
                root = fix_path(root)

                old = root + f
                new = self._out_path + old.replace(self._base_path,'')

                try:
                    new_file = open(new,'w')
                    new_file.write(open(old,'r').read())
                    new_file.flush()
                    new_file.close()
                    print 'File ' + f + ' copied.'
                except IOError:
                    print "Error writing file: " + f
    
    def _remove_from_list(self,base_list = [],item = None):
        if item in base_list:
            base_list.remove(item)        
        return base_list
    
    def set_out_path(self,path = None):
        self._out_path = path
    
    def set_ignores(self,ignores = []):
        self._ignores = ignores