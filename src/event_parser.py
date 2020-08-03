class EventOrdersPoliciesParser:
    def __init__(self, event):
        print(event)
        record = event.get("dynamodb").get("NewImage")
        customer_event = record.get("customer").get("M")
        
        self.customer = Customer(customer_event)
        self.order_policy_id = event.get(
            "dynamodb").get("Keys").get("order_policy_id").get("S")

        self.age_policy = record.get("age_policy").get("BOOL")
        self.commitment_policy = record.get("commitment_policy").get("BOOL")
        self.active = record.get("active").get("BOOL")
        self.score_policy = record.get("score_policy").get("BOOL")
        self.timestamp = record.get("timestamp").get("S")

        self.order_policy_id = event.get(
            "dynamodb", {}).get("Keys").get("order_policy_id").get("S")


class Customer:
    def __init__(self, event):
        self.income = event.get("income").get("S", {})
        self.amount = event.get("amount").get("S", {})
        self.birthdate = event.get("birthdate").get("S", {})
        self.terms = event.get("terms").get("N", {})
        self.name = event.get("name").get("S", {})
        self.cpf = event.get("cpf").get("S", {})
        self.processing_status = event.get("processing_status").get("S", {})
        self.active = event.get("active").get("BOOL", {})
        self.customer_id = event.get("customer_id").get("S", {})
        self.age = event.get("age").get("N", {})
        self.processing_result = event.get("processing_result").get("S", {})
        self.timestamp = event.get("timestamp").get("S", {})
