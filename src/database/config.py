import os
import databases

from dotenv import load_dotenv
import sqlalchemy

load_dotenv()

metadata = sqlalchemy.MetaData()

LoanInfo_table = sqlalchemy.Table("loaninfo", metadata, 
sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("no_of_dependents", sqlalchemy.Integer),
    sqlalchemy.Column("income_annum", sqlalchemy.Integer),
    sqlalchemy.Column("loan_amount", sqlalchemy.Integer),
    sqlalchemy.Column("loan_term", sqlalchemy.Integer),
    sqlalchemy.Column("residential_assets_value", sqlalchemy.Integer),
    sqlalchemy.Column("commercial_assets_value", sqlalchemy.Integer ),
    sqlalchemy.Column("luxury_assets_value",  sqlalchemy.Integer),
    sqlalchemy.Column("bank_asset_value",  sqlalchemy.Integer),
    sqlalchemy.Column("education", sqlalchemy.String),  
    sqlalchemy.Column("self_employed", sqlalchemy.String),  
    sqlalchemy.Column("prediction", sqlalchemy.String)  # store ML output
)

HousePriceInfo_table = sqlalchemy.Table("house_price_info", metadata, 
sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("bedroom", sqlalchemy.Integer),
    sqlalchemy.Column("bathroom", sqlalchemy.Integer),
    sqlalchemy.Column("parking_space", sqlalchemy.Integer),
    sqlalchemy.Column("toilets", sqlalchemy.Integer),
    sqlalchemy.Column("title", sqlalchemy.String),  
    sqlalchemy.Column("town", sqlalchemy.String),  
    sqlalchemy.Column("state", sqlalchemy.String),
    sqlalchemy.Column("output", sqlalchemy.Integer),  # store ML output
)

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("Database URL has not been set or is in accessible")
    # print("DATABASE_URL is not set")

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)

async def connect_db():
    """Connecting to database on startup"""
    await database.connect()

async def disconnect_db():
    """Disconnecting to database on shutdown"""
    await database.disconnect()

def create_tables():
    """Creating tables in database"""
    metadata.create_all(engine)
    print("Created Successfully ✅")

# create_tables()
