import pytest
from cloudmesh.apptainer.apptainer import Apptainer

@pytest.fixture
def apptainer():
    return Apptainer()

def test_add_location(apptainer):
    apptainer.add_location("/path/to/location")
    assert len(apptainer.location) == 1
    assert apptainer.location[0] == "/path/to/location"

def test_images(apptainer):
    images = apptainer.images()
    assert isinstance(images, list)

def test_ps(apptainer):
    processes = apptainer.ps()
    assert isinstance(processes, list)

def test_system(apptainer):
    stdout, stderr = apptainer.system("echo 'Hello, World!'")
    assert stdout.strip() == "Hello, World!"
    assert stderr.strip() == ""

def test_list(apptainer):
    output = apptainer.list()
    assert isinstance(output, tuple)
    assert len(output) == 2

def test_info(apptainer):
    output_dict = apptainer.info()
    assert isinstance(output_dict, dict)
    assert "instances" in output_dict

def test_find_image(apptainer):
    with pytest.raises(ValueError):
        apptainer.find_image("nonexistent_image")

def test_inspect(apptainer):
    result = apptainer.inspect("image_name")
    assert isinstance(result, list)
    assert len(result) > 0

def test_cache(apptainer):
    data = apptainer.cache()
    assert isinstance(data, list)
    assert len(data) > 0

def test_stats(apptainer):
    stdout, stderr = apptainer.stats(output="json")
    assert isinstance(stdout, str)
    assert isinstance(stderr, str)

def test_start(apptainer):
    with pytest.raises(ValueError):
        apptainer.start()
    with pytest.raises(ValueError):
        apptainer.start(name="instance_name")