__author__="morven"
__date__ ="$07-Jul-2011 23:39:04$"

import os
import shutil
import urllib

from compressions.tar import TarArchive
from compressions.zip import ZipArchive

class RemoteManager:
    """
    RemoteManager deals with retrieving a list of sources past to it from an
    XML list of remotes
    
    """
    
    def __init__(self,remotes = None,download_path = None):        
        if not remotes or not download_path:
            raise ValueError("no remotes data  or download path provided")
        
        self._base_path = download_path
        self._remotes = remotes
        self._loop_remotes()
    
    
    def _loop_remotes(self):
        for item in self._remotes:
            filename = item['name'] + '.' + item['type']
            
            print self._base_path
            
            download_path = self._base_path + filename
            extract_path = self._base_path + item['name']
            
            if self._existing_dir(extract_path):
                print "Directory deleted: " + extract_path
                
            print "Attempting to download: " + filename
            
            if self._download(item['url'],download_path):
                print "File downloaded: " + filename
            
            archive = self._get_archive(download_path,item['type'])
            archive.extract(extract_path)
            print "Extracted :" + filename

            os.remove(download_path)
            print "Removed: " + filename
            
        return True
        
    
    def _existing_dir(self, loc):
        """
        Used to check if a location already exists, if it does, delete it and
        return true
        
        """
        if os.path.isdir(loc):
            shutil.rmtree(loc)
            return True
        else:
            return False
        
    
    def _download(self,url,path):
        
        """
        Check if remote has been downloaded before, if so, remove it
        
        """
        try:
            remote = urllib.urlopen(url)
            local = open(path, 'w')
            local.write(remote.read())
            remote.close()
            local.close()
            return True
        except IOError:
            print 'Unable to download module'
            
    
    def _get_archive(self,file,type):
        """
        Determin which compression library to decompress the downloaded archive
        with using the provided type
        
        """
        
        if type == "zip":
            archive = ZipArchive(file)
              
        elif type == "tar":
            archive = TarArchive(file)
              
        elif type == "tar.gz":
            archive = TarArchive(file,'gz')
              
        elif type == "tar.bz2":
            archive = TarArchive(file,'bz2')
        
        return archive
    
    