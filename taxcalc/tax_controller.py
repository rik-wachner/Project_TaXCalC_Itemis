#from taxcalc.tax_error_handling import TaxBaseError @TODO Add error handling class later
from taxcalc.tax_product import TaxProduct


class TaxController:
    def __init__(self, view: any):
        self.view = view
        self.taxProducts: list[TaxProduct] = []

        # Add reference to UI to get user events
        self.view.add_controller_listener(self)

    @staticmethod
    def _check_product_information(product_information: dict):
        pass

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
            # @ TODO Inform UI about change
        except Exception as err:
            pass

    def calculate_receipt(self, a, b):
        pass

    def calculate_total(self) -> dict:
        pass

    def reset_calculation(self):
        pass