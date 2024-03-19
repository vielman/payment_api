from fastapi import APIRouter, Request
from schemas.pay import Pay, Link
import requests
import json
from config.config import settings

pay = APIRouter()

@pay.post("/payment", response_model=Link, tags=["Pay"])
async def payment(pay: Pay):
    url_token = settings.PAYPERTIC_URL_AUTH
    payload = settings.PAYLOAD
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
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

    res_link = requests.request("POST", url, headers=headers, data=payload)
    if res_link.status_code != 200:
        return {"msg": "invalid_request"}
    
    link = res_link.json()

    return {
        "msg":'OK',
        "id":link["id"],
        "form_url":link["form_url"],
        "final_amount":link["final_amount"],
        "status":link["status"],
    }

@pay.post("/notification", tags=["Pay"])
async def notification(request: Request):
    req = await request.body()
    data = json.loads(req)
    print(data)
    if data['status'] == "approved":
        print('-----------------------')
        print(data['final_amount'])
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
        res_token = requests.request("POST", url_token, headers=headers, data=payload)
        if res_token.status_code != 200:
            return {}
    
        data = res_token.json()
        print(data['token'])

        url = settings.ISPCUBE_URL_HOST + "/api/cash/payment_save"

        payload = json.dumps({
        "customer_id": 334455,
        "amount": "100.20",
        "destiny_id": 4
        })
        headers = {
        'login-type': settings.LOGIN_TYPE,
        'username': settings.USERNAME_ISPCUBE,
        'Authorization': 'Bearer ' + data['token'],
        'Accept': 'application/json',
        'api-key': settings.API_KEY,
        'client-id': settings.CLIENT_ID_ISPCUBE,
        'Content-Type': 'application/json'
        }
        print(headers)
        # response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)
        return {}
    

@pay.get("/search/{id}", tags=["Pay"])
async def getId(id):
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

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        return {"msg": "Invalid ID:"+id}
    
    resp = response.json()
    return resp