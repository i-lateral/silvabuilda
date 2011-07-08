import os, tarfile
from abstract import AbstractArchive

class TarArchive(AbstractArchive):
    def extract(self,path):
        self._output_path = path
    
        for member in self._opened_archive.getmembers():
            output = member.name.replace(member.name.split(os.sep)[0], self._output_path, 1)

            if member.isdir():
                self._makedir(output)
                        
            else:
                self._extract_file(member.name,output)
                
    def _open_archive(self):
        if self._archive_type:
            readmode = 'r:' + self._archive_type
        else:
            readmode = 'r' 
        return tarfile.open(self._archive_path,readmode)
    
    def _get_archive_file_contents(self,file_name):
        return self._opened_archive.extractfile(file_name).read()