# -*- coding: utf-8 -*-
"""
Python script to generate G code for milling a slope  
Created on December 19 2022
@author: G de Graaf
"""
import os
from datetime import datetime

time_now = datetime.now().strftime("%H:%M:%S")
rt = datetime.now()
date_now = str(rt.day)+"-"+ str(rt.month) +"-"+ str(rt.year)
TimeInfo = time_now +'    '+ date_now
#  Inputs slope  starts at Xorg, Yorg,z = D
# z=0 = top of material
D = 10.7  #  depth 
L = 10.7   # Length  (x)
T = 3.0    # Tool diameter
W = 10.7  #  width (y)
Tl = 20   # Tool total length (20 mm max)
DZz= 1.0  # milling step vertical down
# Origin DEFINED TO THe CENTER of the pocket !!!
Xorg = 0.0   # Origin X
xorg = str(format(Xorg, '.3f'))
Yorg = 0.0   # origin Y
yorg = str(format(Yorg, '.3f'))

filenamebase1 ="Pocket"
filenamebase3 ="InfoGCode"
filename1 = filenamebase1 + ".nc"
infofilename = filenamebase3 + ".txt"

#  Toolpath
DT = 0.8 *T   # minimum horizontal step with 20% tool overlap
# tool offset
Toy = T/2   # offset for the tool Y
Tox = T/2   # offset for the tool X
if L < 0 : 
    Toy = -T/2   # offset for the tool
if W < 0 : 
    Tox = -T/2   # offset for the tool


# endpoints for W and L pocket mill
# with tool offset !!
# absolute coordinates
Xs = Xorg  + Tox
Xe = Xorg + L - Tox
Ye = Yorg + W - Toy
Ys = Yorg + Toy
# centerX and centerY
# absolute coordinates
Xc = Xs + (Xe-Xs)/2
Yc = Ys + (Ye-Ys)/2

# stepsize in x,y directions (can be negative)

# Z steps  
# D is the flat part depth (z)
Nz = int(D/DZz+1)
DZ = D/(Nz)

NXc = (L/2 - Tox) / DT
NYc = (W/2 - Toy) / DT
# min steps in x y directiono nearest integer 
Nx = abs(int(NXc))+1
Ny = abs(int(NYc))+1
# select the largest number of steps
if Ny > Nx:  # decrease steps for Y
    NT = Ny
else: # decrease steps for Y
    NT = Nx
#   These are the actual steps
DX = abs((L/2 -Tox)/NT)
DY = abs((W/2 -Toy)/NT)
print("Xs =", Xs," Xe =", Xe, " Yb =", Ys, " Ye =",Ye )
print("Nx =", Nx," Ny =", Ny, " N =", NT)
print("Dx =", DX," Dy =", DY)

# GCodes
#  G54; Work Coordinates
#  G21; mm-mode
#  G40 Tool diameter compensation off
#  G90; Absolute Positioning
#  M3 S1000; Spindle On
BeginGcode = "G54 G21 G90 G40 M3 S10000 ; Spindle ON \n"
SafeMoveGcode = "G0 Z5   ; move to z-safe height \n"
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



def writeinfo():
    print("Writing Information to file GcodeInfo.txt ")
    with open(infofilename, "w") as Infof:
        Infof.write("File : " +infofilename+ " (in [mm]) \n")
        Infof.write("Created:  "+TimeInfo + "  \n")
        Infof.write("Depth Z = Dmin            "+str(format(D, '.2f')+"\n"))
        Infof.write("Length (Xdirection)       "+str(format(L, '.2f')+"\n"))
        Infof.write("Width  (Ydirection)       "+str(format(W, '.2f')+"\n"))
        Infof.write("Tool diameter             "+str(format(T, '.2f')+"\n"))
        Infof.write("Tool maximum length       "+str(format(Tl, '.2f')+"\n"))
        Infof.write("Vertical tool steps (DZz) "+str(format(DZz, '.2f')+"\n"))
        Infof.write("Origin X        (Xorg)    "+str(format(Xorg, '.2f')+"\n"))
        Infof.write("Origin Y        (Yorg)    "+str(format(Xorg, '.2f')+"\n"))
    Infof.close()
    return

def StartPocket(Xnz,Ynz,Znz):
    # Gcode : Go to start position Xnz,Ynz
    z = str(format(Znz, '.2f'))  
    xs = str(format(Xnz, '.2f'))
    ys = str(format(Ynz, '.2f'))
    with open(filename1, "a") as GCfout:
        # move up 3mm above workpiece
        GCfout.write("G1 F200 Z1.0 \n") 
        GCfout.write("G0 X"+xs+" Y"+ys+" F500 \n")
        # Move tool down slowly to start mill at depth Z 
        GCfout.write("G1 F50 Z-"+z+"\n") 
    return

def  PocketGcode(XC,YC,X2,Y2,Z):
    # Code for a rectangular pocket   [-x1,-y1] [x1,y1]
    x1 = str(format(XC+X2, '.2f'))
    y1 = str(format(YC+Y2, '.2f')) 
    x2 = str(format(XC-X2, '.2f'))
    y2 = str(format(Yc-Y2, '.2f')) 
    z = str(format(-Z, '.2f'))  
    with open(filename1, "a") as GCfout:
        # Gcode : Mill a line at y2 from x1 to x2
        GCfout.write("G1 X"+x1+" Y"+y1+ " Z"+z+ " F250 \n")             
        # Gcode : Mill a line at x2 from 
        GCfout.write("G1 X"+x2+" Y"+y1+ " Z"+z+ " F250 \n")              
        # Gcode : Mill a line at y=1 from x1 to -y1
        GCfout.write("G1 X"+x2+" Y"+y2+ " Z"+z+ " F250 \n") 
        # Gcode : Mill a line at y=1 from x1 to -y1
        GCfout.write("G1 X"+x1+" Y"+y2+ " Z"+z+ " F250 \n")
        # Gcode : Mill a line at y=1 from x1 to -y1
        GCfout.write("G1 X"+x1+" Y"+y1+ " Z"+z+ " F250 \n")
    return

def PocketFlat(Z):
    # Rectangle depth Z at Xe,Ye  Xb,Yb     
    # Uses global variables Xc Yc and DY DX
    # pocket mill routine 

    # start in the middle
    StartPocket(Xc,Yc,Z)
    # repeat increasing rectangles  
    steps = range(NT)
    X = DX
    Y = DY

    for i in steps :
        print("step =", i)
        PocketGcode(Xc,Yc,X,Y,Z)
        X = X + DX     
        Y = Y + DY
# End pocketflat 
        

# Start at Z = 0 (+ DZ)
Z = DZ 
# Open the file 
print("Start writing Gcode to "+filename1)
with open(filename1, "w") as GCfout:
    GCfout.write("; GCode for milling centered at Xorg, Yorg,z = 0-D  \n")
    GCfout.write("; Use a long flat end cylindrical tool  \n")
    GCfout.write(BeginGcode)
    GCfout.write("; "+TimeInfo +" \n") 
    GCfout.flush()
    zsteps = range(Nz)
    for k in zsteps :
        print('Z=',Z)
        Z = Z + DZ
        PocketFlat(Z)
    GCfout.flush()       
# aDD END CODE to file 
with open(filename1, "a") as GCfout:
    GCfout.write(SafeMoveGcode)
    GCfout.write(EndGcode)
    GCfout.close()
writeinfo()
print("End")





