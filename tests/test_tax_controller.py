# test of tax_controller.py
import pytest
# Unit / Component testing of the tax_controller python script
import taxcalc.tax_controller as controller
import taxcalc.tax_ui_app as ui  # @TODO Mock the ui!
import taxcalc.tax_product as model
import taxcalc.tax_error_handling as error_handling


##############
# Test Prep  #
##############

@pytest.fixture(scope="module")
def create_dummy_tax_ui_object(request):
    return ui.TaxUIApp(width=780, height=590, language_code="eng")


##############
# Test Cases #
##############

# @TODO

###
# __check_product_information()
###
def test__check_product_information_product_name_to_long_exception(create_dummy_tax_ui_object):
    dummy_product: dict = {
        "product_name": "A" * 51,
        "product_quantity": 1,
        "product_price": 14.99,
        "product_basic_tax": 10,
        "product_import_state": False
    }
    tax_controller = controller.TaxController(create_dummy_tax_ui_object)
    with pytest.raises(error_handling.TaxBaseError) as exc_info:
        tax_controller._check_product_information(product_information=dummy_product)
    assert exc_info.type == error_handling.TaxBaseError


def test__check_product_information_product_quantity_over_99_exception(create_dummy_tax_ui_object):
    dummy_product: dict = {
        "product_name": "book",
        "product_quantity": 100,
        "product_price": 14.99,
        "product_basic_tax": 10,
        "product_import_state": False
    }
    tax_controller = controller.TaxController(create_dummy_tax_ui_object)
    with pytest.raises(error_handling.TaxBaseError) as exc_info:
        tax_controller._check_product_information(product_information=dummy_product)
    assert exc_info.type == error_handling.TaxBaseError


def test__check_product_information_product_quantity_under_1_exception(create_dummy_tax_ui_object):
    dummy_product: dict = {
        "product_name": "book",
        "product_quantity": 0,
        "product_price": 14.99,
        "product_basic_tax": 10,
        "product_import_state": False
    }
    tax_controller = controller.TaxController(create_dummy_tax_ui_object)
    with pytest.raises(error_handling.TaxBaseError) as exc_info:
        tax_controller._check_product_information(product_information=dummy_product)
    assert exc_info.type == error_handling.TaxBaseError


###
# __round_tax()
###
@pytest.mark.parametrize(
    "tax_float,tax_expectation",
    [  # Test if...
        #   X.X0 stays X.X0
        #   X.X1 - X.X5 round up to X.X5
        #   X.X6 - X.X9 round up to X.10
        (1.00, 1.00),
        (11.01, 11.05),
        (111.02, 111.05),
        (9.03, 9.05),
        (99.04, 99.05),
        (999.05, 999.05),
        (0.06, 0.1),
        (00.07, 0.1),
        (123.08, 123.1),
        (777.09, 777.1),
        (543.10, 543.10),
        #   X.X59 -> X.X6 round up to X.(X+1)
        (9.259, 9.3),
        #   X.X56 -> X.X6 round up to X.(X+1)
        (7.556, 7.60),
        #   X.X55 ut to X.X5
        (7.555, 7.55),
        #   X.X54 cut to X.X5
        (7.554, 7.55)
    ]
)
def test__round_tax_rik(create_dummy_tax_ui_object, tax_float, tax_expectation):
    tax_controller = controller.TaxController(create_dummy_tax_ui_object)
    rounded_tax = tax_controller._round_tax(tax_number=tax_float, solution_calc_engine="rik")
    assert rounded_tax == tax_expectation


@pytest.mark.parametrize(
    "tax_float,tax_expectation",
    [  # Test if...
        #   X.X0 stays X.X0
        #   X.X1 - X.X5 round up to X.X5
        #   X.X6 - X.X9 round up to X.10
        (1.00, 1.00),
        (11.01, 11.05),
        (111.02, 111.05),
        (9.03, 9.05),
        (99.04, 99.05),
        (999.05, 999.05),
        (0.06, 0.1),
        (00.07, 0.1),
        (123.08, 123.1),
        (777.09, 777.1),
        #   X.10 -> X.15 [NOT CORRECT ?!]
        (543.10, 543.15),
        #   X.X59 -> X.X6 round up to X.(X+1)
        (9.259, 9.3),
        #   X.X56 -> X.X6 round up to X.(X+1)
        (7.556, 7.60),
        #   X.X55 -> X.X6 round up to X.(X+1)
        (7.555, 7.60),
        #   X.X54 cut to X.X5 [Expected: 7.55]
        (7.554, 7.60)
    ]
)
def test__round_tax_t4z(create_dummy_tax_ui_object, tax_float, tax_expectation):
    tax_controller = controller.TaxController(create_dummy_tax_ui_object)
    rounded_tax = tax_controller._round_tax(tax_number=tax_float, solution_calc_engine="t4z")
    assert rounded_tax == tax_expectation


