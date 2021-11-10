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

        connections_file = os.path.join(self.source_path, "Connections", "Connections.json")
        if os.path.isfile(connections_file):
            with open(connections_file, "r") as file:
                connections = json.load(file)

        return connections

    def _get_screen_content(self, screen_name):
        screen_path = os.path.join(self.source_path, "src", screen_name)
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
        # get name from CanvasManifest.json
        manifest_file = os.path.join(self.source_path, "CanvasManifest.json")
        if os.path.isfile(manifest_file):
            with open(manifest_file, "r", encoding="utf-8") as file:
                canvas_manifest = json.load(file)

        return canvas_manifest
