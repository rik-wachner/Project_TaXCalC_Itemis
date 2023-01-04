# test of tax_controller.py
import pytest

import taxcalc.tax_product as product


##############
# Test Cases #
##############

###
# __init__()
###
@pytest.mark.parametrize(
    "product_information",
    [
        {
            "product_name": "gum",
            "product_quantity": 1,
            "product_price": 3.44,
            "product_basic_tax": 0,
            "product_import_state": False
        },
        {
            "product_name": "note",
            "product_quantity": 2,
            "product_price": 1.49,
            "product_basic_tax": 0,
            "product_import_state": True
        },
        {
            "product_name": "book",
            "product_quantity": 1,
            "product_price": 19.00,
            "product_basic_tax": 0,
            "product_import_state": True
        },
        {
            "product_name": "book 2",
            "product_quantity": 1,
            "product_price": 9.99,
            "product_basic_tax": 10,
            "product_import_state": True
        },
        {
            "product_name": "cheese",
            "product_quantity": 4,
            "product_price": 4.44,
            "product_basic_tax": 10,
            "product_import_state": False
        },
        {
            "product_name": "book 3",
            "product_quantity": 9,
            "product_price": 21.95,
            "product_basic_tax": 10,
            "product_import_state": True
        }
    ]
)
def test___init__(product_information):
    """
    TEST: T 1
    Test if the __init___ method of TaxProduct can take the following attributes:
    'name', 'quantity', 'price', 'basic_tax', and 'import_state'
    """
    new_product = product.TaxProduct(
        name=product_information["product_name"],
        quantity=product_information["product_quantity"],
        price=product_information["product_price"],
        basic_tax=product_information["product_basic_tax"],
        import_state=product_information["product_import_state"]
    )
    assert isinstance(new_product, product.TaxProduct)


###
# get_product_information()
###
@pytest.mark.parametrize(
    "product_information",
    [
        {
            "product_name": "perfume",
            "product_quantity": 2,
            "product_price": 18.99,
            "product_basic_tax": 2,
            "product_import_state": False
        },
        {
            "product_name": "headache pills",
            "product_quantity": 5,
            "product_price": 9.75,
            "product_basic_tax": 10,
            "product_import_state": True
        },
        {
            "product_name": "chocolate box",
            "product_quantity": 2,
            "product_price": 19.00,
            "product_basic_tax": 10,
            "product_import_state": True
        },
        {
            "product_name": "music CD",
            "product_quantity": 1,
            "product_price": 14.99,
            "product_basic_tax": 10,
            "product_import_state": True
        },
        {
            "product_name": "bottle of wine",
            "product_quantity": 4,
            "product_price": 7.44,
            "product_basic_tax": 10,
            "product_import_state": False
        },
        {
            "product_name": "book",
            "product_quantity": 1,
            "product_price": 11.11,
            "product_basic_tax": 10,
            "product_import_state": False
        }
    ]
)
def test_get_product_information(product_information):
    """
    TEST: T 2
    Test if the getter method get_product_information() returns the information of a product in the following structure:
    product_information: dict = {
            "product_name": <the product name>,
            "product_quantity": <the product quantity>,
            "product_price": <the product price>,
            "product_basic_tax": <the product basic tax rate>,
            "product_import_state": <the product import state>
        }
    """
    new_product = product.TaxProduct(
        name=product_information["product_name"],
        quantity=product_information["product_quantity"],
        price=product_information["product_price"],
        basic_tax=product_information["product_basic_tax"],
        import_state=product_information["product_import_state"]
    )
    assert isinstance(new_product, product.TaxProduct)
    assert new_product.get_product_information() == product_information
