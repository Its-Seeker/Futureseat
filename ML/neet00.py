# import streamlit as st
# import pandas as pd
#
# @st.cache_data
# def load_data():
#     df = pd.read_csv("D:/neet_colleges_comprehensive.csv")
#     df.columns = df.columns.str.strip().str.lower()
#     return df
#
# df = load_data()
#
# st.title("NEET College Predictor 🏥")
#
#
# rank = st.number_input("Enter your NEET Rank", min_value=1, step=1)
# category = st.selectbox("Select Category", ["GEN", "OBC", "SC", "ST", "EWS"])
# state = st.selectbox("State Preference", ["ALL"] + sorted(df["state"].dropna().unique()))
# college_type = st.selectbox("College Type", ["ALL", "Government", "Private"])
#
#
# def predict_colleges(rank, category, state, college_type, df):
#     result = df.copy()
#
#
#     if "category" in result.columns:
#         result = result[result["category"].str.upper() == category]
#
#
#     if state != "ALL" and "state" in result.columns:
#         result = result[result["state"] == state]
#
#
#     if college_type != "ALL" and "college_type" in result.columns:
#         result = result[result["college_type"].str.lower() == college_type.lower()]
#
#
#     result = result[result["closing_rank"] >= rank]
#
#
#     def chance(row):
#         if rank < row["opening_rank"]:
#             return "🔥 Very Safe"
#         elif row["opening_rank"] <= rank <= row["closing_rank"]:
#             return "✅ Safe"
#         elif rank <= row["closing_rank"] * 1.1:
#             return "🟡 Borderline"
#         else:
#             return "❌ Low"
#
#     result["chance"] = result.apply(chance, axis=1)
#
#     result = result.sort_values(by=["closing_rank"])
#
#     return result[[
#         "college", "state", "opening_rank", "closing_rank", "chance"
#     ]].reset_index(drop=True)
#
#
#
# if st.button("Predict Colleges"):
#     results = predict_colleges(rank, category, state, college_type, df)
#
#     if results.empty:
#         st.error("No colleges found. Try different filters or higher rank.")
#     else:
#         st.success(f"Found {len(results)} colleges 🎯")
#         st.dataframe(results, use_container_width=True)
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("D:/neet_colleges_comprehensive.csv")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename common variations → standard names
    df = df.rename(columns={
        "closing rank": "closing_rank",
        "opening rank": "opening_rank",
        "college name": "college",
        "institute": "college",
        "state name": "state",
        "type": "college_type"
    })

    return df


df = load_data()

st.title("NEET College Predictor 🏥")

# Inputs
rank = st.number_input("Enter your NEET Rank", min_value=1, step=1)
category = st.selectbox("Select Category", ["GEN", "OBC", "SC", "ST", "EWS"])

state = "ALL"
if "state" in df.columns:
    state = st.selectbox(
        "State Preference",
        ["ALL"] + sorted(df["state"].dropna().unique())
    )

college_type = "ALL"
if "college_type" in df.columns:
    college_type = st.selectbox(
        "College Type",
        ["ALL"] + sorted(df["college_type"].dropna().unique())
    )


# Prediction function
def predict_colleges(rank, category, state, college_type, df):
    result = df.copy()

    # Category filter (safe handling)
    if "category" in result.columns:
        result = result[result["category"].astype(str).str.upper() == category]

    # State filter
    if state != "ALL" and "state" in result.columns:
        result = result[result["state"] == state]

    # College type filter
    if college_type != "ALL" and "college_type" in result.columns:
        result = result[result["college_type"].str.lower() == college_type.lower()]

    # Rank filter (IMPORTANT FIX)
    if "closing_rank" not in result.columns:
        st.error("❌ 'closing_rank' column not found in dataset")
        return pd.DataFrame()

    result = result[result["closing_rank"] >= rank]

    # Chance logic
    def chance(row):
        if "opening_rank" in row and rank < row["opening_rank"]:
            return "🔥 Very Safe"
        elif "opening_rank" in row and row["opening_rank"] <= rank <= row["closing_rank"]:
            return "✅ Safe"
        elif rank <= row["closing_rank"] * 1.1:
            return "🟡 Borderline"
        else:
            return "❌ Low"

    result["chance"] = result.apply(chance, axis=1)

    # Select columns safely
    cols = ["college", "state", "opening_rank", "closing_rank", "chance"]
    cols = [c for c in cols if c in result.columns]

    result = result[cols].sort_values(by="closing_rank")

    return result.reset_index(drop=True)


# Button
if st.button("Predict Colleges"):
    results = predict_colleges(rank, category, state, college_type, df)

    if results.empty:
        st.error("No colleges found. Try different filters or higher rank.")
    else:
        st.success(f"Found {len(results)} colleges 🎯")
        st.dataframe(results, use_container_width=True)