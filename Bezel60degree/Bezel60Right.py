# -*- coding: utf-8 -*-
"""
Python script to generate G code for a 60 degree bevel
Created on Nov 27 2022
@author: G de Graaf
"""
import os
import math

# Inputs
D = 10.20  # Material thickness = Depth of Vgroove 
L = 66.00  # Length of Vgroove start at Xorg,Yorg,0
M = 4.00   # Marker hole depth
T = 3.0    # Tool diameter
Ta = 2.0   # Tool active length
DZ = 1.0   # step vertical down < Ta 

DX = DZ/math.sqrt(3) # horizontal step for 60 degree angle  
Ao = 0     #  x offset of Pin Alignment hole  
Xo= T/2    # offset for my tool
Xorg = 0.000 # Origin X
xorg = str(format(Xorg,'.3f'))
Yorg = 0.00  # origin Y
yorg = str(format(Yorg,'.3f'))
# calculate the lateral (X) starting point for 60 degree bevel angle
Xs = -(D-DZ)/math.sqrt(3)+ Xorg
# the lateral (X) ending point  
Xe = Xorg
print ("Start at  = ", Xs)
# Y end coordinate
Ls = str(format(L+Yorg,'.2f'))

## GCodes
## G54; Work Coordinates
## G21; mm-mode
## G40 Tool diameter compensation off
## G90; Absolute Positioning
## M3 S1000; Spindle On
BeginGcode ="G54 G21 G90 G40 M3 S10000 ; Spindle ON \n"
SafeMoveGcode = "G0 Z10; move to z-safe height \n"
# M5 S0; Spindle Off
EndGcode ="M5 S0 ; End Code Stop spindle \n "
 
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
   print("Directory '%s' created" %directory)

print("Program working directory changed to:", mypath)

def writeinfo():
    print("Writing Information to file BezelRightInfo.txt ")
    with open("BezelRightInfo.txt", "w") as Infof:
        Infof.write("File : SphereRightInfo.txt (in [mm]) \n")
        Infof.write("D material (bezel) depth "+str(format(D, '.2f')+"\n"))
        Infof.write("Lenght                   "+str(format(L, '.2f')+"\n"))
        Infof.write("Material thickness       "+str(format(M, '.2f')+"\n"))
        Infof.write("Tool diameter            "+str(format(T, '.2f')+"\n"))
        Infof.write("Tool active length       "+str(format(Ta, '.2f')+"\n"))
        Infof.write("Vertical steps           "+str(format(DZ, '.2f')+"\n"))
        Infof.write("Origin X                 "+str(format(Xorg, '.2f')+"\n"))
        Infof.write("Origin Y                 "+str(format(Xorg, '.2f')+"\n"))
    Infof.close()


GCodefile = "BezelRight60.nc" 
        
print("GCode data to file: "+GCodefile ) 
with open(GCodefile, "w") as GCodefout:
    GCodefout.write(BeginGcode) 
    # define the outer loop with depth steps -Z 
    Z = -DZ  # starting depth 
    while Z >= -D:
          # ---------------------------------------------------------
          # define the inner loop with at Xs until Xe
         X= Xs
         while X <= Xe:
              # -----------------------------------------------------
              # Gcode : Go to start position Xs,0
              Xc = str(format(X, '.2f')) 
              print ("Z : ", format(Z, '.3f'),"X : "+Xc)
              BGCode = "G0 F1000 X"+Xc+" Y"+yorg+" Z1.00\n"
              GCodefout.write(BGCode)
              # Move tool down to Z 
              Zc = str(format(Z, '.2f'))
              LGCode = "G1 F20 Z"+Zc+"\n"
              GCodefout.write(LGCode)
              # Gcode : Mill a line at Xs from y=0 to y=L
              LGCode = "G1 F200 X"+Xc+" Y"+Ls+ " Z"+Zc+ "\n" 
              GCodefout.write(LGCode)
              GCodefout.write(SafeMoveGcode)
              X= X + 0.9 * Xo  # add tooldiameter          
              # -----------------------------------------------------
         Z = -DZ + Z
         Xs = Xs + DX
         GCodefout.write(SafeMoveGcode)
    # ---------------------------------------------------------
    print("Appending end code to file: "+GCodefile)
    with open(GCodefile, "a+") as GCfout:
        GCodefout.write(EndGcode)  
GCodefout.close()
writeinfo()
print("End")