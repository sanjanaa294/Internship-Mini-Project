import streamlit as st
import pickle
import pandas as pd
import time

st.set_page_config(page_title="MediCore Stroke Prediction", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for premium clinical aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Global Background */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Headers */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0f766e, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        padding-top: 10px;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #475569;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    .sidebar-header {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0f766e, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #0d9488 0%, #0891b2 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.8rem;
        border: none;
        box-shadow: 0 4px 14px 0 rgba(13, 148, 136, 0.39);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(13, 148, 136, 0.5);
    }
    
    /* Result Cards */
    .result-card-low {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 8px solid #22c55e;
        padding: 30px;
        border-radius: 16px;
        color: #166534;
        box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.1);
        margin-top: 20px;
    }
    .result-card-high {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 8px solid #ef4444;
        padding: 30px;
        border-radius: 16px;
        color: #991b1b;
        box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.1);
        margin-top: 20px;
    }
    .result-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .result-prob {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .result-desc {
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Login Form styling */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 70vh;
    }
    div[data-testid="stForm"] {
        background-color: #ffffff;
        padding: 50px 40px;
        border-radius: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.08);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner="Loading diagnostic models...")
def load_model_v4():
    return pickle.load(open("model.pkl", "rb"))

model = load_model_v4()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='main-header'>🏥 MediCore Systems</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Enterprise Stroke Risk Assessment Portal</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("""
                <div style='text-align: center; margin-bottom: 30px;'>
                    <div style='font-size: 3rem; margin-bottom: 10px;'>🔐</div>
                    <h2 style='color:#0f172a; font-weight:800; margin-bottom:5px;'>Secure Login</h2>
                    <p style='color:#64748b; font-size: 1.1rem;'>Enter your physician credentials</p>
                </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input("Physician ID / Username", placeholder="Enter 'admin'")
            password = st.text_input("Secure Password", type="password", placeholder="Enter '1234'")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Authenticate & Enter Portal")
            
            if submitted:
                if username == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.success("Authentication successful! Establishing secure connection...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please verify your ID and password.")

def main_app():
    # Sidebar
    with st.sidebar:
        st.markdown("<div class='sidebar-header'>🏥 MediCore</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 👤 Logged In As")
        st.success("Dr. Admin (Neurology)")
        st.markdown("---")
        
        st.markdown("### 📋 Clinical Guidelines")
        st.info("**BMI Categories:**\n\n🟢 Normal: 18.5 - 24.9\n\n🟡 Overweight: 25 - 29.9\n\n🔴 Obese: 30+")
        st.info("**Glucose Levels:**\n\n🟢 Normal: <140 mg/dL\n\n🟡 Prediabetes: 140-199 mg/dL\n\n🔴 Diabetes: >200 mg/dL")
        st.markdown("---")
        if st.button("🚪 Secure Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("<div class='main-header'>Neurological Assessment</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>AI-Powered Cerebrovascular Accident (Stroke) Risk Evaluator</div>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("### 👤 Patient Demographics")
        colA, colB, colC = st.columns(3)
        with colA:
            age = st.slider("Patient Age", 0, 120, 45)
        with colB:
            gender = st.selectbox("Biological Sex", ["Male", "Female", "Other"])
        with colC:
            ever_married = st.selectbox("Marital History (Ever Married?)", ["Yes", "No"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        colD, colE, colF = st.columns(3)
        with colD:
            residence_type = st.selectbox("Primary Residence Type", ["Urban", "Rural"])
        with colE:
            work_type = st.selectbox("Employment Sector", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"])
        with colF:
            smoking_status = st.selectbox("Tobacco Usage Status", ["formerly smoked", "never smoked", "smokes", "Unknown"])

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 🩺 Clinical Metrics & Vitals")
        colG, colH = st.columns(2)
        with colG:
            bmi = st.number_input("Body Mass Index (BMI)", 10.0, 80.0, 25.0)
            hypertension_text = st.selectbox("Hypertension Diagnosis", ["No", "Yes"])
            hypertension = 1 if hypertension_text == "Yes" else 0
        with colH:
            avg_glucose_level = st.number_input("Avg Glucose Level (mg/dL)", 50.0, 300.0, 100.0)
            heart_disease_text = st.selectbox("Heart Disease History", ["No", "Yes"])
            heart_disease = 1 if heart_disease_text == "Yes" else 0

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Predict Action
    if st.button("⚙️ Execute Predictive Analysis", use_container_width=True):
        with st.spinner("Processing clinical parameters via Random Forest classification..."):
            time.sleep(1.5) # Clinical UX delay
            input_data = pd.DataFrame({
                'gender': [gender],
                'age': [age],
                'hypertension': [hypertension],
                'heart_disease': [heart_disease],
                'ever_married': [ever_married],
                'work_type': [work_type],
                'Residence_type': [residence_type],
                'avg_glucose_level': [avg_glucose_level],
                'bmi': [bmi],
                'smoking_status': [smoking_status]
            })
            
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1] * 100
            
            st.markdown("### 📊 Diagnostic Report")
            
            # Progress bar for probability
            st.progress(int(probability) if probability <= 100 else 100)
            
            # In clinical terms, a stroke risk > 10% is extremely high (baseline is ~4%)
            if probability >= 10.0 or prediction == 1:
                st.markdown(f"""
                <div class='result-card-high'>
                    <div class='result-title'>⚠️ Critical Alert: High Stroke Risk Profile</div>
                    <div class='result-prob'>Calculated Probability: <span style="font-size:1.5rem; font-weight:800;">{probability:.1f}%</span></div>
                    <div class='result-desc'><b>Clinical Note:</b> Stroke is a rare event. A probability above 10% represents a significantly elevated clinical risk compared to the general baseline.<br><br><b>Recommendation:</b> Immediate neurological consultation, continuous monitoring, and preventive clinical intervention are strongly advised.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-card-low'>
                    <div class='result-title'>✅ Favorable: Low Stroke Risk Profile</div>
                    <div class='result-prob'>Calculated Probability: <span style="font-size:1.5rem; font-weight:800;">{probability:.1f}%</span></div>
                    <div class='result-desc'><b>Recommendation:</b> Patient is currently in a lower-risk category. Maintain a healthy lifestyle, balanced diet, and continue routine check-ups.</div>
                </div>
                """, unsafe_allow_html=True)

if st.session_state.logged_in:
    main_app()
else:
    login()