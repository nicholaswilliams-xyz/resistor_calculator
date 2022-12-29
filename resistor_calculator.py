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
# COLOUR_TO_DETAILS = {"0 Black": ((0, 0, 0, 1), 0),
#                          "1 Brown": ((1.5, 0.9, 0.5, 1), 1, 0.01, 100),
#                          "2 Red": ((255, 0, 0, 1), 2, 0.02, 50),
#                          "3 Orange": ((2.5, 1.2, 0, 1), 3, 0.03, 15),
#                          "4 Yellow": ((255, 255, 0, 1), 4, 0.04, 25),
#                          "5 Green": ((0, 255, 0, 1), 5, 0.005),
#                          "6 Blue": ((0, 0, 255, 1), 6, 0.0025, 10),
#                          "7 Violet": ((128, 0, 128, 1), 7, 0.001, 5),
#                          "8 Grey": ((1, 1, 1, 1), 8, 0.0005),
#                          "9 White": ((255, 255, 255, 1), 9)}

COLOUR_TO_DIGIT = {"0 Black": ((0, 0, 0, 1), 0),
                   "1 Brown": ((1.5, 0.9, 0.5, 1), 1),
                   "2 Red": ((255, 0, 0, 1), 2),
                   "3 Orange": ((2.5, 1.2, 0, 1), 3),
                   "4 Yellow": ((255, 255, 0, 1), 4),
                   "5 Green": ((0, 255, 0, 1), 5),
                   "6 Blue": ((0, 0, 255, 1), 6),
                   "7 Violet": ((128, 0, 128, 1), 7),
                   "8 Grey": ((1, 1, 1, 1), 8),
                   "9 White": ((255, 255, 255, 1), 9)}

COLOUR_TO_MULTIPLIER = {"0 Black": ((0, 0, 0, 1), 0),
                        "1 Brown": ((1.5, 0.9, 0.5, 1), 1),
                        "2 Red": ((255, 0, 0, 1), 2),
                        "3 Orange": ((2.5, 1.2, 0, 1), 3),
                        "4 Yellow": ((255, 255, 0, 1), 4),
                        "5 Green": ((0, 255, 0, 1), 5),
                        "6 Blue": ((0, 0, 255, 1), 6),
                        "7 Violet": ((128, 0, 128, 1), 7),
                        "8 Grey": ((1, 1, 1, 1), 8),
                        "9 White": ((255, 255, 255, 1), 9),
                        "Gold": ((1, 215 / 255, 0, 1), -1),
                        "Silver": ((192 / 255, 192 / 255, 192 / 255, 1), -2)}

COLOUR_TO_TOLERANCE = {"1 Brown": ((1.5, 0.9, 0.5, 1), 0.01),
                       "2 Red": ((255, 0, 0, 1), 0.02),
                       "3 Orange": ((2.5, 1.2, 0, 1), 0.03),
                       "4 Yellow": ((255, 255, 0, 1), 0.04),
                       "0.5 Green": ((0, 255, 0, 1), 0.005),
                       "0.25 Blue": ((0, 0, 255, 1), 0.0025),
                       "0.1 Violet": ((128, 0, 128, 1), 0.001),
                       "0.05 Grey": ((1, 1, 1, 1), 0.0005),
                       "5 Gold": ((1, 215 / 255, 0, 1), 0.05),
                       "10 Silver": ((192 / 255, 192 / 255, 192 / 255, 1), 0.1)}

COLOUR_TO_TEMP_CO = {"100 Brown": ((1.5, 0.9, 0.5, 1), 1, 0.01, 100),
                     "50 Red": ((255, 0, 0, 1), 2, 0.02, 50),
                     "15 Orange": ((2.5, 1.2, 0, 1), 3, 0.03, 15),
                     "25 Yellow": ((255, 255, 0, 1), 4, 0.04, 25),
                     "10 Blue": ((0, 0, 255, 1), 6, 0.0025, 10),
                     "5 Violet": ((128, 0, 128, 1), 7, 0.001, 5)}


