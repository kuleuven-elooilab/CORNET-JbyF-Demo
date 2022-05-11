import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw,ImageOps
import pickle
import requests, os


from copy import deepcopy
import base64

def show_page():

    def predict_strength(test):
        # A model for each output variable (TT= top tensile test, otherwise ST = shear test)
        if test=="TT":
            openFile = "C:/Users/u0148983/OneDrive - KU Leuven/PythonCode/Scikit_learn/SavedModels/SVR_Max_top_tensile_force_TT.pkl"
        else:
            openFile = "C:/Users/u0148983/OneDrive - KU Leuven/PythonCode/Scikit_learn/SavedModels/SVR_Max_shear_tensile_force_ST.pkl"
        loaded_model = pickle.load(open(openFile , 'rb')) 
        # Must be in the same order as when training the model   
        X = [[material_top,
                material_bottom,
                strength_top,
                strength_bottom,
                sheet_thickness1,
                sheet_thickness2,
                die_depth,
                die_angle_wall,
                die_angle_anvil,
                diameter_anvil,
                punch_angle_wall,
                punch_diameter,
                interlock,neck_thickness,
                bottom_thickness,
                min_topThickness,
                min_bottomThickness,
                joining_force]]
        predicted_force = loaded_model[0].predict(X)
        return float(predicted_force)
        

    # -- Set page config
    

    

    # __________________________________________Menu on the left__________________________________________

    # ----------------Material properties---------------------
    st.sidebar.markdown("# Select the material properties")

    #           ***   Top sheet properties   ***
    st.sidebar.markdown("### Properties for top sheet")

    #-- Set Steel or Aluminum 
    if st.sidebar.selectbox('Select the material:',['Steel', 'Aluminium'])=="Steel":
        # trained model can not handle strings
        material_top = 1
    else:
        material_top = 2
    #-- Set tensile strength                                    
    strength_top = st.sidebar.number_input('What is the tensile strength of the material [MPa]', value = 264.0982459)
    #-- Set sheet thickness
    sheet_thickness1 = st.sidebar.slider('Set the sheet thickness [mm]', 0.0, 2.0, 1.7)

    #           ***   Buttom sheet properties   ***
    st.sidebar.markdown("### Properties for bottom sheet")

    #-- Set Steel or Aluminum
    if st.sidebar.selectbox('Select the material:',['Aluminium','Steel'])=="Steel":
        # trained model can not handle strings
        material_bottom = 1
    else:
        material_bottom = 2
    #-- Set tensile strength                                    
    strength_bottom = st.sidebar.number_input('What is the tensile strength of the material [MPa] ', value = 277.1778877)
    #-- Set sheet thickness
    sheet_thickness2 = st.sidebar.slider('Set the sheet thickness [mm] ', 0.0, 2.0, 1.5)


    # ----------------Material properties---------------------
    st.sidebar.markdown("# Determine the tool geometrie")

    #           ***   Die properties   ***
    st.sidebar.markdown("### Dimensions of the die")

    #-- Set die depth
    die_depth = st.sidebar.slider('Set the depth of the die [mm]', 0.0, 10.0, 1.4)
    #-- Set anvil diameter
    diameter_anvil = st.sidebar.slider('Set the diameter of the anvil [mm]', 0.0, 7.0, 4.9)
    #-- Set wall angle β
    die_angle_wall = st.sidebar.slider('Set the angle of the wall [°]', 0.0, 10.0, 5.0)
    #-- Set anvil angle δ
    die_angle_anvil = st.sidebar.slider('Set the angle between the anvil and the groove [°]', 0.0, 60.0, 21.8)

    #           ***   Punch properties   ***
    st.sidebar.markdown("### Dimensions of the punch")

    #-- Set angle
    punch_angle_wall = st.sidebar.slider('Set the angle of the wall [°] ', 0.0, 10.0, 2.5)
    #-- Set die depth
    punch_diameter = st.sidebar.slider('Set the diameter of punch [mm]', 0.0, 7.0, 5.0)


    # ----------------Joining results---------------------
    st.sidebar.markdown("# Fill in the joining results")

    #-- Set interlock 
    interlock = st.sidebar.number_input('What is the interlock [mm]', value = 0.38)
    #-- Set neck thickness 
    neck_thickness = st.sidebar.number_input('What is the neck thickness [mm]', value = 0.387)
    #-- Set bottom thickness 
    bottom_thickness = st.sidebar.number_input('What is the bottom thickness [mm]', value = 0.673)
    #-- Set min bottom thickness top sheet 
    min_topThickness = st.sidebar.number_input('What is the min bottom thickness top sheet [mm]', value = 0.43)
    #-- Set min bottom thickness bottom sheet 
    min_bottomThickness = st.sidebar.number_input('What is the min bottom thickness bottom sheet [mm]', value = 0.193)
    #-- Set joining force
    joining_force = st.sidebar.number_input('What is the max joining force [kN]', value = 54)



    # __________________________________________Main screen of the application__________________________________________

    # Title the app
    st.markdown('### Strength prognosis of a clinch joint based on machine learning')

    st.markdown("""
    * Use the menu at left to fill in the input parameters
    * The dimensions will be illustrated on the figure below
    * Once you change a parameter, the strength will automatically be recalculated
    """)


    # ----------------Make the prediction---------------------

    col1, col2 = st.columns(2)
    with col1:
        st.metric('Max top tensile strenth',"{:0.2f} kN".format(predict_strength("TT")))
    with col2:
        st.metric('Max shear strength',"{:0.2f} kN".format(predict_strength("ST")))


    # ----------------Display the image---------------------

    #-- Open the image
    image = Image.open('docs/ClinchParameters.png')

    #-- Make it posseble to overlay the image with text 
    draw = ImageDraw.Draw(image)
    colour = (50,50,50)

    #-- Write each parameter on the image based on the pixel coordinate

    # tickness 1
    draw.text((0,315), str(sheet_thickness1), colour)
    # tickness 2
    draw.text((0,365), str(sheet_thickness2), colour)
    # die depth
    draw.text((315,540), str(die_depth), colour)
    # diameter anvil
    draw.text((220,530), str(diameter_anvil), colour)
    # die angle wall
    draw.text((95,560), str(die_angle_wall), colour)
    # die angle anvil
    draw.text((150,585), str(die_angle_anvil), colour)
    # punch angle wall
    draw.text((200,180), str(punch_angle_wall), colour)
    # punch diameter
    draw.text((220,225), str(punch_diameter), colour)
    # interlock
    draw.text((115,270), str(interlock), colour)
    # neck tickness
    draw.text((315,270), str(neck_thickness), colour)
    # bottom thickness
    draw.text((90,400), str(bottom_thickness), colour)
    # min bottom thickness top sheet
    draw.text((400,400), str(min_topThickness), colour)
    # min bottom thickness bottom sheet 
    draw.text((100,465), str(min_bottomThickness), colour)

    # warnings
    draw.text((170,100), 'not used in training data', (255,50,50))
    draw.text((150,610), 'not used in training data', (255,50,50))
    draw.text((315,590), 'not used in training data', (255,50,50))


    #-- Display the image in Streamlit webApp
    st.image(image)

    return
