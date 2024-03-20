from fastapi import APIRouter, Request
from schemas.pay import Pay, Link
import requests
import json
from config.config import settings

pay = APIRouter()

@pay.post("/payment", response_model=Link, tags=["Pay"])
async def payment(pay: Pay):
    try:
        url_token = settings.PAYPERTIC_URL_AUTH
        payload = settings.PAYLOAD
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        # get token PagoTIC
        res_auth = requests.request("POST", url_token, headers=headers, data=payload)
        if res_auth.status_code != 200:
            return {"msg": "Unauthorized User"}
        
        data = res_auth.json()
        url = settings.PAYPERTIC_URL_HOST+"/pagos"
        payload = json.dumps({
            "currency_id": pay.currency_id,
            "external_transaction_id": pay.external_transaction_id,
            "due_date": pay.due_date,
            "last_due_date": pay.last_due_date,
            "notification_url": settings.HOST_API + "/notification",
            "details": [
                {
                "external_reference": pay.details_external_reference,
                "concept_id": pay.details_concept_id,
                "concept_description": pay.details_concept_description,
                "amount": pay.details_amount
                }
            ],
            "payer": {
                "name": pay.payer_name,
                "email": pay.payer_email,
                "identification": {
                "type": pay.payer_identification_type,
                "number": pay.payer_identification_number,
                "country": pay.payer_identification_country
                }
            }
        })
        
        headers = {
            'Authorization': 'Bearer ' + data['access_token'],
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }
        # request payment PagoTIC
        res_link = requests.request("POST", url, headers=headers, data=payload)
        if res_link.status_code != 200:
            return {"msg": "Invalid Request"}
        
        link = res_link.json()
        return {
            "msg":'OK',
            "id":link["id"],
            "form_url":link["form_url"],
            "final_amount":link["final_amount"],
            "status":link["status"],
            "notification_url":link["notification_url"],
        }
    except Exception as err:
        print(f'error in the process: {err}')
        return { "msg":"Error in the process: "+ err}

@pay.post("/notification", tags=["Pay"])
async def notification(request: Request):
    try:
        # receive notification PagoTIC
        req = await request.body()
        data = json.loads(req)
        print(data)
        if data['status'] == "approved":
            print('-----------------------')
            final_amount = data['final_amount']
            doc_number = data['payer']['identification']['number']
            url_token = settings.ISPCUBE_URL_HOST + "/api/sanctum/token"
            payload = json.dumps({
            "username": settings.USERNAME_ISPCUBE,
            "password": settings.PASSWORD_ISPCUBE
            })
            headers = {
            'login-type': settings.LOGIN_TYPE,
            'client-id': settings.CLIENT_ID_ISPCUBE,
            'api-key': settings.API_KEY,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }
            # get token ISPCube
            res_token = requests.request("POST", url_token, headers=headers, data=payload)
            if res_token.status_code != 200:
                print("Error Token")
                return {"msg": "Error Token"}
        
            data_token = res_token.json()
            customer_search_url = settings.ISPCUBE_URL_HOST + "/api/customer?doc_number=" + doc_number
            payload = {}
            headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'api-key': settings.API_KEY,
            'client-id': settings.CLIENT_ID_ISPCUBE,
            'login-type': settings.LOGIN_TYPE,
            'username': settings.USERNAME_ISPCUBE,
            'Authorization': 'Bearer ' + data_token['token']
            }
            # get client_id ISPCube
            res_client = requests.request("GET", customer_search_url, headers=headers, data=payload)
            if res_client.status_code != 200:
                print("Error search client_id")
                return {"msg": "Error search client_id"}
        
            client = res_client.json()
            url_payment = settings.ISPCUBE_URL_HOST + "/api/cash/payment_save"
            payload = json.dumps({
            "customer_id": client['id'],
            "amount": final_amount,
            "destiny_id": 162
            })
            print(payload)
            print(headers)
            # registering the Collection ISPCube
            response = requests.request("POST", url_payment, headers=headers, data=payload)
            print(response.text)
            if response.status_code != 200:
                print("Error when registering the Collection")
                return {"msg": "Error when registering the Collection"}
            
            return {"msg": "OK"}
        
        else:
            return {{"msg": "Status other than approved"}}
    except Exception as err:
        print(f'Empty REQUEST: {err}')
        return {"msg": "Empty REQUEST"}

@pay.get("/search/{id}", tags=["Pay"])
async def getPayId(id):
    try:
        url_token = settings.PAYPERTIC_URL_AUTH
        payload = settings.PAYLOAD
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        res_auth = requests.request("POST", url_token, headers=headers, data=payload)
        if res_auth.status_code != 200:
            return {"msg": "Unauthorized User"}
        
        data = res_auth.json()
        url = settings.PAYPERTIC_URL_HOST+"/pagos/"+id
        payload = {}
        headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + data['access_token']
        }
        # search payment by id PagoTIC
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            return {"msg": "Invalid ID: "+ id}
        
        resp = response.json()
        return resp
    except Exception as err:
        print(f'Empty REQUEST: {err}')
        return {"msg": err}