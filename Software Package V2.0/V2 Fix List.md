Incorporated the new load cell curve fit

fixed a taring issue: changed from setting the current value to the tare value to assigning adding the current load to the tare value 

Control_Settings.py is now a class, this will avoid the settings file being read every time that a the load cell value needs converted

Added a matrix math file that can be used to solve for a 3rd order polynomial given 4 sets of data points