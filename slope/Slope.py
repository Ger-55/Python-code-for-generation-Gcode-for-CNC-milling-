# -*- coding: utf-8 -*-
"""
Python script to generate G code for a  sloped Pocket mill  
Created on December 19 2022
@author: G de Graaf
"""
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


# root window
root = tk.Tk()
root.geometry("250x550")
root.resizable(False, False)
root.title('GCode generator for  a slope ')

time_now = datetime.now().strftime("%H:%M:%S")
rt = datetime.now()
date_now = str(rt.day)+"-"+ str(rt.month) +"-"+ str(rt.year)
TimeInfo = time_now +'    '+ date_now
#  Inputs slope  starts at Xorg, Yorg,z = D
# z=0 = top of material
Dmin = 0.00  # Slope starting depth
Dmax = 14.0   # Slope ending depth 
L = 33.00  # Length of slope
T = 3.0    # Tool diameter and offset
DT = 0.8* T    # Tool overlap
W = 33.0   # Slope width
Tl = 20   # Tool total length (20 mm max)
DZz= 1.0  # milling step vertical down
N = (W-T)/(DT)  # define N 
Tox = T/2   # offset for the tool X
Toy= Tox    # offset for the tool Y
Xorg = 0.000  # Origin X
xorg = str(format(Xorg, '.3f'))
Yorg = 0.000   # origin Y
yorg = str(format(Yorg, '.3f'))
# Zup =safe position for rapid moves
Zup = 2.0 

filenamebase ="Slope"
filename = filenamebase + ".nc"
infofilename = filenamebase + ".txt"

#  Stringvariables for input vars
DepthMin = tk.StringVar(root, value=str(Dmin))
DepthMax = tk.StringVar(root, value=str(Dmax))
Length = tk.StringVar(root, value=str(L))
Width = tk.StringVar(root, value=str(W))
Xorigin = tk.StringVar(root, value=Xorg)
Yorigin = tk.StringVar(root, value=Yorg)
Depthstep = tk.StringVar(root, value=str(DZz))
Tooldiameter = tk.StringVar(root, value=str(T))
Toollength = tk.StringVar(root, value=str(Tl))

def submit_clicked():
    """ callback when the submit button clicked
    """
    Dmin = float(DepthMin_entry.get())
    Dmax = float(DepthMax_entry.get())
    L = float(Length_entry.get())
    W = float(Width_entry.get()) 
    Xorg = float(Xorigin_entry.get())
    Yorg = float(Yorigin_entry.get())
    T = float(Tooldiameter_entry.get())
    Tl = float(Toollength_entry.get())
    DZz = float(Depthstep_entry.get())
    D = Dmax-Dmin
  # D,Dm,L,T,W,GCfout.write,Xorigin,Yorigin
    # do some basic checks for 60 degree tool
    if D > Tl :
        msg = ('You entered a deeper structure than the tool can handle')
        showinfo(title='WARNING', message=msg)
    print("Command clicked")
    # calculate variables 
    DT = 0.8 * T   # minimum horizontal step with 20% tool overlap
    # tool offset
    Toy = T/2   # offset for the tool X
    Tox = T/2   # offset for the tool X
    if L < 0 : 
        Toy = -T/2   # offset for the tool
    if W < 0 : 
        Tox = -T/2   # offset for the tool
    Xs = Xorg + Tox
    Ys = Yorg + Toy
    Xe = Xorg + W - Toy
    Ye = Yorg + L - Toy
    # Z 
    Zs = Dmin
    Ze = Dmax
    
    # program call
 #   flat()
    Slope(Xs,Xe,Ys,Ye,Zs,Ze)
    writeinfo()
    return 

# GCodes
#  G54; Work Coordinates
#  G21; mm-mode
#  G40 Tool diameter compensation off
#  G90; Absolute Positioning
#  M3 S1000; Spindle On
BeginGcode = "G54 G21 G90 G40 M3 S10000 ; Spindle ON \n"
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


