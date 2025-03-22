from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from utils.db import SoybeanMeal
from .exceptions import ContractMonthNotFound, InternalServerError

class FlatPriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_price_by_contract_month(self, contract_month: str) -> float:
        try:
            result = self.db.query(SoybeanMeal.price).filter(SoybeanMeal.contract_month == contract_month).first()
            if result:
                return float(result.price)
            raise ContractMonthNotFound(contract_month)
        except SQLAlchemyError as e:
            raise InternalServerError() from e
    
    