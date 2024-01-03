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
import os
import subprocess
import re

class ApptainerCommand(PluginCommand):
    # noinspection PyUnusedLocal
    @command
    def do_apptainer(self, args, arguments):
        """
        ::

          Usage:
                apptainer list
                apptainer --dir=DIRECTORY
                apptainer --add=SIF
                        apptainer cache
                        apptainer images
                        
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
            print("option cache")
            output = subprocess.check_output("apptainer cache list", shell=True, universal_newlines=True)

            #output = "There are 1 container file(s) using 43.48 MiB and 66 oci blob file(s) using 7.01 GiB of space\nTotal space used: 7.05 GiB"

            container_files = re.search(r"There are (\d+) container file", output).group(1)
            container_space = re.search(r"using ([\d.]+) MiB", output).group(1)
            oci_blob_files = re.search(r"(\d+) oci blob file", output).group(1)
            oci_blob_space = re.search(r"using ([\d.]+) GiB", output).group(1)
            total_space = re.search(r"Total space used: ([\d.]+) GiB", output).group(1)

            print("Container Files:", container_files)
            print("Container Space:", container_space, "MiB")
            print("OCI Blob Files:", oci_blob_files)
            print("OCI Blob Space:", oci_blob_space, "GiB")
            print("Total Space Used:", total_space, "GiB")

            if 'SINGULARITY_CACHEDIR' in os.environ:
                s_cache = os.environ['SINGULARITY_CACHEDIR']
            else:
                s_cache = None
            if 'APPTAINER_CACHEDIR' in os.environ:
                a_cache = os.environ['APPTAINER_CACHEDIR']
            else:
                a_cache = None

            data = [
                {"attribute": "Container Files", "value": container_files},
                {"attribute": "Container Space", "value": container_space + " MiB"},
                {"attribute": "OCI Blob Files", "value": oci_blob_files},
                {"attribute": "OCI Blob Space", "value": oci_blob_space + " GiB"},
                {"attribute": "Total Space Used", "value": total_space + " GiB"},
                {"attribute": "SINGULARITY_CACHEDIR", "value": s_cache},
                {"attribute": "APPTAINER_CACHEDIR", "value": a_cache}
            ]
            print(tabulate(data, headers="keys", tablefmt="simple_grid", showindex="always"))


        elif arguments.add:
            print("option add")
            app.add_location(arguments.add)

        elif arguments.images:
            r = app.images()
            print(tabulate(r, headers="keys", tablefmt="simple_grid", showindex="always"))

        return ""
