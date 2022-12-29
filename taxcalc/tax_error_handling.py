from abc import ABC


# from datetime import datetime


class TaxBaseError(ABC, Exception):
    def __init__(self, message):
        self.message = message
        # self.timestamp = datetime.now()

    def __str__(self):
        return f"{self.message}"
        # return f"{self.message} ({self.timestamp})"

# class TaxProductNameError(TaxBaseError)
# class TaxProductQuantityError(TaxBaseError)
# ...
