import streamlit as st
import pandas as pd
import joblib

model = joblib.load('model.pkl')
encoders = joblib.load('label_encoder.pkl')

st.title("🎯 Job Change Prediction")

city = st.number_input("City Code", min_value=0, max_value=200, value=5)
city_development_index = st.slider("City Development Index", 0.0, 1.0, 0.7)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
relevent_experience = st.selectbox("Relevant Experience", ["Has relevent experience", "No relevent experience"])
enrolled_university = st.selectbox("Enrolled in University", ["no_enrollment", "Full time course", "Part time course"])
education_level = st.selectbox("Education Level", ["Graduate", "Masters", "Phd", "High School", "Primary School"])
major_discipline = st.selectbox("Major Discipline", ["STEM", "Business Degree", "Arts", "Humanities", "No Major", "Other"])
experience = st.selectbox("Years of Experience", ["<1","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20",">20"])
company_size = st.selectbox("Company Size", ["<10","10/49","50-99","100-500","500-999","1000-4999","5000-9999","10000+"])
company_type = st.selectbox("Company Type", ["Pvt Ltd","Funded Startup","Public Sector","Early Stage Startup","NGO","Other"])
last_new_job = st.selectbox("Years Since Last Job", ["never","1","2","3","4",">4"])
training_hours = st.number_input("Training Hours", min_value=0, max_value=400, value=50)

if st.button("Predict"):
    input_dict = {
        'city': city,
        'city_development_index': city_development_index,
        'gender': gender,
        'relevent_experience': relevent_experience,
        'enrolled_university': enrolled_university,
        'education_level': education_level,
        'major_discipline': major_discipline,
        'experience': experience,
        'company_size': company_size,
        'company_type': company_type,
        'last_new_job': last_new_job,
        'training_hours': training_hours,
    }
    input_df = pd.DataFrame([input_dict])
    for col in input_df.select_dtypes(include=['object']).columns:
        if col in encoders:
            input_df[col] = encoders[col].transform(input_df[col])
    try:
        prediction = model.predict(input_df)[0]
        if prediction == 1:
            st.success("✅ This candidate IS looking for a job change.")
        else:
            st.info("🔒 This candidate is NOT looking for a job change.")
    except Exception as e:
        st.error(f"Error: {e}")
