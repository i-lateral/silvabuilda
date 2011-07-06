## SilvaBuilda: The Silverstripe Build Tool

Silvabuilda is intended to be a simple tool that will alow you to manage your
silverstripe project modules without having to commit them all to your project
repo (which, quite frankly, is annoying).

The tool can be used to download all your project modules as Zip files and
Tarballs, then extract them into a "project root". Then copy your existing
developed code from your working copy into this root as well.

It is still early days, but the intention of this project is to allow you to
do the following:

1. Create a "Build file" (probably xml) that you can drop in your project root
   detailing all external packages that you would like to use for your install

2. Run the build.py file providing your confiog location and project root
   location

3. Let builda download, extract and then cleanup your project directory and sync
   your working copy with it
