from pydantic import BaseModel
from typing import List

# Modelo de requisição para o endpoint /api/flat_price
class FlatPriceRequest(BaseModel):
    basis: float
    contract_months: List[str]

# Modelo de resposta para cada item no endpoint /api/flat_price
class FlatPriceResponse(BaseModel):
    contract_month: str
    cbot_price: float
    basis: float
    flat_price: float

# Modelo de resposta completo para o endpoint /api/flat_price
class FlatPriceResults(BaseModel):
    results: List[FlatPriceResponse]