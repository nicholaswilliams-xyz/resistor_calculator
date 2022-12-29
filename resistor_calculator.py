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

# Format for RGBA: | Color name | RGBA counterpart | digit | Tolerance | Temperature Coefficient
#                  | English    | tuple            | 0 - 9 | decimal   |

# Example:         | "Black"    | (0, 0, 0, 1)     | 0     | N/A       | N/A
# Example:         | "Yellow"   | (1, 1, 0, 1)     | 4     | 0.04      | 25
# Multiplier value is not needed, as multiplier = 10^digit
COLOUR_TO_DETAILS = {"0 Black": ((0, 0, 0, 1), 0),
                     "1 Brown": ((165 / 255, 42 / 255, 42 / 255, 1), 1, 0.01, 100),
                     "2 Red": ((1, 0, 0, 1), 2, 0.02, 50),
                     "3 Orange": ((1, 165 / 255, 0, 1), 3, 0.03, 15),
                     "4 Yellow": ((1, 1, 0, 1), 4, 0.04, 25),
                     "5 Green": ((0, 1, 0, 1), 5, 0.005),
                     "6 Blue": ((0, 0, 1, 1), 6, 0.0025, 10),
                     "7 Violet": ((128 / 255, 0, 128 / 255, 1), 7, 0.001, 5),
                     "8 Grey": ((211 / 255, 211 / 255, 211 / 255, 1), 8, 0.0005),
                     "9 White": ((1, 1, 1, 1), 9)}

# Gold and Silver have only multiplier and tolerance purposes and hence their own dictionary
GOLD_SILVER_TO_DETAILS = {"Gold": ((1, 215 / 255, 0, 1), 0.1, 0.05),
                          "Silver": ((192 / 255, 192 / 255, 192 / 255, 1), 0.01, 0.1)}


class ResistorCalculatorApp(App):
    """ResistorCalculatorApp is a Kivy app for calculating the resistance and tolerance of a
    resistor based on the chosen colour bands"""
    resistor_3_values = ListProperty()
    colour_to_details = ListProperty()

    def build(self):
        """Build the Kivy app from the kv file"""
        self.title = "Resistor calculator 1.0"
        self.root = Builder.load_file('resistor_calculator.kv')
        self.resistor_3_values = RESISTOR_3_VALUES
        self.colour_to_details = COLOUR_TO_DETAILS
        return self.root

    def return_rgba(self, colour_name):
        try:
            return COLOUR_TO_DETAILS[colour_name][0]
        except KeyError:
            return f"{colour_name} is not a key in the 'colour_to_details' dictionary."

    def calculate_resistance(self):
        if self.root.ids.r3b1.text != '' and self.root.ids.r3b2.text != '' and self.root.ids.r3b3.text != '':

            resistance = int(str(COLOUR_TO_DETAILS[self.root.ids.r3b1.text][1]) +
                             str(COLOUR_TO_DETAILS[self.root.ids.r3b2.text][1])) * \
                         pow(10, COLOUR_TO_DETAILS[self.root.ids.r3b3.text][1])

            self.root.ids.r3_value.text = f"{resistance} Ω\n{str(resistance / 1000) + ' kΩ' if resistance >= 1000 else ''}" \
                                          f"\n{str(resistance / 1000000) + ' MΩ' if resistance >= 1000000 else ''}" \
                                          f"\n{str(resistance / 1000000000) + ' GΩ' if resistance >= 1000000000 else ''}"

    def display_resistor_colours(self, resistance):
        pass


ResistorCalculatorApp().run()
