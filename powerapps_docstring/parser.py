import os
import json
import yaml


class Parser():
    def __init__(self, source) -> None:
        self.source_path = source

    def get_connections(self) -> dict:
        """Read existing connections
        """
        connections = {}    # create empty dict

        connections_file = self.source_path + "Connections/Connections.json"
        if os.path.isfile(connections_file):
            with open(connections_file, "r") as file:
                connections = json.load(file)

        return connections

    def _get_screen_content(self, screen_name):
        screen_path = self.source_path + "src/" + screen_name
        screen_content = {}

        with open(screen_path, "r", encoding='utf8') as file:
            screen_content = yaml.load(file, Loader=yaml.BaseLoader)

        return screen_content

    def get_screen_objects(self, screen_name) -> tuple:
        screen_content = self._get_screen_content(screen_name)
        # print(screen_content)
        screen_name = screen_name.replace(".fx.yaml", "")
        return screen_name, screen_content

    def get_canvas_manifest(self):
        app_name = "PowerApp_Documentation"
        # get name from CanvasManifest.json
        if os.path.isfile(self.source_path + "CanvasManifest.json"):
            with open(self.source_path + "CanvasManifest.json", "r", encoding="utf-8") as file:
                canvas_manifest = json.load(file)

        return canvas_manifest
