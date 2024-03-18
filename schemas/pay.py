from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Pay(BaseModel):
    currency_id: str
    external_transaction_id: str
    due_date: str
    last_due_date: str
    details_external_reference: str
    details_concept_id: str
    details_concept_description: str
    details_amount: float
    payer_name: str
    payer_email: str
    payer_identification_type: str
    payer_identification_number: str
    payer_identification_country: str

class Link(BaseModel):
    msg:str
    id:Optional[str] = None
    form_url:Optional[str] = None
    final_amount:Optional[float] = None
    status:Optional[str] = None

    
