import pytest


SOURCE_PATH = "example/src/meetingcapturedemo/"


def test_instantiate_parser():
    from powerapps_docstring.parser import Parser
    p = Parser(SOURCE_PATH)

    assert isinstance(p, Parser), ("Should be an instance of parser object")
    assert p.source_path == SOURCE_PATH


def test_get_connections():
    from powerapps_docstring.parser import Parser
    p = Parser(SOURCE_PATH)
    connections = p.get_connections()
    
    # spot check on some values in connection
    for con in connections.items():

        assert "connectionInstanceId" in con[1].keys()
        assert "connectionParameters" in con[1].keys()
        assert "connectionRef" in con[1].keys()


def test_get_screen_objects():
    from powerapps_docstring.parser import Parser
    p = Parser(SOURCE_PATH)
    result = p.get_screen_objects("WelcomeScreen.fx.yaml")
    assert result[0] == "WelcomeScreen", "Should return on index 0 the name of the screen"
    assert isinstance(result[1], dict), "Shall return on index 1 the screen contents as dict"


def test_get_canvas_manifest():
    from powerapps_docstring.parser import Parser
    p = Parser(SOURCE_PATH)
    result = p.get_canvas_manifest()
    assert isinstance(result, dict), "Shall return a dict with CanvasManifest content"