# Sign in frame
DataEntry = ttk.Frame(root)
DataEntry.pack(padx=10, pady=10, fill='x', expand=True)
# Depth of groove
DepthMin_label = ttk.Label(DataEntry, text="Slope starting depth [mm]: ")
DepthMin_label.pack(fill='x', expand=True)
DepthMin_entry = ttk.Entry(DataEntry, textvariable=DepthMin)
DepthMin_entry.pack(fill='x', expand=True)
DepthMin_entry.focus()
# DepthMax
DepthMax_label = ttk.Label(DataEntry, text="Slope ending depth :[mm]")
DepthMax_label.pack(fill='x', expand=True)
DepthMax_entry = ttk.Entry(DataEntry, textvariable=DepthMax)
DepthMax_entry.pack(fill='x', expand=True)
# Slope  length
Length_label = ttk.Label(DataEntry, text="Length Y= [mm]")
Length_label.pack(fill='x', expand=True)
Length_entry = ttk.Entry(DataEntry, textvariable=Length)
Length_entry.pack(fill='x', expand=True)

#  Xorigin
Xorigin_label = ttk.Label(DataEntry, text="X origin: [mm]")
Xorigin_label.pack(fill='x', expand=True)
Xorigin_entry = ttk.Entry(DataEntry, textvariable=Xorigin)
Xorigin_entry.pack(fill='x', expand=True)

#  Yorigin
Yorigin_label = ttk.Label(DataEntry, text="Y origin: [mm]")
Yorigin_label.pack(fill='x', expand=True)
Yorigin_entry = ttk.Entry(DataEntry, textvariable=Yorigin)
Yorigin_entry.pack(fill='x', expand=True)

# Marker distance
Width_label = ttk.Label(DataEntry, text="Width W:[mm]")
Width_label.pack(fill='x', expand=True)
Width_entry = ttk.Entry(DataEntry, textvariable=Width)
Width_entry.pack(fill='x', expand=True)

# Tooldiameter
Tooldiameter_label = ttk.Label(DataEntry, text="Tool diameter: [mm]")
Tooldiameter_label.pack(fill='x', expand=True)
Tooldiameter_entry = ttk.Entry(DataEntry, textvariable=Tooldiameter)
Tooldiameter_entry.pack(fill='x', expand=True)
# Tool Length
Toollength_label = ttk.Label(DataEntry, text="Tool length (total):[mm]")
Toollength_label.pack(fill='x', expand=True)
Toollength_entry = ttk.Entry(DataEntry, textvariable=Toollength)
Toollength_entry.pack(fill='x', expand=True)
# Vertical steps GCfout.write
Depthstep_label = ttk.Label(DataEntry, text="Vertical step (Z) [mm]: ")
Depthstep_label.pack(fill='x', expand=True)
Depthstep_entry = ttk.Entry(DataEntry, textvariable=Depthstep)
Depthstep_entry.pack(fill='x', expand=True)
# ------------------------------


def writeinfo():
    print("Writing Information to file SlopeInfo.txt ")
    with open(infofilename, "w") as Infof:
        Infof.write("File : " +infofilename+ " (in [mm]) \n")
        Infof.write("Created:  "+TimeInfo + "  \n")
        Infof.write("Slope starts at Xorg, Yorg,z = Dmin \n")
        Infof.write("Minimmum depth Z = Dmin   "+str(format(Dmin, '.2f')+"\n"))
        Infof.write("Maximum depth Z = Dmax    "+str(format(Dmax, '.2f')+"\n"))
        Infof.write("Slope width (Xdirection) "+str(format(W, '.2f')+"\n"))
        Infof.write("Slope length (Ydirection) "+str(format(L, '.2f')+"\n"))
        Infof.write("Tool diameter             "+str(format(T, '.2f')+"\n"))
        Infof.write("Tool maximum length       "+str(format(Tl, '.2f')+"\n"))
        Infof.write("Vertical tool steps (DZz) "+str(format(DZz, '.2f')+"\n"))
        Infof.write("Origin X        (Xorg)    "+str(format(Xorg, '.2f')+"\n"))
        Infof.write("Origin Y        (Yorg)    "+str(format(Xorg, '.2f')+"\n"))
    Infof.close()

