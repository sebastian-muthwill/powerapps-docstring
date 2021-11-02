import os
import yaml
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import (FadeTransition, Screen, ScreenManager,
                                    TransitionBase)
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
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

        # TODO: Check source, output and config path / files
        print(self.source.text)
        print(self.output.text)
        print(self.config.text)

        # check config file
        if not os.path.isfile(self.config.text):
            config_file = "config.yaml"
        else:
            config_file = self.config.text

        with open(config_file, "r", encoding='utf8') as file:
            config_instance = yaml.safe_load(file)

        docstring = Docstring(self.source.text, self.output.text, config_instance)
        output_file_path = docstring.create_documentation()
        self.manager.get_screen("result-screen").output_file.text = output_file_path

        print("Created")


class MainApp(MDApp):
    def build(self):
        Window.size = (1080, 720)
        self.theme_cls.theme_style = "Light"  # "Light"
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

MainApp().run()
