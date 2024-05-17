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
            vals = line.split() 
            try:
                    # Try to process the line as numbers
                numbers = [float(num) for num in line.split()]
                    # Process the numbers here # Split each line into "words"
                if len(vals) >= 2:  # Ensure at least two values are present
                    tim.append(float(vals[0]))  # Convert values to floart and assign to corresponding list 
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
            except ValueError: 
                continue 
except FileNotFoundError:
    print("File not found:", file_name)
except Exception as e:
    print("An error occurred:", e)

#set up lists for values, h is corresponding enthalpy, m is mass flow, p is power 

h1w = [] 
h2w = []
hdifw = []
h1r = []
h2r = []
h3r= []
h4r = []
mw  = []
mr = [] 
pw = []
pw2 =[]
pr =[]
copw = []
copw2 =[] 
copr = []
wc = []
pdraw = [] #power drawn by system
h1satT =[]
h1satP =[]

for i in range(700):
    #calculate enthalpies using coolprop
    h1w.append(cp.PropsSI ('H','T',T1w[i],'Q',0.0,"Water")) 
    h2w.append(cp.PropsSI ('H','T',T2w[i],'Q',0.0,"Water"))
    hdifw.append(4200*(T2w[i]-T1w[i]))

    h1r.append(cp.PropsSI ('H','P|gas', p1[i] ,'T',T1r[i],"R134a")) # using t and p here gives sevrely oscillating values of h1 
    h1satT.append(cp.PropsSI ('H','Q', 1,'T',T1r[i],"R134a"))
    h1satP.append(cp.PropsSI ('H','Q', 1,'P',p1[i],"R134a"))
    h2r.append(cp.PropsSI ('H','T',T2r[i],'P',p2[i],"R134a"))
    h3r.append(cp.PropsSI ('H','T',T3r[i],'P',p2[i],"R134a")) # currently assuming no pressure drop through condenser, will need to deal with this 
    h4 = h3r[i]


    pdraw.append(I[i]*240)

    mw.append(qw[i]/60) # calculate water mass flow (assume rho = 1000)
    mr.append(pdraw[i]/(h2r[i]-h1r[i])) # this does not take into account the fan, the actual power drawn by the compressor will be lower 

    pw.append(mw[i]*(hdifw[i])) # calculate power output base on enthalpy gained by water
    pw2.append(mw[i]*(h2w[i]-h1w[i]))
    pr.append(mr[i]*(h2r[i]-h3r[i])) #calculate power output based on enthalpy lost by refrigerant 
    copw.append(pw[i]/pdraw[i]) #calculate COP
    copw2.append(pw2[i]/pdraw[i])
    copr.append(pr[i]/pdraw[i])


prav = st.mean(pr)
copw_av = st.mean(copw)
copw_av2 = st.mean(copw2)
copr_av = st.mean(copr)

T2w = np.array(T2w)
T1w = np.array(T1w)
h2r = np.array(h2r)
h1r = np.array(h1r)
h1satT = np.array(h1satT) 
p1 = np.array(p1)
print("COP Based on water", copw_av, copw_av2 )
print("COP Based on Refrigerant", copr_av )
print(st.mean(mr))
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
ax1.plot(tim[0:700], p1[0:700]/1000)
ax1.set_title('Compressor Inlet Pressure')
ax1.set_xlabel('Time')
ax1.set_ylabel('Pressure (bar)')
ax2.plot(tim[0:700], T1r[0:700])
ax2.set_title('Compressor Inlet Temprature')
ax2.set_xlabel('Time')
ax2.set_ylabel('Temperature (K)')
ax3.plot(tim[0:700], h1r[0:700]/1000)
ax3.plot(tim[0:700], h1satT[0:700]/1000)
ax3.set_xlabel('Time')
ax3.set_ylabel('specific Enthalpy (kJ/kg)')
ax3.set_title('Compressor Inlet Enthalpy vs Saturation')
#ax3.legend('H1 calaculated from T, P', 'H1sat calculated from measured T', 'H1sat calculated from measured P' )

plt.show()