from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager, TransitionBase
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder

# import screen classes
from screens.result_screen.result_screen import ResultScreen


class MainScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # "Light"
        #self.theme_cls.primary_palette = "Teal"


    def on_start(self):
        pass

sm = ScreenManager()
sm.add_widget(MainScreen(name="main-screen"))
sm.add_widget(ResultScreen(name="result-screen"))

MainApp().run()
