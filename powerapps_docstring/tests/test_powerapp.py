import pytest

SOURCE_PATH_SRC = "example/src/meetingcapturedemo/"
SOURCE_PATH_MSAPP = "example/src/meetingcapturedemo.msapp"
SOURCE_PATH_ZIP = "example/src/meetingcapturedemo.zip"

def test_class_init():
    from powerapps_docstring.powerapp import PowerApp

    # currently only the src directory is implemented. 
    pa = PowerApp(SOURCE_PATH_SRC)
    assert isinstance(pa, PowerApp)
    assert pa.source_type == "directory"
    assert pa.source_type != "msapp"
    assert pa.source_type != "zip"