import streamlit as st
from processor import calculate_graph

def stage_1():
    st.title("Rename this ...")

    # Check if the app has been reset; if so, start fresh
    if 'reset_flag' not in st.session_state:
        st.session_state.reset_flag = False

    # Only show Stage 1 if not reset
    if not st.session_state.reset_flag:
        stage_1_()

    # Proceed to Stage 2 only if the number of layers is set
    if 'num_layers' in st.session_state:
        stage_2()

def stage_1_():
    st.subheader("Stage 1: Set the Number of Layers")

    # Initialize the number of layers if not already set
    if 'num_layers' not in st.session_state:
        st.session_state.num_layers = 1

    # Input for the number of layers
    num_layers = st.number_input("Enter the number of layers:", 
                                 min_value=1, 
                                 max_value=100, 
                                 value=st.session_state.num_layers)
    
    # Button to confirm the number of layers
    if st.button("Confirm Number of Layers"):
        st.session_state.num_layers = num_layers
        st.session_state.stage_1_complete = True  # Flag to move to stage 2

def stage_2():
    st.subheader("Stage 2: Configure Materials and Thicknesses")
    
    # Ensure Stage 1 has been completed
    if 'stage_1_complete' not in st.session_state or not st.session_state.stage_1_complete:
        st.warning("Please complete Stage 1 first.")
        return

    # Material choices
    material_choices = [
        "silver", "aluminum", "aluminum dioxide", "gold", 
        "chromium", "copper", "germanium", "silicon",
        "silicon dioxide", "titanium", "titanium dioxide"
    ]
    
    selected_materials = []
    selected_thicknesses = []

    # Collect material and thickness inputs for each layer
    for i in range(st.session_state.num_layers):
        #st.subheader(f"Layer {i + 1}")

        # Create two columns
        cols = st.columns(2)

        with cols[0]:  # First column for material selection
            material = st.selectbox(f"Select material for layer {i + 1}",
                                    material_choices,
                                    key=f'material_{i + 1}')
            selected_materials.append(material)

        with cols[1]:  # Second column for thickness input
            thickness = st.number_input(f"Enter thickness for layer {i + 1} (in micrometers):",
                                        min_value=0.0,
                                        step=0.01,
                                        format="%.2f",
                                        key=f'thickness_{i + 1}')
            selected_thicknesses.append(thickness)
        
        selected_materials.append(material)
        selected_thicknesses.append(thickness)
    
    # Button section to calculate results or reset the app
    cols_buttons = st.columns([6, 2])

    with cols_buttons[0]:  # First column for the Calculate button
        if st.button("Calculate"):
            calculate_graph(selected_materials, selected_thicknesses)

    with cols_buttons[1]:  # Second column for the Reset App button
        st.button("Reset App", on_click=reset_app)

def reset_app():
    # Reset session state values
    st.session_state.num_layers = 1
    st.session_state.reset_flag = False
    st.session_state.stage_1_complete = False  # Reset the completion flag for Stage 1

    # Remove any dynamically created session state entries for materials and thicknesses
    keys_to_remove = [key for key in st.session_state.keys() 
                      if key.startswith('material_') or key.startswith('thickness_')]
    for key in keys_to_remove:
        del st.session_state[key]

    # Streamlit will handle reruns on the next interaction