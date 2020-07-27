from boto3.dynamodb.conditions import Key, Attr
from dynamo_handler import OrdersPoliciesTable

import requests
import boto3
import json


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
        print("RESULT", result)
        return result.get("commitment", 0)

def calc_commitment(commitment, terms, income, amount):
    instalment_value = float(amount)/int(terms)
    commitment_income = float(commitment) * float(income)

    valid = False if instalment_value > commitment_income else True  

    return valid, instalment_value, commitment, commitment_income


def parse_event(event):
    items = event.get("Records", {})[0]
    
    # lambda functions throw syntax error when I break lines 
    cpf =  items.get("dynamodb", {}).get("NewImage", {}).get("customer", {}).get("M", {}).get("cpf", {}).get("S", {})
    income =  items.get("dynamodb", {}).get("NewImage", {}).get("customer", {}).get("M", {}).get("income", {}).get("S", {})
    amount =  items.get("dynamodb", {}).get("NewImage", {}).get("customer", {}).get("M", {}).get("amount", {}).get("S", {})
    terms =  items.get("dynamodb", {}).get("NewImage", {}).get("customer", {}).get("M", {}).get("terms", {}).get("N", {})
    order_policy_id = event.get("Records", {})[0].get("dynamodb", {}).get("Keys").get("order_policy_id").get("S")

    return cpf, income, amount, terms, order_policy_id


def lambda_handler(event, context, customer_id=None):
    print(event)
    print(context)

    cpf, income, amount, terms, order_policy_id = parse_event(event)

    commitment = post_commitment_api(cpf)
    
    commitment_check, instalment_value, commitment, commitment_income = calc_commitment(commitment, terms, income, amount)


    table = OrdersPoliciesTable()
    table.update_order_policy_attr(attr="commitment_policy", 
                                     order_policy_id=order_policy_id, 
                                     value=commitment_check)
    table.update_order_policy_attr(attr="commitment", 
                                     order_policy_id=order_policy_id, 
                                     value=str(commitment))
    table.update_order_policy_attr(attr="commitment_income", 
                                     order_policy_id=order_policy_id, 
                                     value=str(commitment_income))
    table.update_order_policy_attr(attr="instalment_value", 
                                     order_policy_id=order_policy_id, 
                                     value=str(instalment_value))


    return(str(event))
    

if __name__ == "__main__":
    print(post_score_api('12345678901'))
