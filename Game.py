__author__ = "Justin", "Danny"

import kivy
kivy.require("1.8.0")

import random
import sys

from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget


class Background(Widget):
    image1 = ObjectProperty(Image())
    image2 = ObjectProperty(Image())

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self, **kwarg):
        super(Background, self).__init__(**kwarg)
        self.size = (800,600)

    def update(self):
        self.image1.pos = Vector(*self.velocity) + self.image1.pos
        self.image2.pos = Vector(*self.velocity) + self.image2.pos

        if self.image1.right <= 0:
            self.image1.pos = (self.width, 0)
        if self.image2.right <= 0:
            self.image2.pos = (self.width, 0)

    def update_position(self):
        self.image1.pos = (0, 0)
        self.image2.pos = (self.width, 0)


class PlayerObj(Image):

    def __init__(self, pos):

        #placeholder image
        self.allow_stretch = True
        self.source = "images/Rock.gif"
        self.size=(60, 60)
        super(PlayerObj, self).__init__(pos = pos)

        self.velocity_y = 0
        self.gravity = .05

    def update(self):
        if self.velocity_y >= -2.7:
            self.velocity_y -= self.gravity
        self.y += self.velocity_y

    def on_touch_down(self, *ignore):
        if self.velocity_y <= 3.5:
            self.velocity_y += 6



class Game(Widget):
    background = ObjectProperty(Background())

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

        self.background.velocity = [-0.25, 0]
        self.bind(size=self.size_callback)
        self.size = Background().size

        #player's object
        self.player = PlayerObj(pos = (self.width / 4, self.height/2))
        self.add_widget(self.player)

        Clock.schedule_interval(self.update, 1.0/60.0)

    def size_callback(self, instance, value):
        self.background.size = value
        self.background.update_position()

    def update(self, dt):
        self.background.update()
        self.player.update()


class NameApp(App):
    def build(self):
        game = Game()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == "__main__":
    NameApp().run()

