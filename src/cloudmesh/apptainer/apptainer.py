import os
import subprocess


class Apptainer:
    def __init__(self):
        self.processes = {}
        pass

    def ps(self):
        """
        Lists the process ids of the containers.

        Returns:
            tuple: A tuple containing the stdout and stderr of the command.
        """
        return self.processes

    def _run(self, name, command, verbose=False, register=None):
        """
        Runs a command.

        Args:
            command (str): Command to run.
            verbose (bool): Print the command before executing.

        Returns:
            tuple: A tuple containing the stdout and stderr of the command.
        """
        if verbose:
            print(command)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if registeris None:
            pass
        elif register:
            self.processes.append({"name": name, "pid": process})
        elif not register:
            del self.processes[name]
        stdout, stderr = process.communicate()
        return stdout, stderr

    def list(self, output=None, logs=False, verbose=False):
        """
        Lists the instances.

        Args:
            output (str): Output format. Supported values: "json".
            logs (bool): Include logs in the output.
            verbose (bool): Print the command before executing.

        Returns:
            tuple: A tuple containing the stdout and stderr of the command.
        """
        command = "apptainer instance list"
        if "json" in output:
            command += " --json"
        else:
            raise ValueError(f"Output format {output} not supported")
        if logs:
            command += " --logs"
        if verbose:
            print(command)
        stdout, stderr = self._run(command)
        return stdout, stderr

    def stats(self, output=None, verbose=False):
        """
        Displays statistics about the instances.

        Args:
            output (str): Output format. Supported values: "json".
            verbose (bool): Print the command before executing.

        Returns:
            tuple: A tuple containing the stdout and stderr of the command.
        """
        command = "apptainer instance stats"
        if "json" in output:
            command += " --json"
        else:
            raise ValueError(f"Output format {output} not supported")
        if verbose:
            print(command)
        stdout, stderr = self._run(command)
        return stdout, stderr

    def start(self, path, name, args=[]):
        """
        Starts a new instance.

        Args:
            path (str): Path to the instance.
            name (str): Name of the instance.
            args (list): Additional arguments for the instance.

        Returns:
            tuple: A tuple containing the stdout and stderr of the command.
        """
        command = f"apptainer instance start {path} {name}"
        if args:
            command += " " + " ".join(args)
        stdout, stderr = self._run(command, register=True)
        return stdout, stderr

    def stop(
        self, all=False, force=False, signal=None, timeout=10, user=None
    ):
        """
        Stops the instances.

        Args:
            all (bool): Stop all instances.
            force (bool): Force stop the instances.
            signal (str): Signal to send to the instances.
            timeout (int): Timeout in seconds for stopping the instances.
            user (str): User to stop the instances.

        Returns:
            tuple: A tuple containing the stdout and stderr of the command.
        """
        command = "apptainer instance stop"
        if all:
            command += " --all"
        if force:
            command += " --force"
        if signal:
            command += f" --signal {signal}"
        if timeout:
            command += f" --timeout {timeout}"
        if user:
            command += f" --user {user}"
        stdout, stderr = self._run(command, register=False)
        return stdout, stderr

   
    def exec(self, name, command, bind=None, nv=False, home=None):
        """
        Execute a command in a container with optional bind paths, Nvidia support, and a specified home directory.

        Args:
            name (str): The container in which to execute the command.
            command (str): The command to execute.
            bind (List[Dict[str, str]]): A list of dictionaries, each containing 'src', 'dest', and 'opts'. 'src' and 'dest' are outside and inside paths. If 'dest' is not given, it is set equal to 'src'. Mount options ('opts') may be specified as 'ro' (read-only) or 'rw' (read/write, which is the default). Multiple bind paths can be given by a comma separated list.
            nv (bool): A boolean to enable or disable Nvidia support.
            home (str): A string specifying the home directory.

        Returns:
            stdout, stderr

        Raises:
            None

        Examples:
            # Execute a command in a container without bind paths, Nvidia support, and a specified home directory
            exec("my_container", "ls")

            # Execute a command in a container with bind paths, Nvidia support, and a specified home directory
            exec("my_container", "ls", bind=[{"src": "/path1", "dest": "/path2", "opts": "ro"}, {"src": "/path3", "dest": "/path4", "opts": "rw"}], nv=True, home="/home/user")
        
        """
        # Construct the command
        cmd = f"apptainer exec instance://{name} {command}"

        # Add bind paths
        if bind:
            for b in bind:
                cmd += f" --bind {b['src']}:{b.get('dest', b['src'])}:{b.get('opts', 'rw')}"

        # Add Nvidia support
        if nv:
            cmd += " --nv"

        # Add home directory
        if home:
            cmd += f" --home {home}"

        stdout, stderr = self._run(cmd)
        return stdout, stderr
    

    def shell(self, name):
        """
        Open a shell in the specified instance.

        Args:
            name (str): Name of the instance.

        Returns:
            tuple: A tuple containing the stdout and stderr of the command.
        """
        command = f"apptainer shell instance://{name}"
        stdout, stderr = self._run(command)
        return stdout, stderr
        