import pandas as pd
import numpy as np
from constants import *
import math
import cmath
import matplotlib.pyplot as plt


def get_n_k_from_material(material,lambda_):
    csv_file = materials_file[material]
    df = pd.read_csv(csv_file)
    filtered_df = df[df[0] == lambda_]
    n = filtered_df[2]
    k = filtered_df[3]
    return n,k

def calculate_phi(layer_n,layer_k,layer_t,lambda_):
     k = 2*math.pi/lambda_
     phi =  k * (layer_n - (1j*layer_k))*layer_t #confirm this equation
     return phi

def process_layers_for_thickness(materials,thickness,lambda_range):
    # Convert the list of materials into a dictionary
    # processed_dict = {f"layer{i+1}": material for i, material in enumerate(materials)}
    # chart_data = pd.DataFrame(np.random.randn(20, 1), columns=["c"])
    # generate_chart()
    matrix_list = []
    reflectance = np.empty([max_lambda_])
    number_layers = len(materials)
    for lambda_ in lambda_range:
        for layer in range(number_layers+1): #6
            if layer == 0: #air
                D = get_layer_calculation(air_n, air_k)
                matrix_list.append(np.linalg.inv(D))
            elif (layer!=(number_layers+1) 
                    & layer!=0): #layer1
                n,k,lambda_ = get_n_k_from_material(materials[layer],lambda_)
                D = get_layer_calculation(n, k)
                P = get_inter_layer_calculation(n,k,thickness[layer],lambda_)
                matrix_list.append(D)
                matrix_list.append(P)
                matrix_list.append(np.linalg.inv(D))
        M = calculate_dot(matrix_list)
        r = M[1][0]/M[0][0]
        r_star = np.conjugate(r)
        R = np.matmul(r,r_star)
        reflectance[lambda_] = R
    return reflectance    

def validate(materials,thickness):
    materials_len = len(materials)
    thickness_len = len(thickness)
    return materials_len == thickness_len

def process_layers(materials,thickness):
    if validate(materials,thickness) == False:
        raise Exception()

    reflectance = np.empty([max_thickness,max_lambda_])
    ideal_metal_layer = 0
    #ideal metal thickness range
    thickness_range = range(min_thickness,max_thickness,thickness_step)
    lambda_range = range(min_lambda_,max_lambda_,lambda_step)
    for thickness_i in thickness_range:
        thickness.insert(ideal_metal_layer,thickness_i)
        reflectance[thickness_i] = process_layers_for_thickness(materials,thickness,lambda_range)
    return generate_chart(list(lambda_range),list(thickness_range),reflectance)

def calculate_dot(matrix_list):
    Z = np.empty([2,2])
    for i in range(len(matrix_list)):
        if (i==0 & len(matrix_list)>1):
            Z = np.matmul(matrix_list[i],matrix_list[i+1]) # 0,1
        elif (i==1):
            if (len(matrix_list)==2): 
                return Z
            else:
                continue
        elif (i>=2):
            Z = np.matmul(Z, matrix_list[i])
    return Z

def get_layer_calculation(n,k):
    D = [[1,1],[(n-(1j*k)), -(n-(1j*k))]]
    return np.matrix(D)

def get_inter_layer_calculation(n,k,t,lambda_):
    phi = calculate_phi(n,k,t,lambda_)
    D = [[math.exp(1j*phi), 0],[0, math.exp(-1j*phi)]]
    return np.matrix(D)

def generate_chart(lambda_list, thickness_list, reflectance):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    ax1.set_title('The output of st.pyplot()')
    surf = ax1.contourf(np.array(lambda_list), np.array(thickness_list), np.array(reflectance), 200)
    fig1.colorbar(surf)
    return fig1