
# Noverde Application

As credenciais de acesso foram enviadas no corpo do e-mail


## Post /loan/
https://jpcievtp9l.execute-api.us-east-2.amazonaws.com/prod/loan
### payload:
	{
		"name": "String",
		"cpf": "String",
		"birthdate": "String",
		"amount": "Decimal",
		"terms": "integer",
		"income": "Decimal"
	}

### exemplo em curl:
substituir {AccessKey}

	curl -X POST \
	  https://jpcievtp9l.execute-api.us-east-2.amazonaws.com/prod/loan \
	  -H 'Accept: application/json' \
	  -H 'Authorization: AWS4-HMAC-SHA256 Credential={AccessKey}/20200803/us-east-2/execute-api/aws4_request, SignedHeaders=accept;cache-control;content-length;content-type;host;postman-token;x-amz-date, Signature=c5950c303463a62f1a912cae762e8e5af89784c42b6bb342518148f7d300e1c4' \
	  -H 'Content-Length: 120' \
	  -H 'Content-Type: application/json' \
	  -H 'Host: jpcievtp9l.execute-api.us-east-2.amazonaws.com' \
	  -H 'Postman-Token: 217a2502-b222-4a48-8b0e-0f017bb71cf4' \
	  -H 'X-Amz-Date: 20200803T064911Z' \
	  -H 'cache-control: no-cache' \
	  -d '{
		"name": "postman",
		"cpf": "12345678901",
		"birthdate": "29/04/1994",
		"amount": 4000,
		"terms": 6,
		"income": 8000
	}'

## Get /loan/:id


### exemplo em curl:
substituir {AccessKey}

	curl -X GET \
	  'https://jpcievtp9l.execute-api.us-east-2.amazonaws.com/prod/loan?id=706f6537-d555-11ea-91c5-1b3f57961fde' \
	  -H 'Authorization: AWS4-HMAC-SHA256 Credential={AccesKey}/20200803/us-east-2/execute-api/aws4_request, SignedHeaders=cache-control;content-type;host;postman-token;x-amz-date, Signature=027377b50f82cca02df769f305a30f0218ed04e2aaa19b5ad15ea18f7c1562ba' \
	  -H 'Content-Type: application/json' \
	  -H 'Host: jpcievtp9l.execute-api.us-east-2.amazonaws.com' \
	  -H 'Postman-Token: d8f3dfe6-8f00-40e2-bede-d1e0266132e4' \
	  -H 'X-Amz-Date: 20200803T182519Z' \
	  -H 'cache-control: no-cache'
