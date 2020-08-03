from dynamo_handler import OrdersPoliciesTable, CustomerTable, ProposalTable
import json



def lambda_handler(event, context):
    print(event)
    try:
        customer_id = event.get("params").get("querystring", {})["id"]
        print(customer_id)

        table = CustomerTable()
        customer = table.get_customer(customer_id)
        if not customer:
            return {
                "status": 400,
                "message": "user not found"
            }
        print(customer)

        table = ProposalTable()
        proposal = table.get_proposal_by_customer_id(customer_id)
        print(proposal)
        refuser_policy = customer.get("refused_policies")
        res = {
                "statusCode": 200,
                "headers": {"Content-Type":"application/json"},
                "isBase64Encoded": False,
                "body": {
                    "id": customer_id,
                    "status": customer.get("processing_status"),
                    "result": customer.get("processing_result"),
                    "refused_policy": refuser_policy if refuser_policy else None,
                    "amount": str(proposal.get("amount")),
                    "terms": str(proposal.get("approved_terms"))
                }
            }
        print(res)
        return str(res)

    except Exception as e: 
        print(e)
        return {
            "status": 500
        }

