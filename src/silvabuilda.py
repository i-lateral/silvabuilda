## build.py deals with the main execution of SilvaBuilda. Use it as follows:
## 
## python build.py [options] <path/to/config> <path/to/project>
## 
## options
## --local only copies the local working copy, does not putt down remotes (good
##         for updating your local project if your working copy is located
##         seperatly)

__author__="morven"
__date__ ="$07-Jul-2011 23:01:15$"

import os, urllib, sys, shutil
from xml.dom.minidom    import parse
from compressions.zip   import ZipArchive
from compressions.tar   import TarArchive

# Ensure paths are set correctly
args = sys.argv[1:]

# Check if the -l switch is set
if "-l" in args:
    local_only = True
    args.remove('-l')
else:
    local_only = False

try:
    if len(args) == 2:
        config_path, project_path = args
    elif len(args) == 1:
        config_path = args[0]
        project_path = None
except ValueError:
    print 'build.py requires at least a config path'
    sys.exit()

# Load config XML file
config = parse(config_path)

# Set relevent paths based on configuration data
wc_location = config.getElementsByTagName('workingcopy')[0].getAttribute('location')
wc_path = os.path.dirname(config_path) + os.sep
    
if wc_location == 'current':
    path_mod = ''
elif wc_location == 'parent':
    path_mod = ".." + os.sep
elif wc_location == 'grandparent':
    path_mod = ".." + os.sep + ".." + os.sep
    
wc_path = os.path.abspath(wc_path + path_mod) + os.sep

if not project_path:
    project_path = wc_path
    
if not project_path.endswith(os.sep):
    project_path += os.sep
    
if not os.path.exists(project_path):
    os.makedirs(project_path)
    print "Directory Created: " + project_path

# Generate a list of ignores from the config file
ignores = []
for ignore in config.getElementsByTagName('ignore'):
    ignores.append(ignore.getAttribute('name'))


if not local_only:
    # Generate a list of dicts to store the XML remotes data
    remotes = []
    
    for remote in config.getElementsByTagName('remote'):
        remotes.append({
            'name': remote.getAttribute('name'),
            'url': remote.getAttribute('url'),
            'type': remote.getAttribute('type')
        })
    
    # Loop through each remote, download, extract then delete it
    for item in remotes:
        filename = item['name'] + '.' + item['type']
        download_file = project_path + filename
        extract_path = project_path + item['name']
            
        # Check if remote has been downloaded before, if so, remove it
        if os.path.isdir(extract_path):
            shutil.rmtree(extract_path)
            print "Removed module: " + item['name']
        
        print 'Downloading: ' + filename
        remote = urllib.urlopen(item['url'])
        local = open(download_file, 'w')
        local.write(remote.read())
                
        print 'Downloaded: ' + filename
        remote.close()
        local.close()
              
        if item['type'] == "zip":
            archive = ZipArchive(download_file)
              
        elif item['type'] == "tar":
            archive = TarArchive(download_file)
              
        elif item['type'] == "tar.gz":
            archive = TarArchive(download_file,'gz')
              
        elif item['type'] == "tar.bz2":
            archive = TarArchive(download_file,'bz2')
            
        if archive:
            archive.extract(extract_path)
                    
        os.remove(download_file)
        print "Removed: " + filename
    
if not wc_path == project_path:
    # Loop through all files and directories in working copy them to project dir
    for root, dirs, files in os.walk(wc_path):
        # loop through all ignores and remove any files or dirs that match
        for ignore in ignores:
            if ignore in dirs:
                dirs.remove(ignore)
            if ignore in files:
                files.remove(ignore)
    
    
        # Create all required directories
        for d in dirs:
            if not root.endswith(os.sep):
                root = root + os.sep
            
            dest = root + d
            dest = project_path + dest.replace(wc_path,'')
            
            if os.path.isdir(dest):
                shutil.rmtree(dest)
                print 'Directory removed: ' + dest
            
            if not os.path.isdir(dest):
                os.mkdir(dest)
                print 'Directory created at: ' + dest
        
    
        #loop through all files in the directory
        for f in files:
            if not root.endswith(os.sep):
                root = root + os.sep
            
            old = root + f
            new = project_path + old.replace(wc_path,'')
            
            try:
                new_file = open(new,'w')
                new_file.write(open(old,'r').read())
                new_file.flush()
                new_file.close()
                print 'File ' + f + ' copied.'
            except IOError:
                print "Error writing file: " + f