# Gold and Silver have only multiplier and tolerance purposes and hence their own dictionary
# GOLD_SILVER_TO_DETAILS = {"Gold": ((1, 215 / 255, 0, 1), 0.1, 0.05),
#                           "Silver": ((192 / 255, 192 / 255, 192 / 255, 1), 0.01, 0.1)}


class ResistorCalculatorApp(App):
    """ResistorCalculatorApp is a Kivy app for calculating the resistance and tolerance of a
    resistor based on the chosen colour bands"""
    resistor_3_values = ListProperty()
    colour_to_digit = ListProperty()
    colour_to_multiplier = ListProperty()
    colour_to_tolerance = ListProperty()
    colour_to_temp_co = ListProperty()

    def build(self):
        """Build the Kivy app from the kv file"""
        self.title = "Resistor calculator 1.0"
        self.root = Builder.load_file('resistor_calculator.kv')
        self.resistor_3_values = RESISTOR_3_VALUES
        self.colour_to_digit = COLOUR_TO_DIGIT
        self.colour_to_multiplier = COLOUR_TO_MULTIPLIER
        self.colour_to_tolerance = COLOUR_TO_TOLERANCE
        self.colour_to_temp_co = COLOUR_TO_TEMP_CO

        return self.root

    def return_band_colour(self, band_type, colour_name):
        if band_type == "digit":
            try:
                return COLOUR_TO_DIGIT[colour_name][0]
            except KeyError:
                return f"{colour_name} is not a key in the 'colour_to_digit' dictionary."

        if band_type == "multiplier":
            try:
                return COLOUR_TO_MULTIPLIER[colour_name][0]
            except KeyError:
                return f"{colour_name} is not a key in the 'colour_to_digit' dictionary."

        if band_type == "tolerance":
            try:
                return COLOUR_TO_TOLERANCE[colour_name][0]
            except KeyError:
                return f"{colour_name} is not a key in the 'colour_to_digit' dictionary."

        if band_type == "temp_co":
            try:
                return COLOUR_TO_TOLERANCE[colour_name][0]
            except KeyError:
                return f"{colour_name} is not a key in the 'colour_to_digit' dictionary."

    def calculate_resistance(self, number_of_bands):
        if number_of_bands == 3:
            if self.root.ids.r3b1.text != '' and self.root.ids.r3b2.text != '' and self.root.ids.r3b3.text != '':
                resistance = int(str(COLOUR_TO_DIGIT[self.root.ids.r3b1.text][1]) +
                                 str(COLOUR_TO_DIGIT[self.root.ids.r3b2.text][1])) * \
                             pow(10, COLOUR_TO_DIGIT[self.root.ids.r3b3.text][1])

                self.root.ids.r3_value.text = f"{resistance} Ω\n{str(resistance / 1000) + ' kΩ' if resistance >= 1000 else ''}" \
                                              f"\n{str(resistance / 1000000) + ' MΩ' if resistance >= 1000000 else ''}" \
                                              f"\n{str(resistance / 1000000000) + ' GΩ' if resistance >= 1000000000 else ''}"

        if number_of_bands == 4:
            if self.root.ids.r4b1.text != '' and self.root.ids.r4b2.text != '' and self.root.ids.r4b3.text != '':
                resistance = int(str(COLOUR_TO_DIGIT[self.root.ids.r4b1.text][1]) +
                                 str(COLOUR_TO_DIGIT[self.root.ids.r4b2.text][1])) * \
                             pow(10, COLOUR_TO_DIGIT[self.root.ids.r4b3.text][1])

                self.root.ids.r4_value.text = f"{resistance} Ω\n{str(resistance / 1000) + ' kΩ' if resistance >= 1000 else ''}" \
                                              f"\n{str(resistance / 1000000) + ' MΩ' if resistance >= 1000000 else ''}" \
                                              f"\n{str(resistance / 1000000000) + ' GΩ' if resistance >= 1000000000 else ''}"

    def display_resistor_colours(self, resistance):
        pass


ResistorCalculatorApp().run()
