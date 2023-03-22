import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

def H_kJ_mol(E):
    """Converts Hartree to kJ/mol"""
    return E*27.211*96.485 #kJ/mol

def plot_energy(PATHNAME, min_val = False, info = True):
    name = PATHNAME
    fo = open(name, "r")
    lines = fo.readlines()
    fo.close()
    # ------------------------------------------ #


    # -------------- EXTRACT INFO -------------- #	

    if re.search(" O   R   C   A ", lines[2]):
        we_continue = True
    else :
        we_continue = False
    if we_continue:
        Energy = []
        for line in lines:
            if re.search("FINAL SINGLE POINT ENERGY",line):
                temp = line.split()[4]
                Energy.append(temp)
    # convert string to float
        Energy=[(lambda x: float(x))(x) for x in Energy]
    # Make note of error (i.e. calculation not finishing)
    if len(Energy)==0 or len(Energy)==1:
        print("ERROR IN ", PATHNAME.split('/')[-2:])
        return 0
    else:
        diff_E = np.zeros(len(Energy)-1)
        for i in range(len(Energy)-1):
            diff_E[i] = np.abs(Energy[i+1])-np.abs(Energy[i])
    
        index = np.argmax(diff_E)+1
        Energy = Energy[index:]
        
    Energy = H_kJ_mol(np.array(Energy))
    if info == True: 
        if Energy != []:
            plt.figure()
            plt.title("Energy Convergence")
            plt.plot(np.arange(len(Energy)), Energy)
            plt.scatter(np.arange(len(Energy)), Energy)
            plt.show()

        print('Converged energy = ', Energy[-1],'kJ/mol')#np.around(Energy[-1],3),'kJ/mol')
        print('Minimum energy = ', min(Energy),'kJ/mol')#np.around(min(Energy),3),'kJ/mol')
        print('Diffrence = ', np.abs(Energy[-1]-min(Energy)),'kJ/mol')
        if min_val == False:
            return Energy[-1]
        else:
            return min(Energy)
    else:
        if min_val == False:
            return Energy[-1]
        else:
            return min(Energy)

def main(MIPNET_OUT, TAR, MONO):
    #Find number of complexes there are for each bond type
    dir = MIPNET_OUT + "/Complex"
    lst_dir = os.listdir(dir)
    #lst_dir.remove('.DS_Store') #incase of file errors
    Complex_count = len(lst_dir)
      
    #Make final dictionary
    #This dictionary will cosist of the complex file name 
    #(Tar_mono_num) and the calculated geometrically converged energy
    
    dict = {}
    for i in range(1, Complex_count + 1):
        new_entry = TAR + "_" + MONO + "_" + str(i)
        Complex_Path = MIPNET_OUT + "/Complex/" + TAR + "_" + MONO + "_" + str(i) + "/" + TAR + "_" + MONO + "_" + "B3LYP_D3BJ" + ".out"
        Mono_Path = MIPNET_OUT + "/Monomer/" + MONO + "/" + MONO + "_" + "B3LYP_D3BJ" + ".out"
        Tar_Path = MIPNET_OUT + "/Target/" + TAR + "/" + TAR + "_" + "B3LYP_D3BJ" + ".out"

        E_Mono = plot_energy(Mono_Path, min_val = False, info = False)
        E_Tar = plot_energy(Tar_Path, min_val = False, info = False)
        E_Complex = plot_energy(Complex_Path, min_val = False, info = False)
        dict.update({new_entry: E_Complex - (E_Tar + E_Mono)})
    
    #General Monomer    
    print(TAR + " " + MONO)
    molecule_PHE_lst = []
    for entry in dict:
        molecule_PHE_lst.append(dict[entry])
        print(entry, dict[entry])
    PHE_min = min(molecule_PHE_lst)
    print(TAR + "-" + MONO + " min =", PHE_min)


    print("")
    print("")
    print("")

    print("-----------------------------")


    
main("/Volumes/MIP_DESIGN/2-18-2023/batch1-DOP/DOP-MAA","DOP", "MAA")

