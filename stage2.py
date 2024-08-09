import streamlit as st

def stage_2():
    st.title("Stage 2")
    st.write("This is the content for Stage 2.")
    option2 = st.radio("Select a choice for Stage 2:", ["Choice 1", "Choice 2", "Choice 3"])
    st.write(f"You chose: {option2}")
