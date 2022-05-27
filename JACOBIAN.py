import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd 

# GUI code
sg. theme('DarkBlue')

# Excel read code

EXCEL_FILE = 'Cartesian_Design_Data_FK.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay-out code

Main_layout = [
   [sg.Push(), sg.Text('Cartesian MEXE Calculator', font = ("Consolas", 25)), sg.Push()],

   [sg.Text('Fill out the following fields:', font = ("Consolas",15)),
     sg.Push(), sg.Button('Solve Forward Kinematics',
     font = ("Consolas",12), size=(35,0), button_color=('black','yellow')),sg.Push()],
         
  
   [sg.Text('a1 = ', font = ("Consolas", 10)),sg.InputText('', key = 'a1', size =(20,10)),
     sg.Text('d1 = ',font = ("Consolas", 10)),sg.InputText('',key='d1', size=(20,10)),
     sg.Push(), sg.Button('Jacobian Matrix (J)', font = ("Consolas", 12),size=(20,0),button_color=('white','green')), 
     sg.Button('Det(J)',font = ("Consolas", 12), size=(15,0), button_color=('white','orange')),
     sg.Button('Inverse of J',font = ("Consolas", 12), size=(15,0), button_color=('white','gray')),
     sg.Button('Transpose of J', font = ("Consolas", 12), size=(15,0), button_color=('white','blue')), sg.Push()],
   [sg.Text('a2 = ', font = ("Consolas", 10)),sg.InputText('',key='a2', size=(20,10)),
     sg.Text('d2 = ',font = ("Consolas", 10)),
     sg.InputText('',key='d2',size=(20,10)),
     sg.Push(),sg.Button('Inverse Kinematics',font = ("Consolas",12),
     size=(35,0), button_color=('white','green')),
     sg.Push(),sg.Button('Path and Trajectory Planning', font = ("Consolas",12), size=(40,0), button_color=('white','black')), sg.Push()],
 
   [sg.Text('a3 = ', font = ("Consolas", 10)),sg.InputText('',key='a3', size=(20,10)),
     sg.Text('d3 = ',font = ("Consolas", 10)),
     sg.InputText('',key='d3',size=(20,10))],
    
   [sg.Text('a4 = ', font = ("Consolas",10)),sg.InputText('',key='a4', size=(20,10))],


   [sg.Button('Click this before Solving Foward Kinematics',tooltip = 'Solve Forward Kinematics !!!', font = ("Consolas",12), button_color=('white','purple')), sg.Push(),
   sg.Push(),sg.Frame('Position Vector: ',[[
      sg.Text('X= ', font = ("Consolas",12)),sg.InputText(key ='X', size=(20,0)),
      sg.Text('Y= ', font = ("Consolas",12)),sg.InputText(key ='Y', size=(20,0)),
      sg.Text('Z= ', font = ("Consolas",12)),sg.InputText(key ='Z', size=(20,0))]]),sg.Push()],
  
   [sg.Push(), sg.Frame('H0_3 Transformation Matrix = ',[[sg.Output(size=(80,15))]]),
      sg.Push(),sg.Image('Cartesian Manipulator.gif'),sg.Push()],
   [sg.Submit(font = ("Consolas",10)),sg.Exit(font = ("Consolas",10))] 
  
  ]

# Windows Code
window = sg.Window('Cartesian MEXE Calculator', Main_layout, resizable = True)



def clear_input():
    for key in values:
        window[key]('')
    return None

