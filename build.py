###############################################################################
##
## build.py deals with the main execution of SilvaBuilda. Use it as follows:
## 
## python build.py [options] <path/to/config> <path/to/project>
## 
## options
## --local only copies the local working copy, does not putt down remotes (good
##         for updating your local project if your working copy is located
##         seperatly)
##
###############################################################################

import os, urllib, sys
from xml.dom.minidom import parse 
from compressions.zip import ZipArchive
from compressions.tar import TarArchive

try:
    config_path, project_path = sys.argv[1:]
except ValueError:
    print 'build.py requires paths to config and project'
    sys.exit()

if not project_path.endswith('/'):
    project_path += '/'
    
if not os.path.exists(project_path):
    os.mkdir(project_path)
    print "Directory Created: " + project_path

config = parse(config_path)

components = []

for remote in config.getElementsByTagName('remote'):
    components.append({
        'name': remote.getAttribute('name'),
        'url': remote.getAttribute('url'),
        'type': remote.getAttribute('type')
    })


for item in components:
    filename = item['name'] + '.' + item['type']
    download_file = project_path + filename
    extract_path = project_path + item['name']
        
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