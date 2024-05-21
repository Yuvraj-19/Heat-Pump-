
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import numpy as np 
import statistics as st
from tabulate import tabulate

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
file_name = "Max flow, fan 2.5"

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
I_no_comp = 3.2740721739130434 # calculated current when the fan is on full and compressor is not running.
h2w = []
hdifw = []
h1r = []
h2r = []
h3r= []
h4r = []
mw  = []
mr = [] 
mr_dry01 =[]
ma = []
power_w = []
pw2 =[]
power_r =[]
power_r_dry01 =[]
copw = []
copw2 =[] 
copr = []
wc = []
power_draw = [] # power drawn by system
power_draw_compressor = [] # power drawn by compressor
copr2 = []
copr_no_p_loss = []
s4r = []
s3r = []
s2r = []
s1r = []
irr_gen_comp = []
irr_gen_heat_ex =[]
irr_gen_throttle = []
irr_gen_evap = []
p3r = []
p3r_loss = []
h2r_s =[]
eta_c =[]
s1 = []
s2 =[]
h3r_dry01 =[]
p4 = []

for i in range(len(T1w)):
    #calculate enthalpies using coolprop
    hdifw.append(4200*(T2w[i]-T1w[i]))
    
    h1r.append(cp.PropsSI ('H','P|gas', p1[i] ,'T',T1r[i],"R134a")) # using t and p here gives sevrely oscillating values of h1 
    s1.append(cp.PropsSI('S', 'P|gas', p1[i] ,'T',T1r[i],"R134a"))
    h2r.append(cp.PropsSI ('H','T',T2r[i],'P',p2[i],"R134a"))
    h2r_s.append(cp.PropsSI('H', 'P', p2[i] ,'S',s1[i],"R134a"))
    s2.append(cp.PropsSI ('S','T',T2r[i],'P',p2[i],"R134a"))
    eta_c.append((h2r_s[i]-h1r[i])/(h2r[i]-h1r[i]))
    h3r.append(cp.PropsSI ('H','T',T3r[i],'Q',0.0,"R134a")) # assuming wet saturated on exit from the condenser
    h3r_dry01.append(cp.PropsSI ('H','T',T3r[i],'Q',0.1,"R134a")) #Assuming dryness fraction of 0.1 at condenser exit
    h4r.append(h3r[i])
    
    power_draw.append(I[i]*244.5*0.98)
     # now only considering compressor work and using power factor

    mw.append(qw[i]/60) # calculate water mass flow (assume rho = 1000)
    mr.append((mw[i]*hdifw[i])/((h2r[i]-h3r[i]))) # 0.97 for percentage of enthalpy transferred from refrigerant to water
    mr_dry01.append((mw[i]*hdifw[i])/((h2r[i]-h3r_dry01[i])))
    power_draw_compressor.append((h2r[i]-h1r[i])*mr[i])
    power_w.append(mw[i]*(hdifw[i])) # calculate heat output base on enthalpy gained by water
    power_r.append(mr[i]*(h2r[i]-h3r[i]))#
    power_r_dry01.append(mr[i]*(h2r[i]-h3r_dry01[i]))
    copw.append(power_w[i]/power_draw[i]) #calculate COP based on water
    p4.append(cp.PropsSI('P','T',T4r[i],'Q',0.05,"R134a")) #calculate p4 

    #copr.append(pr[i]/pdraw[i])
    copr2.append((h2r[i] - h3r[i])/(h2r[i] - h1r[i])) #calculating COP purely thermodynamically
    copr_no_p_loss.append((h2r[i] - h3r_dry01[i])/(h2r[i] - h1r[i]))
    # calculating air mass flow rate 
    ma.append(mr[i]*(h4r[i] - h1r[i])/(1005*(T2a[i] - T1a[i])))


#looking at irreversible entropy generation and pressure losses.
for i in range(len(T1w)):
    s3r.append(cp.PropsSI ('S','T',T3r[i],'Q',0,"R134a"))
    s2r.append(cp.PropsSI ('S','T',T2r[i],'P',p2[i],"R134a"))
    s1r.append(cp.PropsSI ('S','P|gas', p1[i] ,'T',T1r[i],"R134a"))
    s4r.append(cp.PropsSI ('S','P', p1[i] ,'T',T4r[i],"R134a"))
    p3r.append(cp.PropsSI ('P','Q',0.0 ,'T',T3r[i],"R134a"))
    p3r_loss.append(p2[i] - p3r[i])
    irr_gen_comp.append(s2r[i] - s1r[i])
    irr_gen_throttle.append(s4r[i] - s3r[i])


evap_p_loss = (st.mean(p4)/10**5 - st.mean(p1)/10**5)/(st.mean(p1)/10**5)
ma_av = st.mean(ma)
irr_gen_comp_av = st.mean(irr_gen_comp)
irr_gen_throttle_av = st.mean(irr_gen_throttle)
p3r_loss_av = st.mean(p3r_loss)
copw_av = st.mean(copw)
copr_no_p_loss = st.mean(copr_no_p_loss)
copr2_av = st.mean(copr2)
eta_c_av = st.mean(eta_c)

T2w = np.array(T2w)
T1w = np.array(T1w)
h2r = np.array(h2r)
h1r = np.array(h1r)
p1 = np.array(p1)
power_comp_frac = st.mean(power_draw_compressor)/st.mean(power_draw)

# Data for the table
table_data = [
    ["Calculated mass flow rate of air through evaporator (kg/s)", ma_av],
    ["Pressure of refrigerant lost in the condensor(bar)", p3r_loss_av / 1e5],
    ["Irreversible entropy generation due to compressor (J/kgK)", irr_gen_comp_av],
    ["Irreversible entropy generation due to throttle (J/kgK)", irr_gen_throttle_av],
    ["COP Based on water", copw_av],
    ["COP Based on Refrigerant", copr2_av],
    ["COP Based on Refrigerant assuming no condensor pressure loss", copr_no_p_loss],
    ['Power ouptut based on water (kW)' , st.mean(power_w)],
    ['Power output based on refrigerant (kW)', st.mean(power_r)],
    ['Percentage of Power Draw by Compressor', power_comp_frac],
    ['Compressor Isentropic Efficiency', eta_c_av],
    ['Refrigerant mass flow assuming sat liquid @3', st.mean(mr)],
    ['Refrigerant mass flow assuming no condenser pressure loss', st.mean(mr_dry01)],
    ['Water volumetric flow rate', st.mean(qw)],
    ['Water mass flow rate', st.mean(mw)],
    ['Average T2w', st.mean(T2w)-273.15]
    ['Evaporator Pressure loss', evap_p_loss*100, '%']
    
]

# Print the table using tabulate
print(tabulate(table_data, headers=["Metric", "Value"], tablefmt="grid"))
