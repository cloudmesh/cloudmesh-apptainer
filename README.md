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



The cloudmesh command apptainer command lets you more easily manage apptainers for application-oriented work. The main contributions are:

1. It includes a Python API so containers can be managed directly from Python instead of a command line tool
2. It includes a focussed command line tool with a selected number of features to more easily start, stop, list, and execute commands in a container. 
3. It includes a number of enhanced features to showcase the locations and sizes of the images and instances.
4. A simple YAML database is automatically created when using the API or the command-line tool so that a record is preserved for long-running containers. The record includes also a hostname, making it possible to use this database to manage containers on remote hosts.

TODO: the remote host feature to start and stop containers is not yet fully implemented.

To install it uyou can use 

    pip install cloudmesh-apptainer

To develop you will need the source code 

    git clone https://github.com/cloudmesh/cloudmesh-apptainer.git
    git clone https://github.com/cloudmesh/cloudmesh-common.git

Next, you can generate Python editable sources with

    make pip

and local wheels with

    make local

To update the makefile you can say 

    make readme
    
For more information see the Makefile

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
                --gpu=GPU        sets the GPU to be used
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

            cms apptainer info
                prints information contained in the apptainer.yaml file. An example is given next

                cloudmesh:
                    apptainer:
                        udc-aj34-33:
                        hostname: udc-aj34-33
                        location:
                        - ~/.cloudmesh/apptainer
                        - ../rivanna/images
                        apptainers:
                        - name: cloudmesh-tfs.sif
                            size: 1.5 GB
                            path: ../rivanna/images
                            location: ../rivanna/images/cloudmesh-tfs.sif
                            hostname: udc-aj34-33
                        - name: cloudmesh-tensorflow.sif
                            size: 7.4 GB
                            path: ../rivanna/images
                            location: ../rivanna/images/cloudmesh-tensorflow.sif
                            hostname: udc-aj34-33
                        - name: haproxy_latest.sif
                            size: 45.6 MB
                            path: ../rivanna/images
                            location: ../rivanna/images/haproxy_latest.sif
                            hostname: udc-aj34-33
                        instances:
                        - instance: tfs
                            pid: 337625
                            img: /scratch/$USER/cm/5/rivanna/images/cloudmesh-tfs.sif
                            ip: ''
                            logErrPath: /home/$USER/.apptainer/instances/logs/udc-aj34-33/$USER/tfs.err
                            logOutPath: /home/$USER/.apptainer/instances/logs/udc-aj34-33/$USER/tfs.out
```
<!-- STOP-MANUAL -->