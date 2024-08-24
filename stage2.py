import streamlit as st
from processor import generate_random_graph

def stage_2():
    # Initialize session state for number of boxes and reset flag
    if 'num_layers' not in st.session_state:
        st.session_state.num_layers = 1
    if 'reset_flag' not in st.session_state:
        st.session_state.reset_flag = False

    def update_num_layers():
        st.session_state.num_layers = st.session_state.num_layers_input

    def reset_app():
        st.session_state.num_layers = 1
        st.session_state.num_layers_input = 1
        for key in list(st.session_state.keys()):
            if key.startswith('textbox_') or key.startswith('material_height_'):
                del st.session_state[key]
        st.session_state.reset_flag = True

    # Number input to directly control the number of text boxes
    st.number_input("Enter the number of layers you want:", 
                    min_value=1, 
                    max_value=100, 
                    value=st.session_state.num_layers,
                    key="num_layers_input",
                    on_change=update_num_layers)

    # Generate the text boxes based on the user input
    st.write(f"You selected {st.session_state.num_layers} layers.")

    selected_materials = []
    selected_height = []
    material_choices = ["silver", "aluminum","aluminum dioxide", "gold", "chromium", "copper", "germanium","silicon","silicon dioxide","titanium", "titanium dioxide"]

    for i in range(st.session_state.num_layers):
        cols = st.columns(2)
            
        with cols[0]:
            text_input = st.selectbox(f'Select material for layer {i+1}',material_choices, key=f'textbox_{i+1}')
            selected_materials.append(text_input)

        with cols[1]:    
            # Set default value to 0.0 if reset_flag is True
            default_value = 0.0 if st.session_state.reset_flag else st.session_state.get(f"material_height_{i+1}", 0.0)
            height_input = st.number_input(f"Enter the height for layer {i+1}", 
                                           min_value=0.0, 
                                           step=0.01, 
                                           format="%.2f", 
                                           key=f"material_height_{i+1}",
                                           value=default_value)
            selected_height.append(height_input)

    # Buttons for submitting or resetting the boxes
    cols_button =  st.columns([6, 2])
    with cols_button[0]:
        submit_texts_button = st.button(label='Calculate')

    with cols_button[1]:
        reset_button = st.button(label='Reset Values', on_click=reset_app)

    # Calculate Button            
    if submit_texts_button:
        fig = generate_random_graph(selected_materials,selected_height)
        st.pyplot(fig)

    # Reset the reset_flag after rendering
    if st.session_state.reset_flag:
        st.success("The app has been reset!")
        st.session_state.reset_flag = False
