from boto3.dynamodb.conditions import Key, Attr
from dynamo_handler import OrdersPoliciesTable

import requests
import boto3
import json


def post_score_api(cpf):
        url = "https://challenge.noverde.name/score"

        payload = f'{{"cpf": "{cpf}"}}'
        headers = {
            'x-api-key': "c6V1j6vt1o88Emj7xxsms3ItCwyDxFR68i7DexMb",
            'content-type': "application/json",
            'cache-control': "no-cache"
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        result = json.loads(response.text)
        print("RESULT", result)
        return result.get("score", 0)

def check_score(score):
    return False if score < 600 else True


def parse_event(event):
    items = event.get("Records", {})[0]
    
    # lambda functions throw syntax error when I break lines 
    cpf =  items.get("dynamodb", {}).get("NewImage", {}).get("customer", {}).get("M", {}).get("cpf", {}).get("S", {})
    order_policy_id = event.get("Records", {})[0].get("dynamodb", {}).get("Keys").get("order_policy_id").get("S")

    return cpf, order_policy_id


def lambda_handler(event, context, customer_id=None):
    print(event)
    print(context)

    cpf, order_policy_id = parse_event(event)

    score = post_score_api(cpf)
    score_validated = check_score(score)

    print(score, score_validated)

    table = OrdersPoliciesTable()
    table.update_order_policy_attr(attr="score_policy", 
                                     order_policy_id=order_policy_id, 
                                     value=score_validated)
    table.update_order_policy_attr(attr="score", 
                                     order_policy_id=order_policy_id, 
                                     value=score)


    return(event)
    

if __name__ == "__main__":
    print(post_score_api('12345678901'))
