###############################################################
# pytest -v --capture=no tests/test_apptainer.py
# pytest -v  tests/test_apptainer.py
# pytest -v --capture=no  tests/test_apptainer..py::Test_apptainer::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.apptainer.apptainer import Apptainer
from cloudmesh.common.Printer import Printer
import os

from tabulate import tabulate

apptainer = Apptainer()

def print_table(data):
    print(tabulate(data, headers="keys", tablefmt="simple_grid", showindex="always"))

@pytest.mark.incremental
class TestConfig:

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
            apptainer.delete("dot-tfs.sif")
        except:
            pass
        apptainer.download("dot-tfs.sif", "docker://tensorflow/tensorflow:latest")
        Benchmark.Stop()

        assert os.path.exists("dot-tfs.sif")

    def test_download_in_images_dir(self):
        HEADING()
        Benchmark.Start()
        Shell.mkdir("images")
        try:
            apptainer.delete("images/images-tfs.sif")
        except:
            pass
        apptainer.download("images/images-tfs.sif", "docker://tensorflow/tensorflow:latest")
        Benchmark.Stop()

        assert os.path.exists("images/images-tfs.sif")

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
        where = apptainer.find_image("tfs.sif")
        print(where)
        Benchmark.Stop()
        assert len(where) == 2
        assert where[0] == "tfs.sif"
        assert where[1] == "images/tfs.sif"


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


    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="api")

# TESTE DONE TILL HERE

# 1. call stop all instances
# 2. tests taht no instances are running
# 3. start an instance
# 4. test ps
# 5. test list
# 6. test info
# 7. test stats
# 8. test inspect
# 9. test stop
        

class g:
    def test_info(self):
        HEADING()
        Benchmark.Start()
        output_dict = apptainer.info()
        Benchmark.Stop()
        for key, value in output_dict.items():
            print (f"{key}: {value}")
        assert isinstance(output_dict, dict)
        assert "instances" in output_dict


class a:

    def test_ps(self):
        HEADING()
        Benchmark.Start()
        processes = apptainer.ps()
        Benchmark.Stop()
        assert isinstance(processes, list)


    def test_list(self):
        HEADING()
        Benchmark.Start()
        # hello
        output = apptainer.list()
        Benchmark.Stop()
        assert isinstance(output, tuple)
        assert len(output) == 2



    def test_inspect(self):
        HEADING()
        Benchmark.Start()
        result = apptainer.inspect("image_name")
        Benchmark.Stop()
        assert isinstance(result, list)
        assert len(result) > 0


    def test_stats(self):
        HEADING()
        Benchmark.Start()
        stdout, stderr = apptainer.stats(output="json")
        Benchmark.Stop()
        assert isinstance(stdout, str)
        assert isinstance(stderr, str)

    def test_start(self):
        HEADING()
        Benchmark.Start()
        with pytest.raises(ValueError):
            apptainer.start()
        with pytest.raises(ValueError):
            apptainer.start(name="instance_name")
        Benchmark.Stop()