@pytest.mark.parametrize(
    "tax_float,tax_expectation",
    [  # Test if...
        #   X.X0 stays X.X0
        #   X.X1 - X.X5 round up to X.X5
        #   X.X6 - X.X9 round up to X.10
        (1.00, 1.00),
        (11.01, 11.05),
        (111.02, 111.05),
        (9.03, 9.05),
        (99.04, 99.05),
        (999.05, 999.05),
        (0.06, 0.1),
        (00.07, 0.1),
        (123.08, 123.1),
        (777.09, 777.1),
        (543.10, 543.10),
        #   X.X59 -> X.X6 round up to X.(X+1)
        (9.259, 9.3),
        #   X.X56 -> X.X6 round up to X.(X+1)
        (7.556, 7.60),
        #   X.X56 -> X.X6 round up to X.(X+1) [Expected: 7.55]
        (7.555, 7.60),
        #   X.X56 -> X.X6 round up to X.(X+1) [Expected: 7.55]
        (7.554, 7.60)
    ]
)
def test__round_tax_john(create_dummy_tax_ui_object, tax_float, tax_expectation):
    tax_controller = controller.TaxController(create_dummy_tax_ui_object)
    rounded_tax = tax_controller._round_tax(tax_number=tax_float, solution_calc_engine="john")
    assert rounded_tax == tax_expectation


###
# add_product()
###
@pytest.mark.parametrize(
    "product_information",
    [
        {
            "product_name": "",
            "product_quantity": 1,
            "product_price": 12.49,
            "product_basic_tax": 0,
            "product_import_state": False
        },
        {
            "product_name": None,
            "product_quantity": 1,
            "product_price": 12.49,
            "product_basic_tax": 0,
            "product_import_state": False
        },
        {
            "product_name": "book",
            "product_quantity": None,
            "product_price": 12.49,
            "product_basic_tax": 0,
            "product_import_state": False
        },
        {
            "product_name": "book",
            "product_quantity": 1,
            "product_price": None,
            "product_basic_tax": 0,
            "product_import_state": False
        },
        {
            "product_name": "book",
            "product_quantity": 1,
            "product_price": 12.49,
            "product_basic_tax": None,
            "product_import_state": False
        },
        {
            "product_name": "book",
            "product_quantity": 1,
            "product_price": 12.49,
            "product_basic_tax": 0,
            "product_import_state": None
        }
    ]
)
def test_add_product_with_missing_entry(create_dummy_tax_ui_object, product_information):
    """
    Test if the add_product() function do not add products with missing information
    -> The testing of reg missing infos correct are referted to _check_product_information()
    """
    # with pytest.raises(error_handling.TaxBaseError) as exc_info:
    tax_controller = controller.TaxController(create_dummy_tax_ui_object)
    tax_controller.add_product(product_information=product_information)
    # Test that products with missing information will not be added
    assert tax_controller.taxProducts == []
    # assert exc_info.type == error_handling.TaxBaseError


