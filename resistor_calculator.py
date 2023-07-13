"""
Calculate the resistance and tolerances of a resistor based on the chosen colour bands.
Currently works with Python interpreter 3.10
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
import re

__author__ = 'Nicholas Williams'

NON_ZERO_NUMBERS = ("1", "2", "3", "4", "5", "6", "7", "8", "9")

UNITS_TO_POWER = {"Ω": 0,
                  "kΩ": 3,
                  "MΩ": 6,
                  "GΩ": 9}

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
                        "-1 Gold": ((1, 215 / 255, 0, 1), -1),
                        "-2 Silver": ((192 / 255, 192 / 255, 192 / 255, 1), -2)}

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

COLOUR_TO_TEMP_CO = {"100 Brown": ((1.5, 0.9, 0.5, 1), 100),
                     "50 Red": ((255, 0, 0, 1), 50),
                     "15 Orange": ((2.5, 1.2, 0, 1), 15),
                     "25 Yellow": ((255, 255, 0, 1), 25),
                     "10 Blue": ((0, 0, 255, 1), 10),
                     "5 Violet": ((128, 0, 128, 1), 5)}

PERMITTED_CHARS = {"backspace": 8,
                   "delete": 127,
                   "left": 276,
                   "right": 275}


class ResistorCalculatorApp(App):
    """ResistorCalculatorApp is a Kivy app for calculating the resistance and tolerance of a
    resistor based on the chosen colour bands"""
    units = ListProperty()
    colour_to_digit = ListProperty()
    colour_to_multiplier = ListProperty()
    colour_to_tolerance = ListProperty()
    colour_to_temp_co = ListProperty()

    def build(self):
        """Build the Kivy app from the kv file"""
        self.title = "Resistor calculator 1.0"
        self.root = Builder.load_file('resistor_calculator.kv')
        self.units = UNITS_TO_POWER
        self.colour_to_digit = COLOUR_TO_DIGIT
        self.colour_to_multiplier = COLOUR_TO_MULTIPLIER
        self.colour_to_tolerance = COLOUR_TO_TOLERANCE
        self.colour_to_temp_co = COLOUR_TO_TEMP_CO

        Window.size = (1200, 1000)

        return self.root

    class FloatInput(TextInput):
        """FloatInput is a subclass of TextInput that allows only numbers 0-9 and one decimal place."""
        pat = re.compile('[^0-9]')

        def keyboard_on_key_down(self, window, keycode, text, modifiers):
            """Allow backspace to be pressed"""

            if keycode[0] in PERMITTED_CHARS.values():
                self.readonly = False
                TextInput.keyboard_on_key_down(self, window, keycode, text, modifiers)

            print(self.text)
            if len(self.text.replace(".", '')) >= self.max_char:  # Remove full-stop
                self.readonly = True
                if keycode[0] == 48 or keycode[0] == 256:  # character '0' is represented by ASCII integer 48
                    if len(self.text) < self.max_char + 1:
                        self.readonly = False
                        TextInput.keyboard_on_key_down(self, window, keycode, text, modifiers)
                    else:
                        self.readonly = True
                        TextInput.keyboard_on_key_down(self, window, keycode, text, modifiers)

        def insert_text(self, substring, from_undo=False):
            pat = self.pat
            if '.' in self.text:
                s = re.sub(pat, '', substring)
            else:
                s = '.'.join(
                    re.sub(pat, '', s)
                    for s in substring.split('.', 1)
                )

            return super().insert_text(s, from_undo=from_undo)

    def find_colour_bands(self, digits, unit, bands):
        """Change colour bands depending on typed value."""
        # pass
        if unit != '' and digits != '':
            # print(f"digits: '{digits}', power: '{UNITS_TO_POWER[unit]}'")
            if '.' in digits:
                digits = digits.split('.')
                if len(digits) == 1:
                    digits = ['0', digits[0]]
                    mantissa = int(digits[0]) + int(digits[1])
                    resistance = mantissa * pow(10, UNITS_TO_POWER[unit])
                else:
                    print(digits)
                    if digits[1] == '':
                        digits[1] = 0
                    mantissa = int(digits[0]) + int(digits[1])/10
                    resistance = mantissa * pow(10, UNITS_TO_POWER[unit])
            else:
                mantissa = int(digits)
                resistance = mantissa * pow(10, UNITS_TO_POWER[unit])

            if bands == 3:
                print(f"digits: '{digits}', mantissa: '{mantissa}', power: '{UNITS_TO_POWER[unit]}', resistance: '{resistance}'")
                self.root.ids.r3b1.text = list(COLOUR_TO_DIGIT.keys())[int(str(digits[0]))]
                self.root.ids.r3b2.text = list(COLOUR_TO_DIGIT.keys())[0] if len(str(mantissa)) < 2 else list(COLOUR_TO_DIGIT.keys())[int(str(digits[1]))]
                self.root.ids.r3b3.text = list(COLOUR_TO_MULTIPLIER.keys())[UNITS_TO_POWER[unit] - 2] if resistance < 10 else list(COLOUR_TO_MULTIPLIER.keys())[UNITS_TO_POWER[unit] - 1]


    def return_band_colour(self, band_type, colour_name):
        """Return the colour for the corresponding band based on the spinner selection."""
        if band_type == "digit":
            try:
                return COLOUR_TO_DIGIT[colour_name][0]
            except KeyError:
                return f"{colour_name} is not a key in the 'colour_to_digit' dictionary."

        if band_type == "multiplier":
            try:
                return COLOUR_TO_MULTIPLIER[colour_name][0]
            except KeyError:
                return f"{colour_name} is not a key in the 'colour_to_multiplier' dictionary."

        if band_type == "tolerance":
            try:
                return COLOUR_TO_TOLERANCE[colour_name][0]
            except KeyError:
                return f"{colour_name} is not a key in the 'colour_to_tolerance' dictionary."

        if band_type == "temp_co":
            try:
                return COLOUR_TO_TEMP_CO[colour_name][0]
            except KeyError:
                return f"{colour_name} is not a key in the 'colour_to_temp_co' dictionary."

    def calculate_resistance(self, number_of_bands):
        """Calculate the resistance once enough spinners have been selected"""
        if number_of_bands == 3:
            if self.root.ids.r3b1.text != '' and self.root.ids.r3b2.text != '' and self.root.ids.r3b3.text != '':
                resistance = round(int(str(COLOUR_TO_DIGIT[self.root.ids.r3b1.text][1]) +
                                       str(COLOUR_TO_DIGIT[self.root.ids.r3b2.text][1])) *
                                   pow(10, COLOUR_TO_MULTIPLIER[self.root.ids.r3b3.text][1]), 10)

                self.root.ids.r3_value.text = f"\n{resistance} Ω\n{str(resistance / 1000) + ' kΩ' if resistance >= 1000 else ''}" \
                                              f"\n{str(resistance / 1000000) + ' MΩ' if resistance >= 1000000 else ''}" \
                                              f"\n{str(resistance / 1000000000) + ' GΩ' if resistance >= 1000000000 else ''}"

        if number_of_bands == 4:
            if self.root.ids.r4b1.text != '' and self.root.ids.r4b2.text != '' and self.root.ids.r4b3.text != '':
                resistance = round(int(str(COLOUR_TO_DIGIT[self.root.ids.r4b1.text][1]) +
                                       str(COLOUR_TO_DIGIT[self.root.ids.r4b2.text][1])) *
                                   pow(10, COLOUR_TO_MULTIPLIER[self.root.ids.r4b3.text][1]), 10)

                tolerance = 0
                if self.root.ids.r4b4.text != '':
                    tolerance = COLOUR_TO_TOLERANCE[self.root.ids.r4b4.text][1]

                self.root.ids.r4_value.text = f"\n{resistance} Ω\n{str(resistance / 1000) + ' kΩ' if resistance >= 1000 else ''}" \
                                              f"\n{str(resistance / 1000000) + ' MΩ' if resistance >= 1000000 else ''}" \
                                              f"\n{str(resistance / 1000000000) + ' GΩ' if resistance >= 1000000000 else ''}" \
                                              f"\n\n{'±' + str(tolerance * 100) + ' %' if self.root.ids.r4b4.text != '' else ''}" \
                                              f"\n{str(round(self.format_tolerance_resistance(resistance)[0] * (1 - tolerance), 10)) + ' - ' + str(round(self.format_tolerance_resistance(resistance)[0] * (1 + tolerance), 10)) + self.format_tolerance_resistance(resistance)[1] if self.root.ids.r4b4.text != '' else ''}"
        if number_of_bands == 5:
            if self.root.ids.r5b1.text != '' and self.root.ids.r5b2.text != '' and self.root.ids.r5b3.text != '' and self.root.ids.r5b4.text != '':
                resistance = round(int(str(COLOUR_TO_DIGIT[self.root.ids.r5b1.text][1]) +
                                       str(COLOUR_TO_DIGIT[self.root.ids.r5b2.text][1]) +
                                       str(COLOUR_TO_DIGIT[self.root.ids.r5b3.text][1])) *
                                   pow(10, COLOUR_TO_MULTIPLIER[self.root.ids.r5b4.text][1]), 10)

                tolerance = 0
                if self.root.ids.r5b5.text != '':
                    tolerance = COLOUR_TO_TOLERANCE[self.root.ids.r5b5.text][1]

                self.root.ids.r5_value.text = f"\n{resistance} Ω\n{str(resistance / 1000) + ' kΩ' if resistance >= 1000 else ''}" \
                                              f"\n{str(resistance / 1000000) + ' MΩ' if resistance >= 1000000 else ''}" \
                                              f"\n{str(resistance / 1000000000) + ' GΩ' if resistance >= 1000000000 else ''}" \
                                              f"\n\n{'±' + str(tolerance * 100) + ' %' if self.root.ids.r5b5.text != '' else ''}" \
                                              f"\n{str(round(self.format_tolerance_resistance(resistance)[0] * (1 - tolerance), 10)) + ' - ' + str(round(self.format_tolerance_resistance(resistance)[0] * (1 + tolerance), 10)) + self.format_tolerance_resistance(resistance)[1] if self.root.ids.r5b5.text != '' else ''}"
        if number_of_bands == 6:
            if self.root.ids.r6b1.text != '' and self.root.ids.r6b2.text != '' and self.root.ids.r6b3.text != '' and self.root.ids.r6b4.text != '':
                resistance = round(int(str(COLOUR_TO_DIGIT[self.root.ids.r6b1.text][1]) +
                                       str(COLOUR_TO_DIGIT[self.root.ids.r6b2.text][1]) +
                                       str(COLOUR_TO_DIGIT[self.root.ids.r6b3.text][1])) *
                                   pow(10, COLOUR_TO_MULTIPLIER[self.root.ids.r6b4.text][1]), 10)

                tolerance = 0
                if self.root.ids.r6b5.text != '':
                    tolerance = COLOUR_TO_TOLERANCE[self.root.ids.r6b5.text][1]

                temp_co = 0
                if self.root.ids.r6b6.text != '':
                    temp_co = COLOUR_TO_TEMP_CO[self.root.ids.r6b6.text][1]

                self.root.ids.r6_value.text = f"\n{resistance} Ω\n{str(resistance / 1000) + ' kΩ' if resistance >= 1000 else ''}" \
                                              f"\n{str(resistance / 1000000) + ' MΩ' if resistance >= 1000000 else ''}" \
                                              f"\n{str(resistance / 1000000000) + ' GΩ' if resistance >= 1000000000 else ''}" \
                                              f"\n\n{'±' + str(tolerance * 100) + ' %' if self.root.ids.r6b5.text != '' else ''}" \
                                              f"\n{str(round(self.format_tolerance_resistance(resistance)[0] * (1 - tolerance), 10)) + ' - ' + str(round(self.format_tolerance_resistance(resistance)[0] * (1 + tolerance), 10)) + self.format_tolerance_resistance(resistance)[1] if self.root.ids.r6b5.text != '' else ''}" \
                                              f"\n\n{str(temp_co) + ' ppm/°C' if self.root.ids.r6b6.text != '' else ''}"

    def format_tolerance_resistance(self, resistance):
        """Format the tolerance resistance for tidiness"""
        if resistance < 1000:
            abbreviation = ' Ω'
            return resistance, abbreviation
        elif 1000 <= resistance <= 1000000:
            abbreviation = ' kΩ'
            return resistance / 1000, abbreviation
        elif 1000000 <= resistance <= 1000000000:
            abbreviation = ' MΩ'
            return resistance / 1000000, abbreviation
        else:  # 999 GΩ is maximum possible allowed
            abbreviation = ' GΩ'
            return resistance / 1000000000, abbreviation


ResistorCalculatorApp().run()
