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

builda
--local
----workingcopy[location]
--remotes
----remote[name,url,type]

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

### remotes

The remotes node is where you add your remote modules. Each module is added as
a child node. These children are:

*remote*: An instance of a remote module and uses the following attributes:

* name (the name of the module. EG sappphire, cms, dataobject_manager)
* url (the location of the download for the module.
  EG https://github.com/silverstripe/sapphire/tarball/2.4.5)
* type (the type of compression used on the archive, can be either: 'zip', 
  'tar', 'tar.gz', 'tar.bz2')