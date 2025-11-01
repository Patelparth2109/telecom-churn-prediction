import pandas as pd
import numpy as np


def preprocess_input(input_df, scaler):
    """
    Apply all preprocessing steps to match training data
    """

    df = input_df.copy()

    # ============================================
    # 1. BINARY ENCODING
    # ============================================
    df['gender'] = df['gender'].map({'Female': 0, 'Male': 1})
    df['Partner'] = df['Partner'].map({'Yes': 1, 'No': 0})
    df['Dependents'] = df['Dependents'].map({'Yes': 1, 'No': 0})
    df['PhoneService'] = df['PhoneService'].map({'Yes': 1, 'No': 0})
    df['PaperlessBilling'] = df['PaperlessBilling'].map({'Yes': 1, 'No': 0})

    # ============================================
    # 2. HANDLE "NO SERVICE" CATEGORIES
    # ============================================
    df['MultipleLines'] = df['MultipleLines'].replace('No phone service', 'No')
    df['OnlineSecurity'] = df['OnlineSecurity'].replace('No internet service', 'No')
    df['OnlineBackup'] = df['OnlineBackup'].replace('No internet service', 'No')
    df['DeviceProtection'] = df['DeviceProtection'].replace('No internet service', 'No')
    df['TechSupport'] = df['TechSupport'].replace('No internet service', 'No')
    df['StreamingTV'] = df['StreamingTV'].replace('No internet service', 'No')
    df['StreamingMovies'] = df['StreamingMovies'].replace('No internet service', 'No')

    # Encode to binary
    df['MultipleLines'] = df['MultipleLines'].map({'Yes': 1, 'No': 0})
    df['OnlineSecurity'] = df['OnlineSecurity'].map({'Yes': 1, 'No': 0})
    df['OnlineBackup'] = df['OnlineBackup'].map({'Yes': 1, 'No': 0})
    df['DeviceProtection'] = df['DeviceProtection'].map({'Yes': 1, 'No': 0})
    df['TechSupport'] = df['TechSupport'].map({'Yes': 1, 'No': 0})
    df['StreamingTV'] = df['StreamingTV'].map({'Yes': 1, 'No': 0})
    df['StreamingMovies'] = df['StreamingMovies'].map({'Yes': 1, 'No': 0})

    # ============================================
    # 3. ORDINAL ENCODING (Contract)
    # ============================================
    df['Contract'] = df['Contract'].map({
        'Month-to-month': 0,
        'One year': 1,
        'Two year': 2
    })

    # ============================================
    # 4. ONE-HOT ENCODING
    # ============================================
    df = pd.get_dummies(df, columns=['InternetService', 'PaymentMethod'],
                        drop_first=True, dtype=int)

    # ============================================
    # 5. FEATURE ENGINEERING
    # ============================================

    # Ensure numeric types
    df['tenure'] = pd.to_numeric(df['tenure'])
    df['MonthlyCharges'] = pd.to_numeric(df['MonthlyCharges'])
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
    df['SeniorCitizen'] = pd.to_numeric(df['SeniorCitizen'])

    # Tenure-based features
    df['IsNewCustomer'] = (df['tenure'] <= 12).astype(int)
    df['IsEstablished'] = ((df['tenure'] > 12) & (df['tenure'] <= 24)).astype(int)
    df['IsLoyalCustomer'] = (df['tenure'] > 48).astype(int)

    # Charge-based features
    df['ChargePerTenureMonth'] = df['TotalCharges'] / (df['tenure'] + 1)
    df['IsHighSpender'] = (df['MonthlyCharges'] > 70).astype(int)
    df['ChargeTenureRatio'] = df['MonthlyCharges'] / (df['tenure'] + 1)

    # Service bundle features
    has_internet_no = 1 if 'InternetService_No' in df.columns and df['InternetService_No'].iloc[0] == 1 else 0

    df['TotalServices'] = (
            df['PhoneService'].iloc[0] +
            (1 - has_internet_no) +
            df['OnlineSecurity'].iloc[0] +
            df['OnlineBackup'].iloc[0] +
            df['DeviceProtection'].iloc[0] +
            df['TechSupport'].iloc[0] +
            df['StreamingTV'].iloc[0] +
            df['StreamingMovies'].iloc[0]
    )

    df['ServiceDensity'] = df['TotalServices'] / (df['tenure'] + 1)
    df['HasMinimalServices'] = (df['TotalServices'] <= 2).astype(int)

    # High-risk profiles
    has_fiber = 1 if 'InternetService_Fiber optic' in df.columns and df['InternetService_Fiber optic'].iloc[
        0] == 1 else 0
    has_echeck = 1 if 'PaymentMethod_Electronic check' in df.columns and df['PaymentMethod_Electronic check'].iloc[
        0] == 1 else 0

    df['HighRiskProfile'] = int(
        (df['Contract'].iloc[0] == 0) and
        (has_fiber == 1) and
        (has_echeck == 1)
    )

    df['SeniorNoSupport'] = int(
        (df['SeniorCitizen'].iloc[0] == 1) and
        (df['TechSupport'].iloc[0] == 0)
    )

    df['SingleNoFamily'] = int(
        (df['Partner'].iloc[0] == 0) and
        (df['Dependents'].iloc[0] == 0)
    )

    df['NewHighSpender'] = int(
        (df['tenure'].iloc[0] <= 12) and
        (df['MonthlyCharges'].iloc[0] > 70)
    )

    # Payment & billing features
    df['PaperlessElectronicCheck'] = int(
        (df['PaperlessBilling'].iloc[0] == 1) and
        (has_echeck == 1)
    )

    has_bank = 1 if 'PaymentMethod_Bank transfer (automatic)' in df.columns and \
                    df['PaymentMethod_Bank transfer (automatic)'].iloc[0] == 1 else 0
    has_cc = 1 if 'PaymentMethod_Credit card (automatic)' in df.columns and \
                  df['PaymentMethod_Credit card (automatic)'].iloc[0] == 1 else 0

    df['HasAutoPay'] = int((has_bank == 1) or (has_cc == 1))

    # Internet service quality
    df['FiberNoAddons'] = int(
        (has_fiber == 1) and
        (df['OnlineSecurity'].iloc[0] == 0) and
        (df['TechSupport'].iloc[0] == 0)
    )

    # ============================================
    # 6. SCALING
    # ============================================
    cols_to_scale = ['tenure', 'MonthlyCharges', 'TotalCharges']
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # ============================================
    # 7. ENSURE CORRECT COLUMN ORDER & MISSING COLUMNS
    # ============================================

    # Expected columns from training (in exact order)
    expected_columns = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'MonthlyCharges', 'TotalCharges',
        'IsNewCustomer', 'IsEstablished', 'IsLoyalCustomer',
        'ChargePerTenureMonth', 'IsHighSpender', 'ChargeTenureRatio',
        'TotalServices', 'ServiceDensity', 'HasMinimalServices',
        'HighRiskProfile', 'SeniorNoSupport', 'SingleNoFamily',
        'NewHighSpender', 'PaperlessElectronicCheck', 'HasAutoPay',
        'FiberNoAddons', 'InternetService_Fiber optic', 'InternetService_No',
        'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check',
        'PaymentMethod_Mailed check'
    ]

    # Add missing columns with 0
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    # Reorder columns to match training
    df = df[expected_columns]

    return df