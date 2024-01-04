import os
import subprocess
import sys
from cloudmesh.common. variables import Variables
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import banner
import re
from cloudmesh.common.debug import VERBOSE
import humanize
import json
import json
from yamldb import YamlDB
from cloudmesh.common.console import Console


class Apptainer:
    def __init__(self):
        self.processes = []
        self.location = []
        self.apptainers = []
        self.variables = Variables()
        try:
            self.hostname = os.environ.get("HOSTNAME") or os.uname()[1] 
        except:
            self.hostname = "localhost"
        self.prefix = f"cloudmesh.apptainer.{self.hostname}"

        self.db = YamlDB(filename="apptainer.yaml")

        self.load_location_from_db()

        self.save()

    def get_db(self, key):
        return self.db[f"{self.prefix}.{key}"]

    def save(self):
        try:
            prefix = self.prefix
            self.db[f"{prefix}.hostname"] = self.hostname
            self.db[f"{prefix}.location"] = self.location
            self.db[f"{prefix}.apptainers"] = self.apptainers 
            self.db.save()  
        except:
            Console.error("apptainer.yaml could not be written")

    def load(self):
        if os.path.isfile("apptainer.yaml"):
            prefix = self.prefix
            self.hostname = self.db[f"{prefix}.hostname"]
            self.location = self.db[f"{prefix}.location"]
            self.apptainers = self.db[f"{prefix}.apptainers"]
        else:
            Console.warning("apptainer.yaml does not exist")

    


    def load_location_from_db(self):
            """
            Load the location of apptainers from the cloudmesh variable `apptainers` which is a coma separated string of dirs and sif files.
            """
            self.load()
   
            self.apptainers = []
            for entry in self.location:
                entry = path_expand(entry)
                if os.path.isdir(entry):
                    for name in os.listdir(entry):
                        if name.endswith(".sif"):
                            location = entry + "/" + name  # Fix: Removed unnecessary curly braces
                            try:
                                size = humanize.naturalsize(os.path.getsize(location))
                            except:
                                size = "unknown"
                            if os.path.isfile(location):
                                self.apptainers.append({"name": name, 
                                                        "size": size, 
                                                        "path": entry, 
                                                        "location": location,
                                                        "hostname": self.hostname}
                                                        )  # Fix: Removed unnecessary double quotes
                elif entry.endswith(".sif"):
                    if os.path.isfile(entry):
                        self.apptainers.append({"name": os.path.basename(entry), "size": size, "path": os.path.dirname(entry), "location": entry})
                        try:
                            size = humanize.naturalsize(os.path.getsize(entry))
                        except:
                            size = "unknown"
                        
    def add_location(self, path):
        """
        Adds a location to the Apptainer object.

        Parameters:
        path (str): The path of the location to be added.

        Returns:
        None
        """
        self.load_location_from_db()

    def images(self, directory=None):
            """
            Retrieves a list of images from the apptainer.yaml file.
            
            Args:
                directory (str): The directory to search for images. If not specified, all images will be retrieved.
            
            Returns:
                list: A list of images found in the specified directory.
            """
            all = self.load_location_from_db()
            return self.apptainers


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
        if register is None or register is False:
            pass
        elif register:
            self.processes.append({"name": name, "pid": process})
        elif not register:
            del self.processes[name]
        stdout, stderr = process.communicate()
        return stdout, stderr

    def list(self, output=None, verbose=False):
        """
        Lists the instances.

        Args:
            output (str): Output format. Supported values: "json".
            verbose (bool): Print the command before executing.

        Returns:
            tuple: A tuple containing the stdout and stderr of the command.
        """
        r = self.info()
        return r
    

    def info(self, logs=False, verbose=False):
        """
        Lists the instances.

        Args:
            output (str): Output format. Supported values: "json".
            logs (bool): Include logs in the output.
            verbose (bool): Print the command before executing.

        Returns:
            dict: A dictionary containing the stdout as a dictionary.
        """
        command = "apptainer instance list --json"
        if logs:
            command += " --logs"
        if verbose:
            banner(command)
        stdout, stderr = self._run("list", command, register=False)
        
        output_dict = json.loads(stdout)
        self.db[f"{self.prefix}.instances"] = output_dict["instances"]
        
        return output_dict
    

    def find_image(self, name, smart=True):
        """
        Finds the image of an instance.

        Args:
            name (str): Name of the instance.

        Returns:
            str: The image of the instance.
        """
        for image in self.apptainers:
            if image["name"] == name:
                return image["name"], image["location"]
        for image in self.apptainers:
            if name in image["name"]:
                return image["name"], image["location"]
        raise ValueError(f"Image {name} not found") 
        
    
    # ...

    def inspect(self, name):
        """
        Inspects the instance.

        Args:
            name (str): Name of the instance.

        Returns:
            dict: A dictionary containing the JSON data from stdout.
            str: The stderr of the command.
        """
        _name,location = self.find_image(name)
        command = f"apptainer inspect --json {location}"
        stdout, stderr = self._run("inspect", command, register=False)

        data = json.loads(stdout)

        labels = data['data']['attributes']['labels']
        result = []
        result.append({'attribute': 'name','value':  _name})
        result.append({'attribute': 'location','value':  location})
        result.append({"attribute": "hostname", "value": self.hostname})
        result += [{'attribute': key, 'value': value} for key, value in labels.items()]        
        result.append(        {'attribute': 'type','value':  data['type']})
        size = humanize.naturalsize(os.path.getsize(location))
        result.append({'attribute': 'size','value':  size})
        
        return result
    


    def cache(self):
        output = subprocess.check_output("apptainer cache list", shell=True, universal_newlines=True)

        #output = "There are 1 container file(s) using 43.48 MiB and 66 oci blob file(s) using 7.01 GiB of space\nTotal space used: 7.05 GiB"

        container_files = re.search(r"There are (\d+) container file", output).group(1)
        container_space = re.search(r"using ([\d.]+) MiB", output).group(1)
        oci_blob_files = re.search(r"(\d+) oci blob file", output).group(1)
        oci_blob_space = re.search(r"using ([\d.]+) GiB", output).group(1)
        total_space = re.search(r"Total space used: ([\d.]+) GiB", output).group(1)

        if 'SINGULARITY_CACHEDIR' in os.environ:
            s_cache = os.environ['SINGULARITY_CACHEDIR']
        else:
            s_cache = None
        if 'APPTAINER_CACHEDIR' in os.environ:
            a_cache = os.environ['APPTAINER_CACHEDIR']
        else:
            a_cache = None

        data = [
            {"attribute": "hostname", "value": self.hostname},
            {"attribute": "Container Files", "value": container_files},
            {"attribute": "Container Space", "value": container_space + " MiB"},
            {"attribute": "OCI Blob Files", "value": oci_blob_files},
            {"attribute": "OCI Blob Space", "value": oci_blob_space + " GiB"},
            {"attribute": "Total Space Used", "value": total_space + " GiB"},
            {"attribute": "SINGULARITY_CACHEDIR", "value": s_cache},
            {"attribute": "APPTAINER_CACHEDIR", "value": a_cache}
        ]
        return data


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

    def start(self, name=None, image=None, gpu=None, home=None, clean=True, options=None, dryrun=False):
        if name is None:
            raise ValueError("Name of the instance must be specified")
        if image is None:
            raise ValueError("Image of the instance must be specified")
        
        # check if name is not alrady in use

        if clean:
            try:
                out,err = self.stop(name=name)
            except:
                out = ""

            assert "no instance found" not in out

            out = self.info()
            assert name not in out

        if home:
            if home == "pwd":
                home = os.getcwd()
            home = f"--home {home}"
        else:
            home = ""

        if gpu is None:
            gpu_visible_devices = ""
        else:
            gpu_visible_devices = f"CUDA_VISIBLE_DEVICES={gpu} "


        _name,path = self.find_image(image)

        banner(f"Start {name} {path} {home}")

        command = gpu_visible_devices + f"apptainer instance start --nv {home} {path} {name}"
        if options:
            command += " " + " ".join(options)
        if dryrun:
            print("DRYRUN:", command)
        else:
            banner(command)
            stdout, stderr = self._run(name, command, register=True)
        return stdout, stderr
    

    # def start(self, gpu=None, clean=False, wait=True):
    #     """
    #     Starts the TFS instance.
    #     1. fisrt ist looks for containers with the same name and stops them
    #     2. it checks if no container with the name is used.
    #     3. ist starts the container 

    #     """

    #     self.system(f"{gpu_visible_devices} apptainer instance start --nv --home {pwd} {self.IMAGE} {self.INSTANCE} ")

    #     self.instance_exec(f"tensorflow_model_server --port={self.PORT} --rest_api_port=0 --model_config_file=benchmark/models.conf >& log-{self.INSTANCE}.log &")
    #     r = self.system("apptainer instance list")

    #     self.wait_for_port(port=self.PORT)

    #     print ("Server is up")


    def stop(
        self, name=None, force=False, signal=None, timeout=10, user=None
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
        if force:
            command += " --force"
        if signal:
            command += f" --signal {signal}"
        if timeout:
            command += f" --timeout {timeout}"
        if user:
            command += f" --user {user}"
        if name == "all":
            command += " --all"
        else :
            command += f" {name}"
        stdout, stderr = self._run("stop", command, register=False)
        return stdout, stderr

   
    def exec(self, name, command, bind=None, nv=False, home=None):
        """
        Execute a command in a container with optional bind paths, Nvidia support, and a specified home directory.

        Args:
            name (str): The container in which to execute the command.
            command (str): The command to execute.
            bind (List[Dict[str, str]]): A list of dictionaries, each containing 'src', 'dest', and 'opts'. 'src' and 
                                        'dest' are outside and inside paths. If 'dest' is not given, it is set equal to 'src'. 
                                        Mount options ('opts') may be specified as 'ro' (read-only) or 'rw' (read/write, which is the default). 
                                        Multiple bind paths can be given by a comma separated list.
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
            exec("my_container", "ls", bind=[{"src": "/path1", "dest": "/path2", "opts": "ro"}, 
            {"src": "/path3", "dest": "/path4", "opts": "rw"}], nv=True, home="/home/user")
        
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

def main():
    arguments = ' '.join(sys.argv[1:])
    os.system(f"cms apptainer {arguments}")
    
if __name__ == "__main__":
    main()
