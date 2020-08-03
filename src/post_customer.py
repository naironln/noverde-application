from payload_parser import PayloadParser
from dynamo_handler import CustomerTable, OrdersPoliciesTable

import json
import boto3


dynamodb = boto3.resource('dynamodb')

costumers_table = dynamodb.Table('Customers')

def lambda_handler(event, context):
    parser = PayloadParser(event)
    parsed_customer = parser.parse()
    print(parsed_customer)

    CustomerTable().put_customer(parsed_customer)
    OrdersPoliciesTable().put_order_policy(parsed_customer)

    
    return str({
        "status": 200,
        "uuid": parsed_customer.get("customer_id")
    })
