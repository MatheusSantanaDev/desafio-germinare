from typing import OrderedDict
from sqlalchemy.orm import Session
from utils.db import SoybeanMeal
from .exceptions import ContractMonthNotFound

class FlatPriceRepository:
    def __init__(
            self,
            db: Session, 
            max_cache_size: int = 1000
        ):
        self.db = db
        self.cache: OrderedDict[str, float] = OrderedDict()
        self.max_cache_size = max_cache_size

    def get_price_by_contract_month(self, contract_month: str) -> float:
        if contract_month in self.cache:
            self.cache.move_to_end(contract_month)
            return self.cache[contract_month]

        future_price = self._query_local_database(contract_month)

        self.cache[contract_month] = future_price

        if len(self.cache) > self.max_cache_size:
            self.cache.popitem(last=False)

        return future_price

    def _query_local_database(self, contract_month: str) -> float:
        result = self.db.query(SoybeanMeal.price).filter(SoybeanMeal.contract_month == contract_month).first()
        if not result:
            raise ContractMonthNotFound(contract_month)
        return float(result.price)