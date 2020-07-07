from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import StringProperty,ObjectProperty
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.event import EventDispatcher
from kivymd.uix.button import MDRectangleFlatButton,MDRoundFlatButton,MDRectangleFlatButton,MDRaisedButton
import json 
import requests
import time
from kivy.uix.textinput import TextInput
from kivy.network.urlrequest import UrlRequest
import random
from urllib.request import urlopen
from kivy.uix.popup import Popup
from kivy.graphics import Color
import urllib.parse
import urllib.request
import inspect, os
import _thread
import threading
from kivy.core.window import Window

class Quiz(Screen):
    pass


class Main1q1App(MDApp):
    sm = ScreenManager(transition=FadeTransition())
    def build(self):
        self.sm.add_widget(Quiz(name="quiz"))
        return self.sm

if __name__ == "__main__":
    Main1q1App().run()