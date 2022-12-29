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
        # self.language_code = language_code @TODO Add language support later
        # set connected controller to None in init
        self.connected_controller = None

        def __set_treeview_columns(treeview: tkinter.ttk.Treeview, column_names: dict):
            column_names_keys = column_names.keys()
            # Using tuple() for unpacking dictionary keys into tuple
            treeview['columns'] = tuple(column_names_keys)  # var refs
            # ("product_name", "product_quantity", "product_price", "product_import_state")

            # Formate / "remove" the treeview index columns
            treeview.column("#0", width=0, stretch="no")

            # Formatting the Heading and the Column for each name
            for key in column_names_keys:
                treeview.heading(key, text=column_names[key])
                treeview.column(key, anchor="w", width=120)

        # configure window
        self.title("TaXCalC")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # configure grid layout (3x2)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # Receipt input field
        self.treeview = tkinter.ttk.Treeview(self, show="headings")
        self.treeview.grid(row=0, column=0, columnspan=4, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # Set the Table columns to the TaxProduct language
        __set_treeview_columns(
            self.treeview,
            {
                # "product_id": "ID",
                "product_name": "Product",
                "product_quantity": "Quantity (Unit)",
                "product_price": "Price ($)",
                "product_basic_tax": "Tax (%)",
                "product_import_state": "Imported",
            }
        )

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

    def __clear_input_fields(self):
        """
        For a better usability, the function clears all used input fields
        :return: None
        :rtype: None
        """
        self.product_name.delete(0, "end")
        self.product_quantity.delete(0, "end")
        self.product_price.delete(0, "end")
        self.import_checkbox.deselect()

    def add_controller_listener(self, controller: TaxController):
        """
        Register a controller to be able to pass click events and information
        :param controller: Controller for managing the data transfer between ui and data
        :type controller: TaxController
        :return: None
        :rtype: None
        """
        self.connected_controller = controller

    def add_product_click(self):
        """
        Function gets called after the 'Add Product' button were pressed
        and adds a new product with the information in the input fields
        :return: None
        :rtype: None
        """
        chosen_basic_tax_option = self.basic_tax.get()
        basic_tax = 0
        # position_of_tax_translation = tax_translation.index(chosen_basic_tax_option)
        if chosen_basic_tax_option == "10%":
            basic_tax = 10
        self.add_new_product(
            product_name=self.product_name.get(),
            product_quantity=self.product_quantity.get(),
            product_price=self.product_price.get(),
            product_basic_tax=basic_tax,
            product_import_state=bool(self.import_checkbox.get())
        )
        self.__clear_input_fields()

    def reset_calculation_click(self):
        self.connected_controller.reset_calculation()

    def show_receipt_click(self):
        pass

    def add_new_product(
            self,
            product_name: str,
            product_quantity: int,
            product_price: float,
            product_basic_tax: int,
            product_import_state: bool
    ):
        """
        Calls the tax controller to add a product with the given information
        :param product_name: Product name
        :type product_name: str
        :param product_quantity: Quantity of that product
        :type product_quantity: int
        :param product_price: Price of that product
        :type product_price: float
        :param product_basic_tax: The chosen basic tax rate (either 0 or 10)
        :type product_basic_tax: int
        :param product_import_state: Indicates if the product were imported and need the 5% import duty
        :type product_import_state: bool
        :return: None
        :rtype: None
        """
        product_information: dict = {
            "product_name": product_name,
            "product_quantity": product_quantity,
            "product_price": product_price,
            "product_basic_tax": product_basic_tax,
            "product_import_state": product_import_state
        }
        self.connected_controller.add_product(product_information)

    def reset_calculation(self):
        """
        Delete each element in the treeview and clear the ui input fields as a reset
        :return: None
        :rtype: None
        """
        # List of all elements in the tree view
        for record in self.treeview.get_children():
            self.treeview.delete(record)
        self.__clear_input_fields()

    def display_new_record(self, product_information: dict):
        """
        Add the new product record to the treeview table

        The information of the product has the following structure:

        product_information: dict = {
            "product_name": <the product name>,
            "product_quantity": <the product quantity>,
            "product_price": <the product price>,
            "product_basic_tax": <the product basic tax rate>,
            "product_import_state": <the product import state>
        }

        :param product_information: Map with the required product information to create a new TaxProduct object
        :type product_information: dict
        :return: None
        :rtype: None
        """
        # Visual Change
        #   > For the UI, change 'True' / 'False' to 'YES' / 'NO' (eng version)
        product_import_state_word = "YES" if product_information["product_import_state"] else "NO"

        # Add the new record to the treeview widget in the ui
        self.treeview.insert(
            parent='',
            index='end',
            text='',
            values=(
                product_information["product_name"],
                product_information["product_quantity"],
                product_information["product_price"],
                product_information["product_basic_tax"],
                product_import_state_word
            )
        )
        self.__clear_input_fields()

    def show_receipt(self):
        pass
