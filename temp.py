from constants import materials_file, air_k,air_n
import pandas as pd
import cmath
import math
import numpy as np

def get_value(n,k):
    val= n-1j*k
    return val

def caclulate_impact(n0,k0,n1,k1):
    # val0 = get_value(n0,k0)
    # val1 = get_value(n1,k1)
    # D0 = [[1,1],[val0, -val0]]
    # D1 = [[1,1],[val1, -val1]]
    D0 = np.array([[1, 1], [n0 - 1j * k0, -(n0 - 1j * k0)]])
    D1 = np.array([[1, 1], [n1 - 1j * k1, -(n1 - 1j * k1)]])
    D1_inv = np.linalg.inv(D1)
    D0_inv = np.linalg.inv(D0)
    return D0, D1, D1_inv, D0_inv
    

def calculate_propogation(n,k,t,lambda_):
    lambda_ = lambda_/1000
    k_ = 2 * np.pi / lambda_
    phi_P2 = k_ * (n - 1j * k) * t
    P2 = np.array([[np.exp(1j * phi_P2), 0], [0, np.exp(-1j * phi_P2)]])
    return P2




def get_n_k(material,lambda_):
    csv_file = materials_file[material]
    df = pd.read_csv(csv_file,names=["lambda", "n", "k"])
    df["lambda"]=df["lambda"].apply(lambda x:x*1000)
    filtered_df = df[df["lambda"] == lambda_]
    n = float(filtered_df["n"].iloc[0])
    k = float(filtered_df["k"].iloc[0])
    return n,k
    # return 1,2

def calculate_dot_of_this_layer(D0_inv,D1,D1_inv,P1):
    return D0_inv @ D1 @ P1 @ D1_inv



def main():
    materials_list=["aluminum"]
    thickness_list=[0.010]
    lambda_ = 400
    n_prev = air_n
    k_prev = air_k
    t_prev = 0
    for material_i in range(len(materials_list)):
        n,k = get_n_k(materials_list[material_i],lambda_)
        n, k = 0.385211589, 4.281283449
        t = thickness_list[material_i]
        D0, D1,D1_inv,D0_inv = caclulate_impact(n_prev,k_prev,n,k)        
        P1 = calculate_propogation(n,k,t,lambda_)
        M_this_layer = calculate_dot_of_this_layer(D0_inv,D1,D1_inv,P1)
        if material_i == 0:
            M = M_this_layer
        else:
            M = np.dot(M, M_this_layer)
        print("Layer",material_i)
        print("n",n)
        print("k",k)
        print("D1",D0)
        print("D2",D1)
        print("D1_inv",D0_inv)
        print("D2_inv",D1_inv)
        print("P1",P1)
        print("M_this_layer",M_this_layer)
        n_prev = n
        k_prev = k
        t_prev = t
        #D_prev = D1
    print("M",M)
    r = M[1,0] / M[0,0]
    r_star = np.conj(r)
    R = r*r_star
    print("r",r)
    print("r_star",r_star)
    print("R",R)
    print("R real: ", R.real)



    



main()

