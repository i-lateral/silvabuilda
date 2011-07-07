import os

class AbstractArchive:
    """
    AbstractArchive creates a simple abstract for other module decompression
    libraries.
    
    The purpose of these libraries is to deal with the process of extracting 
    silverstripe modules and placing them in the relevent location in the
    document root of your website install.
    
    Providing an abstraction means that in time, additional archive formats can
    be added more easily.
    
    
    """
    def __init__(self,archive_path,archive_type = None):
        """
        Initialise class, setup core variables, then retrieve the archive
        from the path and open it. 
        
        Keyword arguments:
        archive_path -- path to archive file (absolute or relative)
        archive_type -- *optional* use this if you need to identify a sup archive
                        type (eg: you must set 'gz' or 'bz2' for TarArchive)
        
        Variables:
        _archive_path -- path to archive file to be extracted
        _opened_archive -- an opened archive object, using the class' internal
                           method self._open_archive()
        _output_path -- path to extract to
        
        """
        self._archive_path = archive_path
        self._archive_type = archive_type
        self._opened_archive = self._open_archive()
        self._output_path = None
        
    def extract(self,path = None):
        """
        Method that deals with the overall process of extracting files from the
        downloaded archive
        
        Keyword arguments:
        path -- location that archive will be extracting to
        
        """
        raise NotImplementedError
        
    def _open_archive(self):
        """
        Method that deals with opening the archived file as an archive object that
        can be dealt with by the class
        
        __return__ return an archive object, opened using the relevent archive class
                   EG: zipfile.ZipFile(self._archive_path)
        
        """
        raise NotImplementedError
        
        
    def _get_contents(self):
        """
        Method responsible for returning a list of all files from within the
        archive opened file.
        
        __return__ list of file paths from within the archive
        
        """
        raise NotImplementedError
        
    def _extract_file(self,ar_file,out_file):
        """
        Extract existing file from archive and add to output directory.
        
        Keyword arguments:
        ar_file -- Path to file WITHIN the archive
        out_file -- Path to where the file will be extracted
        
        """
        outfile = open(out_file, 'wb')
        outfile.write(self._get_archive_file_contents(ar_file))
        outfile.flush()
        outfile.close()
        print "Extracted: " + out_file
        
    def _makedir(self,path):
        """
        Check if the current path exists and if not, create it.
        
        Keyword arguments:
        path -- Path of the directory that needs to be created
                (absolute or relative) 
        
        """
        if not os.path.exists(path):
            os.mkdir(path)
            print "Directory Created: " + path
        else:
            print "Directory: " + path + "exists"
