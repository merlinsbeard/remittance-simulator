# Mayannah

Simulates a remittance transaction

## Installation

Requirements:

* Postgresql container named mayannah-db

```bash
$ git clone <repo>
$ cd mayannah
$ docker build -t mayannah:latest .
# link to a postgresql container
$ docker run --name mayannah --link mayannah-db -d mayannah:latest
# Create a superuser
$ docker exec -it mayannah python manage.py createsuperuser
# open in browser 
# http://localhost:8000
```

## Usage

### Environment Variables

Mayannah uses the file `prod.env` for its environment variable. Edit as needed

| Name | Description |
|------|-------------|
| DATABASE_URL | Configuration for Database |
| SENTRY | DSN of sentry |

Reference:

[Django Environ](https://github.com/joke2k/django-environ)
[Sentry](https://sentry.io/)



### Admin Page

`http://localhost:8000/admin/`

Admin Page is used to create Users, It can also create, edit, and view Remittance records.

### API

#### Authentication

*Basic Authentication* is required for all API calls. All users with login credentials can access the API. 

Use Admin page to create a User.

#### Create Remittance

`POST /v1/remittance`

fields:

|name | type | description|
|---------|---------|----------------|
|source_reference_number| string | required |
| remitter| person | required person details|
|beneficiary | person | required person details|
|payout_amount| integer | required |
|payout_currency | string | required |



**Person**

|name |type | description |
|---------|---------|-----------------|
|first_name| string | required |
|last_name| string | required |
|address | string | optional |
| country | string | optional or it defaults to Philippines|
|contact_number| string | optional|


Request:

```json
{
	"source_reference_number": "remittance-quatro",
	"remitter": {
		"first_name": "remi",
		"last_name": "ter",
		"address": "Manila",
		"country": "Philippines"
	},
	"beneficiary": {
		"first_name": "beni",
		"last_name": "ficiary",
		"contact_number": "555000668899",
		"address": "",
		"country": "Philippines",
		"identification_type": "SSS",
		"identification_id": "55552222111"
	},
	"payout_amount": 500000,
	"payout_currency": "PH"
	
}
```

Response

```json
{
	"source_reference_number": "remittance-quatro",
	"slug": "remittance-quatro",
	"remitter": {
		"first_name": "remi",
		"last_name": "ter",
		"contact_number": "",
		"address": "Manila",
		"country": "Philippines",
		"identification_type": "",
		"identification_id": ""
	},
	"beneficiary": {
		"first_name": "beni",
		"last_name": "ficiary",
		"contact_number": "555000668899",
		"address": "",
		"country": "Philippines",
		"identification_type": "SSS",
		"identification_id": "55552222111"
	},
	"payout_amount": 500000,
	"payout_currency": "PH",
	"status": "AVAILABLE"
}
```


#### List Remittance

List all Remittance

`GET /v1/remittance`

Response:

```json
[
	{
		"source_reference_number": "remittance-uno",
		"slug": "remittance-uno",
		"remitter": {
			"first_name": "remi",
			"last_name": "ter",
			"contact_number": "",
			"address": "Manila",
			"country": "Philippines",
			"identification_type": "",
			"identification_id": ""
		},
		"beneficiary": {
			"first_name": "beni",
			"last_name": "ficiary",
			"contact_number": "555000668899",
			"address": "",
			"country": "Philippines",
			"identification_type": "SSS",
			"identification_id": "55552222111"
		},
		"payout_amount": 50000,
		"payout_currency": "PH",
		"status": "PAID"
	},
	{
		"source_reference_number": "remittance-dos",
		"slug": "remittance-dos",
		"remitter": {
			"first_name": "remi",
			"last_name": "ter",
			"contact_number": "",
			"address": "Manila",
			"country": "Philippines",
			"identification_type": "",
			"identification_id": ""
		},
		"beneficiary": {
			"first_name": "beni",
			"last_name": "ficiary",
			"contact_number": "555000668899",
			"address": "",
			"country": "Philippines",
			"identification_type": "SSS",
			"identification_id": "55552222111"
		},
		"payout_amount": 500000,
		"payout_currency": "PH",
		"status": "AVAILABLE"
	},
	{
		"source_reference_number": "remittance-tres",
		"slug": "remittance-tres",
		"remitter": {
			"first_name": "remi",
			"last_name": "ter",
			"contact_number": "",
			"address": "Manila",
			"country": "Philippines",
			"identification_type": "",
			"identification_id": ""
		},
		"beneficiary": {
			"first_name": "beni",
			"last_name": "ficiary",
			"contact_number": "555000668899",
			"address": "",
			"country": "Philippines",
			"identification_type": "SSS",
			"identification_id": "55552222111"
		},
		"payout_amount": 1000,
		"payout_currency": "PH",
		"status": "AVAILABLE"
	}
]
```

#### List Remittance Details

Returns a dictionary of the detail of a specific remittance

`GET /v1/remittance/<remittance_slug>/`

Parameter


| Name | Type | Description |
|:-------:|:--------:|:-------------:|
|remittance_slug| string | slug of remittance transaction. Can be seen during create remittance. |

Response:

```json
{
	"source_reference_number": "remittance-dos",
	"slug": "remittance-dos",
	"remitter": {
		"first_name": "remi",
		"last_name": "ter",
		"contact_number": "",
		"address": "Manila",
		"country": "Philippines",
		"identification_type": "",
		"identification_id": ""
	},
	"beneficiary": {
		"first_name": "beni",
		"last_name": "ficiary",
		"contact_number": "555000668899",
		"address": "",
		"country": "Philippines",
		"identification_type": "SSS",
		"identification_id": "55552222111"
	},
	"payout_amount": 500000,
	"payout_currency": "PH",
	"status": "AVAILABLE"
}

```


#### Pay Remittance

Updates the status of remittance record to PAID. Only available transactions can be PAID.

`POST /v1/remittance/<remittance_slug>/pay`

Inputs:

|Name|Type|Description|
|--------|--------|----------------|
|source_reference_number| string | required|

Request:

```json
{
	"source_reference_number": "remittance-quatro"
}
```

Response:

```json
{
	"message": "Successfully Tagged as Paid"
}
```


Curl:

```
curl --request POST \
  --url http://localhost:8000/v1/remittance/remittance-quatro/pay/ \
  --header 'authorization: Basic Ymo6aWRvbnRrbm93MTI=' \
  --header 'content-type: application/json' \
  --data '{"source_reference_number": "remittance-quatro"}'
```
