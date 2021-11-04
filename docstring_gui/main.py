import os, sys
import yaml
import webbrowser
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import (FadeTransition, Screen, ScreenManager,
                                    TransitionBase)
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.resources import resource_add_path, resource_find

# import powerapps classes
from powerapps_docstring.documentation import Docstring

# import screen classes
from docstring_gui.screens.result_screen.result_screen import ResultScreen


class MainScreen(Screen):
    source = ObjectProperty(None)
    output = ObjectProperty(None)
    config = ObjectProperty(None)

    def create_documentation(self):
        #docstring = Docstring(pa_src_path, output_path, config)
        # docstring.create_documentation()

        # Spot check on CanvasManifest.json file. If this exists, it should be
        # a correct power apps source path
        if not os.path.isfile(self.source.text + "CanvasManifest.json"):
            self.source.error = True
            self.source.helper_text = "Path is not an Power Apps source"
            if not self.source.text.endswith("\\"):
                self.source.text = self.source.text + "\\"
            return
        else:
            self.source.error = False
            self.source.helper_text = "/path/to/src/app/"

        # check if output path is existing
        if not os.path.isdir(self.output.text) or self.output.text == "":
            self.output.error = True
            self.output.helper_text = "Not a directory or not existing"
            return
        else:
            self.output.error = False
            self.output.helper_text = "./output/"

        # check config file
        if not os.path.isfile(self.config.text):
            print(resource_find("config.yaml"))
            config_file = resource_find("config.yaml")
        else:
            config_file = self.config.text

        with open(config_file, "r", encoding='utf8') as file:
            config_instance = yaml.safe_load(file)

        # create documentation
        # TODO: add try block and show error page if somethin went wrong
        docstring = Docstring(self.source.text, self.output.text, config_instance)
        output_file_path = docstring.create_documentation()

        # navigate to succeed page
        self.manager.transition.direction = "left"
        self.manager.current = "result-screen"

        self.manager.get_screen("result-screen").output_file.text = output_file_path

        print("Created")

    def open_github(self):
        webbrowser.open_new_tab("https://github.com/sebastian-muthwill/powerapps-docstring")
    
    def open_new_issue(self):
        webbrowser.open_new_tab("https://github.com/sebastian-muthwill/powerapps-docstring/issues/new")


class MainApp(MDApp):
    def build(self):
        Window.size = (1080, 720)
        self.theme_cls.theme_style = "Light"  # "Light"
        #Builder.load_file("./docstring_gui/main.kv")
        #self.theme_cls.primary_palette = "Teal"

    def on_start(self):
        pass


# the ScreenManager handles all screens and changes
# screen change can be called from kv with:
# on_press:
#    root.manager.transition.direction = 'left'
#    root.manager.current = "result-screen"
sm = ScreenManager()
sm.add_widget(MainScreen(name="main-screen"))
sm.add_widget(ResultScreen(name="result-screen"))

# needed for pyinstaller onefile exe
if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))

MainApp().run()
