#from taxcalc.tax_error_handling import TaxBaseError @TODO Add error handling class later
from taxcalc.tax_product import TaxProduct


class TaxController:
    def __init__(self, view: any):
        self.view = view
        self.taxProducts: list[TaxProduct] = []

    @staticmethod
    def _check_product_information(product_information: dict):
        pass

    @staticmethod
    def _round_tax(tax_number: float, solution_calc_engine: str = "t4z") -> float:
        pass

    def add_product(self, product_information: dict):
        pass

    def calculate_receipt(self):
        pass

    def calculate_total(self) -> dict:
        pass

    def reset_calculation(self):
        pass