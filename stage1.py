import streamlit as st
from processor import process_line_chart
from processor import process_layers  # Import the processing function

def reset_inputs():
    # Clear all session state values to reset the form
    st.session_state.clear()

def stage_1():
    if "num_layers" not in st.session_state:
        st.session_state.num_layers = 1
    if "material_height_0" not in st.session_state:
        st.session_state.material_height_0 = 0.00

    num_layers = st.session_state.num_layers
    #height = st.session_state.height

    # Step 1: Get the number of layers
    num_layers = st.number_input("Enter the number of layers", value=num_layers, min_value=1, step=1, key="num_layers")

    # Step 2: Generate the dropdowns for material selection based on the number of layers
    if num_layers > 0:
        st.write(f"You selected {num_layers} layers.")

        selected_materials = []
        selected_height = []
        material_choices = ["silver", "aluminum","aluminum dioxide", "gold", "chromium", "copper", "germanium","silicon","silicon dioxide","titanium", "titanium dioxide"]  # Example materials

        for i in range(num_layers):
            cols = st.columns(2)
            
            with cols[0]:
                key = f"material_{i}"
                material = st.selectbox(f"Select material for layer {i+1}", material_choices, key=key)
                selected_materials.append(material)

            with cols[1]:
                key_h = f"material_height_{i}"
                height = st.number_input(f"Enter the height for layer {i+1}", min_value=0.0, step=0.01, format="%.2f", key=key_h)
                selected_height.append(height)

        # Store the selected materials in the session state
        st.session_state["materials"] = selected_materials
        st.session_state["materials_height"] = selected_height
    

    cols_button = st.columns([6, 1])

    # Calculate Button
    with cols_button[0]:
        if st.button("Calculate"):
            if "materials" in st.session_state and "materials_height" in st.session_state:
                # Process the materials and get the dictionary
                print(st.session_state["materials"], st.session_state["materials_height"])
                # thickness = [0.7,0.9] # materials_height
                # material = ["silver","chromium"] # materials
                chart_data = process_line_chart(st.session_state["materials"],st.session_state["materials_height"]) #gives line_chart
                # chart_data = process_layers(material, thickness) #give countour
                # chart_data = process_layers(st.session_state["materials"], st.session_state["materials_height"])
                # Display the result
                st.write("Processed Data:")            
                st.pyplot(chart_data)
            else:
                st.warning("Please complete all inputs before calculating.")

    # Reset Button
    with cols_button[1]:
        if st.button("Reset"):
            reset_inputs()

# Run the function to display the form
stage_1()
