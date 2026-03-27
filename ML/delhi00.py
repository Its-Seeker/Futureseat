import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    df = pd.read_csv("D:/combined_all_colleges.csv")  # Keep this file in same folder
    df.columns = df.columns.str.strip().str.lower()
    return df


df = load_data()

st.title("Delhi College Predictor")

rank = st.number_input("Enter your JEE Rank", min_value=1, step=1)
category = st.selectbox("Select Category", ["GEN", "OBC", "SC", "ST", "EWS"])
branch = st.selectbox("Preferred Branch",
                      ["ALL", "CSE", "IT", "ECE", "EE", "ME", "CE", "CHE", "AE", "SE", "MAC", "DS-AI", "AI-ML", "BT"])
gender = st.selectbox("Gender", ["Male", "Female"])


def predict_colleges(rank, category, branch, gender, df):
    result = df.copy()


    result = result[result["category"] == category]

    #
    result = result[result["special"].fillna("") == ""]


    if gender == "Female":
        result = result[result["gender"].isin(["Male", "Female"])]
    else:
        result = result[result["gender"] == "Male"]


    if branch != "ALL":
        result = result[result["branch"].str.contains(branch, case=False, na=False)]


    result = result[result["closing_rank"] >= rank]


    def chance(row):
        if row["opening_rank"] <= rank <= row["closing_rank"]:
            return "✅ Safe"
        return "🟡 Good"

    result["chance"] = result.apply(chance, axis=1)
    result = result.sort_values(["chance", "closing_rank"])

    return result[["college", "branch", "opening_rank",
                   "closing_rank", "chance"]].reset_index(drop=True)


if st.button("Predict Colleges"):
    results = predict_colleges(rank, category, branch, gender, df)
    if results.empty:
        st.error("No colleges found. Try a higher rank or change filters.")
    else:
        st.success(f"Found {len(results)} possible college(s)!")
        st.dataframe(results, use_container_width=True)