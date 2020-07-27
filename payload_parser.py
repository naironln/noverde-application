import uuid

from datetime import datetime, date
from decimal import Decimal



class PayloadParser:
    def __init__(self, payload):
        self.name = payload.get("name")
        self.cpf = payload.get("cpf")
        self.birthdate = payload.get("birthdate")
        self.amount = payload.get("amount")
        self.terms = payload.get("terms")
        self.income = payload.get("income")
        
        self.age = None
        self.uuid = None
        self.timestamp = None
        self.error_messages = []


    def parse(self):
        try:
            self.parse_cpf()
            self.parse_age_birthdate()
            self.parse_amount()
            self.parse_income()
            self.validate_terms()
            self.get_timestamp()
            self.get_customer_id()

            return {
                "customer_id": str(self.uuid),
                "name": self.name,
                "cpf": self.cpf,
                "birthdate": str(self.birthdate),
                "age": self.age,
                "amount": str(self.amount),
                "terms": self.terms,
                "income": str(self.income),
                "timestamp": str(self.timestamp),
                "status": "processing",
                "active": True,
                "result": "NULL",
            }

        except Exception as e:
            print(e)
    
    def error(self, message):
        self.error_messages.append(message)


    def get_customer_id(self):
        self.uuid = uuid.uuid1()


    def get_timestamp(self):
        now = datetime.now()
        self.timestamp = now.timestamp()


    def parse_cpf(self):
        try:
            self.cpf = self.cpf.replace(".", "").replace("-", "")

            if len(self.cpf) != 11:
                self.error("invalid cpf")

        except TypeError as e:
            self.error("invalid cpf")
 
    
    def parse_age_birthdate(self):
        birthdate = datetime.strptime(self.birthdate, "%d/%m/%Y")
        today = date.today()

        age = today.year - birthdate.year - ((today.month, today.day) < \
                                             (birthdate.month, birthdate.day))
        self.birthdate = birthdate
        self.age = age
        

    def parse_amount(self):
        try:
            self.amount = Decimal(self.amount)

        except Exception as e:
            error("amount must be a decimal value")

    def validate_terms(self):
        try:
            self.terms = int(self.terms)

            if self.terms not in [6, 9, 12]:
                self.error("terms must be one of the following options (6, 9, 12)")

        except Exception as e:
            self.error("terms must be an integer")

    def parse_income(self):
        try:
            self.income = Decimal(self.income)

        except Exception as e:
            error("income must be a decimal value")


if __name__ == "__main__":

    payload = {
        "name": "Nairon",
        "cpf": "431.166.898-81",
        "birthdate": "29/04/1994",
        "amount": "4000",
        "terms": "9",
        "income": "8000"
    }
    parser = PayloadParser(payload)
    print(parser.parse())