# Script for CNC GCode basic shapes in Python 
 Python Script for CNC GCode for spherical cap

The programs have a graphical user interface (GUI) to set parameters such as:
Origin X,Y ( in mm)
Width Length rsdius Toolsize etc.

For a sphere you may want to run the program twice:
1) coarse milling using a large flat tool ( see photo)
2) Fine milling using a small ball shaped tool. 

There s a Windows executable available ( *.exe).
The program creates a GCode file ( *.nc) and an information file (*.txt). Make subdirectory CNC in the directory where slope.exe is placed.
Before you send the GCode to your machine I recommend to use NCViewer to check the GCode toolpath of the generated file (https://NCViewer.com)
If you want to set other parameters then available in the GUI you may download the Python code and modify and run it for your needs.    