#Variable Codes for disabling buttons
disable_FK = window['Solve Forward Kinematics']
disable_J = window['Jacobian Matrix (J)']
disable_DetJ = window['Det(J)']
disable_IV = window ['Inverse of J']
disable_TJ = window ['Transpose of J']
disable_PT = window ['Path and Trajectory Planning']

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event ==('Click this before Solving Forward Kinematics'):
        disable_J.update(disabled=True)
        disable_DetJ.update(disabled=True)
        disable_IV.update(disabled=True)
        disable_TJ.update(disabled=True)
        disable_PT.update(disabled=True)
   

    if event == 'Solve Forward Kinematics':
       
        # Forward Kinematic Codes
        # link lengths in cm
        a1 = values['a1'] # For Testing, 150cm
        a2 = values['a2'] # For Testing, 80cm
        a3 = values['a3'] # For Testing, 80cm
        a4 = values['a4'] # For Testing, 80cm

        # Joint Variable Thetas in degrees
        d1 = values['d1'] # For Testing, 40cm
        d2 = values['d2'] # For Testing, 30cm
        d3 = values['d3'] # For Testing, 70cm

        # If Joint Variable are ds don't need to convert

        ## D-H Parameter Table (This is the only part you only edit for every new mechanical manipulator.)
        # Rows = no. of HTM, Colums = no. of Parameters
        # Theta, alpha, r, d

        DHPT = [[0,(270.0/180.0)*np.pi,0,float(a1)],
                [(270.0/180.0)*np.pi,(270.0/180.0)*np.pi,0,float(a2)+float(d1)],
                [(270.0/180.0)*np.pi,(90.0/180.0)*np.pi,0,float(a3)+float(d2)],
                [0,0,0,float(a4)+float(d3)]
                ]

        # np.trigo function (DHPT[row][column])

        i = 0
        H0_1 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                 [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                 [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                 [0,0,0,1]]

        i = 1
        H1_2 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                 [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                 [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                 [0,0,0,1]]

        i = 2
        H2_3 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                 [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                 [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                 [0,0,0,1]]

        i = 3
        H3_4 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                 [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                 [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                 [0,0,0,1]]

        # Transportation Matrices from base to end-effector
        #print("H0_1 = ")
        #print(np.matrix(H0_1))
        #print("H1_2 = ")
        #print(np.matrix(H1_2))
        #print("H2_3 = ")
        #print(np.matrix(H2_3))

        # Dot Product of H0_3 = H0_1*H1_2*H2_3
        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)
        H0_4 = np.dot(H0_3,H3_4)

        # Transportation Matrix of the Manipulator
        print("H0_3 = ")
        print(np.matrix(H0_3))

        # Position Vector X Y Z
        X0_4 = H0_4[0,3]
        print("X = ", X0_4)
        Y0_4 = H0_4[1,3]
        print("Y = ", Y0_4)
        Z0_4 = H0_4[2,3]
        print("Z = ", Z0_4)

        disable_J.update(disabled=False)
        disable_PT.update(disabled=False)
   

    if event == 'Submit' :
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data Saved!')
       
    #JACOBIAN MATRIX CODE
    if event == 'Jacobian Matrix (J)':
        Z_1 = [[0],[0],[1]] #the [0,0,1] vector

       #  Row 1 - 3, Column 1
        J1 = [[1,0,0],[0,1,0],[0,0,1]]
        J1 = np.dot(J1,Z_1)
        J1 = np.matrix(J1)
        #print('J1 = ')
        #print(np.matrix(J1))
         
        try:
            H0_1 = np.matrix(H0_1)
        except:
            H0_1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI then, go first "Click before Solving Forward Kinematics!!!"')
            break
        # Row 1 - 3, Column 2

        J2a = H0_1[0:3,0:3]
        J2a = np.dot(J2a,Z_1)
        #print("J2a = ")
        #print(J2a)

        J2b_1 = H0_3[0:3,3:]
        J2b_1 = np.matrix(J2b_1)
        #print(J2b_1)

        J2b_2 = H0_1[0:3,3:]
        J2b_2 = np.matrix(J2b_2)
        #print(J2b_2)

        J2b = J2b_1 - J2b_2
        #print('J2b= ')
        #print(J2b)

        #cross product
        J2 = [[(J2a[1,0]*J2b[2,0])-(J2a[2,0]*J2b[1,0])],
            [(J2a[2,0]*J2b[0,0])-(J2a[0,0]*J2b[2,0])],
            [(J2a[0,0]*J2b[1,0])-(J2a[1,0]*J2b[0,0])]]
        #print("J2 = ")
        #print(np.matrix(J2))

        # Row 1 - 3, Column 3

        J3a = H0_1 [0:3,0:3]
        J3a = np.dot(J3a,Z_1)
        #print("J3a = ")
        #print(J3a)

        J3b_1 = H0_3[0:3,3:]
        J3b_1 = np.matrix(J3b_1)
        #print("J3b_1 = ")


        J3b_2 = H0_2[0:3,3:]
        J3b_2 = np.matrix(J3b_2) 
        #print("J3b_2 = ")

        J3b = J3b_1 - J3b_2
        #print('J3b= ')
        #print(J3b)

        #cross product
        J3 = [[(J3a[1,0]*J3b[2,0])-(J3a[2,0]*J3b[1,0])],
            [(J3a[2,0]*J3b[0,0])-(J3a[0,0]*J3b[2,0])],
            [(J3a[0,0]*J3b[1,0])-(J3a[1,0]*J3b[0,0])]]
        #print("J3 = ")
        #print(np.matrix(J3))
        
        #Rotation/Orientation Vectors
        J4 = [[0],[0],[0]]
        J4 = np.matrix(J4)
        #print("J4 = ")
        #print(J4)

        J5 = H0_1[0:3,0:3]
        J5 = np.dot(J5,Z_1)
        J5 = np.matrix(J5)
        #print("J5 = ")
        #print(J5)

        J6 = H0_1[0:3,0:3]
        J6 = np.dot(J6,Z_1)
        J6 = np.matrix(J6)
        #print("J6 = ")
        #print(J6)
 
        #CONCATENATED JACOBIAN VECTORS
        JM1 = np.concatenate((J1,J2,J3),1)
        #print(JM1)
        JM2 = np.concatenate((J4,J5,J6),1)
        #print(JM2)

        J = np.concatenate((JM1,JM2),0)
        #print("J = ") 
        #print(J)

        sg.popup('J = ',J)
        DJ = np.linalg.det(JM1)
        if DJ == 0.0 or DJ == -0:
            disable_IV.update(disabled=True)
            sg.popup('Warning:Jacobian Matrix is Non-Invertible!')
        elif DJ != 0.0 or DJ != -0:
            disable_IV.update(disabled=False)

        disable_J.update(disabled=True)
        disable_DetJ.update(disabled=False)
        disable_TJ.update(disabled=False)

    if event == 'Det(J)':
        # Singularity = Det(J)
        # np.linalg.    det(M)
        # Let JM1 become the 3x3 position matrix for obtaining  the Determinant
        try:
            JM1 = np.concatenate((J1,J2,J3),1)
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI then, go first "Click before Solving Forward Kinematics!!!"')
            break

        DJ = np.linalg.det(JM1)
        #print("DJ = ",DJ)
        sg.popup('DJ = ', DJ)
      
        if DJ == 0.0 or DJ == -0:
            disable_IV.update(disabled=True)
            sg.popup('Warning:Jacobian Matrix is Non-Invertible!')

    if event == 'Inverse of J':
        # Inv(J)
        try:
            JM1 = np.concatenate((J1,J2,J3),1)
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI then, go first "Click before Solving Forward Kinematics!!!"')
            break

    
        IJ = np.linalg.inv (JM1)
        #print("IV =")
        #print(IV)
        sg.popup('IJ = ',IJ)

    if event == 'Transpose of J':
        #Transpose of Jacobian Matrix
        try:
            JM1 = np.concatenate((J1,J2,J3),1)
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI then, go first "Click before Solving Forward Kinematics!!!"')
            break


        TJ = np.transpose(JM1)
        #print("TJ= ",TJ)
        sg.popup('TJ = ',TJ)

    


window.close()
