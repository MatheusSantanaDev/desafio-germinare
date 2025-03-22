from sqlalchemy.orm import Session
from utils.db import SoybeanMealPrice

class SoybeanMealRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_price_by_contract_month(self, contract_month: str) -> float:

        result = self.db.query(SoybeanMealPrice.price).filter(SoybeanMealPrice.contract_month == contract_month).first()
        
        if result:
            return float(result.price)

        return 0.0