from cloudmesh.apptainer.apptainer import Apptainer
from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.util import banner
from cloudmesh.common.util import path_expand
from cloudmesh.common.variables import Variables
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.shell.command import map_parameters
from cloudmesh.common.Printer import Printer
from tabulate import tabulate
from cloudmesh.common.util import readfile


class ApptainerCommand(PluginCommand):
    # noinspection PyUnusedLocal
    @command
    def do_apptainer(self, args, arguments):
        """
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



        """


        #variables = Variables()
        #variables["apptainer_dir"] = True

        map_parameters(arguments, "output")

        
        # arguments = Parameter.parse(
        #     arguments, parameter="expand", experiment="dict", COMMAND="str"
        # )

        # VERBOSE(arguments)

        app = Apptainer()
        r = app.images(directory="images")
        
        if arguments["--dir"]:
            print("option dir")

        elif arguments.info:
            out = app.info()
            app.save()
            r = readfile("apptainer.yaml")
            print (r)

        elif arguments.list:
            out = app.list()
            app.save()
            r = readfile("apptainer.yaml")
            prefix = app.prefix
            data = app.db[f"{prefix}.instances"]
            # if arguments.output == "table":
            #     print(tabulate(data, headers="keys", tablefmt="simple_grid", showindex="always"))
            # else:
            print(Printer.write(data, order=None, output=arguments.output))


        elif arguments.cache:

            data = app.cache()
            print(tabulate(data, headers="keys", tablefmt="simple_grid", showindex="always"))

        elif arguments["--add"]:
            print("option add")
            app.add_location(arguments["--add"])

        elif arguments.inspect:
            r = app.inspect(arguments.NAME)
            print(tabulate(r, headers="keys", tablefmt="simple_grid", showindex="always"))

        elif arguments.start:
            r = app.start(name=arguments.NAME, image=arguments.IMAGE, home=arguments.home, gpu=arguments.gpu, options=arguments.OPTIONS)

        elif arguments.stop:
            r = app.stop(arguments.NAME)

        elif arguments.shell:
            r = app.shell(arguments.NAME)

        elif arguments.exec:
            r = app.exec(arguments.NAME)

        elif arguments.images:
            directory = arguments.DIRECTORY
            r = app.images(directory=directory)
            print(tabulate(r, headers="keys", tablefmt="simple_grid", showindex="always"))

        return ""
