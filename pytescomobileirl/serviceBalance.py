from datetime import datetime

class ServiceBalance:

    def __init__(self, basic_data, adv_data):
        self.balance_type = adv_data["type"]
        self.is_active = adv_data["status"] == "ACTIVE"
        self.serviceCode = adv_data["serviceCode"]

        if basic_data["expiryDate"] is not None:
            self.balance_expires = datetime.strptime(basic_data["expiryDate"], "%d-%b-%Y %H:%M")
        else:
            self.balance_expires = None

    def days_remaining(self):
        now = datetime.now()
        return int(round(((self.__balance_expires) - now).days))

class GenericBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = adv_data["unit"]
        ServiceBalance.__init__(self, basic_data, adv_data)

class DataBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = "MB"
        ServiceBalance.__init__(self, basic_data, adv_data)

class VoiceBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = "Mins"
        ServiceBalance.__init__(self, basic_data, adv_data)

class TextBalance(ServiceBalance):

    def __init__(self, basic_data, adv_data):
        self.unit = "Msgs"
        ServiceBalance.__init__(self, basic_data, adv_data)
