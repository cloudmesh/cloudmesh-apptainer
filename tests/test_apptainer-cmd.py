###############################################################
# pytest -v --capture=no tests/test_apptainer_api.py
# pytest -v  tests/test_apptainer_api.py
# pytest -v --capture=no  tests/test_apptainer_cmd.py::TestConfig::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.apptainer.apptainer import Apptainer
from cloudmesh.common.Printer import Printer
from cloudmesh.common.console  import Console
import os
import yaml
import json
import time

from tabulate import tabulate
from pprint import pprint

DOCKERHUB="docker://nvcr.io/nvidia/tensorflow:23.12-tf2-py3"
# DOCKERHUB="docker://nvidia/cuda:12.2.0-devel-ubuntu20.04"


def print_table(data):
    print(tabulate(data, headers="keys", tablefmt="simple_grid", showindex="always"))

@pytest.mark.incremental
class TestConfig:

    def test_apptainer_cmd(self):
        HEADING()
        Benchmark.Start()
        r = Shell.run("apptainer help")
        Benchmark.Stop()

        if "not found" in r:
            print("Please do module load apptainer")
            assert False

    def test_system(self):
        HEADING()
        Benchmark.Start()
        result = Shell.run("echo 'Hello, World!'")
        Benchmark.Stop()
        assert result.strip() == "Hello, World!"
    
    def test_help(self):
        HEADING()
        Benchmark.Start()
        result = Shell.run("cma help")
        Benchmark.Stop()
        VERBOSE(result)

        assert "apptainer info" in result
        assert "apptainer download NAME URL" in result

    def test_download(self):
        HEADING()
        Benchmark.Start()
        sif = "dot-tf.sif"
        result = Shell.run(f"cma delete {sif}")
        result = Shell.run(f"cma download {sif} {DOCKERHUB}")
        Benchmark.Stop()

        assert os.path.exists(sif)

    def test_download_in_images_dir(self):
        HEADING()
        Benchmark.Start()

        Shell.mkdir("images")
        
        sif = "images/dot-tf.sif"
        result = Shell.run(f"cma delete {sif}")
        result = Shell.run(f"cma download {sif} {DOCKERHUB}")
        Benchmark.Stop()

        assert os.path.exists(sif)

    def test_list_images(self):
        HEADING()

        Benchmark.Start()
        # find all images in . amd images/

        #apptainer.load([".", "images"])
        result = Shell.run("cma images")
        print (result)
        result = Shell.run("cma images --output=json")
        result = json.loads(result)
        print (result)
        Benchmark.Stop()
        assert isinstance(result, dict)
        assert len(result.keys()) == 2 

    
    def test_cache(self):
        HEADING()
        Benchmark.Start()
        data = Shell.run("cma cache")
        print(data)
        data = Shell.run("cma cache --output=json")
        print ("JSON:", data)

        data = json.loads(data)["json"]
        
        Benchmark.Stop()    

        print(Printer.attribute(data))

        assert isinstance(data, dict)
        assert len(data) > 0
        assert data["hostname"] == "localhost"

    def test_add_location(self):
        HEADING()
        Benchmark.Start()
        Shell.mkdir("more-images")

        Shell.run('cma --add=more-images')
        # apptainer.add_location("more-images")
        Shell.run('cma save')
        # apptainer.save()
        
        Benchmark.Stop()
        yaml_printed = yaml.safe_load(Shell.run("cma info"))
        pprint(yaml_printed)

        location = yaml_printed['cloudmesh']['apptainer']['location']
        assert "more-images" in location
        assert len(location) >= 1
        assert location[0] == "images"
        assert location[1] == "more-images"

    
    def test_stop_all(self):
        HEADING()
        Benchmark.Start()

        instances = Shell.run("cma list")
        # instances = apptainer.list()
        if len(instances) > 0:
            result = Shell.run("cma stop all")
            print(result)
            # apptainer.stop(name="all")
            Benchmark.Stop()
            instances = Shell.run("cma list").strip()
        
            for i in range(0, 10):
                if "tf" not in instances:
                    break
                time.sleep(1)
                instances = Shell.run("cma list").strip()
        
        assert 'tf' not in instances

    def test_list_for_empty(self):
        HEADING()
        Benchmark.Start()
        
        output = Shell.run("cma list").strip()
        # output = apptainer.list()
        Benchmark.Stop()
        print (output)
        assert isinstance(output, str)
        assert len(output) == 0


    def test_start(self):
        HEADING()
        Benchmark.Start()
        Shell.run("cma start tf tf.sif")       
        Benchmark.Stop()

        instances = Shell.run("cma list")
        assert len(instances) > 0


    def test_list_instance(self):
        HEADING()
        Benchmark.Start()
        
        # output = apptainer.list()
        output = Shell.run("cma list")

        Benchmark.Stop()
        print (output)
        assert isinstance(output, str)
        assert len(output) > 0
        # print (Printer.write(output))

    def test_info(self):
        HEADING()
        Benchmark.Start()

        output_dict = yaml.safe_load(Shell.run("cma info"))
        # output_dict = apptainer.info()
        Benchmark.Stop()
        # for key, value in output_dict.items():
            # print (f"{key}: {value}")
        pprint(output_dict)
        assert isinstance(output_dict, dict)
        assert "instances" in output_dict['cloudmesh']['apptainer']

    def test_stats(self):
        HEADING()
        instance = "tf"
        Benchmark.Start()
        try:
            stdout = Shell.run(f"cma stats {instance} --output=json")
            stderr = ""
            # stdout, stderr = apptainer.stats(name=instance, output="json", verbose=True)
        except Exception as e:
            Console.error(e, traceflag=True)
            stdout = ""
            stderr = ""
            assert False

        Benchmark.Stop()
        print (stdout)
        print(stderr)
        assert isinstance(stdout, str)
        assert isinstance(stderr, str)

    def test_inspect(self):
        HEADING()
        Benchmark.Start()

        result = Shell.run("cma inspect tf")
        
        Benchmark.Stop()
        print (result)
        assert True

    def test_exec_ls(self):
        HEADING()
        Benchmark.Start()

        stdout = Shell.run("cma exec tf ls")
        # stdout, stderr = apptainer.exec(name="tf", command="ls")

        Benchmark.Stop()
        print(stdout)
        # print(stderr)
        assert "dot-tf.sif" in stdout

    def test_exec_python(self):
        HEADING()
        Benchmark.Start()

        command = r"python -c 'import tensorflow as tf\; print(tf.__version__)'"
        stdout = Shell.run("cma exec tf \"{command}\"")
        # stdout, stderr = apptainer.exec(name="tf", command=command, nv=True)
        Benchmark.Stop()
        print(stdout)
        # print(stderr)
        assert "2." in stdout

    def test_stop_tf(self):
        HEADING()
        Benchmark.Start()

        # instances = apptainer.list()
        instances = Shell.run("cma list")
        if len(instances) > 0:
            Shell.run("cma stop tf")
            Benchmark.Stop()
            instances = Shell.run("cma list")
        assert len(instances) == 0

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="api")



