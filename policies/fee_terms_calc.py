


def parse_event(event):
    items = event.get("Records", {})[0]
    
    # lambda functions throw syntax error when I break lines 
    terms =  items.get("dynamodb", {}).get("NewImage", {}).get("M", {}).get("terms", {}).get("N", 0)
    amount =  items.get("dynamodb", {}).get("NewImage", {}).get("M", {}).get("amount", {}).get("S", 0)
    customer_id = event.get("Records", {})[0].get("dynamodb", {}).get("Keys").get("customer_id").get("S")

    return terms, amount, customer_id

def fee_calc(terms, score, amount):
    terms_options = [6, 9, 12]
    fee_tb = {
        "600": [6.4, 6.6, 6,9],
        "700": [5.5, 5.8, 6.1],
        "800": [4.7, 5.0, 5.3],
        "900": [3.9, 4.2, 4.5],
    }

    term_i = terms_options.index(terms)

    if score >= 900:
        return fee_tb.get("900")[term_i]
    if score >= 800:
        return fee_tb.get("800")[term_i]
    if score >= 700:
        return fee_tb.get("700")[term_i]
    if score >= 600:
        return fee_tb.get("600")[term_i]

def instalment_calc(terms, amount, fee)
    instalment_value = amount * ((((1 + fee)** terms) * fee) / (((1 + fee)** terms) - fee))

    return instalment_value


def lambda_handler(event, context):
    terms, amount, customer_id = parse_event(event)
    
    fee = fee_calc(terms, score, amount)
    print(event)