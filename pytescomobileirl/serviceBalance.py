from datetime import datetime

class ServiceBalance:

    def __init__(self, addon_data):
        serviceBundle = addon_data["serviceBundle"]
        self.balance_type = serviceBundle["type"]
        self.unit = serviceBundle["unit"]
        self.is_active = serviceBundle["status"] == "ACTIVE"
        self.remaining_balance = addon_data["balance"]

        if addon_data["expiryDate"] is not None:
            self.balance_expires = datetime.strptime(addon_data["expiryDate"], "%d-%b-%Y %H:%M")
        else:
            self.balance_expires = None

    def days_remaining(self):
        now = datetime.now()
        return int(round(((self.__balance_expires) - now).days))