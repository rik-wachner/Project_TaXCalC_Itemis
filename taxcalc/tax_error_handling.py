from abc import ABC


class TaxBaseError(ABC, Exception):
    def __init__(self, error_code: str = "TAX-e000", message: str = ""):
        """
        Initialize a TaxBaseError Exception object
        :param error_code: Error code for a specific error/exception
        :type error_code: str
        :param message: The message should be written in either the developer's native language or English (optional)
        :type message: str
        """
        self.error_code = error_code
        self.message = message
        # self.timestamp = datetime.now()

    def __str__(self):
        return f"[{self.error_code}]: {self.message}"
        # return f"{self.message} ({self.timestamp})"

# Better approach to do this with fixed defined error codes, but for a small not necessary
# class TaxProductNameError(TaxBaseError) + attribute error_code = X
# class TaxProductQuantityError(TaxBaseError) + attribute error_code = X+1
# ... + + attribute error_code = X+...