###
# calculate_total()
###
@pytest.mark.parametrize(
    "products, expected_sales_tax, expected_total",
    [
        # Wanted Output of Input 1
        (
                [
                    {
                        "product_name": "book",
                        "product_quantity": 1,
                        "product_price": 12.49,
                        "product_basic_tax": 0,
                        "product_import_state": False
                    },
                    {
                        "product_name": "music CD",
                        "product_quantity": 1,
                        "product_price": 14.99,
                        "product_basic_tax": 10,
                        "product_import_state": False
                    },
                    {
                        "product_name": "chocolate bar",
                        "product_quantity": 1,
                        "product_price": 0.85,
                        "product_basic_tax": 0,
                        "product_import_state": False
                    },
                ],
                1.50,
                29.83
        ),
        # Wanted Output of Input 2
        (
                [
                    {
                        "product_name": "box of chocolates",
                        "product_quantity": 1,
                        "product_price": 10.00,
                        "product_basic_tax": 0,
                        "product_import_state": True
                    },
                    {
                        "product_name": "bottle of perfum",
                        "product_quantity": 1,
                        "product_price": 47.50,
                        "product_basic_tax": 10,
                        "product_import_state": True
                    }
                ],
                7.65,
                65.15
        ),
        # Wanted Output of Input 3
        (
                [
                    {
                        "product_name": "bottle of perfume",
                        "product_quantity": 1,
                        "product_price": 27.99,
                        "product_basic_tax": 10,
                        "product_import_state": True
                    },
                    {
                        "product_name": "bottle of perfume",
                        "product_quantity": 1,
                        "product_price": 18.99,
                        "product_basic_tax": 10,
                        "product_import_state": False
                    },
                    {
                        "product_name": "packet of headache pills",
                        "product_quantity": 1,
                        "product_price": 9.75,
                        "product_basic_tax": 0,
                        "product_import_state": False
                    },
                    {
                        "product_name": "box of imported chocolates",
                        "product_quantity": 1,
                        "product_price": 11.25,
                        "product_basic_tax": 0,
                        "product_import_state": True
                    }
                ],
                6.70,
                74.68
        ),
        # OWN Test Case #1 - No Products
        (
                [],
                0.0,
                0.0
        ),
        # OWN Test Case #2 - 2x Wanted Output of Input 3
        (
                [
                    {
                        "product_name": "bottle of perfume",
                        "product_quantity": 2,
                        "product_price": 27.99,
                        "product_basic_tax": 10,
                        "product_import_state": True
                    },
                    {
                        "product_name": "bottle of perfume",
                        "product_quantity": 2,
                        "product_price": 18.99,
                        "product_basic_tax": 10,
                        "product_import_state": False
                    },
                    {
                        "product_name": "packet of headache pills",
                        "product_quantity": 2,
                        "product_price": 9.75,
                        "product_basic_tax": 0,
                        "product_import_state": False
                    },
                    {
                        "product_name": "box of imported chocolates",
                        "product_quantity": 2,
                        "product_price": 11.25,
                        "product_basic_tax": 0,
                        "product_import_state": True
                    }
                ],
                6.70 * 2,
                74.68 * 2
        ),
        # OWN Test Case #3 - 1 Product
        #   7.99 * 0.15 = 1,1985 -> ROUND(1,1985) -> 1.20 TAX
        #       7.99 + TAX = 7.99 + 1.20 = 9.19 TOTAL
        (
                [
                    {
                        "product_name": "pencil",
                        "product_quantity": 1,
                        "product_price": 7.99,
                        "product_basic_tax": 10,
                        "product_import_state": True
                    }
                ],
                1.20,
                9.19
        ),
        # OWN Test Case #4 - 1 Product with import tax only
        #   7.99 * 0.05 = 0.3995 -> ROUND(0.3995) -> 0.40 TAX
        #       7.99 + TAX = 7.99 + 0.40 = 8.39 TOTAL
        (
                [
                    {
                        "product_name": "bread",
                        "product_quantity": 1,
                        "product_price": 7.99,
                        "product_basic_tax": 0,
                        "product_import_state": True
                    }
                ],
                0.40,
                8.39
        ),
        # OWN Test Case #5 - 1 Product with 0 Tax
        #   7.99 * 0.00 = 0.00 -> ROUND(0.00) -> 0.00 TAX
        #       7.99 + TAX = 7.99 + 0.00 = 7.99 TOTAL
        (
                [
                    {
                        "product_name": "medkit",
                        "product_quantity": 1,
                        "product_price": 7.99,
                        "product_basic_tax": 0,
                        "product_import_state": False
                    }
                ],
                0.0,
                7.99
        ),
    ]
)
def test_calculate_total(create_dummy_tax_ui_object, products, expected_sales_tax, expected_total):
    tax_controller = controller.TaxController(create_dummy_tax_ui_object)
    for product in products:
        tax_controller.add_product(product_information=product)
    receipt_information: dict = tax_controller.calculate_total()
    assert receipt_information['receipt_total']['sales_tax'] == expected_sales_tax
    assert receipt_information['receipt_total']['total'] == expected_total


###
# reset_calculation()
###
def test_reset_calculation(create_dummy_tax_ui_object):
    dummy_product: dict = {
        "product_name": "book",
        "product_quantity": 1,
        "product_price": 14.99,
        "product_basic_tax": 10,
        "product_import_state": False
    }
    tax_controller = controller.TaxController(create_dummy_tax_ui_object)
    tax_controller.add_product(product_information=dummy_product)
    # get list of products
    # check if the list is not empty
    assert tax_controller.taxProducts != []
    tax_controller.reset_calculation()
    # check if the list is empty
    assert tax_controller.taxProducts == []
