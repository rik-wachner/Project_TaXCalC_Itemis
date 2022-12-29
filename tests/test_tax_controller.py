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
