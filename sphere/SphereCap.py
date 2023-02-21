# -*- coding: utf-8 -*-
"""
A Python script to generate Gcode
to engrave a spherical cap
See notes.txt for info
Created on Fri Dec  2 22:35:52 2022
@author: G de Graaf
All sizes in [mm]
"""
import os
import math
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# root window
root = tk.Tk()
root.geometry("250x500")
root.resizable(False, False)
root.title('GCode generator for spheres')

time_now = datetime.now().strftime("%H:%M:%S")
rt = datetime.now()
date_now = str(rt.day) + "-" + str(rt.month) + "-" + str(rt.year)
TimeInfo = time_now +'    '+ date_now


R = 60.50  # R total milling radius
RM = 92.00  # Radius outer circle
H = 45.0  # Sphere depth
TF = 1.5   # Tool diameter fine
TC = 6.0   # Tool diameter coarse
Tl = 55.0   # Tool effective length
HM = 50.0  # Material thickness ( > H )
DZ = 2  # step vertical down

# Fine milling : change the tool to Ball tip
DZZ = DZ/3  # Vertical step for fine milling

#  Stringvariables for input vars
Radius = tk.StringVar(root, value=str(R))
Outerradius = tk.StringVar(root, value=str(RM))
ToolC = tk.StringVar(root, value=str(TC))
ToolF = tk.StringVar(root, value=str(TF))
Depth = tk.StringVar(root, value=str(H))
Toollength = tk.StringVar(root, value=str(Tl))
Materialthickness = tk.StringVar(root, value=str(HM))


# calculate some values from the input variables
Z = 0.00  # start cutting depth
Rend = R   # no more vertical steps after Rend
Rsph = (H**2 + R**2)/(2*H) # calculate the sphere radius
Rsphc = Rsph - TC/2 # The coarse sphere radius is somewhat larger
print("Fine sphere radius = ", Rsph)
print("Fine sphere radius = ", Rsphc)
# where to start for coarse milling
RS = math.sqrt(2 * Rsph * Z - Z**2)
DX =  TC  # horizontal steps DX (coarse milling )
# where to start for fine milling
RSS = math.sqrt(2 * Rsph * DZZ - DZZ**2)
DXX = 0.5  # horizontal steps DXx (fine milling)
# counters for circles xy and z
Kf = 0 
Kc = 0
# GCodes
# G54; Work Coordinates
# G21; mm-mode
# G40 Tool diameter compensation off
# G90; Absolute Positioning
# M3 S1000; Spindle On
BeginGcode = "G54 G21 G90 G17 G40 M3 S10000 ; Spindle ON \n"
SafeMoveGcode = "G0 Z10; move to z-safe height \n"
# M5 S0; Spindle Off
EndGcode = "M5 S0 ; End Code Stop spindle \n "

global mypath
#  file manipulation
cwd = os.getcwd()
print("Your working directory is ", cwd)
# read the template file
directory = "CNC"
path = os.path.join(cwd, directory)
mypath = path
os.chdir(mypath)
if not os.path.exists(path):
    os.makedirs(path)
    print("Directory '%s' created" %directory )
print("Program working directory changed to:", mypath)
GCode_Fine="Spherecapfine.nc"
GCode_Coarse="Spherecapcoarse.nc"

# Sign in frame
DataEntry = ttk.Frame(root)
DataEntry.pack(padx=10, pady=10, fill='x', expand=True)
# Depth of sphere 
Depth_label = ttk.Label(DataEntry, text="Sphere height [mm]: ")
Depth_label.pack(fill='x', expand=True)
Depth_entry = ttk.Entry(DataEntry, textvariable=Depth)
Depth_entry.pack(fill='x', expand=True)
Depth_entry.focus()

# Sphere  radius
Radius_label = ttk.Label(DataEntry, text="Sphere radius R  [mm]")
Radius_label.pack(fill='x', expand=True)
Radius_entry = ttk.Entry(DataEntry, textvariable=Radius)
Radius_entry.pack(fill='x', expand=True)

