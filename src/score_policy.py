from boto3.dynamodb.conditions import Key, Attr
from dynamo_handler import OrdersPoliciesTable, CustomerTable
from commitment_handler import commitment_hander
from event_parser import EventOrdersPoliciesParser

import requests
import boto3
import json


def resolve_policies(order_policy_id, customer_id):
    print("RESOLVER")
    table = OrdersPoliciesTable()
    is_complete, result, policies = table.check_all_policies(order_policy_id)
    table = CustomerTable()

    if is_complete:
        print("IS COMPLETE")
        table.update_customer_attr(attr="processing_status",
                                   customer_id=customer_id,
                                   value="completed")
        table.update_customer_attr(attr="processing_result",
                                   customer_id=customer_id,
                                   value=result)

    print("END RESOLVER")


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
        return result.get("score", 0)

def check_score(score):
    return False if score < 600 else True



def lambda_handler(event, context, customer_id=None):
    events = event.get("Records") 

    for event in events:
        if event.get("eventName") == "INSERT":
            order_policy = EventOrdersPoliciesParser(event)
            customer = order_policy.customer

            # cpf, order_policy_id, customer_id = parse_event(order_policy)

            score = post_score_api(customer.cpf)
            is_score_valid = check_score(score)


            table = OrdersPoliciesTable()
            print("FIRST UPDATE")
            table.update_order_policy_attr(attr="score_policy", 
                                            order_policy_id=order_policy.order_policy_id, 
                                            value=is_score_valid)
            print("SECOND UPDATE")
            table.update_order_policy_attr(attr="score", 
                                            order_policy_id=order_policy.order_policy_id, 
                                            value=score)

            customer.score = score
            commitment_hander(order_policy, customer)
            print("COMMITMENT COMPLETE")
            resolve_policies(order_policy.order_policy_id, customer.customer_id)
            print("END DO END")

    return(event)
    

if __name__ == "__main__":
    print(post_score_api('12345678901'))

