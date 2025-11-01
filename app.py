import streamlit as st
import pandas as pd
import numpy as np
import pickle
from preprocessing import preprocess_input
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Churn Risk Predictor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple, clean CSS
st.markdown("""
<style>
    /* Clean white background */
    .main {
        background-color: #ffffff;
    }

    .stApp {
        background-color: #ffffff;
    }

    /* All text black */
    * {
        color: #000000 !important;
    }

    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2c3e50;
        margin-bottom: 10px;
        padding: 20px;
        background: #ecf0f1;
        border-radius: 10px;
    }

    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #34495e;
        margin-bottom: 30px;
    }

    /* Cards */
    .card {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        border: 2px solid #dee2e6;
        margin: 15px 0;
    }

    /* Risk cards */
    .risk-high {
        background: #ffebee;
        padding: 30px;
        border-radius: 10px;
        border: 3px solid #f44336;
        text-align: center;
        margin: 20px 0;
    }

    .risk-medium {
        background: #fff3e0;
        padding: 30px;
        border-radius: 10px;
        border: 3px solid #ff9800;
        text-align: center;
        margin: 20px 0;
    }

    .risk-low {
        background: #e8f5e9;
        padding: 30px;
        border-radius: 10px;
        border: 3px solid #4caf50;
        text-align: center;
        margin: 20px 0;
    }

    /* Metric cards */
    .metric-card {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #dee2e6;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
    }

    .metric-label {
        font-size: 1rem;
        color: #7f8c8d;
        margin-top: 5px;
    }

    /* Button */
    .stButton > button {
        background-color: #3498db !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 15px 40px !important;
        border-radius: 8px !important;
        border: none !important;
    }

    .stButton > button:hover {
        background-color: #2980b9 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }

    /* Form elements */
    .stSelectbox label, .stNumberInput label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }

    /* Success boxes */
    .stSuccess {
        background-color: #d4edda !important;
        border: 1px solid #c3e6cb !important;
        border-radius: 5px !important;
        padding: 10px !important;
    }
</style>
""", unsafe_allow_html=True)


# Load models
@st.cache_resource
def load_models():
    try:
        with open('churn_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('threshold.pkl', 'rb') as f:
            threshold = pickle.load(f)
        return model, scaler, threshold, True
    except Exception as e:
        return None, None, None, False


model, scaler, threshold, models_loaded = load_models()

# Header
st.markdown('<div class="main-header">🎯 Customer Churn Predictor</div>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Risk Assessment System | 85.8% Recall Rate</p>', unsafe_allow_html=True)

if not models_loaded:
    st.error("⚠️ Model files not found. Please ensure .pkl files are in the directory.")
    st.stop()

# Layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("## 📝 Customer Information")

    with st.form("churn_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        with col2:
            internet_service = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        with col3:
            tenure = st.number_input("Tenure (months)", 0, 72, 12)

        col4, col5, col6 = st.columns(3)

        with col4:
            monthly_charges = st.number_input("Monthly Charges ($)", 18.0, 120.0, 70.0, step=5.0)
        with col5:
            payment_method = st.selectbox("Payment Method",
                                          ["Electronic check", "Mailed check", "Bank transfer (automatic)",
                                           "Credit card (automatic)"])
        with col6:
            paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])

        col7, col8 = st.columns(2)

        with col7:
            online_security = st.selectbox("Online Security", ["No", "Yes"])
        with col8:
            tech_support = st.selectbox("Tech Support", ["No", "Yes"])

        st.markdown("---")
        submitted = st.form_submit_button("🔮 Predict Churn Risk", use_container_width=True)