#  Outer radius
Outerradius_label = ttk.Label(DataEntry, text="Outer radius RM [mm]")
Outerradius_label.pack(fill='x', expand=True)
Outerradius_entry = ttk.Entry(DataEntry, textvariable=Outerradius)
Outerradius_entry.pack(fill='x', expand=True)

#  ToolC
ToolClabel = ttk.Label(DataEntry, text="Tool diameter coarse: [mm]")
ToolClabel.pack(fill='x', expand=True)
ToolCentry = ttk.Entry(DataEntry, textvariable=ToolC)
ToolCentry.pack(fill='x', expand=True)
# ToolF
ToolFlabel = ttk.Label(DataEntry, text="Tool diameter fine  : [mm]")
ToolFlabel.pack(fill='x', expand=True)
ToolFentry = ttk.Entry(DataEntry, textvariable=ToolF)
ToolFentry.pack(fill='x', expand=True)
# Material thickness
Material_label = ttk.Label(DataEntry, text="Material thickness:[mm]")
Material_label.pack(fill='x', expand=True)
Material_entry = ttk.Entry(DataEntry, textvariable=Materialthickness)
Material_entry.pack(fill='x', expand=True)

# Tool Length
Toollength_label = ttk.Label(DataEntry, text="Tool length (total):[mm]")
Toollength_label.pack(fill='x', expand=True)
Toollength_entry = ttk.Entry(DataEntry, textvariable=Toollength)
Toollength_entry.pack(fill='x', expand=True)

# ------------------------------



def writeinfo():
    print("Writing Information to file SphereInfo.txt ")
    with open("SphereInfo.txt", "w") as Infof:
        Infof.write("File : SphereInfo.txt (in [mm]) \n")
        Infof.write("Created:  "+TimeInfo + "  \n")
        Infof.write("Coarse Gcode file:  "+GCode_Coarse +".  \n")
        Infof.write("Final  Gcode file:  "+GCode_Fine +".  \n")
        Infof.write("R total milling Radius "+str(format(R, '.2f')+"\n"))
        Infof.write("Rm outer circle Radius "+str(format(RM, '.2f')+"\n"))
        Infof.write("Sphere depth             "+str(format(H, '.2f')+"\n"))
        Infof.write("Tool diameter coarse     "+str(format(TC, '.2f')+"\n"))
        Infof.write("Tool diameter fine       "+str(format(TF, '.2f')+"\n"))
        Infof.write("Material thickness (> H) "+str(format(HM, '.2f')+"\n"))
        Infof.write("Vertical steps  (coarse) "+str(format(DZ, '.2f')+"\n"))
        Infof.write("Milling circles (coarse) "+str(format(Kc, '.2f')+"\n"))
        Infof.write("Milling circles (fine)   "+str(format(Kf, '.2f')+"\n"))
        Infof.write("Sphere radius  (coarse)  "+str(format(Rsphc, '.2f')+"\n"))
        Infof.write("Sphere radius  (fine)    "+str(format(Rsph, '.2f')+"\n"))
        Infof.write("Start milling x,y coarse "+str(format(RS, '.2f')+"\n"))
        Infof.write("Start milling x,y fine   "+str(format(RSS, '.2f')+"\n"))
    Infof.close()
    
