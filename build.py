import os, urllib
from builda.zip import ZipArchive
from builda.tar import TarArchive

components = {
    'sapphire': {
        'url': 'https://github.com/silverstripe/sapphire/tarball/2.4.5',
        'type': 'tar.gz'
    },
    'cms': {
        'url': 'https://github.com/silverstripe/silverstripe-cms/zipball/2.4.5',
        'type': 'zip'
    }
}

for item in components.iteritems():
    filename = item[0] + '.' + item[1]['type']
        
    print 'Downloading: ' + filename
    remote = urllib.urlopen(item[1]['url'])
    local = open(filename, 'w')
    local.write(remote.read())
            
    print 'Downloaded: ' + filename
    remote.close()
    local.close()
          
    if item[1]['type'] == "zip":
        archive = ZipArchive(filename)
        archive.extract(item[0])
          
    elif item[1]['type'] == "tar.gz":
        archive = TarArchive(filename,'gz')
        archive.extract(item[0])
          
    elif item[1]['type'] == "tar.bz2":
        archive = TarArchive(filename,'bz2')
        archive.extract(item[0])
                
    os.remove(filename)
    print "Removed: " + filename