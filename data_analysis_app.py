import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt

# initial settings
ready_analysis = False

# st.sidebar.header("Here is a sidebar")
st.title("Basic Data Visualization")
col1, col2 = st.columns(2)
with col1:
    st.caption("bryson_je@hotmail.com")
with col2:
    st.write("**Strength Prediction** [link](https://strengthprediction.herokuapp.com)")
link_openMV = "https://openmv.net"
st.write("We will use a file from **OpenMV.net**: distillation-tower.csv  [link](https://openmv.net)")
st.write("1. Let's start by **uploading** the file")

# upload the csv file
st.sidebar.header("Use this panel for user input")
upload_csv_file = st.sidebar.checkbox("Click here to upload the csv file")
if upload_csv_file:
    df = pd.read_csv("https://openmv.net/file/distillation-tower.csv")
    st.write("File has:", df.shape[1], "columns and:", df.shape[0], "rows")
    st.dataframe(data = df, width = 700, height = 150)
    st.write("2. Select the **amount** and the **variables** and for **analysis**")
    df["time"] = np.arange(0, df.shape[0])
    amount_variables = ["one", "two", "tree", "four"]
    amount_variable = st.sidebar.radio("Select how much variables to analyze:", amount_variables)
    # selecting variables
    if amount_variable:
        column_options = df.columns.tolist()
        if amount_variable == "one":
            columns = st.sidebar.multiselect("Select 1 variable", column_options)
        if amount_variable == "two":
            columns = st.sidebar.multiselect("Select 2 variables", column_options)
        if amount_variable == "tree":
            columns = st.sidebar.multiselect("Select 3 variables", column_options)
        if amount_variable == "four":
            columns = st.sidebar.multiselect("Select 4 variables", column_options)
        ready_analysis = st.sidebar.checkbox("Click here when ready")

# Showing plots
if ready_analysis:
    st.write("3. Here below is the **visualization**")
    if amount_variable == "one" and len(columns) == 1:
        col1, col2 = st.columns(2)
        fig1, ax1 = plt.subplots(figsize = (6, 2.5))
        ax1.hist(df[columns], bins = 40)
        fig2, ax2, = plt.subplots(figsize = (6, 2.5))
        ax2.boxplot(df[columns], vert = False, widths = 0.75)
        with col1:
            st.write("**frequency** plot")
            st.pyplot(fig1)
        with col2:
            st.write("**box** plot")
            st.pyplot(fig2)
        data = df[["time", columns[0]]]
        fig3, ax3 = plt.subplots(figsize = (8, 2))
        sns.lineplot(data = data, x = "time", y = columns[0])
        st.pyplot(fig3)
    if amount_variable == "two" and len(columns) == 2:
        fig, ax = plt.subplots(figsize = (3, 3))
        fig = sns.jointplot(x = df[columns[0]], y = df[columns[1]],
            kind = "scatter", height = 10, marginal_kws = dict(bins = 25, fill = True))
        st.pyplot(fig)
    if amount_variable == "tree" and len(columns) == 3:
        data = df[[columns[0], columns[1], columns[2]]]
        chart = alt.Chart(data).mark_circle(size = 20).encode(x = columns[0], y = columns[1],
        color = columns[2], tooltip = [columns[0], columns[1], columns[2]]).interactive()
        st.altair_chart(chart, use_container_width = True)
        fig, ax = plt.subplots(figsize = (5, 5))
        fig = sns.pairplot(data, height = 4)
        st.pyplot(fig)
    if amount_variable == "four" and len(columns) == 4:
        data = df[[columns[0], columns[1], columns[2], columns[3]]]
        fig, ax = plt.subplots(figsize = (5, 5))
        sns.heatmap(data.corr(), ax = ax, cmap = "YlGnBu", linewidths = 0.1)
        col1, col2 = st.columns(2)
        with col1:
            st.write("**correlation** plot")
            st.pyplot(fig)
        with col2:
            st.write("**basic** data information")
            st.dataframe(data = data.describe())
