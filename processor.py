import pandas as pd
import numpy as np
import math
import cmath
from constants import *
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


materials_data = {"silver":None,
                  "aluminum":None,
                  "aluminum dioxide":None,
                  "gold":None,
                  "chromium":None,
                  "copper":None,
                  "germanium":None,
                  "silicon":None,
                  "silicon dioxide":None,
                  "titanium":None,
                  "titanium dioxide":None,}

def get_data_for_material(materials):
    for material in materials:
        if(material!="air"):
            csv_file = materials_file[material]
            df = pd.read_csv(csv_file,names=["lambda", "n", "k"])
            df["lambda"]=df["lambda"].apply(lambda x:x*1000)
            materials_data[material] = df

def get_n_k_from_material(material,lambda_):
    df = materials_data[material]
    filtered_df = df[df["lambda"] == lambda_]
    n = float(filtered_df["n"])
    k = float(filtered_df["k"])
    return n,k

def calculate_phi(layer_n,layer_k,layer_t,lambda_):
     k = 2*math.pi/lambda_
     phi =  k * (layer_n - (1j*layer_k))*layer_t 
     return phi

def process_layers_for_thickness(materials,thickness,lambda_range):
    # Convert the list of materials into a dictionary
    # processed_dict = {f"layer{i+1}": material for i, material in enumerate(materials)}
    # chart_data = pd.DataFrame(np.random.randn(20, 1), columns=["c"])
    # generate_chart()
    get_data_for_material(materials)
    matrix_list = []
    reflectance = []
    number_layers = len(materials)
    for lambda_ in lambda_range:
        for layer in range(0,number_layers): #6
            if layer == 0: #air
                D = get_layer_calculation(air_n, air_k)
                matrix_list.append(np.linalg.inv(D))
                # print("D"+str(layer)+"inv")
            elif layer == (number_layers-1): #last layer
                n,k = get_n_k_from_material(materials[layer],lambda_)
                D = get_layer_calculation(n, k)
                matrix_list.append(D)
                # print("D"+str(layer))
            elif layer != (number_layers): #layer1
                n,k = get_n_k_from_material(materials[layer],lambda_)
                D = get_layer_calculation(n, k)
                P = get_inter_layer_calculation(n,k,thickness[layer],lambda_)
                matrix_list.append(D)
                # print("D"+str(layer))
                matrix_list.append(P)
                # print("P"+str(layer))
                matrix_list.append(np.linalg.inv(D))
                # print("D"+str(layer)+"inv")
        M = calculate_dot(matrix_list[:-2]).tolist()
        r = M[1][0]/M[0][0]
        r_star = np.conjugate(r)
        R = r*r_star
        reflectance.append(R)
        # print(R)
        # break
    return reflectance        

def validate(materials,thickness):
    materials_len = len(materials)
    thickness_len = len(thickness)
    return materials_len == thickness_len

def process_line_chart(materials,thickness):
    #Added air as a layer to keep the layer 1 as actual material layer 1
    materials.insert(0,"air")
    thickness.insert(0,0) 
    if validate(materials,thickness) == False:
        raise Exception()
    lambda_range = range(min_lambda_,max_lambda_,lambda_step)
    reflectance = process_layers_for_thickness(materials,thickness,lambda_range)
    return generate_line_chart(reflectance,lambda_range)

def process_layers(materials,thickness):
    #Added air as a layer to keep the layer 1 as actual material layer 1
    materials.insert(0,"air")
    thickness.insert(0,0) 
    if validate(materials,thickness) == False:
        raise Exception()

    ideal_metal_layer = 0
    #ideal metal thickness range
    thickness_range = range(min_thickness,max_thickness,thickness_step)
    lambda_range = range(min_lambda_,max_lambda_,lambda_step)
    reflectance = np.empty([len(thickness_range),len(lambda_range)])

    for thickness_i in thickness_range:
        thickness.insert(ideal_metal_layer,thickness_i)
        reflectance_list = process_layers_for_thickness(materials,thickness,lambda_range)
        reflectance[thickness_i] = np.array(reflectance_list)
    return generate_chart(list(lambda_range),list(thickness_range),reflectance)

def calculate_dot(matrix_list):
    Z = np.empty([2,2])
    for i in range(len(matrix_list)):
        if (i==0 & len(matrix_list)>1):
            Z = np.dot(matrix_list[i],matrix_list[i+1]) # 0,1
        elif (i==1):
            if (len(matrix_list)==2): 
                return Z
            else:
                continue
        elif (i>=2):
            Z = np.dot(Z, matrix_list[i])
    return Z

def get_layer_calculation(n,k):
    val = n-(1j*k)
    D = [[1,1],[val, -val]]
    return np.matrix(D,dtype=np.complex128)

def get_inter_layer_calculation(n,k,t,lambda_):
    phi = calculate_phi(n,k,t,lambda_)
    val = 1j*phi
    P = [[cmath.exp(val), 0],[0, cmath.exp(-val)]]
    return np.matrix(P,dtype=np.complex128)

def generate_chart(lambda_list, thickness_list, reflectance):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    ax1.set_title('The output of st.pyplot()')
    surf = ax1.contourf(np.array(lambda_list), np.array(thickness_list), np.array(reflectance), 200)
    fig1.colorbar(surf)
    return fig1

def generate_line_chart(reflectance,lambda_range):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    ax1.set_title('The output of st.pyplot()')
    ax1.set_xlabel('Lambda')
    ax1.set_ylabel('reflectance')
    ax1.plot(list(lambda_range), reflectance)
    return fig1
