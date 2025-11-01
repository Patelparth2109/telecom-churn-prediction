# 🎯 Telecom Customer Churn Prediction

An end-to-end machine learning project to predict customer churn using advanced feature engineering and XGBoost, deployed as an interactive Streamlit web application.

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-00ADD8?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

## 🎯 Project Overview

Developed a customer churn prediction system for a telecom company, achieving **85.8% recall** and identifying actionable retention strategies that could save **$173K annually**.

### 🔑 Key Highlights
- **85.8% Recall Rate** - Catches 86 out of 100 churners
- **68% Reduction** in missed churners (from 166 to 53)
- **$173K Annual Savings** in prevented customer loss
- **Real-time Predictions** via interactive web app

---

## 📊 Business Problem

The telecom company faced a **26.58% churn rate**, resulting in significant revenue loss. The goal was to:
1. Identify key churn drivers
2. Build a predictive model to flag at-risk customers
3. Provide actionable retention recommendations

---

## 🔍 Methodology

### 1. **SQL Analysis** (MySQL)
Performed comprehensive exploratory data analysis on 7,032 customers:
- **Data Validation:** Verified data quality and consistency
- **Univariate Analysis:** Churn rates by contract type, payment method, services
- **Segmentation:** Tenure-based cohorts, service combinations
- **Financial Metrics:** Revenue loss calculation, CLV analysis

**Key SQL Insights:**
- Month-to-month contracts: **42.71% churn**
- Fiber optic + Electronic check: **54.61% churn** (highest risk)
- Tech support reduces churn by **26 percentage points**

### 2. **Feature Engineering** (Python)
Created 16 advanced features that drove model performance:
- **Tenure-based:** IsNewCustomer, IsLoyalCustomer
- **Financial:** ChargePerTenureMonth, ChargeTenureRatio
- **Service bundles:** TotalServices, ServiceDensity
- **Risk profiles:** HighRiskProfile, NewHighSpender, FiberNoAddons

**Impact:** 5 out of top 10 most important features were engineered!

### 3. **Machine Learning** (Python)
Trained and compared multiple models:
- **Logistic Regression:** Baseline (56% recall)
- **Random Forest:** Strong performance (79% recall)
- **XGBoost:** Best model (85.8% recall after tuning)

**Optimization Techniques:**
- Hyperparameter tuning (RandomizedSearchCV)
- Class imbalance handling (scale_pos_weight)
- Threshold optimization (0.40 for business ROI)

### 4. **Deployment** (Streamlit)
Built interactive web application with:
- 8-question simplified input form
- Real-time churn probability prediction
- Risk level classification
- Personalized retention recommendations
- Visual risk gauge

---

## 📈 Results

### Model Performance

| Metric | Value |
|--------|-------|
| **Recall (Churners)** | 85.8% |
| **Precision** | 47.3% |
| **Accuracy** | 75-80% |
| **F1-Score** | 61% |
| **False Negatives** | 53 (vs 166 baseline) |

### Business Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Missed Churners** | 166 | 53 | **68% reduction** |
| **Revenue at Risk** | $254K | $81K | **$173K saved** |
| **Recall Rate** | 56% | 85.8% | **+29.8 points** |

---

## 🚀 Key Features

### Top 10 Most Important Features (by XGBoost)
1. **Contract Type** (month-to-month = highest risk)
2. **FiberNoAddons** (engineered feature)
3. **InternetService_Fiber optic**
4. **NewHighSpender** (engineered feature)
5. **InternetService_No**
6. **HighRiskProfile** (engineered feature)
7. **ChargeTenureRatio** (engineered feature)
8. **PaperlessElectronicCheck** (engineered feature)
9. **PaymentMethod_Electronic check**
10. **OnlineSecurity**

---

## 💡 Business Recommendations

Based on the model insights:

### Immediate Actions (High ROI)
1. **Contract Conversion Campaign** - Target month-to-month customers with 1-year discounts
2. **Payment Method Incentives** - Move electronic check users to automatic payments
3. **Proactive Tech Support** - Offer free support to fiber optic customers

### Long-term Strategy
- Improve fiber optic service quality/reliability
- Develop early warning system for 0-12 month customers
- Create retention playbook for high-risk profiles

**Expected Impact:** $173K annual savings from reduced churn

---

## 🛠️ Tech Stack

**Languages & Tools:**
- Python 3.9+
- MySQL
- Streamlit

**Libraries:**
```
pandas
numpy
scikit-learn
xgboost
plotly
streamlit
```

**ML Techniques:**
- Feature Engineering
- XGBoost Classifier
- Hyperparameter Tuning (RandomizedSearchCV)
- Threshold Optimization
- Class Imbalance Handling

---

## 📦 Installation & Usage

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run Streamlit App
```bash
streamlit run src/app.py
```

### Train Model (Optional)
```bash
jupyter notebook notebooks/03_model_training.ipynb
```

---

## 📊 Live Demo

🔗 **[Try the Live App](https://your-app-name.streamlit.app)**

---

## 📁 Project Structure
```
telecom-churn-prediction/
├── data/                  # Dataset
├── notebooks/             # Jupyter notebooks
├── sql/                   # SQL analysis queries
├── models/                # Trained models
├── src/                   # Source code
│   ├── app.py            # Streamlit app
│   └── preprocessing.py  # Data preprocessing
├── requirements.txt       # Dependencies
└── README.md             # This file
```

---

## 🎓 Key Learnings

1. **Feature engineering drives performance** - 5 of top 10 features were engineered
2. **Business context matters** - Optimized for recall (catching churners) over accuracy
3. **Threshold tuning is powerful** - Moved from 56% to 85.8% recall
4. **SQL + ML synergy** - SQL insights informed feature engineering
5. **Deployment matters** - Simplified UX (8 questions) increases adoption

---

## 📈 Future Improvements

- [ ] Add time-series analysis for churn trends
- [ ] Implement SHAP values for model explainability
- [ ] A/B test retention strategies
- [ ] Add customer segmentation clustering
- [ ] Deploy on AWS/Azure for production use

---

## 👤 Author

**Parth Patel**
- LinkedIn: (https://www.linkedin.com/in/parth-patel-03800917a/)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Dataset: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Inspiration: Real-world telecom churn challenges

---

**⭐ If you found this project helpful, please consider giving it a star!**
