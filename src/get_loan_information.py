from dynamo_handler import OrdersPoliciesTable, CustomerTable, ProposalTable
import json



def lambda_handler(event, context):
    try:
        customer_id = event.get("params").get("querystring", {})["id"]

        table = CustomerTable()
        customer = table.get_customer(customer_id)
        if not customer:
            return {
                "status": 400,
                "message": "user not found"
            }

        table = ProposalTable()
        proposal = table.get_proposal_by_customer_id(customer_id)
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
        return str(res)

    except Exception as e: 
        return {
            "status": 500
        }