def LineGcode(X1,DX,Y1,Y2,Z1,Z2):
    # Start at x1,y1,Z1 !!! 
    # stop at x2,y1,Z1 !!!
    # Back-forth    
    x1 = str(format(X1, '.2f'))
    X2 = X1 + DX/2
    x2 = str(format(X2, '.2f'))
    X3 = X1 + DX
    x3 = str(format(X3, '.2f'))
    y1 = str(format(Y1, '.2f'))
    y2 = str(format(Y2, '.2f')) 
    zy1 = str(format(-Z1, '.2f'))  
    zy2 = str(format(-Z2, '.2f')) 
    with open(filename, "a") as GCfout:
    # Gcode : Mill a line at X1 from y1 to y2   (Ymove)
        GCfout.write("G1 X"+x1+" Y"+y1+ " Z"+zy1+ " F250 \n")
        # Gcode : Mill a line at y2 from x1 to x2 (xmove)
        GCfout.write("G1 X"+x1+" Y"+y2+ " Z"+zy2+ " F250 \n")             
        # Gcode : Mill a line at x2 from y=y2 to y=y1 (-Ymove)
        GCfout.write("G1 X"+x2+" Y"+y2+ " Z"+zy2+ " F250 \n") 
        # Gcode : Mill a line at y1 from x1 to x2 (xmove)
        GCfout.write("G1 X"+x2+" Y"+y1+ " Z"+zy1+ " F250 \n")  
        # Gcode : Mill a line at y1 from x1 to x2 (xmove)
        GCfout.write("G1 X"+x3+" Y"+y1+ " Z"+zy1+ " F250 \n")             
    return

def newzeroGCode(Xnz,Ynz,Znz,Zup):
    # Gcode : Go to start position Xnz,Ynz,Znz
    zz = str(format(Znz, '.2f'))  
    xs = str(format(Xnz, '.2f'))
    ys = str(format(Ynz, '.2f'))
    zup = str(format(Zup, '.2f'))
    # move up 1mm above workpiece
    with open(filename, "a") as GCfout:
        GCfout.write("G0 F400 Z"+zup+ "\n") 
        GCfout.write("G0 X"+xs+" Y"+ys+" F1000 \n")
        # Move tool down slowly to start mill at depth Z 
        GCfout.write("G1 F80 Z-"+zz+"\n") 
    return


def LayerGCode(Xs,Xe,Ys,Ye,ZS,ZE): 
    # coordinates for W and L square layer mill
    # with tool offset !!
    # Running variables
    XS = Xs
    XE = Xe
    YS = Ys
    YE = Ye  
    # Safe move to new location 
    newzeroGCode(XS,YS,ZS,Zup) 
    z = str(format(ZE, '.2f'))
    with open(filename, "a") as GCfout:
        GCfout.write("; Depth = "+z+"\n")
    print("; Depth = "+z+"\n")
    Nx = (W-T)/(DT)  # define N 
    Nxx = abs(int(Nx+1))
    print("Nx =", Nx," Nxx =", Nxx) 
    DX = (W-2*Tox)/Nxx
    xsteps = range(Nxx + 1)
    # Loop for the flat part
    for k in xsteps: 
        # renew x and y
        # mill a line If dx = 0 the last line
        LineGcode(XS,DX,YS,YE,ZS,ZE)
        XS = XS+DX
        XE = XE+DX
   # end loop
    # last line  = a SINGLE line  !!!
    LineGcode(XS,0,YS,YE,ZS,ZE)   
    # ---------------------------------------------------------
    return

def Slope(Xs,Xe,Ys,Ye,ZS,ZE):
    # coordinates for X,Y  square layer mill
    # with tool offset !!
    D = (ZE-ZS)
    Nz = int(D/DZz)+1
    # DZ is the depth step
    DZ = D/Nz
    
    print("Adding Gcode to file "+filename)
    with open(filename, "w") as GCfout:
        GCfout.write("; GCode for a slope at Xorg, Yorg, Width = W(mm), Length = L (mm)  \n")
        GCfout.write("; Depth (Z) starts at Dmin and ends at Dmax  \n")
        GCfout.write(BeginGcode)
        GCfout.write("; "+TimeInfo +" \n") 
        # Loop for the flat part
        zsteps = range(Nz)
        Z = ZS
        for k in zsteps: 
            # renew x and y
            XS = Xs
            XE = Xe
            YS = Ys
            YE = Ye
            ZE = Z + DZ 
      #      newzeroGCode(XS,YS,ZS,Zup) 
            # do a layer 
            LayerGCode(XS,XE,YS,YE,ZS,Z)
            Z = Z + DZ
        # end loop
        GCfout.write(SafeMoveGcode)
        GCfout.write(EndGcode)
        GCfout.close()
        # ---------------------------------------------------------
    return


# Submit button
Submit_button = ttk.Button(DataEntry, text="Submit", command=submit_clicked)
Submit_button.pack(fill='x', pady=30)
# Exit button
Exit_button = ttk.Button(DataEntry, text="Exit",  command=root.destroy)
Exit_button.pack(fill='x', pady=10)
print("End")
root.mainloop()

