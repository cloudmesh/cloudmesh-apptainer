import os

from cloudmesh.apptainer.apptainer import Apptainer
from cloudmesh.common.Printer import Printer
from cloudmesh.common.util import readfile
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.shell.command import map_parameters
from tabulate import tabulate


class ApptainerCommand(PluginCommand):
    # noinspection PyUnusedLocal
    @command
    def do_apptainer(self, args, arguments):
        """
        ::

            Usage:
                apptainer download NAME URL
                apptainer inspect NAME
                apptainer list [--detail] [--output=OUTPUT]
                apptainer info
                apptainer --dir=DIRECTORY
                apptainer --add=SIF
                apptainer cache [--output=OUTPUT]
                apptainer images [DIRECTORY] [--output=OUTPUT]
                apptainer start NAME IMAGE [--home=PWD] [--gpu=GPU] [OPTIONS] [--dryrun]
                apptainer stop NAME
                apptainer shell NAME
                apptainer exec NAME COMMAND
                apptainer stats NAME [--output=OUTPUT]

                This command can be used to manage apptainers.

                Arguments:
                    FILE   a file name
                    PARAMETER  a parameterized parameter of the form "a[0-3],a5"
                    OPTIONS   Options passed to the start command
                    IMAGE     The name of the image to be used
                    NAME      The name of the apptainer
                    URL       The URL of the file to be downloaded

                Options:
                    --dir=DIRECTORY    sets the the directory of the a list of aptainers
                    --add=SIF          adds a sif file to the list of apptainers
                    --image=IMAGE      sets the image to be used
                    --home=PWD         sets the home directory of the apptainer
                    --gpu=GPU          sets the GPU to be used
                    --command=COMMAND  sets the command to be executed
                    --output=OUTPUT    the format of the output [default: table]
                    --detail           shows more details [default: False]
                    -c COMMAND         sets the command to be executed

            Description:

                cms apptainer list
                    lists the apptainers in the specified directory
                    by default the directory is

                cms apptainer --dir=DIRECTORY
                    sets the default apptainer directory in the cms variable
                    apptainer_dir

                cms apptainer --add=SIF
                    adds a sif file to the list of apptainers

                cms apptainer cache
                    lists the cached apptainers

                cms apptainer info
                    prints information contained in the apptainer.yaml file.
                    An example is given next

                    cloudmesh:
                        apptainer:
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

        # variables = Variables()
        # variables["apptainer_dir"] = True

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
            print(r)

        elif arguments.list:
            detail = arguments["--detail"]

            out = app.list()
            app.save()
            r = readfile("apptainer.yaml")
            prefix = app.prefix
            data = app.db[f"{prefix}.instances"]
            # if arguments.output == "table":
            #     print(tabulate(data, headers="keys", tablefmt="simple_grid", showindex="always"))
            # else:
            if detail:
                print(Printer.write(data, order=None, output=arguments.output))
            else:
                for entry in data:
                    entry.pop("logErrPath")
                    entry.pop("logOutPath")
                # print(Printer.write(data, order=None, output=arguments.output))
                print(
                    tabulate(
                        data, headers="keys", tablefmt="simple_grid", showindex="always"
                    )
                )

        elif arguments.cache:
            data = app.cache()
            print(Printer.attribute(data, output=arguments.output))

        elif arguments["--add"]:
            print("option add")
            app.add_location(arguments["--add"])

        elif arguments.inspect:
            data = app.inspect(arguments.NAME)
            print(Printer.attribute(data))

        elif arguments.stats:
            r = app.stats(name=arguments.NAME, output="json")

            print(Printer.attribute(r, output=arguments.output))

        elif arguments.start:
            r = app.start(
                name=arguments.NAME,
                image=arguments.IMAGE,
                home=arguments.home,
                gpu=arguments.gpu,
                options=arguments.OPTIONS,
            )

        elif arguments.stop:
            r = app.stop(arguments.NAME)

        elif arguments.shell:
            r = app.shell(arguments.NAME)

        elif arguments.exec:
            command = arguments.COMMAND

            if os.path.isfile(command):
                script = command
                command = f"sh {script}"

            name = arguments.NAME

            stdout, stderr = app.exec(name=name, command=command)
            print(stdout)
            print(stderr)

        elif arguments.images:
            directory = arguments.DIRECTORY
            data = app.images(directory=directory)
            print(Printer.write(data, output=arguments.output))

        elif arguments.download:
            name = arguments.NAME
            if not name.endswith(".sif"):
                name += ".sif"
            print(f"NAME>{name}<")

            app.download(name=name, url=arguments.URL)

        elif arguments.load:
            r = app.load()

        elif arguments.save:
            r = app.save()

        return ""
