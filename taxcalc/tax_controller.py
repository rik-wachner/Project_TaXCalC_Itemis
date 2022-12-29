from taxcalc.tax_error_handling import TaxBaseError
from taxcalc.tax_product import TaxProduct


class TaxController:
    def __init__(self, view: any):
        self.view = view
        self.taxProducts: list[TaxProduct] = []

        # Add reference to UI to get user events
        self.view.add_controller_listener(self)

    @staticmethod
    def _check_product_information(product_information: dict):
        """
        Check the content of the given product information with the following structure:

        product_information: dict = {
            "product_name": <the product name>,
            "product_quantity": <the product quantity>,
            "product_price": <the product price>,
            "product_basic_tax": <the product basic tax rate>,
            "product_import_state": <the product import state>
        }

        :param product_information: Map with the required product information to check against
        :type product_information: dict
        :return: None or raised TaxBaseError exception
        :rtype: None or a TaxBaseError exception object
        """

        def __check_missing_content():
            """
            Check if the product information content contains missing entries ("" or NULL) in the following structure:
            :return: None or raised TaxBaseError exception
            :rtype: None or a TaxBaseError exception object
            """
            product_information_values = product_information.values()
            if None in product_information_values or "" in product_information_values:
                raise TaxBaseError("Input fields cannot be empty! Like the product name, quantity or price")

        def __check_product_name(product_name: str):
            """
            Check if the product name contains less than 50 chars. If exceeded, an error is thrown
            :param product_name: Product name
            :type product_name: str
            :return: None or raised TaxBaseError exception
            :rtype: None or a TaxBaseError exception object
            """
            if len(product_name) > 50:
                raise TaxBaseError("Product name is to long (max 50 characters)")

        def __check_product_quantity(product_quantity: int):
            """
            Check whether the product quantity is greater than 0 and less than 99. If exceeded, an error is thrown
            :param product_quantity: Product quantity
            :type product_quantity: int
            :return: None or raised TaxBaseError exception
            :rtype: None or a TaxBaseError exception object
            """
            if product_quantity < 1:
                raise TaxBaseError("Product quantity cannot be zero (0) or negative (-1, -2, ...)")

            if product_quantity > 99:
                raise TaxBaseError("Product quantity cannot be greater then ninety-nine (> 99)")

        def __check_product_price(product_price: float):
            """
            Check if the product price is greater than 0. If exceeded and negative, an error is thrown
            :param product_price: Product price
            :type product_price: float
            :return: None or raised TaxBaseError exception
            :rtype: None or a TaxBaseError exception object
            """
            if product_price <= 0:
                raise TaxBaseError("Product price cannot be zero (0) or negative (-1, -2, ...)")

            # No ruling for a limit price range -> dangerous because of MAX_INTEGER values in the calculation
            # if product_price > ?:
            #    raise TaxBaseError("Product price cannot be greater then ? (> ?)")

        # Check 1
        __check_missing_content()
        # Check 2
        __check_product_name(product_information["product_name"])
        # Check 3 with cast str -> int
        __check_product_quantity(int(product_information["product_quantity"]))
        # Check 4 with cast str -> int
        __check_product_price(float(product_information["product_price"]))

    @staticmethod
    def _round_tax(tax_number: float, solution_calc_engine: str = "t4z") -> float:
        """
        Round a given tax float to the nearest 0.05 base by a chosen solution engine

        Engine 1 by myself -> solution_calc_engine: str = "rik"
        Engine 2 by t4z -> solution_calc_engine: str = "t4z"
        Engine 3 by john -> solution_calc_engine: str = "john"

        :param tax_number: taxed value as float
        :type tax_number: float
        :param solution_calc_engine: chosen solution engine to round the tax number
        :type solution_calc_engine: str
        :return: rounded tax number
        :rtype: float
        """

        def __round_decimal_by_rik(float_number: float) -> float:
            """
            Round decimal number to the nearest base by myself :)
            :param float_number: float tax number to round to the nearest 0.05
            :type float_number: float
            :return: rounded tax float
            :rtype: float
            """
            rounded_float_number = round(float_number, 2)
            integer_string, decimal_string = f"{rounded_float_number:.2f}".split(".")
            decimal_up_rounding_condition = int(decimal_string[1])
            diff_to_add = 0
            if 0 < decimal_up_rounding_condition < 5:
                diff_to_add = 5 - decimal_up_rounding_condition  # calculate diff to 5
            elif decimal_up_rounding_condition > 5:
                diff_to_add = 10 - decimal_up_rounding_condition  # calculate diff to 10
            # Add diff (if nessesary) to rounded number
            rounded_float_number += float(f"0.0{diff_to_add}")
            return rounded_float_number

        def __round_decimal_by_t4z(decimal_number: float) -> float:
            """
            Round decimal number to the nearest base by 't4z' on Stack Overflow
            Profile: https://stackoverflow.com/users/3380169/t4z
            Thread: https://stackoverflow.com/questions/37825909/round-python-decimal-to-nearest-0-05
            Note: This is not the best solution because -> 423.10 -> 423.15
            :param decimal_number: decimal number to round to the nearest base
            :type decimal_number: float
            :return: rounded tax float
            :rtype: float
            """
            from decimal import Decimal, ROUND_UP
            round_decimal = Decimal("0.05") * (Decimal(decimal_number) / Decimal("0.05")).quantize(
                1,
                rounding=ROUND_UP
            )
            return float(round_decimal)

        def __round_decimal_by_john(decimal_number: float) -> float:
            """
            Round float number to the nearest base by 'John Au-Yeung' on The Web Dev
            Profile: https://thewebdev.info/author/admin/
            Thread: https://thewebdev.info/2022/02/06/how-to-round-up-to-the-nearest-0-05-in-javascript/
            :param decimal_number: decimal number to round to the nearest base
            :type decimal_number: float
            :return: rounded tax float
            :rtype: float
            """
            import math
            # With this line the function can be fixed for decimal_values like 0.555555 or 0.05555
            # decimal_number = round(decimal_number, 2)
            calculated_number = round(math.ceil(decimal_number * 20) / 20, 2)
            return calculated_number

        round_tax_solutions: dict = {
            "rik": __round_decimal_by_rik,
            "t4z": __round_decimal_by_t4z,
            "john": __round_decimal_by_john
        }
        engine_function = round_tax_solutions.get(solution_calc_engine, "Invalid Engine")
        return round(engine_function(tax_number), 2)

    def add_product(self, product_information: dict):
        """
        Adds a new product to the receipt with the following structure:

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
        try:
            self._check_product_information(product_information)
            new_product: TaxProduct = TaxProduct(
                name=str(product_information["product_name"]),
                quantity=int(product_information["product_quantity"]),
                price=float(product_information["product_price"]),
                basic_tax=int(product_information["product_basic_tax"]),
                import_state=bool(product_information["product_import_state"])
            )
            self.taxProducts.append(new_product)
            # new_product.getProductInformation() == product_information
            self.view.display_new_record(new_product.getProductInformation())
        except TaxBaseError as tax_base_exception:
            self.view.error_handling(message=str(tax_base_exception))
        # Inappropriate argument value (of correct type)
        except ValueError as buildin_value_error:
            self.view.error_handling(message=str(buildin_value_error))

    def calculate_receipt(self):
        receipt = self.calculate_total()
        self.view.show_receipt(receipt)

    def calculate_total(self) -> dict:
        """
        Calculating the total cost of the items and the total amounts of sales taxes

        The rounding rules for sales tax are that for a tax rate of n%,
        a shelf price of p contains (np/100 rounded up to the nearest 0.05)
        amount of sales tax.

        tax = n*p/100; for a tax rate of n% and a price of p

        :return:
        :rtype: dict
        """
        product_calculation_info = {}
        total_sales_tax = 0.0
        total = 0.0
        for index, product in enumerate(self.taxProducts):
            product_name = getattr(product, "name")
            product_price = getattr(product, "price")
            product_quantity = getattr(product, "quantity")
            basic_tax = getattr(product, 'basic_tax')
            import_state = getattr(product, 'import_sate')
            tax = basic_tax + (5 if import_state else 0)
            # The rounding rules for sales tax are that for a tax
            # rate of n%, a shelf price of p contains (np/100 rounded up to the nearest 0.05) amount of
            # sales tax.
            product_tax = tax * product_price / 100
            rounded_tax_value = self._round_tax(tax_number=product_tax, solution_calc_engine="rik")
            product_taxed_price = round(((product_price + rounded_tax_value) * product_quantity), 2)
            # print("TAX RATE:", tax)
            # print(f"TAX FEE: {product_tax} -> {rounded_tax_value}")
            # print(f"PRODUCT PRICE: {product_price} -> {product_tax_price}")
            total_sales_tax += rounded_tax_value * product_quantity
            total += product_taxed_price
            # Add product to dict for ui data transfer
            product_calculation_info[index] = {
                "product_name": product_name,
                "import_state": import_state,
                "quantity": product_quantity,
                "taxed_price": product_taxed_price
            }
        receipt_calculation = {
            "receipt_total": {
                "sales_tax": round(total_sales_tax, 2),
                "total": round(total, 2)
            },
            "products": product_calculation_info
        }
        print(receipt_calculation)
        return receipt_calculation

    def reset_calculation(self):
        self.taxProducts = []
        self.view.reset_calculation()
