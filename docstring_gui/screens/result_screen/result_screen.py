import subprocess
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class ResultScreen(Screen):
    output_file = ObjectProperty(None)

    def open_file(self, path):
        subprocess.Popen(f'explorer /select,{path}')
