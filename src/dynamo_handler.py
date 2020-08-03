from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
import boto3
import uuid
import json


class DynamoHandler:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')


class CustomerTable(DynamoHandler):
    def __init__(self):
        super().__init__()
        self.customer_table = self.dynamodb.Table('Customers')


    def get_approval(self, customer_id):
        customer = self.get_customer(customer_id)

        processing_result = customer.get("processing_result")
        return True if processing_result == "approved" else False
    
    
    def get_customer(self, customer_id):

        customer = self.customer_table.get_item(Key={
                    "customer_id": customer_id
                    }).get("Item", {})

        return customer

    
    def update_customer_attr(self, attr, customer_id, value):
        response = self.customer_table.update_item(
            Key={
                'customer_id': customer_id
            },
            UpdateExpression=f'SET {attr} = :attr',
            ConditionExpression="customer_id = :customer_id",
            ExpressionAttributeValues={
                ':attr': value,
                ':customer_id': customer_id
            }
        )
    

    def put_customer(self, customer):
        cpf = customer.get('cpf') \
                      .replace(".", "") \
                      .replace("-", "")

        items = self.customer_table.scan(
            FilterExpression=Attr('cpf').eq(cpf)
        ).get('Items', [])

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
        # item = self.get_order_policy(order_policy_id)

        response = self.orders_policies_table.update_item(
            Key={
                'order_policy_id': order_policy_id
            },
            UpdateExpression=f'SET {attr} = :attr',
            ConditionExpression="order_policy_id = :order_policy_id",
            ExpressionAttributeValues={
                ':attr': value,
                ':order_policy_id': order_policy_id
            }
        )
        return response

    def get_order_policy_by_customer_id(self, customer_id):
        order_policy = self.orders_policies_table.scan(
            FilterExpression=Attr('customer_id').eq(customer_id)
        ).get('Items', [])[-1]

        return order_policy


    def get_order_policy(self, order_policy_id):
        response = self.orders_policies_table.get_item(Key={
            "order_policy_id": order_policy_id
            })                
        return response.get("Item")


    def check_all_policies(self, order_policy_id):
        response = self.orders_policies_table.get_item(Key={
            "order_policy_id": order_policy_id
            })
        age_policy = response.get("Item", {}).get("age_policy")
        score_policy = response.get("Item", {}).get("score_policy")
        commitment_policy = response.get("Item", {}).get("commitment_policy")
        policies = [age_policy, score_policy, commitment_policy]


        is_complete = False if "NULL" in policies else True
        result = "refused" if False in policies or "NULL" in policies else "approved"

        return is_complete, result, policies


    def put_order_policy(self, customer):

        order_policy_id = str(uuid.uuid1())
        order_policy = {
            "order_policy_id": order_policy_id,
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


    def put_proposal(self, customer, fee, terms_value, amount, approved_terms):
        proposal = {
            "proposal_id": str(uuid.uuid1()),
            "customer_id": customer.get("customer_id"),
            "customer": json.dumps(customer),
            "fee": str(fee),
            "terms_value": str(terms_value),
            "approved_terms": approved_terms,
            "amount": str(amount),
            "active": True,
            "timestamp": str(datetime.now().timestamp()),
        }   

        return self.proposal_table.put_item(Item=proposal)

    
    def get_proposal_by_customer_id(self, customer_id):
        proposal = self.proposal_table.scan(
            FilterExpression=Attr('customer_id').eq(customer_id)
        ).get("Items", {})
        if proposal:
            return proposal[-1]
        
        return proposal

