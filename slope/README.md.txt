# Script for CNC GCode basic shapes in Python 
 Python Script for CNC GCode for a slope

There s a Windows executable available ( *.exe).

The programs have a graphical user interface (GUI) to set parameters such as:
Origin X,Y ( in mm)
Width Length depth depthstep Toolsize etc.

Run SphereCap.exe
Fill in parameters and submit

- The program creates two  GCode file ( *.nc) one for coarse the other for fine milling and an information file (*.txt). 
- Make subdirectory CNC in the directory where SphereCap.exe is placed.
- Before you send the GCode to your machine I recommend to use NCViewer to check the GCode toolpath of the generated file (https://NCViewer.com)
- If you want to set other parameters then available in the GUI you may download the Python code and modify and run it for your needs.    