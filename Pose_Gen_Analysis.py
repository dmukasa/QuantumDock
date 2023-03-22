import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from operator import itemgetter
import subprocess as sp
from subprocess import check_output

def H_kJ_mol(E):
    """Converts Hartree to Kj/mol"""
    return E*27.211*96.485 #kJ/mol

def plot_energy(PATHNAME):
    name = PATHNAME
    fo = open(name, "r")
    lines = fo.readlines()
    fo.close()
    # ------------------------------------------ #


    # -------------- EXTRACT INFO -------------- #	
#     print(lines[2])	

    if re.search(" O   R   C   A ", lines[2]):
        #print('this is an orca output')
        we_continue = True
    else :
        print('dunno this output format!')
        we_continue = False


    if we_continue:
        Energy = 0
        for line in lines:
            if re.search("FINAL SINGLE POINT ENERGY", line):
                Energy = H_kJ_mol(float(line.split()[4]))
    if Energy ==0:
        Energy = np.nan
    return Energy

def main(MIPNET_OUT,TAR, MONO):
    #Find number of complexes there are
    Complex_count = 0

    dir = MIPNET_OUT 
    lst_dir = os.listdir(dir)
    #lst_dir.remove('.DS_Store')
    Complex_count = len(lst_dir)
    
    #Make final dictionary
    #This dictionary will cosist of the complex file name 
    #(PHE_mono_num) and the calculated geometrically converged energy
    
    E_array = np.array([["Complex","Energy"]], dtype=object)
    for i in range(1, Complex_count + 1):
        new_entry = TAR + "_" + MONO + "_" + str(i)
        Complex_Path = MIPNET_OUT + "/" + TAR + "_" + MONO + "_" + str(i) + "/" + TAR + "_" + MONO + ".out"

        #only calculate the confomer energy, the lowest is the most stable the other two variables are constants
        E_complex = plot_energy(Complex_Path)
        E_array = np.append(E_array, np.array([[new_entry, E_complex]], dtype=object), axis=0)

    
    #Remove the title line from the array
    E_array = E_array[1:,:]

    #Sort the array with the most negative energy up top
    Sorted_E_array = E_array[np.argsort(E_array[:,1])]

    #Only keep the top 20 stable conformations, save their names in a csv
    Keep_E_array = Sorted_E_array[:20,0]

    #Delete all files except those in Sorted_array
    #First make sure your in the right directory and make a new directory "Complex"
    command = """cd """ + MIPNET_OUT + """; mkdir Complex ;"""
 
    #Now move all the files in Keep_E_array to Complex
    for file in Keep_E_array:
        command += """mv """ + MIPNET_OUT + """/""" + str(file) + """ """ + MIPNET_OUT + """/""" + """Complex ;"""
    
    #First make sure your in the right directory
    command += """cd """ + MIPNET_OUT + """ ;"""

    #Now delete all the directories except Complex and it contents
    #####CURRENTLY COMMENTED OUT TO KEEP ALL DATA (i.e. Keeping data for publication)#####
    #Delete_E_array = Sorted_E_array[20:,0]

    #for file in Delete_E_array:
    #    command += """rm -r """ + str(file) + """; """

    #Go into Complex and Rename all the files 1-N arbitrarily
    command += """cd """ + MIPNET_OUT + """/Complex ;"""
   
    #Rename a temperary name to avoid overlap
    for i in range(len(Keep_E_array)):
        command += """mv """ + str(Keep_E_array[i]) + """ """ + TAR + """_""" + MONO + """_""" + str(i+1) + """_TMP ;"""
  

    #Execute command
    #print(command)
    proc = sp.Popen(args=command, shell=True)
    #wait for this command to finish
    proc.wait()

     
main(sys.argv[1], sys.argv[2], sys.argv[3])    

