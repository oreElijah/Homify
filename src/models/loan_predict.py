from pydantic import BaseModel

class LoanInputData(BaseModel):
    income_annum: int
    no_of_dependents: int
    loan_amount: int
    loan_term: int
    residential_assets_value: int
    commercial_assets_value: int
    luxury_assets_value: int
    bank_asset_value: int
    education: str
    self_employed: str
