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
        pass

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

    def calculate_receipt(self, a, b):
        pass

    def calculate_total(self) -> dict:
        pass

    def reset_calculation(self):
        self.taxProducts = []
        self.view.reset_calculation()
