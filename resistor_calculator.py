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


class ResistorCalculatorApp(App):
    """ResistorCalculatorApp is a Kivy app for calculating the resistance and tolerance of a
    resistor based on the chosen colour bands"""
    resistor_3_values = ListProperty()
    current_resistor_3_value = StringProperty()

    def build(self):
        """Build the Kivy app from the kv file"""
        self.title = "Resistor calculator 1.0"
        self.root = Builder.load_file('resistor_calculator.kv')
        self.resistor_3_values = RESISTOR_3_VALUES
        self.current_resistor_3_value = self.resistor_3_values[0]
        return self.root

    def calculate_resistance(self, res):
        pass

    def display_resistor_colours(self, resistance):
        pass


ResistorCalculatorApp().run()
