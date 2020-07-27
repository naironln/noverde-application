from boto3.dynamodb.conditions import Key, Attr
from dynamo_handler import OrdersPoliciesTable, CustomerTable

import boto3


def parse_event(event):
    items = event.get("Records", {})[0]
    
    # lambda functions throw syntax error when I break lines 
    customer_id =  items.get("dynamodb", {}).get("NewImage", {}).get("customer", {}).get("M", {}).get("customer_id", {}).get("S", {})
    order_policy_id = event.get("Records", {})[0].get("dynamodb", {}).get("Keys").get("order_policy_id").get("S")

    return customer_id, order_policy_id


def resolve_policies(order_policy_id, customer_id):
    table = OrdersPoliciesTable()
    is_complete, result, policies = table.check_all_policies(order_policy_id)
    print("RESOLVER", is_complete, result, policies)
    table = CustomerTable()
    if is_complete:
        table.update_customer_attr(attr="processing_status",
                                   customer_id=customer_id,
                                   value="completed")
        table.update_customer_attr(attr="processing_result",
                                   customer_id=customer_id,
                                   value=result)

        if result == "refused":
            refused_policy = policies.remove(True)
            table.update_customer_attr(attr="refused_policy",
                                    customer_id=customer_id,
                                    value=refused_policy)

def lambda_handler(event, context, customer_id=None):
    print(event)
    print(context)

    items = event.get("Records", {})[0]
    age =  items.get("dynamodb", {}).get("NewImage", {}).get("customer", {}).get("M", {}).get("age", {}).get("N", {})
    
    customer_id, order_policy_id = parse_event(event)
    print(age)
    age_validation = False if int(age) < 18 else True

    table = OrdersPoliciesTable()
    table.update_order_policy_attr(attr="age_policy", 
                                   order_policy_id=order_policy_id, 
                                   value=age_validation)
    resolve_policies(order_policy_id, customer_id)




    return(str(event))
    

# if __name__ == "__main__":
#     customer_id = 'c4a58dd6-ce05-11ea-8cd1-454726804912'

#     lambda_handler(customer_id)
