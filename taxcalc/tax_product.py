class TaxProduct:

    def __init__(self, name: str, quantity: int, price: float, basic_tax: int, import_state: bool):
        # self.id = id,
        self.name: str = name
        self.quantity: int = quantity
        self.price: float = price
        self.basic_tax: int = basic_tax
        self.import_sate: bool = import_state

    def getProductInformation(self):
        return {
            # "product_id": self.id,
            "product_name": self.name,
            "product_quantity": self.quantity,
            "product_price": self.price,
            "product_basic_tax": self.basic_tax,
            "product_import_state": self.import_sate
        }
