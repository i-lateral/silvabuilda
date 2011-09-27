# build.py deals with the main execution of SilvaBuilda. Use it as follows:
# 
# python build.py [options] <path/to/config> <path/to/project>
# 
# options
# --local only copies the local working copy, does not putt down remotes (good
#         for updating your local project if your working copy is located
#         seperatly)

__author__="morven"
__date__ ="$07-Jul-2011 23:01:15$"

import os
import sys

from xml.dom.minidom import parse
from silvabuilda.filesystem.remotes import RemoteManager
from silvabuilda.filesystem.locals import LocalManager

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

if not local_only:
    # Generate a list of dicts to store the XML remotes data
    remotes = []  
    for remote in config.getElementsByTagName('remote'):
        remotes.append({
            'name': remote.getAttribute('name'),
            'url': remote.getAttribute('url'),
            'type': remote.getAttribute('type')
        })
    
    RemoteManager(remotes,project_path)
 
if not wc_path == project_path:
    # Generate a list of ignores from the config file
    ignores = []
    for ignore in config.getElementsByTagName('ignore'):
        ignores.append(ignore.getAttribute('name'))
        
    locals = LocalManager(wc_path)
    locals.set_ignores(ignores)
    locals.set_out_path(project_path)
    locals.execute()