import streamlit as st
from home import home_page
from stage1 import stage_1

# Sidebar dropdown
page = st.sidebar.selectbox("Select Stage", ["Home Page", "Stage 1", "Stage 2"])

# Page content based on dropdown selection
if page == "Home Page":
    home_page()

elif page == "Stage 1":
    stage_1()

elif page == "Stage 2":
    #stage_2()
    pass

