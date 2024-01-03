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


class ApptainerCommand(PluginCommand):
    # noinspection PyUnusedLocal
    @command
    def do_apptainer(self, args, arguments):
        """
        ::

          Usage:
                apptainer inspect NAME
                apptainer list
                apptainer --dir=DIRECTORY
                apptainer --add=SIF
                apptainer cache
                apptainer images
                apptainer start NAME
                apptainer stop NAME
                apptainer shell NAME
                apptainer exec NAME COMMAND
                        
                  This command can be used to manage apptainers.

                  Arguments:
                      FILE   a file name
                      PARAMETER  a parameterized parameter of the form "a[0-3],a5"

                  Options:
                        --dir=DIRECTORY  sets the the directory of the a list of aptainers
                        --add=SIF        adds a sif file to the list of apptainers

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

        """


        variables = Variables()
        variables["apptainer_dir"] = True

        map_parameters(arguments, "dir", "add")

        
        # arguments = Parameter.parse(
        #     arguments, parameter="expand", experiment="dict", COMMAND="str"
        # )

        # VERBOSE(arguments)

        app = Apptainer()

        if arguments.dir:
            print("option dir")

        elif arguments.list:
            print("option list")
            out,err = app.list()
            print (out)
            print(err)

        elif arguments.cache:

            data = app.cache()
            print(tabulate(data, headers="keys", tablefmt="simple_grid", showindex="always"))

        elif arguments.add:
            print("option add")
            app.add_location(arguments.add)

        elif arguments.inspect:
            r = app.inspect(arguments.NAME)
            print(tabulate(r, headers="keys", tablefmt="simple_grid", showindex="always"))

        elif arguments.images:
            r = app.images()
            print(tabulate(r, headers="keys", tablefmt="simple_grid", showindex="always"))

        return ""
