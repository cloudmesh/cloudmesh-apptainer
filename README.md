# Cloudmesh Command apptainer

[![GitHub Repo](https://img.shields.io/badge/github-repo-green.svg)](https://github.com/cloudmesh/cloudmesh-apptainer)
[![image](https://img.shields.io/pypi/pyversions/cloudmesh-apptainer.svg)](https://pypi.org/project/cloudmesh-apptainer)
[![image](https://img.shields.io/pypi/v/cloudmesh-apptainer.svg)](https://pypi.org/project/cloudmesh-apptainer/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![General badge](https://img.shields.io/badge/Status-Production-<COLOR>.svg)](https://shields.io/)
[![GitHub issues](https://img.shields.io/github/issues/cloudmesh/cloudmesh-apptainer.svg)](https://github.com/cloudmesh/cloudmesh-apptainer/issues)
[![Contributors](https://img.shields.io/github/contributors/cloudmesh/cloudmesh-apptainer.svg)](https://github.com/cloudmesh/cloudmesh-apptainer/graphs/contributors)
[![General badge](https://img.shields.io/badge/Other-repos-<COLOR>.svg)](https://github.com/cloudmesh/cloudmesh)


[![Linux](https://img.shields.io/badge/OS-Linux-orange.svg)](https://www.linux.org/)
[![macOS](https://img.shields.io/badge/OS-macOS-lightgrey.svg)](https://www.apple.com/macos)
[![Windows](https://img.shields.io/badge/OS-Windows-blue.svg)](https://www.microsoft.com/windows)


The cloudmesh command apptainer command lest you more easily manage apptainers for applicatio oriented work. The main contribution are:

1. It includes a Python API so containers can be managed directly from python instead of a commandline tool
2. It includesa focussed commandline tool with a selected number of features to more easily start, stop, list and execute commands in a container. 
3. It includes a number of enhanced features to show case locations and sises of the images and instances.
4. A simple yaml database is automatically created when using the API or the commandline tool so that a record is preserved for long running containers. THe record includes also a hostname, making it possible to use this dattabase to manage containers on remote hosts.

TODO: the remote host feature to start stop containers is not yet fully implemented.

To sinstall it uyou can use 

    pip install cloudmesh-apptainer

To develop you will need the source code 

    git clone https://github.com/cloudmesh/cloudmesh-apptainer.git
    git clone https://github.com/cloudmesh/cloudmesh-common.git

Next you can generate python editable sources with

    make pip

and local wheels with

    make local

To update the makefile you can say 

    make readme
    
For more information see the makefile

## Manual Page

<!-- START-MANUAL -->
```
Command apptainer
=================

::

  Usage:
        apptainer inspect NAME
        apptainer list [--output=OUTPUT]
        apptainer info
        apptainer --dir=DIRECTORY
        apptainer --add=SIF
        apptainer cache
        apptainer images [DIRECTORY]
        apptainer start NAME IMAGE [--home=PWD] [--gpu=GPU] [OPTIONS] [--dryrun]
        apptainer stop NAME 
        apptainer shell NAME
        apptainer exec NAME COMMAND

          This command can be used to manage apptainers.

          Arguments:
              FILE   a file name
              PARAMETER  a parameterized parameter of the form "a[0-3],a5"
              OPTIONS   Options passed to the start command
              IMAGE     The name of the image to be used

          Options:
                --dir=DIRECTORY  sets the the directory of the a list of aptainers
                --add=SIF        adds a sif file to the list of apptainers
                --image=IMAGE    sets the image to be used
                --home=PWD       sets the home directory of the apptainer
                --gpu=GPU        sets the gpu to be used
                --output=OUTPUT  the format of the output [default: table]

          Description:


            cms apptainer list
                lists the apptainers in the specified directory 
                by default the directory is 

            cms apptainer --dir=DIRECTORY
                sets the default apptainer directory in the cms variable apptainer_dir

            cms apptainer --add=SIF
                adds a sif file to the list of apptainers

            cms apptainer cache
                lists the cached apptainers
```
<!-- STOP-MANUAL -->