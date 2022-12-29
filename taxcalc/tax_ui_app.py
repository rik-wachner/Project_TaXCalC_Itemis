import tkinter
import customtkinter  # https://pypi.org/project/customtkinter/
from taxcalc.tax_controller import TaxController

# Library specific 'global' settings
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class TaxUIApp(customtkinter.CTk):
    pass