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
        self.language_code = language_code

        # set connected controller to None in init
        self.connected_controller = None

        # Load language pack
        self.product_lan_inf = TaxUIApp.getProductLanguageInformation(self.language_code)

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
        self.title(self.product_lan_inf["app_title"])
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
        __set_treeview_columns(self.treeview, self.product_lan_inf["table_headline"])

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
            text=f"{self.product_lan_inf['product_input_fields']['product_name_label']}:",
            font=customtkinter.CTkFont(size=12)
        )
        self.product_name_label.grid(row=0, column=0, padx=10, pady=10)
        # Product Name
        #   -> input field
        self.product_name = customtkinter.CTkEntry(
            self.tax_input_frame,
            placeholder_text=self.product_lan_inf['product_input_fields']['product_name_input_label']
        )
        self.product_name.grid(row=0, column=1, padx=(10, 20), pady=10, columnspan=2, sticky="nsew")
        # Product Quantity
        #   -> label
        self.product_quantity_label = customtkinter.CTkLabel(
            self.tax_input_frame,
            text=f"{self.product_lan_inf['product_input_fields']['product_quantity_label']}:",
            font=customtkinter.CTkFont(size=12)
        )
        self.product_quantity_label.grid(row=1, column=0, padx=10, pady=10)
        #   -> input field
        self.product_quantity = customtkinter.CTkEntry(
            self.tax_input_frame,
            placeholder_text=self.product_lan_inf['product_input_fields']['product_quantity_input_label']
        )
        self.product_quantity.grid(row=1, column=1, padx=(10, 20), pady=10, columnspan=2, sticky="nsew")
        # Product Price
        #   -> label
        self.product_price_label = customtkinter.CTkLabel(
            self.tax_input_frame,
            text=f"{self.product_lan_inf['product_input_fields']['product_price_label']}:",
            font=customtkinter.CTkFont(size=12)
        )
        self.product_price_label.grid(row=2, column=0, padx=10, pady=10)
        #   -> input field
        self.product_price = customtkinter.CTkEntry(
            self.tax_input_frame,
            placeholder_text=self.product_lan_inf['product_input_fields']['product_price_input_label']
        )
        self.product_price.grid(row=2, column=1, padx=(10, 20), pady=10, columnspan=2, sticky="nsew")
        # Product Tax -> Tax Rate
        #   -> label
        self.basic_tax_label = customtkinter.CTkLabel(
            self.tax_input_frame,
            text=f"{self.product_lan_inf['product_input_fields']['product_basic_tax_label']}:",
            font=customtkinter.CTkFont(size=12)
        )
        self.basic_tax_label.grid(row=3, column=0, padx=10, pady=10)
        #   -> input field
        self.basic_tax = customtkinter.CTkOptionMenu(
            self.tax_input_frame,
            dynamic_resizing=True,
            # > First Option: 0%
            # > Second Option: 10%
            values=self.product_lan_inf['product_input_fields']['product_basic_tax_input_labels']
        )
        self.basic_tax.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        # Product Tax -> Import Tax Rate
        #   -> label + input field
        self.import_checkbox = customtkinter.CTkCheckBox(
            master=self.tax_input_frame,
            text=self.product_lan_inf['product_input_fields']['product_import_checkbox_label']
        )
        self.import_checkbox.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
        # Create and place 'Add Product' button
        self.add_product_button = customtkinter.CTkButton(
            master=self.tax_input_frame,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            text=self.product_lan_inf['buttons']['add_product'],
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
            text=self.product_lan_inf['buttons']['reset_calculation'],
            command=self.__reset_calculation_click
        )
        self.reset_calculation_button.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
        # Create and place 'Show Receipt' button
        self.show_receipt_button = customtkinter.CTkButton(
            self.window_option,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            fg_color="#00B300",
            hover_color="#006700",
            text=self.product_lan_inf['buttons']['show_receipt'],
            command=self.__show_receipt_click,
        )
        self.show_receipt_button.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # create segmented button for loading examples in
        self.load_example_button = customtkinter.CTkSegmentedButton(
            master=self,
            values=[
                self.product_lan_inf['examples']['example_1'],
                self.product_lan_inf['examples']['example_2'],
                self.product_lan_inf['examples']['example_3']
            ],
            command=self.__load_example_click
        )
        self.load_example_button.grid(row=2, column=0, columnspan=4, padx=(20, 20), pady=(0, 20), sticky="nsew")

    @staticmethod
    def getProductLanguageInformation(language: str) -> dict:
        language_packs = {
            "eng": {
                "app_title": "TaXCalC",
                "table_headline": {
                    # "product_id": "ID",
                    "product_name": "Product",
                    "product_quantity": "Quantity (Unit)",
                    "product_price": "Price ($)",
                    "product_basic_tax": "Tax (%)",
                    "product_import_state": "Imported",
                },
                "product_input_fields": {
                    "product_name_label": "Product Name",
                    "product_name_input_label": "Enter product name ...",
                    "product_quantity_label": "Quantity",
                    "product_quantity_input_label": "Enter product quantity ...",
                    "product_price_label": "Price",
                    "product_price_input_label": "Enter product price ...",
                    "product_basic_tax_label": "Tax Rate",
                    "product_basic_tax_input_labels": ["Tax Free (0 %)", "Basic Sales Tax (10 %)"],
                    "product_import_checkbox_label": "Imported",
                },
                "buttons": {
                    "add_product": "Add Product",
                    "reset_calculation": "Reset Calculation",
                    "show_receipt": "Show Receipt"
                },
                "examples": {
                    "example_1": "Load Example 1",
                    "example_2": "Load Example 2",
                    "example_3": "Load Example 3"
                },
                "receipt": {
                    "imported": "imported",
                    "sales_taxes": "Sales Taxes",
                    "total": "Total",
                    "accept": "Close Receipt"
                },
                "error_handling": {
                    "TAX-e000": "Unknown / Undefined error occur",
                    "TAX-e001": "The product name, quantity or price cannot be empty!" + "\n"
                                "Please add some information for the calculation",
                    "TAX-e002": "The product name is to long. Name the product with max 50 characters",
                    "TAX-e003": "The product quantity cannot be zero (0) or negative (-1, -2, ...) for the calculation",
                    "TAX-e004": "The product quantity cannot be greater then ninety-nine (> 99) for the calculation",
                    "TAX-e005": "The product price cannot be zero (0) or negative (-1, -2, ...) for the calculation",
                    "PY-e001": "Check the types of your input!" + "\n"
                               "The quantity or price should be numeric with '.' as decimal point",
                    "accept": "OK"
                },
                "misc": {
                    "product_import_state_choice": ["YES", "NO"]
                }
            },
            "de": {
                "app_title": "TaXCalC",
                "table_headline": {
                    # "product_id": "ID",
                    "product_name": "Produkt",
                    "product_quantity": "Menge (Stk.)",
                    "product_price": "Preis ($)",
                    "product_basic_tax": "Steuer (%)",
                    "product_import_state": "Eingefuehrt",
                },
                "product_input_fields": {
                    "product_name_label": "Produktname",
                    "product_name_input_label": "Produktnamen eingeben ...",
                    "product_quantity_label": "Menge",
                    "product_quantity_input_label": "Produktmenge eingeben ...",
                    "product_price_label": "Preis",
                    "product_price_input_label": "Produktpreis eingeben ...",
                    "product_basic_tax_label": "Steuersatz",
                    "product_basic_tax_input_labels": ["Steuerfrei (0 %)", "Grundumsatzsteuer (10 %)"],
                    "product_import_checkbox_label": "Eingefuehrt",
                },
                "buttons": {
                    "add_product": "Produkt hinzufügen",
                    "reset_calculation": "Berechnung zurücksetzen",
                    "show_receipt": "Quittung anzeigen"
                },
                "examples": {
                    "example_1": "Lade Beispiel 1",
                    "example_2": "Lade Beispiel 2",
                    "example_3": "Lade Beispiel 3"
                },
                "receipt": {
                    "imported": "importierte(s)",
                    "sales_taxes": "Umsatzsteuer",
                    "total": "Gesamt",
                    "accept": "Quittung schließen"
                },
                "error_handling": {
                    "TAX-e000": "Unbekannter Fehler ist aufgetreten",
                    "TAX-e001": "Der Produktname, die Menge oder der Preis dürfen nicht leer sein!" + "\n"
                                "Bitte fuegen Sie die fehlenden Informationen für die Berechnung hinzu",
                    "TAX-e002": "Der Produktname ist zu lang. Benennen Sie das Produkt mit maximal 50 Zeichen",
                    "TAX-e003": "Die Produktmenge darf bei der Berechnung nicht 0 oder negativ (-1, -2, ...) sein",
                    "TAX-e004": "Die Produktmenge kann bei der Berechnung nicht größer als 99 sein",
                    "TAX-e005": "Der Produktpreis kann bei der Berechnung nicht 0 oder negativ (-1, -2, ...) sein.",
                    "PY-e001": "Überprüfen Sie die Art Ihrer Eingabe!" + "\n"
                               "Die Menge oder der Preis sollte numerisch sein mit '.' als Dezimalkomma",
                    "accept": "OK"
                },
                "misc": {
                    "product_import_state_choice": ["JA", "NEIN"]
                }
            }
        }
        return language_packs.get(language, "Invalid Language Code")

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

    def __reset_calculation_click(self):
        self.connected_controller.reset_calculation()

    def __show_receipt_click(self):
        self.connected_controller.calculate_receipt()

    def __load_example_click(self, value):
        self.connected_controller.reset_calculation()
        load_products: list = []
        if value == self.product_lan_inf['examples']['example_1']:
            load_products.append(["book", 1, 12.49, 0, False])
            load_products.append(["music CD", 1, 14.99, 10, False])
            load_products.append(["chocolate bar", 1, 0.85, 0, False])
        elif value == self.product_lan_inf['examples']['example_2']:
            load_products.append(["box of chocolates", 1, 10.00, 0, True])
            load_products.append(["bottle of perfume", 1, 47.50, 10, True])
        elif value == self.product_lan_inf['examples']['example_3']:
            load_products.append(["box of perfume", 1, 27.99, 10, True])
            load_products.append(["bottle of perfume", 1, 18.99, 10, False])
            load_products.append(["headache pills", 1, 9.75, 0, False])
            load_products.append(["chocolates", 1, 11.25, 0, True])

        for product in load_products:
            self.add_new_product(
                product_name=product[0],
                product_quantity=product[1],
                product_price=product[2],
                product_basic_tax=product[3],
                product_import_state=product[4]
            )
        self.load_example_button.set(None)

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
        # Position Map Ruling
        # > POS 0 == First Option: 0%
        # > POS 1 == Second Option: 10%
        tax_translation = self.product_lan_inf['product_input_fields']['product_basic_tax_input_labels']
        position_of_tax_translation = tax_translation.index(chosen_basic_tax_option)
        basic_tax = 0 if position_of_tax_translation == 0 else 10
        self.add_new_product(
            product_name=self.product_name.get(),
            product_quantity=self.product_quantity.get(),
            product_price=self.product_price.get(),
            product_basic_tax=basic_tax,
            product_import_state=bool(self.import_checkbox.get())
        )
        self.__clear_input_fields()

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
        import_state_translation = self.product_lan_inf['misc']['product_import_state_choice']
        product_import_state_word = import_state_translation[0] \
            if product_information["product_import_state"] \
            else import_state_translation[1]

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

    def error_handling(self, error_code: str, alternative_message: str):
        error_message = self.product_lan_inf['error_handling'].get(error_code)
        if error_message:
            self.__show_error_popup_message(message=error_message)
        else:
            self.__show_error_popup_message(message=alternative_message)

    def show_receipt(self, receipt_details: dict):
        message_str = ""
        receipt_total_details = receipt_details["receipt_total"]
        product_details = receipt_details["products"]
        for product in product_details:
            import_statement = (
                    self.product_lan_inf['receipt']['imported'] + " "
            ) if product_details[product]['import_state'] else ""
            message_str += f"{product_details[product]['quantity']}" +\
                           " " \
                           f"{import_statement} {product_details[product]['product_name']}:" +\
                           " " \
                           f"{product_details[product]['taxed_price']}" \
                           + "\n"
        # Add sales tex to string
        message_str += f"{self.product_lan_inf['receipt']['sales_taxes']}: {receipt_total_details['sales_tax']}" + "\n"
        # Add total amount to string
        message_str += f"{self.product_lan_inf['receipt']['total']}: {receipt_total_details['total']}"
        self.__show_receipt_popup_message(message=message_str)

    def __show_error_popup_message(self, message: str):
        # Create a new popup window
        popup_window = customtkinter.CTkToplevel(self)
        popup_window.geometry("500x150")
        popup_window.resizable(False, False)
        popup_window.title(self.product_lan_inf["app_title"])
        popup_window.grab_set()

        # create label on CTkToplevel window
        message_label = customtkinter.CTkLabel(popup_window, text=message)
        message_label.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        accept_button = customtkinter.CTkButton(
            master=popup_window,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            text=self.product_lan_inf['error_handling']['accept'],
            command=popup_window.destroy
        )
        accept_button.pack(padx=20, pady=20)

    def __show_receipt_popup_message(self, message: str):
        # Create a new popup window
        popup_window = customtkinter.CTkToplevel(self)
        popup_window.geometry("700x350")
        popup_window.resizable(False, False)
        popup_window.title(self.product_lan_inf["app_title"])
        popup_window.grab_set()

        # create textbox on CTkToplevel window
        receipt_textbox = customtkinter.CTkTextbox(popup_window)
        # receipt_textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        receipt_textbox.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        # Insert text into the textbox and then disable it
        #   > state="disabled" -> Read Only
        receipt_textbox.insert(index="1.0", text=message)
        receipt_textbox.configure(state="disabled")

        accept_button = customtkinter.CTkButton(
            master=popup_window,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            text=self.product_lan_inf['receipt']['accept'],
            command=popup_window.destroy
        )
        accept_button.pack(padx=20, pady=(10, 20))
