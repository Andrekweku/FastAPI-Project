from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost:5432/Fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Test_Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     db = Test_Sessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()



# client = TestClient(app)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Test_Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    #clear our database for the code runs
    # Base.metadata.drop_all(bind=engine)
    #run our code before we run our test
    # Base.metadata.create_all(bind=engine)
    yield  TestClient(app)
    # Base.metadata.drop_all(bind=engine) - you can use this too and delete the one above
    #run our code after our test finishes
