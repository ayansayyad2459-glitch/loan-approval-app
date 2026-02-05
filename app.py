import streamlit as st
import pandas as pd
import numpy as np
import pickle

# --- PAGE SETUP ---
st.set_page_config(page_title="CreditWise Elite", page_icon="💎", layout="wide")

# --- LOAD MODEL ---
@st.cache_resource
def load_data():
    with open('best_loan_model.pkl', 'rb') as f: model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f: scaler = pickle.load(f)
    with open('model_columns.pkl', 'rb') as f: col_names = pickle.load(f)
    return model, scaler, col_names

try:
    model, scaler, model_columns = load_data()
except:
    st.error("⚠️ Model files missing.")
    st.stop()


st.markdown("""
<style>
    /* 1. FORCE DARK THEME BACKGROUND */
    .stApp {
        background-color: #0E1117;
        background-image: radial-gradient(circle at 50% -20%, #2e1065, #0E1117);
        color: white;
    }

    /* 2. GLASSMORPHISM CARDS */
    div.css-1r6slb0.e1tzin5v2, [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }

    /* 3. NEON TITLES */
    h1 {
        background: linear-gradient(90deg, #4FCCFF, #9F55FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 3rem;
    }
    h2, h3 { color: #e0e0e0 !important; }
    
    /* 4. CUSTOM INPUTS */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1c24 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 8px;
    }
    label { color: #b0b0b0 !important; }

    /* 5. GLOWING BUTTON */
    div.stButton > button {
        background: linear-gradient(45deg, #4F46E5, #9333EA);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        transition: 0.3s;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.5);
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(147, 51, 234, 0.7);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_1, col_2 = st.columns([1, 4])
with col_1:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
with col_2:
    st.title("CreditWise Elite")
    st.write("AI-Powered Financial Risk Assessment System")

st.markdown("---")

# --- MAIN LAYOUT (3 Columns) ---
col_left, col_mid, col_right = st.columns([1, 1, 1], gap="medium")

# --- COLUMN 1: WHO? ---
with col_left:
    st.markdown("### 👤 The Applicant")
    with st.container():
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.slider("Age", 18, 70, 28)
        married = st.selectbox("Marital Status", ["Single", "Married"])
        education = st.radio("Education", ["Graduate", "Not Graduate"], horizontal=True)
        dependents = st.selectbox("Dependents", [0, 1, 2, "3+"])
        if dependents == "3+": dependents = 3

# --- COLUMN 2: MONEY? ---
with col_mid:
    st.markdown("### 💰 The Finances")
    with st.container():
        app_income = st.number_input("Monthly Income ($)", 0, 100000, 5000, step=500)
        co_income = st.number_input("Co-Applicant Income", 0, 50000, 0, step=500)
        savings = st.number_input("Total Savings", 0, 1000000, 15000, step=1000)
        emp_status = st.selectbox("Employment", ["Salaried", "Self-employed", "Unemployed"])
        employer_cat = st.selectbox("Employer Type", ["Private", "Government", "MNC", "Business"])

# --- COLUMN 3: LOAN? ---
with col_right:
    st.markdown("### 🏦 The Loan")
    with st.container():
        loan_amt = st.number_input("Loan Amount ($)", 5000, 500000, 120000, step=5000)
        loan_term = st.selectbox("Loan Term (Months)", [12, 36, 60, 120, 180, 360], index=5)
        credit_score = st.slider("Credit Score", 300, 850, 720)
        
        
        st.markdown(f"""
        <div style="background:#2A2D3A; padding:10px; border-radius:10px; margin-top:10px; border-left: 4px solid #4FCCFF;">
            <p style="margin:0; font-size:12px; color:#aaa;">Estimated EMI</p>
            <h3 style="margin:0; color:white;">${(loan_amt/loan_term):.0f} <span style="font-size:14px">/mo</span></h3>
        </div>
        """, unsafe_allow_html=True)
        
        loan_purpose = st.selectbox("Purpose", ["Home", "Car", "Personal", "Education"])
        property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])
        existing_loans = st.number_input("Existing Loans", 0, 5, 0)

st.write("")
st.write("")


analyze = st.button("✨ ANALYZE APPLICATION")

if analyze:
    # 1. Prepare Data
    dti_simulated = existing_loans / (app_income + co_income + 1) # Simple calc
    
    input_df = pd.DataFrame({
        'Applicant_Income': [app_income], 'Coapplicant_Income': [co_income],
        'Age': [age], 'Dependents': [dependents], 'Existing_Loans': [existing_loans],
        'Savings': [savings], 'Collateral_Value': [0], 'Loan_Amount': [loan_amt],
        'Loan_Term': [loan_term], 'Credit_Score': [credit_score], 'DTI_Ratio': [0.3], # Defaulting DTI if not asked
        'Gender': [gender], 'Marital_Status': [married], 'Education_Level': [education],
        'Employment_Status': [emp_status], 'Employer_Category': [employer_cat],
        'Property_Area': [property_area], 'Loan_Purpose': [loan_purpose]
    })
    
    # 2. Process
    input_df['Gender'] = input_df['Gender'].map({'Male': 1, 'Female': 0})
    input_df['Marital_Status'] = input_df['Marital_Status'].map({'Married': 1, 'Single': 0})
    input_df['Education_Level'] = input_df['Education_Level'].map({'Graduate': 1, 'Not Graduate': 0})
    
    input_df = pd.get_dummies(input_df, columns=['Employer_Category', 'Loan_Purpose', 'Property_Area', 'Employment_Status'], drop_first=True)
    input_df['DTI_Ratio_squared'] = input_df['DTI_Ratio'] ** 2
    input_df['Credit_Score_squared'] = input_df['Credit_Score']**2
    input_df['Applicant_Income_log'] = np.log1p(input_df['Applicant_Income'])
    
    # Align cols
    input_df = input_df.drop(['DTI_Ratio', 'Credit_Score'], axis=1, errors='ignore')
    input_df = input_df.reindex(columns=model_columns, fill_value=0)
    
    # Predict
    input_scaled = scaler.transform(input_df)
    pred = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0][1]

    # --- RESULT POPUP ---
    st.write("---")
    if pred == 1:
        st.balloons()
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #11998e, #38ef7d); padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 10px 30px rgba(56, 239, 125, 0.3);">
            <h1 style="color: white; margin:0; font-size: 50px;">APPROVED</h1>
            <p style="color: #e8f5e9; font-size: 20px;">Probability: {prob:.1%}</p>
            <p style="color: white;">The system recommends approving this loan.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #cb2d3e, #ef473a); padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 10px 30px rgba(239, 71, 58, 0.3);">
            <h1 style="color: white; margin:0; font-size: 50px;">REJECTED</h1>
            <p style="color: #ffebee; font-size: 20px;">Risk Score: {1-prob:.1%}</p>
            <p style="color: white;">High risk factors detected. Manual review required.</p>
        </div>
        """, unsafe_allow_html=True)