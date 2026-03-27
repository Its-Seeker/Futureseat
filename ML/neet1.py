# import numpy as np
# from scipy.interpolate import interp1d
# import streamlit as st
#
# marks_data = [720,700,680,650,620,600,580,550,520,500,480,450,420,400,380,350,320,300,250,200,150,100,50,0]
#
# rank_data  = [1,50,200,1000,3000,5000,8000,15000,25000,40000,60000,90000,130000,180000,230000,300000,380000,450000,650000,900000,1200000,1500000,1800000,2000000]
#
# marks_data_rev=marks_data[::1]
# rank_data_rev=rank_data[::1]
#
# model=interp1d(marks_data_rev,rank_data_rev)
# def predict_rank(marks):
#     marks=max(0,min(720,marks))
#     return int(model(marks))
#
# def predict_percentile(rank, total=2000000):
#     return round((1 - rank/total)*100, 3)
#
# def rank_range(rank):
#     return (int(rank*0.9), int(rank*1.1))
#
# import streamlit as st
#
# st.title("NEET Rank Predictor")
#
# marks = st.slider("Enter Marks", 0, 720, 300)
#
# rank = predict_rank(marks)
# percentile = predict_percentile(rank)
#
# st.write("Predicted Rank:", rank)
# st.write("Percentile:", percentile)

import streamlit as st
import numpy as np


marks_data = [720,700,680,650,620,600,580,550,520,500,480,450,420,400,380,350,320,300,250,200,150,100,50,0]

rank_data  = [1,50,200,1000,3000,5000,8000,15000,25000,40000,60000,90000,130000,180000,230000,300000,380000,450000,650000,900000,1200000,1500000,1800000,2000000]



def predict_rank(marks):
    return int(np.interp(marks, marks_data[::-1], rank_data[::-1]))

def predict_percentile(rank, total=2000000):
    return round((1 - rank/total)*100, 3)

def rank_range(rank):
    return (int(rank*0.9), int(rank*1.1))



st.set_page_config(page_title="NEET Predictor", layout="centered")

st.title("🎯 NEET Rank & Percentile Predictor")

marks = st.text_input("Enter your NEET marks (0 - 720)")

if st.button("Predict"):
    if marks == "":
        st.warning("Please enter marks")
    else:
        try:
            marks = int(marks)

            if marks < 0 or marks > 720:
                st.error("Marks must be between 0 and 720")
            else:
                rank = predict_rank(marks)
                percentile = predict_percentile(rank)
                low, high = rank_range(rank)

                st.success("Prediction Result 👇")

                st.write(f"📊 Marks: {marks}")
                st.write(f"🏆 Predicted Rank: {rank}")
                st.write(f"📉 Percentile: {percentile}")
                st.write(f"📌 Rank Range: {low} - {high}")

        except:
            st.error("Enter a valid number")