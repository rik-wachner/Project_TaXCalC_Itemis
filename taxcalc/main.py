from taxcalc.tax_controller import TaxController
from taxcalc.tax_ui_app import TaxUIApp

if __name__ == "__main__":
    # Crate new UI Instance
    #     FIX_WIDTH = 780
    #     FIX_HEIGHT = 520
    tax_ui_app = TaxUIApp(width=780, height=590, language_code="eng") # @TODO: Add Lang Support

    # Create new TaxController Instance
    tax_controller = TaxController(tax_ui_app)

    # Only use 1 Thread for the UI, because the controller do not have other dependencies
    tax_ui_app.mainloop()
    #app = App()
    #app.mainloop()