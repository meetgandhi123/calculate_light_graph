import streamlit as st
from processor import process_layers  # Import the processing function

def reset_inputs():
    # Clear all session state values to reset the form
    st.session_state.clear()

def stage_1():
    if "num_layers" not in st.session_state:
        st.session_state.num_layers = 1
    if "height" not in st.session_state:
        st.session_state.height = 0.00

    num_layers = st.session_state.num_layers
    height = st.session_state.height

    # Step 1: Get the number of layers
    num_layers = st.number_input("Enter the number of layers", value=num_layers, min_value=1, step=1, key="num_layers")

    # Step 2: Generate the dropdowns for material selection based on the number of layers
    if num_layers > 0:
        st.write(f"You selected {num_layers} layers.")

        selected_materials = []
        material_choices = ["silver", "aluminum", "gold", "chromium", "copper", "germanium"]  # Example materials

        for i in range(num_layers):
            key = f"material_{i}"
            material = st.selectbox(f"Select material for layer {i+1}", material_choices, key=key)
            selected_materials.append(material)

        # Store the selected materials in the session state
        st.session_state["materials"] = selected_materials

    # Step 3: Input for the height
    height = st.number_input("Enter the height (in meters)", min_value=0.0, step=0.01, format="%.2f", key="height")

    # Calculate Button
    if st.button("Calculate"):
        if "materials" in st.session_state:
            # Process the materials and get the dictionary
            thickness = [0.7,0.9]
            material = ["silver","chromium"]
            chart_data = process_layers(material, thickness)
            # chart_data = process_layers(st.session_state["materials"], st.session_state["height"])
            # Display the result
            st.write("Processed Data:")            
            st.pyplot(chart_data)
        else:
            st.warning("Please complete all inputs before calculating.")

    # Reset Button
    if st.button("Reset"):
        reset_inputs()

# Run the function to display the form
stage_1()
