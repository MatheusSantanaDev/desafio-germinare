import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_app.models import SoybeanMealPrice, Base

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_soybean_meal_price_model(db_session):
    price = SoybeanMealPrice(contract_month="Jan2024", price=100.50)
    db_session.add(price)
    db_session.commit()

    result = db_session.query(SoybeanMealPrice).filter(SoybeanMealPrice.contract_month == "Jan2024").first()
    assert result is not None
    assert result.price == 100.50