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


class ApptainerCommand(PluginCommand):
    # noinspection PyUnusedLocal
    @command
    def do_apptainer(self, args, arguments):
        """
        ::

          Usage:
                apptainer --file=FILE
                apptainer list
                apptainer [--parameter=PARAMETER] [--experiment=EXPERIMENT] [COMMAND...]

          This command does some useful things.

          Arguments:
              FILE   a file name
              PARAMETER  a parameterized parameter of the form "a[0-3],a5"

          Options:
              -f      specify the file

          Description:

            > cms apptainer --parameter="a[1-2,5],a10"
            >    example on how to use Parameter.expand. See source code at
            >      https://github.com/cloudmesh/cloudmesh-apptainer/blob/main/cloudmesh/apptainer/command/apptainer.py
            >    prints the expanded parameter as a list
            >    ['a1', 'a2', 'a3', 'a4', 'a5', 'a10']

            > apptainer exp --experiment=a=b,c=d
            > example on how to use Parameter.arguments_to_dict. See source code at
            >      https://github.com/cloudmesh/cloudmesh-apptainer/blob/main/cloudmesh/apptainer/command/apptainer.py
            > prints the parameter as dict
            >   {'a': 'b', 'c': 'd'}

        """

        # arguments.FILE = arguments['--file'] or None

        # switch debug on

        variables = Variables()
        variables["debug"] = True

        banner("original arguments", color="RED")

        VERBOSE(arguments)

        banner(
            "rewriting arguments so we can use . notation for file, parameter, and experiment",
            color="RED",
        )

        map_parameters(arguments, "file", "parameter", "experiment")

        VERBOSE(arguments)

        banner(
            "rewriting arguments so we convert to appropriate types for easier handling",
            color="RED",
        )

        arguments = Parameter.parse(
            arguments, parameter="expand", experiment="dict", COMMAND="str"
        )

        VERBOSE(arguments)

        banner("showcasing tom simple if parsing based on teh dotdict", color="RED")

        m = Apptainer()

        #
        # It is important to keep the programming here to a minimum and any substantial programming ought
        # to be conducted in a separate class outside the command parameter manipulation. If between the
        # elif statement you have more than 10 lines, you may consider putting it in a class that you import
        # here and have proper methods in that class to handle the functionality. See the Manager class for
        # an example.
        #

        if arguments.file:
            print("option a")
            m.list(path_expand(arguments.file))

        elif arguments.list:
            print("option b")
            m.list("just calling list without parameter")

        Console.error("This is just a sample of an error")
        Console.warning("This is just a sample of a warning")
        Console.info("This is just a sample of an info")

        Console.info(
            " You can witch debugging on and off with 'cms debug on' or 'cms debug off'"
        )

        return ""