with col_right:
    st.markdown("## 📊 Model Performance")

    st.markdown("""
    <div class="card">
        <div style="text-align: center;">
            <div class="metric-value">85.8%</div>
            <div class="metric-label">Recall Rate</div>
            <hr style="margin: 20px 0;">
            <div style="font-size: 1.1rem; font-weight: 600; line-height: 2;">
                📈 Accuracy: 75-80%<br>
                🎯 Precision: 47.3%<br>
                💰 Savings: $173K/year
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚨 Top Risk Factors")
    st.markdown("""
    <div class="card">
        <ol style="line-height: 2; font-weight: 500;">
            <li>Month-to-month contract</li>
            <li>Fiber without support</li>
            <li>Electronic check payment</li>
            <li>High monthly charges</li>
            <li>New customer (&lt;12 months)</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Prediction Results
if submitted:
    total_charges = tenure * monthly_charges

    input_dict = {
        'Contract': contract, 'InternetService': internet_service, 'tenure': tenure,
        'MonthlyCharges': monthly_charges, 'TotalCharges': total_charges,
        'PaymentMethod': payment_method, 'PaperlessBilling': paperless_billing,
        'OnlineSecurity': online_security if internet_service != 'No' else 'No internet service',
        'TechSupport': tech_support if internet_service != 'No' else 'No internet service',
        'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
        'PhoneService': 'Yes', 'MultipleLines': 'No', 'OnlineBackup': 'No',
        'DeviceProtection': 'No', 'StreamingTV': 'No', 'StreamingMovies': 'No'
    }

    input_df = pd.DataFrame([input_dict])

    try:
        with st.spinner("🔄 Analyzing customer profile..."):
            processed_df = preprocess_input(input_df, scaler)
            churn_probability = model.predict_proba(processed_df)[0][1]
            will_churn = 1 if churn_probability >= threshold else 0

        st.markdown("---")
        st.markdown("## 🎯 Prediction Results")

        # Metrics
        met1, met2, met3, met4 = st.columns(4)

        with met1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{churn_probability * 100:.1f}%</div>
                <div class="metric-label">Churn Probability</div>
            </div>
            """, unsafe_allow_html=True)

        with met2:
            risk_level = "HIGH" if will_churn else "LOW"
            risk_color = "#e74c3c" if will_churn else "#27ae60"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {risk_color};">{risk_level}</div>
                <div class="metric-label">Risk Level</div>
            </div>
            """, unsafe_allow_html=True)

        with met3:
            confidence = min(abs(churn_probability - threshold) / threshold * 100, 99)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{confidence:.0f}%</div>
                <div class="metric-label">Confidence</div>
            </div>
            """, unsafe_allow_html=True)

        with met4:
            expected_ltv = 0 if will_churn else 1532
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${expected_ltv}</div>
                <div class="metric-label">Expected LTV</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Risk assessment
        if churn_probability >= 0.7:
            risk_class = "risk-high"
            title = "🚨 CRITICAL RISK"
            message = "Immediate intervention required!"
        elif churn_probability >= 0.4:
            risk_class = "risk-medium"
            title = "⚠️ MEDIUM RISK"
            message = "Proactive retention recommended"
        else:
            risk_class = "risk-low"
            title = "✅ LOW RISK"
            message = "Customer likely to stay"

        st.markdown(f"""
        <div class="{risk_class}">
            <h1 style="margin: 0; font-size: 2.5rem;">{title}</h1>
            <h2 style="margin: 10px 0; font-size: 2rem;">{churn_probability * 100:.1f}% Churn Probability</h2>
            <p style="font-size: 1.2rem; margin: 5px 0;">{message}</p>
        </div>
        """, unsafe_allow_html=True)

        # Recommendations
        if will_churn:
            st.markdown("### 💡 Recommended Actions")

            rec_col1, rec_col2 = st.columns(2)

            recommendations = []
            if contract == "Month-to-month":
                recommendations.append("📋 Offer 1-year contract with 20% discount")
            if payment_method == "Electronic check":
                recommendations.append("💳 Incentivize automatic payment switch")
            if internet_service == "Fiber optic" and tech_support == "No":
                recommendations.append("🛠️ Provide 3 months free tech support")
            if online_security == "No":
                recommendations.append("🔒 Offer online security at 50% off")
            if monthly_charges > 70:
                recommendations.append("💰 Review pricing/loyalty discount")
            if tenure < 12:
                recommendations.append("👥 Assign dedicated account manager")

            for i, rec in enumerate(recommendations):
                if i % 2 == 0:
                    rec_col1.success(rec)
                else:
                    rec_col2.success(rec)

        # Gauge chart
        st.markdown("### 📊 Risk Gauge")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=churn_probability * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Churn Probability", 'font': {'size': 24, 'color': '#2c3e50'}},
            number={'font': {'size': 48, 'color': '#2c3e50'}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#2c3e50"},
                'bar': {'color': "#3498db"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#95a5a6",
                'steps': [
                    {'range': [0, 40], 'color': '#d4edda'},
                    {'range': [40, 70], 'color': '#fff3cd'},
                    {'range': [70, 100], 'color': '#f8d7da'}
                ],
                'threshold': {
                    'line': {'color': "#e74c3c", 'width': 4},
                    'thickness': 0.75,
                    'value': threshold * 100
                }
            }
        ))

        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="white",
            font={'color': "#2c3e50", 'family': "Arial"}
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error making prediction: {e}")

# Sidebar
with st.sidebar:
    st.markdown("# ℹ️ About")
    st.markdown("""
    ### 🤖 Technology
    - XGBoost Algorithm
    - 40+ Features
    - 5,600+ Samples

    ### 🎯 Performance
    - **85.8% Recall**
    - **75% Accuracy**
    - **$173K Savings/year**

    ### 📈 Key Insights

    **High Risk Factors:**
    - Month-to-month contracts
    - Electronic check payments
    - Short tenure

    **Protection Factors:**
    - Long-term contracts
    - Tech support
    - Automatic payments
    """)

    st.markdown("---")
    st.caption("Built with Streamlit & XGBoost")