import json
import requests

from dynamo_handler import OrdersPoliciesTable, ProposalTable, CustomerTable
from event_parser import EventOrdersPoliciesParser



def post_commitment_api(cpf):
    url = "https://challenge.noverde.name/commitment"

    payload = f'{{"cpf": "{cpf}"}}'
    headers = {
        'x-api-key': "c6V1j6vt1o88Emj7xxsms3ItCwyDxFR68i7DexMb",
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    result = json.loads(response.text)
    return result.get("commitment", 0)


def calc_commitment(commitment, income, instalment_value):
    commitment_income = float(commitment) * float(income)
    remaining_income = float(income) - commitment_income


    valid = False if instalment_value > remaining_income else True
    return valid


def instalment_calc(terms, amount, fee):
    terms = int(terms)
    amount = float(amount)
    fee = fee / 100.0


    divider = (((1 + fee)** terms) * fee)
    dividend = (((1 + fee)** terms) - fee)

    terms_value = amount * (divider / dividend)

    return terms_value


def calc_terms(score, commitment, terms, income, amount):
    fee_tb = {
        "600": [6.4, 6.6, 6,9],
        "700": [5.5, 5.8, 6.1],
        "800": [4.7, 5.0, 5.3],
        "900": [3.9, 4.2, 4.5],
    }


    terms = int(terms)
    
    terms_options = [6, 9, 12]
    for i in terms_options:
        score_option = f"{str(score)[0]}00"
        term_option = terms_options.index(i)
        fee = fee_tb[score_option][term_option]
        instalment_value = instalment_calc(i, amount, fee)
        is_valid = calc_commitment(commitment, income, instalment_value)

        return is_valid, instalment_value, fee, i


def format_customer(customer):
    customer["amount"] = str(customer["amount"])
    customer["income"] = str(customer["income"])
    customer["timestamp"] = str(customer["timestamp"])
    customer["terms"] = str(customer["terms"])
    customer["age"] = str(customer["age"])

    return customer


def commitment_hander(event, customer):
    
    commitment = post_commitment_api(customer.cpf)

    commitment_validation = False
    instalment_value = "NULL"

    if customer.score > 600:
        commitment_validation, \
        instalment_value, fee, approved_terms = calc_terms(score=customer.score,
                                                           terms=customer.terms,
                                                           commitment=commitment,
                                                           income=customer.income,
                                                           amount=customer.amount)


    orders_policies_tb = OrdersPoliciesTable()
    orders_policies_tb.update_order_policy_attr(attr="commitment_policy",
                                                order_policy_id=event.order_policy_id,
                                                value=commitment_validation)
    orders_policies_tb.update_order_policy_attr(attr="commitment",
                                                order_policy_id=event.order_policy_id,
                                                value=str(commitment))
    orders_policies_tb.update_order_policy_attr(attr="instalment_value",
                                                order_policy_id=event.order_policy_id,
                                                value=str(instalment_value))
    
    if commitment_validation:
        table = CustomerTable()
        customer = table.get_customer(customer.customer_id)
        customer = format_customer(customer)

        proposal_tb = ProposalTable()
        proposal_tb.put_proposal(customer=customer, 
                                fee=fee, 
                                terms_value=instalment_value, 
                                amount=customer.get("amount"),
                                approved_terms=approved_terms)
    

    return(str(event))


# if __name__ == "__main__"
