# SilvaBuilda: The Silverstripe Build Tool

Silvabuilda is intended to be a simple tool that will alow you to manage your
silverstripe project modules without having to commit them all to your project
repo (which, quite frankly, is annoying).

The tool can be used to download all your project modules as Zip files and
Tarballs, then extract them into a "project root". Then copy your existing
developed code from your working copy into this root as well.

## Intended use

It is still early days, but the intention of this project is to allow you to
do the following:

1. Create a "Build file" (probably xml) that you can drop in your project root
   detailing all external packages that you would like to use for your install

2. Run the build.py file providing your confiog location and project root
   location

3. Let builda download, extract and then cleanup your project directory and sync
   your working copy with it

## Requirements

### The command line tool

The CLI is written in pure Python, so all you should need is an install of
Python 2 (2.6+ is recommended).

### Web interface

Not sure how this will be implemented yet, but I am imagining that it will use
PHP 5.3. So in order to make use of this you would need a webserver capable of
executing php documents.

## Instalation

As long as python is installed, all you need to do is the following:

1. Download SilvaBuilda and extract to a folder on your computer
2. CD to that folder from your command line
3. Run python build.py [options] </path/to/config> </path/to/project/folder/>

## Usage

SilvaBuilda can be used in 2 ways. You can use it to either:

### Combine local and remote in a seperate location

Combine a local working copy with a pre defined set of remote modules into a
seperate project directory (say inside a web root).

To do this you just need to run build.py with two arguments:

1. The location of your config file
2. The location of your project directory

*example:*
    python build.py /path/to/config/file /path/to/ptoject/directory/

### Pull remote files into your working copy

Pull down remote files into your working copy. This can be usefull to automate
adding common modules to your repo, or combined with something like .gitignore,
would allow you to use external modules without adding them to your repo.

To use this option, you only need to add one argument:

1. The location of your config file

*example:*
    python build.py /path/to/config/file
    
*NOTE*: In both instances above, the config file MUST be inside your working
copy and must have the <workingcopy/> element set (explained in configuration
below)
 
## Switches

You can also use the "-l" switch to set SilvaBuila to build only using your
local working copy.

Why would you want to do this? Well, if your working copy is located seperatly
to your project directory and you make code changes that you want to preview,
runnin with this flag will only copy your local files and not pull down remote
modules 

## Configuration

The idea behind SilvaBuilda is to create a tool that allows you to keep your
working copy of a project, seperater from modules that you will not be
developing. Because of Silverstripe's modular nature, you can end up with a
project containing loads of folders that you will never open or use!

In order to achieve this, you will only need to create an XML config file
(something like builda.config) and drop it into your working copy. This will
identify all your remote modules as zip files or tarballs.

### XML config layout

The XML config will need the following layout (an example config is also
included with the download of SilvaBuilda)

* builda
* --local
* ----workingcopy[location]
* ----ignores
* ------ignore[name]
* --remotes
* ----remote[name,url,type]

#### builda

This is the root node and *MUST* be included for this file to be recognised as a
SilvaBuilda config

#### local

This node contains *local* project settings, that will relate to the machine(s)
you are deploying on.

local contains the following children:

*workingcopy*: Specifies the location of the working copy of your project
(set via the *location* attribute). This can be one of the following:

* current (the same directory as the config file)
* parent (the parent directory of the config file)
* grandparent (the parent of the parent of config file)

*ignores*: here you can list any names of files folders you want to be ignored.
At the moment it is not very cleaver and only checks the against file/folder
name, no advanced pattern matching as of yet.

You can add a new ignore by adding an ignore child and then setting the "name"
attribute to the file/folder name you wish to ignore (*NOTE* currently this is
matched recursivly) 

#### remotes

The remotes node is where you add your remote modules. Each module is added as
a child node. These children are:

*remote*: An instance of a remote module and uses the following attributes:

* name (the name of the module. EG sappphire, cms, dataobject_manager)
* url (the location of the download for the module.
  EG https://github.com/silverstripe/sapphire/tarball/2.4.5)
* type (the type of compression used on the archive, can be either: 'zip', 
  'tar', 'tar.gz', 'tar.bz2')