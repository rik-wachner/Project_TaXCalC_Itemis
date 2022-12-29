from taxcalc.tax_error_handling import TaxBaseError
from taxcalc.tax_product import TaxProduct


class TaxController:
    def __init__(self, width: int, height: int, language_code: str):
        pass

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