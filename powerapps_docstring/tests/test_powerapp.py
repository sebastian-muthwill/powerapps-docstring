import pytest

SOURCE_PATH_SRC = "example/src/meetingcapturedemo/"
SOURCE_PATH_MSAPP = "example/src/meetingcapturedemo.msapp"
SOURCE_PATH_ZIP = "example/src/meetingcapturedemo.zip"

def test_class_init():
    from powerapps_docstring.powerapp import PowerApp

    pa = PowerApp(SOURCE_PATH_SRC)
    assert isinstance(pa, PowerApp)

def test__check_source_type_directory():
    from powerapps_docstring.powerapp import PowerApp

    pa = PowerApp(SOURCE_PATH_SRC)
    assert pa.source_type == "directory"

def test__check_source_type_msapp():
    from powerapps_docstring.powerapp import PowerApp

    pa = PowerApp(SOURCE_PATH_MSAPP)
    assert pa.source_type == "msapp"

def test__check_source_type_zip():
    from powerapps_docstring.powerapp import PowerApp

    pa = PowerApp(SOURCE_PATH_ZIP)
    assert pa.source_type == "zip"