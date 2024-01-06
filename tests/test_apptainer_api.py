###############################################################
# pytest -v --capture=no tests/test_apptainer_api.py
# pytest -v  tests/test_apptainer_api.py
# pytest -v --capture=no  tests/test_apptainer_api..py::test_apptainer_api::<METHODNAME>
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
import time

from tabulate import tabulate

DOCKERHUB="docker://nvcr.io/nvidia/tensorflow:23.12-tf2-py3"
# DOCKERHUB="docker://nvidia/cuda:12.2.0-devel-ubuntu20.04"

apptainer = Apptainer()

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
            assert False
            print("Please do module load apptainer")

    def test_system(self):
        HEADING()
        Benchmark.Start()
        stdout, stderr = apptainer.system("echo 'Hello, World!'")
        Benchmark.Stop()
        assert stdout.strip() == "Hello, World!"
        assert stderr.strip() == ""
    
    def test_help(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cma help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "apptainer info" in result
        assert "apptainer download NAME URL" in result

    def test_download(self):
        HEADING()
        Benchmark.Start()
        try:
            apptainer.delete("dot-tf.sif")
        except:
            pass
        apptainer.download("dot-tf.sif", DOCKERHUB)
        Benchmark.Stop()

        assert os.path.exists("dot-tf.sif")

    def test_download_in_images_dir(self):
        HEADING()
        Benchmark.Start()
        Shell.mkdir("images")
        try:
            apptainer.delete("images/images-tf.sif")
        except:
            pass
        apptainer.download("images/images-tf.sif", DOCKERHUB)
        Benchmark.Stop()

        assert os.path.exists("images/images-tf.sif")

    def test_images(self):
        HEADING()

        Benchmark.Start()
        # find all images in . amd images/

        #apptainer.load([".", "images"])
        apptainer.load()
        apptainer.save()


        # print the list of found images absed on load
        images = apptainer.images()

        print (images)
        print_table(images)
        Benchmark.Stop()
        assert isinstance(images, list)

    def test_cache(self):
        HEADING()
        Benchmark.Start()
        data = apptainer.cache()
        Benchmark.Stop()    
        print(Printer.attribute(data))

        assert isinstance(data, dict)
        assert len(data) > 0
        assert data["hostname"] == "localhost"


    def test_find_image(self):
        HEADING()
        Benchmark.Start()
        with pytest.raises(ValueError):
            apptainer.find_image("nonexistent_image")
        where = apptainer.find_image("tf.sif")
        print(where)
        Benchmark.Stop()
        assert len(where) == 2
        assert where[0] == "tf.sif" or "images/tf.sif"
        assert where[1] == "images/tf.sif" or "tf.sif"


    def test_add_location(self):
        HEADING()
        Benchmark.Start()
        Shell.mkdir("more-images")
        apptainer.add_location("more-images")
        apptainer.save()
        Benchmark.Stop()
        print (apptainer.location)

        assert "more-images" in apptainer.location
        assert len(apptainer.location) >= 1
        assert apptainer.location[0] == "images"
        assert apptainer.location[1] == "more-images"


    def test_stop_all(self):
        HEADING()
        Benchmark.Start()
        instances = apptainer.list()
        if len(instances) > 0:
            apptainer.stop(name="all")
            Benchmark.Stop()
            instances = apptainer.list()
        assert len(instances) == 0

    def test_list_for_empty(self):
        HEADING()
        Benchmark.Start()
        # hello
        output = apptainer.list()
        Benchmark.Stop()
        print (output)
        assert isinstance(output, list)
        assert len(output) == 0

    def test_start(self):
        HEADING()
        Benchmark.Start()
        with pytest.raises(ValueError):
            apptainer.start()
        apptainer.start(name="tf", image="tf.sif")
        Benchmark.Stop()
        instances = apptainer.list()
        assert len(instances) == 1

    def test_ps(self):
        HEADING()
        Benchmark.Start()
        processes = apptainer.ps()
        print (processes)
        Benchmark.Stop()
        assert isinstance(processes, list)

    def test_list_instance(self):
        HEADING()
        Benchmark.Start()
        # hello
        output = apptainer.list()
        Benchmark.Stop()
        print (output)
        assert isinstance(output, list)
        assert len(output) == 1
        print (Printer.write(output))

    def test_info(self):
        HEADING()
        Benchmark.Start()
        output_dict = apptainer.info()
        Benchmark.Stop()
        for key, value in output_dict.items():
            print (f"{key}: {value}")
        assert isinstance(output_dict, dict)
        assert "instances" in output_dict
    
    def test_stats(self):
        HEADING()
        instance = "tf"
        Benchmark.Start()
        try:
            stdout, stderr = apptainer.stats(name=instance, output="json", verbose=True)
        except Exception as e:
            Console.error(e, traceflag=True)
            stdout = ""
            stderr = ""

        Benchmark.Stop()
        print (stdout)
        print(stderr)
        assert isinstance(stdout, str)
        assert isinstance(stderr, str)

    def test_inspect(self):
        HEADING()
        Benchmark.Start()
        result = apptainer.inspect("tf")
        Benchmark.Stop()
        print (result)
        assert isinstance(result, dict)
        assert len(result) > 0
        assert result['hostname'] == 'localhost'
        print(Printer.attribute(result))

    def test_exec_ls(self):
        HEADING()
        Benchmark.Start()
        stdout, stderr = apptainer.exec(name="tf", command="ls")
        Benchmark.Stop()
        print(stdout)
        print(stderr)
        assert "dot-tf.sif" in stdout

    def test_exec_tf_version(self):
        HEADING()
        Benchmark.Start()
        command = "python -c 'import tensorflow as tf; print(tf.__version__)'"
        stdout, stderr = apptainer.exec(name="tf", command=command, nv=True)
        Benchmark.Stop()
        print(stdout)
        print(stderr)
        assert "2." in stdout

    def test_stop_tf(self):
        HEADING()
        Benchmark.Start()
        instances = apptainer.list()
        if len(instances) > 0:
            apptainer.stop(name="tf")
            Benchmark.Stop()
            time.sleep(1)
            instances = apptainer.list()
        assert len(instances) == 0

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="api")




