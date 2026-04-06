import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Insider Threat Detection", layout="centered")
st.title("🔐 Insider Threat Detection System")

st.write("Upload a CSV file to detect suspicious users based on login activity.")

# File upload
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        st.subheader("📄 Dataset Preview")
        st.dataframe(data)

        # Accept both 'login_attempts' and 'login attempts' column names
        if 'login_attempts' in data.columns:
            col_name = 'login_attempts'
        elif 'login attempts' in data.columns:
            col_name = 'login attempts'
        else:
            st.error("❌ CSV must contain 'login_attempts' or 'login attempts' column")
            st.stop()

        # Risk detection
        data["Risk Level"] = data[col_name].apply(lambda x: "High" if x > 5 else "Low")

        st.subheader("⚠️ Risk Analysis")
        st.dataframe(data)

        # High risk users
        high_risk = data[data["Risk Level"] == "High"]
        st.subheader("🚨 High Risk Users")
        if len(high_risk) > 0:
            st.dataframe(high_risk)
        else:
            st.success("No high risk users found ✅")

        # Risk graph
        st.subheader("📊 Risk Distribution")
        risk_counts = data["Risk Level"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(risk_counts.index, risk_counts.values)
        ax.set_xlabel("Risk Level")
        ax.set_ylabel("Number of Users")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("⬆️ Please upload a CSV file to continue")