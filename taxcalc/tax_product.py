class TaxProduct:
    """
    Class representing a product in the receipt calculation
    """
    def __init__(self, name: str, quantity: int, price: float, basic_tax: int, import_state: bool):
        """
        Initialize a TaxProduct object
        :param name: Name of the product
        :type name: str
        :param quantity: Quantity of the product
        :type quantity: int
        :param price: Price of the product
        :type price: float
        :param basic_tax: The basic tax rate (either 0'%' or 10'%') of the product
        :type basic_tax: int
        :param import_state: Indication whether the product was imported (True) and therefore requires the 5% import duty
        :type import_state: bool
        """
        # self.id = id,
        self.name: str = name
        self.quantity: int = quantity
        self.price: float = price
        self.basic_tax: int = basic_tax
        self.import_sate: bool = import_state

    ##################
    # Public Methods #
    ##################

    def get_product_information(self) -> dict:
        """
        Product information getter with the following structure:

        product_information: dict = {
            "product_name": <the product name>,
            "product_quantity": <the product quantity>,
            "product_price": <the product price>,
            "product_basic_tax": <the product basic tax rate>,
            "product_import_state": <the product import state>
        }

        :return: Product information
        :rtype: dict
        """
        return {
            # "product_id": self.id,
            "product_name": self.name,
            "product_quantity": self.quantity,
            "product_price": self.price,
            "product_basic_tax": self.basic_tax,
            "product_import_state": self.import_sate
        }
