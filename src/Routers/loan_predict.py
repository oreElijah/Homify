from fastapi import APIRouter, HTTPException
from database.config import LoanInfo_table, database
from models.loan_predict import LoanInputData
import numpy as np
import joblib

router = APIRouter() 

model = joblib.load("ml_models/loan_approval_model.model")

@router.post("/loan_eligibility_predictor", status_code=201)
async def predict_eligibility(data: LoanInputData):
    edu_map = {"graduate": 1, "not graduate": 0}
    self_emp_map = {"yes": 1, "no": 0}

    if data.education not in edu_map or data.self_employed not in self_emp_map:
        raise HTTPException(status_code=400, detail="Invalid education or self-employed value")

    education_encoded = edu_map[data.education]
    self_employed_encoded = self_emp_map[data.self_employed]
    input_array = np.array([[
        data.no_of_dependents,
        data.income_annum,
        data.loan_amount,
        data.loan_term,
        data.residential_assets_value,
        data.commercial_assets_value,
        data.luxury_assets_value,
        data.bank_asset_value,
        education_encoded,
        self_employed_encoded
    ]])
    prediction = model.predict(input_array)
    output = prediction.tolist()[0] 

    def status(x):
        if  x== 1:
            return "Approved"
        else:
            return "Unapproved"

    query = LoanInfo_table.insert().values(no_of_dependents=data.no_of_dependents, income_annum=data.income_annum, 
                                           loan_amount = data.loan_amount, loan_term = data.loan_term, 
                                           residential_assets_value = data.residential_assets_value, commercial_assets_value = data.commercial_assets_value,
                                           luxury_assets_value = data.luxury_assets_value,bank_asset_value = data.bank_asset_value,
                                           education = data.education, self_employed = data.self_employed, prediction = status(output)
                                           )
    probs = model.predict_proba(input_array)[0][0]
    await database.execute(query)
    if output == 1:  # Approved
        return {
            "loan_eligibility": "Eligible",
            "risk_level": "Low" if probs >= 0.8 else "Moderate",
            "advice": "This applicant shows a high likelihood of repayment. You may consider offering standard or lower interest rates." if probs >= 0.8 else "Moderate approval probability. Adjust loan amount accordingly.",
            "summary": "Eligible candidate. Verify all documents before proceeding."
        }
    else:  # Not Approved
        return {
            "loan_eligibility": "Not Eligible",
            "risk_level": "High",
            "advice": "This applicant has a low predicted ability to repay. Recommend applying for a lower loan amount if proceeding.",
            "summary": "High risk. Lending is discouraged unless collateral is secured."
        }
