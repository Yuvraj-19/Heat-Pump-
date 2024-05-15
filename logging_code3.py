import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import numpy as np 
import statistics as st
# Initiate lists for values, number is circuit locations,w is wataer, a is air , r is refrigerant
# p1 is compressor inlet, 2 is outlet, see diagram in handout for reference
tim = []    
T1w = []
T2w = []
T1a = []
T2a = []
T1r = []
T2r = []
T3r = []
T4r = []
p1=[]
p2 = []
I = []
qw= []
#pick the text file to use
file_name = "HP_May10_05"

#add values from files to list 

try:
    with open(file_name, "r") as data_file:  # Open file using "with" statement for automatic closure
        title = data_file.readline()  # Read first header line
        props = data_file.readline()  # Read second header line

        # Now read in data line by line
        for line in data_file:
            vals = line.split()  # Split each line into "words"
            if len(vals) >= 2:  # Ensure at least two values are present
                tim.append(float(vals[0]))  # Convert values to float and assign to corresponding list 
                T1w.append(float(vals[1])+273.15)  # Convert the second value to floating point and append to T1w[]
                T2w.append(float(vals[2])+273.15)  # convert temp to K
                T1a.append(float(vals[3])+273.15)
                T2a.append(float(vals[4])+273.15)
                T1r.append(float(vals[5])+273.15)
                T2r.append(float(vals[6])+273.15)
                T3r.append(float(vals[7])+273.15)
                T4r.append(float(vals[8])+273.15)
                p1.append(float(vals[9])*10**5) # convert pressures to Pa
                p2.append(float(vals[10])*10**5)
                I.append(float(vals[11]))
                qw.append(float(vals[12]))
            else:
                print("Skipping line with insufficient data:", line)
except FileNotFoundError:
    print("File not found:", file_name)
except Exception as e:
    print("An error occurred:", e)

#set up lists for values, h is corresponding enthalpy, m is mass flow, p is power 

h1w = [] 
h2w = []
h1r = []
h2r = []
h3r= []
h4r = []
mw  = []
mr = [] 
pw = []
pr =[]
copw = []
copr = []
wc = []
pdraw = [] #power drawn by system

# Removed for loop here since cp.PropsSI can take arrays as arguments
h1w = (cp.PropsSI ('H','T',T1w,'Q',0.0,"Water")) 
h2w = (cp.PropsSI ('H','T',T2w,'Q',0.0,"Water"))

# I changed this since h4r =! h3r. 
h1r = (cp.PropsSI ('H','T',T1r,'Q',1.0,"R134a"))
h2r = (cp.PropsSI ('H','T',T2r,'P',p2,"R134a"))
h3r = (cp.PropsSI ('H','T',T3r,'Q',0.0,"R134a")) # currently assuming no pressure drop through heat exchanger, will need to deal with this 
h4r = (cp.PropsSI ('H','T',T3r,'P',p2,"R134a"))

for i in range(len(T1w)):
    pdraw.append(I[i]*240/np.sqrt(2))

    mw.append(qw[i]/60) # calculate water mass flow (assume rho = 1000)
    mr.append(pdraw[i]/(h2r[i]-h1r[i])) # this does not take into account the fan, the actual power drawn by the compressor will be lower 

    pw.append(mw[i]*(h2w[i]-h1w[i])) # calculate power output base on enthalpy gained by water
    pr.append(mr[i]*(h2r[i]-h3r[i])) #calculate power output based on enthalpy lost by refrigerant 
    copw.append(pw[i]/pdraw[i]) #calculate COP
    copr.append(pr[i]/pdraw[i])

copw_av = st.mean(copw)
copr_av = st.mean(copr)
print("COP Based on water", copw_av )
print("COP Based on Refrigerant", copr_av )

