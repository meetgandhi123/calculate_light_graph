import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

def generate_graph(lambda_vals, Reflectance):
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plot the data
    ax.plot(lambda_vals, Reflectance)

    # Set the limits and labels with increased font size
    ax.set_xlim([0.4, 0.8])
    ax.set_ylim([0, 1])
    ax.set_xlabel('Wavelength (μm)', fontsize=24)  # Increase the font size
    ax.set_ylabel('Reflectance', fontsize=24)      # Increase the font size
    ax.set_title('Reflectance vs Wavelength', fontsize=20)  # Increase the font size

    # Use Streamlit's st.pyplot() and pass the figure directly
    st.pyplot(fig)



materials_data = {"silver":"Ag",
                  "aluminum":"Al",
                  "aluminum dioxide":"Al2O3",
                  "gold":"Au",
                  "chromium":"Cr",
                  "copper":"Cu",
                  "germanium":"Ge",
                  "silicon":"Si",
                  "silicon dioxide":"SiO2",
                  "titanium":"Ti",
                  "titanium dioxide":"TiO2",}

def calculate_graph(selected_materials,selected_height):

    material_list = selected_materials
    thickness_list = selected_height

    # material_list = ["Au"]
    # thickness_list = [0.030]

    def get_data(material):
        material = materials_data[material]
        file_name = f"data/{material} for sensitivity.csv"
        return pd.read_csv(file_name).values

    def get_lambda_n_k(layer_n_data):
        return layer_n_data[:, 0], layer_n_data[:, 1], layer_n_data[:, 2]

    def get_air_n_k(len_lambda):
        return np.ones(len_lambda), np.zeros(len_lambda)

    def calculate_D_and_P(n, k, thickness, lambda_vals):
        """Calculate D and P matrices for a given layer."""
        phi = (2 * np.pi / lambda_vals) * (n - 1j * k) * thickness
        D = np.array([
            [[1, 1],
            [n[j] - 1j * k[j], -(n[j] - 1j * k[j])]]
            for j in range(len(n))
        ])
        D_inv = np.linalg.inv(D)
        P = np.array([
            [[np.exp(1j * phi[j]), 0],
            [0, np.exp(-1j * phi[j])]]
            for j in range(len(phi))
        ])
        return D, D_inv, P
        

    # Load initial data for the first material to get lambda values
    lambda_vals, layer_1_n, layer_1_k = get_lambda_n_k(get_data(material_list[0]))

    # Get air n and k values
    air_n, air_k = get_air_n_k(len(lambda_vals))

    # Calculate D and P matrices for the air layer
    D_air, D_air_inv, _ = calculate_D_and_P(air_n, air_k, 0, lambda_vals)  # No thickness for air

    # Initialize M matrix as the identity matrix for the air
    M_air = D_air_inv

    # Iterate through each layer and compute matrices
    for index, (material, thickness) in enumerate(zip(material_list, thickness_list)):
        print("index: ",index)
        print("material: ",material)
        print("thickness: ",thickness)
        layer_data = get_data(material)
        lambda_vals, layer_n, layer_k = get_lambda_n_k(layer_data)
        D, D_inv, P = calculate_D_and_P(layer_n, layer_k, thickness, lambda_vals)

        # Update M matrix with the current layer matrices
        if index == 0:             
            M = D @ P @ D_inv
        elif index == len(material_list) - 1:
            M = M @ D
        else:
            M = M @ D @ P @ D_inv

    M_final = M_air @ M

    # Calculate reflectance
    r = M_final[:, 1, 0] / M_final[:, 0, 0]
    Reflectance = (r * np.conj(r)).real

    generate_graph(lambda_vals, Reflectance)
