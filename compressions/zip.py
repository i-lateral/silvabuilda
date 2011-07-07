import os, zipfile
from abstract import AbstractArchive

class ZipArchive(AbstractArchive):
    def extract(self,path):
        self._output_path = path
    
        for name in self._opened_archive.namelist():
            output = name.replace(name.split(os.sep)[0], self._output_path, 1)

            if output.endswith(os.sep):
                self._makedir(output)
                        
            else:
                self._extract_file(name,output)
                
    def _open_archive(self):
        return zipfile.ZipFile(self._archive_path)
    
    def _get_archive_file_contents(self,file_name):
        return self._opened_archive.read(file_name)