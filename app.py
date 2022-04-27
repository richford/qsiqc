#!/opt/conda/bin/python

import pandas as pd
import streamlit as st
import time
import json

from predict_ratings import predict_ratings

if "example" not in st.session_state:
    st.session_state["example"] = False


def input_detected():
    st.session_state["example"] = False


@st.cache
def load_data(input_file):
    if input_file.endswith(".csv"):
        df = pd.read_csv(input_file, index_col="subject_id")
    elif input_file.endswith(".json"):
        with open(input_file) as f:
            dd = json.loads(f.read())
            df = pd.DataFrame(dd["subjects"])
            df = df.set_index("subject_id")
    return df


@st.cache
def predict(input_df):
    return predict_ratings(input_df=input_df)


@st.cache
def convert_df(df):
    # Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


def display_input_output(uploaded_file):
    st.subheader("Input Dataset")

    with st.spinner(text="Loading input..."):
        df_input = load_data(uploaded_file)
        st.dataframe(df_input)

    st.subheader("Predicted QC Ratings")

    with st.spinner(text="Calculating QC ratings..."):
        df_ratings = predict(df_input)
        st.dataframe(df_ratings)

        csv = convert_df(df_ratings)
        st.download_button(
            label="Download QC ratings as CSV",
            data=csv,
            file_name="qsiqc_ratings.csv",
            mime="text/csv",
            key=uploaded_file,
        )


######################################
# Page layout
######################################
st.set_page_config(
    page_title="Predict QSIPrep QC Ratings", page_icon="🧠", layout="wide"
)

######################################
## Page Title and sub title
######################################
st.title("Predict QSIPrep QC Ratings")
st.write("**Made By: [Adam Richie-Halford](https://richiehalford.org)**")
st.write(
    "This app predicts quality ratings for diffusion MRI data using "
    "automated metrics generated from QSIPrep."
)

######################################
## Sidebar
######################################
# Input your csv
st.sidebar.header("Upload your QSIPrep QC metrics")
uploaded_file = st.sidebar.file_uploader(
    "Upload your input CSV/JSON file",
    type=["csv", "json"], on_change=input_detected
)
if st.sidebar.button("or click here to use an example dataset"):
    uploaded_file = (
        "https://raw.githubusercontent.com/richford/qsiqc/main/example_dwiqc.csv"
    )
    display_input_output(uploaded_file)
    st.session_state["example"] = True

######################################
# Main panel
######################################

if uploaded_file is None:
    st.info("Awaiting input CSV/JSON file...")
else:
    if not st.session_state.example:
        display_input_output(uploaded_file)