print("Writing coarse gcode to file: "+GCode_Coarse)
with open(GCode_Coarse, "w") as GCfout:
    GCfout.write("; Gcode for sphere: "+GCode_Coarse+" \n")
    GCfout.write(BeginGcode)
    Z = DZ 
    while Z <= H:
        # Outer loop: vertical coarse milling at Z linear depth step DZ 
        # and variable starting point RS
        # Calculate starting point RS from variable Z
        # RS = horintal (x) point on a circle RS^2 +(2*Rsp-Z)^2 = Rsp^2
        # Rs^2 = -3Rsp^2 + 4Rsp*Z - Z^2
        RS = math.sqrt(2 * Rsphc * Z - Z**2)
        rs = str(format(RS, '.2f'))
        X = RS
        # decrease the calculated milling depth with 1.5 mm
        # to leave some material for the fine step
        #
        z = "Z-"+str(format((Z-TF), '.2f'))+"\n"
        print ("Depth = -" + z)
        while X <= RM:
            # Inner loop : Horizontal milling 
            # Remove a layer DZ by inside circles clockwise and a move 
            # with steps DX from X=Rstart until X=RM
            r = str(format(X, '.2f')+" ")
            # Move to start position at safe level
            GCfout.write("G0 F200 X"+r+" Y0 Z1.0 \n")
            # Plunge down
            # Start slow milling down to Z
            GCfout.write("G1 F50 "+z)
            GCfout.write("G3 F300 X0 Y"+r+" I-"+r+"J0 \n")
            GCfout.write("G3 F300 X-"+r+"Y0 I0 J-"+r+"\n")
            GCfout.write("G3 F300 X0 Y-"+r+"I"+r+ "J0 \n")
            GCfout.write("G3 F300 X"+r+"Y0 I0 J"+r+" \n")
            X = X + DX
            Kc = Kc+1
        #
        Z = Z + DZ  # absolute Depth position
    GCfout.write(SafeMoveGcode)
    GCfout.write(EndGcode)
GCfout.close()
    #     

# fine milling file 
print("Writing fine gcode to file: "+GCode_Fine)
with open(GCode_Fine, "w") as GCf2:
    GCf2.write("; Gcode for sphere: "+GCode_Fine+" \n")
    GCf2.write(BeginGcode)
    X=  DXX
    while X <= R:
        # Circles vertical fine engraving with increasing depth Z
        # and constant step DXX
        # Calculate Z from sphere and increasing X coordnate
        Z =  -(Rsph - math.sqrt(Rsph**2 - X**2)) 
        print("X="+str(format(X, '.4f'))+" Z="+str(format(Z, '.4f')))
        z = "Z"+str(format(Z, '.2f'))+"\n"
        # Remove a  circle clockwise 
        # with steps DX from X=Rst until X=RM
        r = str(format(X, '.2f')+" ")
        # Move to start position at safe level
        GCf2.write("G0 F200 X"+r+" Y0 Z1.0 \n")
        # Plunge down
        # Start fine milling down to Z
        GCf2.write("G1 F50 "+z)
        GCf2.write("G3 F300 X0 Y"+r+" I-"+r+"J0 \n")
        GCf2.write("G3 F300 X-"+r+"Y0 I0 J-"+r+"\n")
        GCf2.write("G3 F300 X0 Y-"+r+"I"+r+ "J0 \n")
        GCf2.write("G3 F300 X"+r+"Y0 I0 J"+r+" \n")
        X = X + DXX  #  Next circle
        Kf = Kf +1
        # ----------------
    # ----------------
    GCf2.write(SafeMoveGcode)
    GCf2.write(EndGcode)
    GCf2.close()
writeinfo()
def submit_clicked():
    """ callback when the submit button clicked
    """
    global R, H, TC, TF, Tl, HM, RM
    H = float(Depth_entry.get())
    R = float(Radius_entry.get())
    TC = float(ToolCentry.get())
    TF = float(ToolFentry.get())
    Tl = float(Toollength_entry.get())
    HM = float(Material_entry.get()) 
    RM = float(Outerradius_entry.get())
    # do some basic checks for 60 degree tool
    if H > Tl :
        msg = ('You entered a deeper carve than the tool can handle')
        showinfo(title='WARNING', message=msg)
    if H > HM :
        msg = ('You entered a larger height than the material thickness')
        showinfo(title='WARNING', message=msg)
    print("Command clicked")
    writeinfo()
    msg = ('Writing GCode to files\n'+GCode_Coarse+'\n'+GCode_Fine+' \n')
    showinfo(title='', message=msg)
    return 

# Submit button
Submit_button = ttk.Button(DataEntry, text="Submit", command=submit_clicked)
Submit_button.pack(fill='x', pady=30)

# Exit button
Exit_button = ttk.Button(DataEntry, text="Exit",  command=root.destroy)
Exit_button.pack(fill='x', pady=10)
print("End")
root.mainloop()


print("End")
