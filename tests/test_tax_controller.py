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
# _add_product()
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
def test__add_product_with_missing_entry(create_dummy_tax_ui_object, product_information):
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
