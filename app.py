import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
import csv
import os
from datetime import datetime
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Health Insight Support System", layout="wide")

# ---------------- GLOBAL CSS STYLING ----------------
st.markdown("""
<style>

/* ═══════════════════════════════════════
   LIGHT MODE (default)
═══════════════════════════════════════ */

.stApp {
    background-color: #f4f9ff;
}

.main-header {
    text-align: center;
    color: #0e4d92;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    font-family: 'Segoe UI', sans-serif;
}
.main-subtext {
    text-align: center;
    color: #4a6080;
    font-size: 1rem;
    margin-bottom: 8px;
    font-family: 'Segoe UI', sans-serif;
}
.header-divider {
    border: none;
    border-top: 2px solid #0e4d92;
    margin: 8px auto 24px auto;
    width: 80%;
    opacity: 0.25;
}

.card {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(14, 77, 146, 0.09);
    border: 1px solid #dde8f5;
}

.section-title {
    color: #0e4d92;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid #e0ecfa;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0.3px;
}

/* Buttons */
.stButton > button {
    background-color: #0e4d92 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 28px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: background-color 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(14, 77, 146, 0.2) !important;
}
.stButton > button:hover {
    background-color: #0a3a70 !important;
}
.stDownloadButton > button {
    background-color: #1a6bb5 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    transition: background-color 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background-color: #0e4d92 !important;
}

/* Input Fields */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 6px !important;
    border: 1px solid #c4d8ef !important;
    background-color: #fafcff !important;
    color: #1a1a2e !important;
}
.stTextInput > label,
.stNumberInput > label,
.stSelectbox > label,
.stMultiSelect > label {
    color: #2c3e60 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}
.stMultiSelect > div > div {
    border-radius: 6px !important;
    border: 1px solid #c4d8ef !important;
}

/* Progress Bars */
.stProgress > div > div > div {
    background-color: #0e4d92 !important;
    border-radius: 4px !important;
}
.stProgress > div > div {
    background-color: #dde8f5 !important;
    border-radius: 4px !important;
}

/* Hospital Cards */
.hospital-card {
    background-color: #ffffff;
    border: 1px solid #c4d8ef;
    border-left: 4px solid #0e4d92;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 14px;
}
.hospital-name {
    color: #0e4d92;
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 4px;
}
.hospital-address {
    color: #4a6080;
    font-size: 0.9rem;
    margin-bottom: 8px;
}
.hospital-link a {
    color: #1a6bb5;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
}
.hospital-link a:hover {
    text-decoration: underline;
    color: #0e4d92;
}

/* Prediction Items */
.prediction-item {
    background-color: #f0f6ff;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 12px;
    border-left: 4px solid #0e4d92;
}
.prediction-label {
    color: #0e4d92;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 4px;
}
.prediction-pct {
    color: #4a6080;
    font-size: 0.88rem;
    margin-bottom: 6px;
}

/* Disease Info Card */
.disease-card {
    background-color: #f8fbff;
    border: 1px solid #dde8f5;
    border-radius: 8px;
    padding: 18px 22px;
    margin-top: 8px;
}
.disease-field {
    margin-bottom: 10px;
    font-size: 0.95rem;
    color: #2c3e60;
}
.disease-field strong {
    color: #0e4d92;
}

/* Footer */
.footer-disclaimer {
    text-align: center;
    color: #cc0000;
    font-size: 0.95rem;
    font-weight: 700;
    padding: 16px 20px;
    border-top: 2px solid #e8e8e8;
    margin-top: 16px;
}

/* Dividers & Headings */
hr {
    border-color: #dde8f5 !important;
    opacity: 0.6 !important;
}
h2, h3 {
    color: #0e4d92 !important;
}


/* ═══════════════════════════════════════
   DARK MODE
═══════════════════════════════════════ */

@media (prefers-color-scheme: dark) {

    .stApp {
        background-color: #0f172a !important;
    }

    .main-header {
        color: #60a5fa !important;
    }
    .main-subtext {
        color: #94a3b8 !important;
    }
    .header-divider {
        border-top-color: #60a5fa !important;
        opacity: 0.3 !important;
    }

    .card {
        background-color: #1e293b !important;
        border-color: #334155 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4) !important;
    }

    .section-title {
        color: #93c5fd !important;
        border-bottom-color: #334155 !important;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #0f172a !important;
        border-color: #334155 !important;
        color: #f1f5f9 !important;
    }
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stMultiSelect > label {
        color: #cbd5e1 !important;
    }
    .stMultiSelect > div > div {
        background-color: #0f172a !important;
        border-color: #334155 !important;
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background-color: #3b82f6 !important;
    }
    .stProgress > div > div {
        background-color: #1e3a5f !important;
    }

    /* Hospital cards */
    .hospital-card {
        background-color: #1e293b !important;
        border-color: #334155 !important;
        border-left-color: #3b82f6 !important;
    }
    .hospital-name {
        color: #93c5fd !important;
    }
    .hospital-address {
        color: #94a3b8 !important;
    }
    .hospital-link a {
        color: #60a5fa !important;
    }
    .hospital-link a:hover {
        color: #93c5fd !important;
    }

    /* Prediction items */
    .prediction-item {
        background-color: #1a3050 !important;
        border-left-color: #3b82f6 !important;
    }
    .prediction-label {
        color: #93c5fd !important;
    }
    .prediction-pct {
        color: #94a3b8 !important;
    }

    /* Disease card */
    .disease-card {
        background-color: #172033 !important;
        border-color: #334155 !important;
    }
    .disease-field {
        color: #cbd5e1 !important;
    }
    .disease-field strong {
        color: #93c5fd !important;
    }

    /* Footer */
    .footer-disclaimer {
        color: #f87171 !important;
        border-top-color: #334155 !important;
    }

    /* Dividers and headings */
    hr {
        border-color: #334155 !important;
        opacity: 0.7 !important;
    }
    h2, h3 {
        color: #93c5fd !important;
    }

    /* Streamlit native text */
    p, li, span, div {
        color: #f1f5f9;
    }

    /* Buttons stay the same — white text on blue is fine in dark mode */
    .stButton > button {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }
    .stButton > button:hover {
        background-color: #1e40af !important;
    }
    .stDownloadButton > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
    }
    .stDownloadButton > button:hover {
        background-color: #1d4ed8 !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-header">Health Insight &amp; Support System</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtext">Describe your symptoms and receive AI-assisted health insights. This tool is intended to inform, not replace, professional medical care.</div>', unsafe_allow_html=True)
st.markdown('<hr class="header-divider">', unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# ---------------- PATIENT INFORMATION SECTION ----------------
st.markdown('<div class="card"><div class="section-title">Patient Information</div>', unsafe_allow_html=True)

pat_col1, pat_col2, pat_col3 = st.columns(3)
with pat_col1:
    patient_name = st.text_input("Full Name", placeholder="Enter your full name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with pat_col2:
    patient_age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1)
with pat_col3:
    pat_height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.1, key="pat_height")
    pat_weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1, key="pat_weight")

st.markdown('</div>', unsafe_allow_html=True)

# Compute BMI from patient details
pat_bmi = None
pat_bmi_category = ""
if pat_height_cm > 0:
    pat_height_m = pat_height_cm / 100
    pat_bmi = pat_weight_kg / (pat_height_m ** 2)
    if pat_bmi < 18.5:
        pat_bmi_category = "Underweight"
    elif pat_bmi < 25:
        pat_bmi_category = "Normal"
    elif pat_bmi < 30:
        pat_bmi_category = "Overweight"
    else:
        pat_bmi_category = "Obese"

# ---------------- SYMPTOM SELECTION SECTION ----------------
st.markdown('<div class="card"><div class="section-title">Symptom Selection</div>', unsafe_allow_html=True)

display_columns = [col.replace("_", " ").title() for col in columns]
symptom_mapping = dict(zip(display_columns, columns))

selected_display_symptoms = st.multiselect(
    "Select all symptoms you are currently experiencing:",
    display_columns
)

selected_symptoms = [symptom_mapping[s] for s in selected_display_symptoms]

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CITY INPUT ----------------
st.markdown('<div class="card"><div class="section-title">Find Nearby Medical Facilities</div>', unsafe_allow_html=True)
city = st.text_input("Enter Your City", placeholder="Example: Mumbai, Delhi, Kolkata")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DISEASE INFO DICTIONARY ----------------
disease_info = {
    "Fungal infection": {
        "Description": "A fungal infection is caused by fungi and can affect the skin, nails, and internal organs.",
        "Precautions": "Keep skin dry and clean, avoid sharing personal items, wear breathable clothing.",
        "When to see doctor": "If symptoms persist more than 2 weeks or spread rapidly."
    },
    "Allergy": {
        "Description": "An allergy is an immune system reaction to a foreign substance that's not typically harmful.",
        "Precautions": "Avoid known allergens, carry antihistamines, keep an allergy journal.",
        "When to see doctor": "If you experience difficulty breathing, swelling, or severe reactions."
    },
    "GERD": {
        "Description": "Gastroesophageal reflux disease (GERD) is a chronic digestive disorder where stomach acid flows back into the esophagus.",
        "Precautions": "Avoid spicy/fatty foods, eat smaller meals, don't lie down immediately after eating.",
        "When to see doctor": "If symptoms occur more than twice a week or over-the-counter medications don't help."
    },
    "Chronic cholestasis": {
        "Description": "A condition where bile flow from the liver is reduced or blocked.",
        "Precautions": "Avoid alcohol, follow a low-fat diet, take prescribed vitamins.",
        "When to see doctor": "If you experience jaundice, severe itching, or dark urine."
    },
    "Drug Reaction": {
        "Description": "An adverse drug reaction is an unintended harmful reaction to a medication.",
        "Precautions": "Always inform doctors about all medications you take, never self-medicate.",
        "When to see doctor": "Immediately if you experience rash, difficulty breathing, or swelling."
    },
    "Peptic ulcer disease": {
        "Description": "Sores that develop on the lining of the stomach, small intestine, or esophagus.",
        "Precautions": "Avoid NSAIDs, limit alcohol, quit smoking, manage stress.",
        "When to see doctor": "If you have severe abdominal pain, blood in stool, or vomiting blood."
    },
    "AIDS": {
        "Description": "Acquired immunodeficiency syndrome, caused by HIV, weakens the immune system.",
        "Precautions": "Practice safe sex, avoid sharing needles, regular HIV testing.",
        "When to see doctor": "Immediately upon suspected exposure or positive HIV test."
    },
    "Diabetes": {
        "Description": "A chronic condition that affects how the body processes blood sugar (glucose).",
        "Precautions": "Monitor blood sugar regularly, maintain healthy diet, exercise regularly.",
        "When to see doctor": "If you experience frequent urination, excessive thirst, unexplained weight loss."
    },
    "Gastroenteritis": {
        "Description": "Inflammation of the stomach and intestines, typically resulting from a viral or bacterial infection.",
        "Precautions": "Stay hydrated, wash hands frequently, avoid contaminated food/water.",
        "When to see doctor": "If symptoms last more than 3 days, or you see blood in stool."
    },
    "Bronchial Asthma": {
        "Description": "A condition in which airways narrow and swell, producing extra mucus and making breathing difficult.",
        "Precautions": "Avoid triggers, keep rescue inhaler available, follow asthma action plan.",
        "When to see doctor": "If symptoms worsen or your inhaler isn't providing relief."
    },
    "Hypertension": {
        "Description": "High blood pressure, a common condition where the force of blood against artery walls is too high.",
        "Precautions": "Reduce salt intake, exercise regularly, manage stress, avoid smoking.",
        "When to see doctor": "If blood pressure consistently reads above 140/90 mmHg."
    },
    "Migraine": {
        "Description": "A neurological condition causing intense headaches, often accompanied by nausea and sensitivity to light.",
        "Precautions": "Identify and avoid triggers, maintain regular sleep, stay hydrated.",
        "When to see doctor": "If headaches are severe, frequent, or accompanied by neurological symptoms."
    },
    "Cervical spondylosis": {
        "Description": "Age-related wear and tear affecting the spinal disks in the neck.",
        "Precautions": "Maintain good posture, do neck exercises, use ergonomic furniture.",
        "When to see doctor": "If you experience numbness, tingling, or weakness in arms/hands."
    },
    "Paralysis (brain hemorrhage)": {
        "Description": "Loss of muscle function due to bleeding in the brain.",
        "Precautions": "Control blood pressure, avoid smoking, maintain healthy lifestyle.",
        "When to see doctor": "Immediately - this is a medical emergency."
    },
    "Jaundice": {
        "Description": "A condition causing yellowing of skin and eyes due to excess bilirubin.",
        "Precautions": "Avoid alcohol, stay hydrated, follow prescribed diet.",
        "When to see doctor": "Immediately upon noticing yellow discoloration of skin or eyes."
    },
    "Malaria": {
        "Description": "A mosquito-borne infectious disease affecting red blood cells.",
        "Precautions": "Use mosquito repellent, sleep under nets, take preventive medications when traveling.",
        "When to see doctor": "Immediately if you have fever after visiting malaria-prone areas."
    },
    "Chicken pox": {
        "Description": "A highly contagious viral infection causing an itchy rash with blister-like sores.",
        "Precautions": "Isolate from others, avoid scratching, keep sores clean.",
        "When to see doctor": "If symptoms are severe or you're immunocompromised."
    },
    "Dengue": {
        "Description": "A mosquito-borne tropical disease causing severe flu-like illness.",
        "Precautions": "Use mosquito repellent, eliminate standing water, wear protective clothing.",
        "When to see doctor": "Immediately if you have high fever with severe headache or bleeding."
    },
    "Typhoid": {
        "Description": "A bacterial infection due to Salmonella typhi, spread through contaminated food/water.",
        "Precautions": "Drink clean water, eat properly cooked food, practice good hygiene.",
        "When to see doctor": "If you have sustained high fever lasting more than 3 days."
    },
    "Hepatitis A": {
        "Description": "A viral liver infection transmitted through contaminated food and water.",
        "Precautions": "Get vaccinated, practice good hygiene, avoid contaminated food/water.",
        "When to see doctor": "If you experience jaundice, severe fatigue, or abdominal pain."
    },
    "Hepatitis B": {
        "Description": "A viral infection that attacks the liver and can cause chronic disease.",
        "Precautions": "Get vaccinated, practice safe sex, avoid sharing needles.",
        "When to see doctor": "Immediately upon possible exposure or if you notice symptoms."
    },
    "Hepatitis C": {
        "Description": "A viral infection causing liver inflammation, sometimes leading to serious liver damage.",
        "Precautions": "Avoid sharing needles, practice safe sex, don't share personal items.",
        "When to see doctor": "Get tested if you've had potential exposure; see doctor immediately if symptomatic."
    },
    "Hepatitis D": {
        "Description": "A liver infection caused by hepatitis D virus, only occurring alongside hepatitis B.",
        "Precautions": "Get hepatitis B vaccination, avoid sharing needles.",
        "When to see doctor": "If you have hepatitis B and notice worsening symptoms."
    },
    "Hepatitis E": {
        "Description": "A liver disease caused by the hepatitis E virus, spread through contaminated water.",
        "Precautions": "Drink clean water, practice good hygiene, avoid raw/undercooked meat.",
        "When to see doctor": "If you develop jaundice or severe abdominal pain."
    },
    "Alcoholic hepatitis": {
        "Description": "Liver inflammation caused by excessive alcohol consumption.",
        "Precautions": "Stop alcohol consumption, eat nutritious food, stay hydrated.",
        "When to see doctor": "Immediately - this is a serious condition requiring medical care."
    },
    "Tuberculosis": {
        "Description": "A serious infectious disease that mainly affects the lungs.",
        "Precautions": "Complete full course of medication, cover mouth when coughing, ensure good ventilation.",
        "When to see doctor": "If you have persistent cough lasting more than 3 weeks."
    },
    "Common Cold": {
        "Description": "A viral infection of the upper respiratory tract.",
        "Precautions": "Rest, stay hydrated, wash hands frequently.",
        "When to see doctor": "If symptoms last more than 10 days or are accompanied by high fever."
    },
    "Pneumonia": {
        "Description": "An infection that inflames air sacs in one or both lungs.",
        "Precautions": "Get vaccinated, practice good hygiene, avoid smoking.",
        "When to see doctor": "Immediately if you have difficulty breathing, chest pain, or high fever."
    },
    "Dimorphic hemorrhoids (piles)": {
        "Description": "Swollen veins in the lowest part of the rectum and anus.",
        "Precautions": "Eat high-fiber diet, stay hydrated, avoid straining during bowel movements.",
        "When to see doctor": "If you notice rectal bleeding or severe pain."
    },
    "Heart attack": {
        "Description": "Occurs when blood flow to the heart is blocked.",
        "Precautions": "Maintain healthy lifestyle, control blood pressure and cholesterol, avoid smoking.",
        "When to see doctor": "Call emergency services immediately - this is a life-threatening emergency."
    },
    "Varicose veins": {
        "Description": "Enlarged, twisted veins visible just under the skin surface.",
        "Precautions": "Exercise regularly, elevate legs, avoid standing for long periods.",
        "When to see doctor": "If veins are painful, cause skin changes, or develop sores."
    },
    "Hypothyroidism": {
        "Description": "A condition where the thyroid gland doesn't produce enough thyroid hormone.",
        "Precautions": "Take medication as prescribed, eat iodine-rich foods, exercise regularly.",
        "When to see doctor": "If you have unexplained weight gain, fatigue, or cold sensitivity."
    },
    "Hyperthyroidism": {
        "Description": "A condition where the thyroid gland produces too much thyroid hormone.",
        "Precautions": "Follow treatment plan, avoid excess iodine, manage stress.",
        "When to see doctor": "If you have rapid heartbeat, unexplained weight loss, or tremors."
    },
    "Hypoglycemia": {
        "Description": "Abnormally low blood sugar levels.",
        "Precautions": "Eat regular meals, carry fast-acting sugar, monitor blood glucose.",
        "When to see doctor": "If episodes are frequent or you lose consciousness."
    },
    "Osteoarthritis": {
        "Description": "A degenerative joint disease causing breakdown of joint cartilage.",
        "Precautions": "Maintain healthy weight, exercise regularly, protect joints from injury.",
        "When to see doctor": "If joint pain significantly impacts daily activities."
    },
    "Arthritis": {
        "Description": "Inflammation of one or more joints, causing pain and stiffness.",
        "Precautions": "Stay active, maintain healthy weight, protect joints.",
        "When to see doctor": "If joint pain is severe, persistent, or accompanied by swelling."
    },
    "Vertigo": {
        "Description": "A sensation of feeling off balance or that surroundings are spinning.",
        "Precautions": "Move slowly, avoid sudden movements, use safety rails.",
        "When to see doctor": "If vertigo is severe, recurring, or accompanied by hearing loss."
    },
    "Acne": {
        "Description": "A skin condition occurring when hair follicles become plugged with oil and dead skin cells.",
        "Precautions": "Keep skin clean, avoid touching face, use non-comedogenic products.",
        "When to see doctor": "If acne is severe, cystic, or causing scarring."
    },
    "Urinary tract infection": {
        "Description": "An infection in any part of the urinary system.",
        "Precautions": "Stay hydrated, urinate after sex, wipe front to back.",
        "When to see doctor": "If symptoms persist after 2 days or you have fever and back pain."
    },
    "Psoriasis": {
        "Description": "A skin disease causing red, itchy, scaly patches.",
        "Precautions": "Moisturize regularly, avoid triggers, manage stress.",
        "When to see doctor": "If symptoms are severe or affect quality of life."
    },
    "Impetigo": {
        "Description": "A highly contagious bacterial skin infection causing sores.",
        "Precautions": "Keep skin clean, avoid touching sores, don't share personal items.",
        "When to see doctor": "Immediately - requires antibiotic treatment."
    }
}

# ---------------- HOSPITAL FUNCTION ----------------
def get_nearby_hospitals(city):
    try:
        geocode_url = "https://nominatim.openstreetmap.org/search"
        geocode_params = {
            "q": city,
            "format": "json",
            "limit": 1
        }

        geocode_response = requests.get(
            geocode_url,
            params=geocode_params,
            headers={"User-Agent": "health-insight-app"}
        )

        if geocode_response.status_code != 200:
            return []

        geocode_data = geocode_response.json()
        if not geocode_data:
            return []

        lat = geocode_data[0]["lat"]
        lon = geocode_data[0]["lon"]

        overpass_url = "https://overpass-api.de/api/interpreter"

        query = f"""
        [out:json][timeout:25];
        (
          node["amenity"="hospital"](around:15000,{lat},{lon});
          way["amenity"="hospital"](around:15000,{lat},{lon});
          relation["amenity"="hospital"](around:15000,{lat},{lon});
        );
        out center 20;
        """

        response = requests.post(overpass_url, data=query)

        if response.status_code != 200:
            return []

        data = response.json()
        hospitals = []

        for element in data.get("elements", []):
            name = element.get("tags", {}).get("name", "Medical Facility")

            tags = element.get("tags", {})
            address_parts = [
                tags.get("addr:housenumber", ""),
                tags.get("addr:street", ""),
                tags.get("addr:city", ""),
                tags.get("addr:postcode", "")
            ]
            address = ", ".join([part for part in address_parts if part])

            if "lat" in element:
                h_lat = element["lat"]
                h_lon = element["lon"]
            else:
                h_lat = element.get("center", {}).get("lat")
                h_lon = element.get("center", {}).get("lon")

            if h_lat and h_lon:
                hospitals.append({
                    "Hospital Name": name,
                    "Address": address if address else None,
                    "Google Maps": f"https://www.google.com/maps?q={h_lat},{h_lon}"
                })

        return hospitals[:5]

    except:
        return []

# ---------------- SAVE HISTORY FUNCTION ----------------
def save_to_history(symptoms, primary_condition, probability, name, age, gender, bmi):
    filename = "user_history.csv"
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "Date/Time", "Name", "Age", "Gender", "BMI",
                "Symptoms", "Primary Condition", "Probability (%)"
            ])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name if name else "N/A",
            age,
            gender,
            f"{bmi:.2f}" if bmi else "N/A",
            ", ".join(symptoms),
            primary_condition,
            f"{probability * 100:.2f}"
        ])

# ---------------- PDF GENERATION FUNCTION ----------------
def generate_pdf(symptoms, top3, severity_level, city,
                 patient_name, patient_age, gender,
                 pat_height_cm, pat_weight_kg, pat_bmi, pat_bmi_category):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=18, spaceAfter=12)
        heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=13, spaceAfter=8)
        normal_style = styles['Normal']

        story.append(Paragraph("Health Insight & Support System", title_style))
        story.append(Paragraph("Health Analysis Report", heading_style))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        if city:
            story.append(Paragraph(f"City: {city}", normal_style))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Patient Details", heading_style))
        patient_data = [
            ["Name", patient_name if patient_name else "N/A"],
            ["Age", str(patient_age)],
            ["Gender", gender],
            ["Height", f"{pat_height_cm} cm"],
            ["Weight", f"{pat_weight_kg} kg"],
            ["BMI", f"{pat_bmi:.2f} — {pat_bmi_category}" if pat_bmi else "N/A"],
        ]
        pt = Table(patient_data, colWidths=[2 * inch, 3.5 * inch])
        pt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(pt)
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Selected Symptoms", heading_style))
        for sym in symptoms:
            story.append(Paragraph(f"• {sym.replace('_', ' ').title()}", normal_style))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Top 3 Predicted Conditions", heading_style))
        data = [["Condition", "Probability"]]
        for _, row in top3.iterrows():
            data.append([row["Condition"], f"{row['Probability'] * 100:.2f}%"])
        t = Table(data, colWidths=[3.5 * inch, 1.5 * inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph(f"Severity Level: {severity_level}", heading_style))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph(
            "Disclaimer: This report is generated by an AI-based system and is not a substitute for "
            "professional medical advice. Please consult a qualified healthcare professional for proper diagnosis and treatment.",
            ParagraphStyle('Disclaimer', parent=styles['Normal'], textColor=colors.red, fontSize=9)
        ))

        doc.build(story)
        buffer.seek(0)
        return buffer
    except ImportError:
        return None

# ---------------- PREPARE INPUT ----------------
input_data = np.zeros(len(columns))

for symptom in selected_symptoms:
    index = columns.index(symptom)
    input_data[index] = 1

# ---------------- BMI CALCULATOR ----------------
st.markdown('<div class="card"><div class="section-title">BMI Calculator</div>', unsafe_allow_html=True)

bmi_col1, bmi_col2 = st.columns(2)
with bmi_col1:
    height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=pat_height_cm, step=0.1, key="bmi_height")
with bmi_col2:
    weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=pat_weight_kg, step=0.1, key="bmi_weight")

if height_cm > 0:
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    st.write(f"**Your BMI: {bmi:.2f}**")
    if bmi < 18.5:
        st.info("Category: Underweight")
    elif bmi < 25:
        st.success("Category: Normal")
    elif bmi < 30:
        st.warning("Category: Overweight")
    else:
        st.error("Category: Obese")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYZE BUTTON ----------------
st.markdown("<div style='margin: 8px 0 4px 0;'>", unsafe_allow_html=True)
if st.button("Analyze Symptoms"):

    if not selected_symptoms:
        st.warning("Please select at least one symptom to proceed.")
    else:

        probabilities = model.predict_proba([input_data])[0]

        prob_df = pd.DataFrame({
            "Condition": model.classes_,
            "Probability": probabilities
        }).sort_values(by="Probability", ascending=False)

        top3 = prob_df.head(3)

        primary = top3.iloc[0]["Condition"]
        second = top3.iloc[1]["Condition"]
        third = top3.iloc[2]["Condition"]
        primary_prob = top3.iloc[0]["Probability"]

        # ---------------- SYMPTOM INTERPRETATION ----------------
        st.markdown('<div class="card"><div class="section-title">Symptom Interpretation</div>', unsafe_allow_html=True)
        st.write(
            f"Based on the selected symptoms, the most likely condition is **{primary}**. "
            f"Similar symptom patterns are also associated with **{second}** and **{third}**. "
            f"Symptoms can overlap across multiple conditions — monitoring changes over time and seeking professional consultation is advised."
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- BASIC HEALTH ADVICE SECTION ----------------
        st.markdown('<div class="card"><div class="section-title">General Care Guidance</div>', unsafe_allow_html=True)

        if any(sym in selected_symptoms for sym in ["fever", "cough", "fatigue"]):
            st.write("• Prioritize rest and allow the body adequate recovery time.")
            st.write("• Maintain sufficient fluid intake throughout the day.")
            st.write("• Warm fluids such as soups or herbal teas may provide comfort.")

        if any(sym in selected_symptoms for sym in ["headache", "stress"]):
            st.write("• Reduce screen time and take regular short breaks.")
            st.write("• Controlled breathing exercises and light stretching may alleviate tension.")

        if any(sym in selected_symptoms for sym in ["joint_pain", "muscle_pain"]):
            st.write("• Gentle activity and proper hydration can support recovery.")
            st.write("• Avoid physical overexertion for several days.")

        st.write("If symptoms persist beyond several days or worsen in intensity, consult a qualified healthcare professional promptly.")
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- TOP 3 PREDICTIONS WITH PROGRESS BARS ----------------
        st.markdown('<div class="card"><div class="section-title">Top 3 Predicted Conditions</div>', unsafe_allow_html=True)

        for _, row in top3.iterrows():
            cond = row["Condition"]
            prob = row["Probability"]
            st.markdown(f"""
            <div class="prediction-item">
                <div class="prediction-label">{cond}</div>
                <div class="prediction-pct">Probability: {prob * 100:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(float(prob))

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- SEVERITY LEVEL INDICATOR ----------------
        st.markdown('<div class="card"><div class="section-title">Risk Level Assessment</div>', unsafe_allow_html=True)

        if primary_prob >= 0.70:
            severity_level = "High Risk"
            st.error(f"High Risk — The primary condition has a {primary_prob * 100:.2f}% probability. Please seek medical attention promptly.")
        elif primary_prob >= 0.40:
            severity_level = "Moderate Risk"
            st.warning(f"Moderate Risk — The primary condition has a {primary_prob * 100:.2f}% probability. Monitor symptoms closely and consider consulting a physician.")
        else:
            severity_level = "Low Risk"
            st.success(f"Low Risk — The primary condition has a {primary_prob * 100:.2f}% probability. Maintain healthy habits and observe any changes.")

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- DISEASE INFORMATION SECTION ----------------
        st.markdown(f'<div class="card"><div class="section-title">Condition Information: {primary}</div>', unsafe_allow_html=True)

        if primary in disease_info:
            info = disease_info[primary]
            st.markdown(f"""
            <div class="disease-card">
                <div class="disease-field"><strong>Description:</strong> {info['Description']}</div>
                <div class="disease-field"><strong>Precautions:</strong> {info['Precautions']}</div>
                <div class="disease-field"><strong>When to See a Doctor:</strong> {info['When to see doctor']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Condition information is currently unavailable for this diagnosis.")

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- SAVE USER HISTORY ----------------
        save_to_history(
            selected_symptoms, primary, primary_prob,
            patient_name, patient_age, gender, pat_bmi
        )

        # ---------------- DOWNLOADABLE PDF REPORT ----------------
        st.markdown('<div class="card"><div class="section-title">Download Health Report</div>', unsafe_allow_html=True)

        pdf_buffer = generate_pdf(
            selected_symptoms, top3, severity_level, city,
            patient_name, patient_age, gender,
            pat_height_cm, pat_weight_kg, pat_bmi, pat_bmi_category
        )

        if pdf_buffer:
            st.download_button(
                label="Download Health Report (PDF)",
                data=pdf_buffer,
                file_name=f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        else:
            st.info("PDF generation requires the 'reportlab' library. Install it with: pip install reportlab")

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- HOSPITAL SECTION ----------------
        # FIX: Each hospital card rendered via st.markdown(..., unsafe_allow_html=True)
        # to ensure links are clickable and HTML is properly interpreted by Streamlit.
        if city:
            st.markdown(f'<div class="card"><div class="section-title">Nearby Medical Facilities &#8212; {city}</div>', unsafe_allow_html=True)

            with st.spinner("Locating nearby hospitals..."):
                hospitals = get_nearby_hospitals(city)

            if hospitals:
                for hospital in hospitals:
                    address_html = (
                        f'<div class="hospital-address">&#128205; {hospital["Address"]}</div>'
                        if hospital["Address"] else ""
                    )
                    maps_url = hospital["Google Maps"]
                    hospital_name = hospital["Hospital Name"]

                    st.markdown(
                        f'<div class="hospital-card">'
                        f'<div class="hospital-name">{hospital_name}</div>'
                        f'{address_html}'
                        f'<div class="hospital-link">'
                        f'<a href="{maps_url}" target="_blank" rel="noopener noreferrer">'
                        f'View on Google Maps &#8594;</a></div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.info("Unable to retrieve nearby hospital data at this time. Please try again.")

            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MEDICAL DISCLAIMER ----------------
st.markdown("""
<hr style="border-top: 2px solid #e0e0e0; margin-top: 28px; margin-bottom: 12px;">
<div class="footer-disclaimer">
    &#9888; Disclaimer: This system provides AI-based insights and is not a substitute for professional medical advice.
    Always consult a qualified healthcare professional for proper diagnosis and treatment.
</div>
""", unsafe_allow_html=True)
