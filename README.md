# Python-code-for-generation-Gcode-for-CNC-milling-

This repository holds some python scripts for controlling CNC machines. 
 The Pythons scripts generate GCode for carving simple 3D structures
A graphical user interface is present to set the input parameters.
The file generates files with Gcode for CNC control software such as Candle or Openboards 

1) 60degree  V-Grooves with adjustable length and depth
2) 60 bezels with adjustable length and depth
3) Spherical caps with adjustable heigth and radius
4) Slope ( Y,Z direction)
5) Pockets

Most programs have a graphical user interface (GUI) to set parameters such as:
Origin X,Y ( in mm) Width Length Depth Toolsize etc.

For each program there is a Windows executable available ( *.exe).
The programs create a GCode file ( *.nc) and an information file (*.txt).
Before you send the GCode to your machine I recommend to use NCViewer to check the GCode toolpath of the generated file (https://NCViewer.com)
If you want to set other parameters then available in the GUI you may download the Python code and modify and run it for your needs.  

Please be aware that I am not a Python programmer ! Python is just a tool to use for my 
CNC carving hobby. I use a 4030 Genmitsu ProVerXL.
Documentation wili be added here soon.
Februari 2023 Ger de Graaf
