"""
Calculate the resistance and tolerances of a resistor based on the chosen colour bands.
Currently works with Python interpreter 3.10
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import StringProperty

__author__ = 'Nicholas Williams'

RESISTOR_3_VALUES = ("1", "2.2", "2.7", "3.3", "3.9", "4.7", "5.6", "6.8", "8.2", "9.1", "10")

COLOUR_TO_RGBA = {"Black": (0, 0, 0, 1),
                  "Brown": (165 / 255, 42 / 255, 42 / 255, 1),
                  "Red": (1, 0, 0, 1),
                  "Orange": (1, 165 / 255, 0, 1),
                  "Yellow": (1, 1, 0, 1),
                  "Green": (0, 1, 0, 1),
                  "Blue": (0, 0, 1, 1),
                  "Violet": (128 / 255, 0, 128 / 255, 1),
                  "Grey": (211 / 255, 211 / 255, 211 / 255, 1),
                  "White": (1, 1, 1, 1),
                  "Gold": (1, 215 / 255, 0, 1),
                  "Silver": (192 / 255, 192 / 255, 192 / 255, 1)}


class ResistorCalculatorApp(App):
    """ResistorCalculatorApp is a Kivy app for calculating the resistance and tolerance of a
    resistor based on the chosen colour bands"""
    resistor_3_values = ListProperty()
    colour_to_rgba = ListProperty()

    def build(self):
        """Build the Kivy app from the kv file"""
        self.title = "Resistor calculator 1.0"
        self.root = Builder.load_file('resistor_calculator.kv')
        self.resistor_3_values = RESISTOR_3_VALUES
        self.colour_to_rgba = COLOUR_TO_RGBA
        return self.root

    def return_rgba(self, colour_name):
        try:
            if self.root.ids.r3b1.text != '' and self.root.ids.r3b2.text != '' and self.root.ids.r3b3.text != '':
                self.calculate_resistance()
            return COLOUR_TO_RGBA[colour_name]
        except KeyError:
            return f"{colour_name} is not a key in the 'colour_to_rgba' dictionary."

    def calculate_resistance(self):
        self.root.ids.r3_value.text = "HELLO!"

    def display_resistor_colours(self, resistance):
        pass


ResistorCalculatorApp().run()
