from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from boto3 import *
import boto3
import uuid

class DynamoHandler:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')


class CustomerTable(DynamoHandler):
    def __init__(self):
        super().__init__()
        self.customer_table = self.dynamodb.Table('Customers')


    def get_approval(self, customer_id):

        item = self.customer_table.get_item(Key={
                    "customer_id": customer_id
                    }).get("Item", {})

        processing_result = item.get("processing_result")
        is_approved if processing_result == "approved"
        
        return True

    
    def update_customer_attr(self, attr, customer_id, value):
        print("ATTR", attr, customer_id, value)
        response = self.customer_table.update_item(
            Key={
                'customer_id': customer_id
            },
            UpdateExpression=f'SET {attr} = :attr',
            ExpressionAttributeValues={
                ':attr': value
            }
        )
    

    def put_customer(self, customer):
        cpf = customer.get('cpf') \
                      .replace(".", "") \
                      .replace("-", "")

        items = self.customer_table.scan(
            FilterExpression=Attr('cpf').eq(cpf)
        ).get('Items', [])

        print('CPFFF',items)
        items = sorted(items, key=lambda k: k['timestamp']) 

        if items and customer.get('active'):
            previous_record = items[-1]
            response = self.customer_table.update_item(
                Key={
                    'customer_id': previous_record.get('customer_id')
                },
                UpdateExpression='SET active = :active',
                ExpressionAttributeValues={
                    ':active': False
                }
            )

        return self.customer_table.put_item(Item=customer)


class OrdersPoliciesTable(DynamoHandler):
    def __init__(self):
        super().__init__()
        self.orders_policies_table = self.dynamodb.Table('OrdersPolicies')


    def update_order_policy_attr(self, attr, order_policy_id, value):
        response = self.orders_policies_table.update_item(
            Key={
                'order_policy_id': order_policy_id
            },
            UpdateExpression=f'SET {attr} = :attr',
            ExpressionAttributeValues={
                ':attr': value
            }
        )

    
    def check_all_policies(self, order_policy_id):
        response = self.orders_policies_table.get_item(Key={
            "order_policy_id": order_policy_id
            })
        age_policy = response.get("Item", {}).get("age_policy")
        score_policy = response.get("Item", {}).get("score_policy")
        commitment_policy = response.get("Item", {}).get("commitment_policy")
        policies = [age_policy, score_policy, commitment_policy]

        print(policies)

        is_complete = False if None in policies else True
        result = "refused" if False in policies else "approved"

        return is_complete, result, policies


    def put_order_policy(self, customer):

        # print(response)

        order_policy = {
            "order_policy_id": str(uuid.uuid1()),
            "customer_id": customer.get("customer_id"),
            "customer": customer,
            "age_policy": "NULL",
            "score_policy": "NULL",
            "commitment_policy": "NULL",
            "active": True,
            "timestamp": str(datetime.now().timestamp()),
        }   

        return self.orders_policies_table.put_item(Item=order_policy)


class ProposalTable(DynamoHandler):
    def __init__(self):
        super().__init__()
        self.proposal_table = self.dynamodb.Table('Proposal')


    def put_proposal(self, customer, fee, terms_value, amount):
        proposal = {
            "proposal_id": str(uuid.uuid1()),
            "customer_id": customer.get("customer_id"),
            "customer": customer,
            "fee": fee,
            "terms_value": terms_value,
            "amount": amount,
            "active": True,
            "timestamp": str(datetime.now().timestamp()),
        }   

        return self.orders_policies_table.put_item(Item=order_policy)