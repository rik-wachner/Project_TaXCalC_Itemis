import tkinter
import customtkinter  # https://pypi.org/project/customtkinter/
from taxcalc.tax_controller import TaxController

# Library specific 'global' settings
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class TaxUIApp(customtkinter.CTk):
    def __init__(self, width: int, height: int, language_code: str):
        super().__init__()

        self.width = width
        self.height = height
        #self.language_code = language_code @TODO Add language support later
        # set connected controller to None in init
        self.connected_controller = None

        # configure window
        self.title("TaXCalC")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # configure grid layout (3x2)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # Receipt input field
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=0, column=0, columnspan=4, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # create checkbox and switch frame
        self.tax_input_frame = customtkinter.CTkFrame(self)
        self.tax_input_frame.grid(row=1, column=0, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")
        # self.tax_input_frame.grid_rowconfigure(, weight=1)
        self.tax_input_frame.grid_columnconfigure(1, weight=1)
        self.tax_input_frame.grid_rowconfigure(4, weight=1)

        # Product Name
        #   -> label
        self.product_name_label = customtkinter.CTkLabel(
            self.tax_input_frame,
            text="Product Name:",
            font=customtkinter.CTkFont(size=12)
        )
        self.product_name_label.grid(row=0, column=0, padx=10, pady=10)
        # Product Name
        #   -> input field
        self.product_name = customtkinter.CTkEntry(
            self.tax_input_frame,
            placeholder_text="Enter product name..."
        )
        self.product_name.grid(row=0, column=1, padx=(10, 20), pady=10, columnspan=2, sticky="nsew")
        # Product Quantity
        #   -> label
        self.product_quantity_label = customtkinter.CTkLabel(
            self.tax_input_frame,
            text="Quantity:",
            font=customtkinter.CTkFont(size=12)
        )
        self.product_quantity_label.grid(row=1, column=0, padx=10, pady=10)
        #   -> input field
        self.product_quantity = customtkinter.CTkEntry(
            self.tax_input_frame,
            placeholder_text="Enter product quantity..."
        )
        self.product_quantity.grid(row=1, column=1, padx=(10, 20), pady=10, columnspan=2, sticky="nsew")
        # Product Price
        #   -> label
        self.product_price_label = customtkinter.CTkLabel(
            self.tax_input_frame,
            text="Price:",
            font=customtkinter.CTkFont(size=12)
        )
        self.product_price_label.grid(row=2, column=0, padx=10, pady=10)
        #   -> input field
        self.product_price = customtkinter.CTkEntry(
            self.tax_input_frame,
            placeholder_text="Enter product price..."
        )
        self.product_price.grid(row=2, column=1, padx=(10, 20), pady=10, columnspan=2, sticky="nsew")
        # Product Tax -> Tax Rate
        #   -> label
        self.basic_tax_label = customtkinter.CTkLabel(
            self.tax_input_frame,
            text="Basic sales tax",
            font=customtkinter.CTkFont(size=12)
        )
        self.basic_tax_label.grid(row=3, column=0, padx=10, pady=10)
        #   -> input field
        self.basic_tax = customtkinter.CTkOptionMenu(
            self.tax_input_frame,
            dynamic_resizing=True,
            # > First Option: 0%
            # > Second Option: 10%
            values=["0%", "10%"]
        )
        self.basic_tax.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        # Product Tax -> Import Tax Rate
        #   -> label + input field
        self.import_checkbox = customtkinter.CTkCheckBox(
            master=self.tax_input_frame,
            text="Imported"
        )
        self.import_checkbox.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
        # Create and place 'Add Product' button
        self.add_product_button = customtkinter.CTkButton(
            master=self.tax_input_frame,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            text="Add product",
            command=self.add_product_click
        )
        self.add_product_button.grid(row=4, column=0, padx=(10, 10), pady=(10, 10), columnspan=3, sticky="nsew")

        # Create window option tab as frame
        self.window_option = customtkinter.CTkFrame(self)
        self.window_option.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.window_option.grid_rowconfigure((0, 1), weight=1)
        # Create and place 'Reset Calculation' button
        self.reset_calculation_button = customtkinter.CTkButton(
            master=self.window_option,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            fg_color="#CC0000",
            hover_color="#990000",
            text="Reset calculation",
            command=self.reset_calculation_click
        )
        self.reset_calculation_button.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
        # Create and place 'Show Receipt' button
        self.show_receipt_button = customtkinter.CTkButton(
            self.window_option,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            fg_color="#00B300",
            hover_color="#006700",
            text="Show receipt",
            command=self.show_receipt_click,
        )
        self.show_receipt_button.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

    def add_product_click(self):
        pass

    def reset_calculation_click(self):
        pass

    def show_receipt_click(self):
        pass

    def add_new_product(self):
        pass

    def show_receipt(self):
        pass