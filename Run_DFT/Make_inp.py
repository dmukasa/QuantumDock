import sys
import subprocess as sp
import re

def Make_inp(FILENAME,functional,basis,WD):
    """ Function to make FILENAME_functional_basis.inp from FILENAME.xyz:

        FILENAME: The afforementioned FILENAME, typically target.xyz,
        monomer.xyz, or complex.xyz

        functional: Any functional from the ORCA manual: NOTE, FUNCTIONAL CANNOT HAVE SPACES IN THE NAME
        ELSE IT WILL BE CONFUSED THE THE BASIS SET

        basis: Any basis set from the ORCA manual

        WD: The working directory path containing FILENAME.xyz
        For math path/to/current/directory
        no slash at the end
    """
####################################################################################################
    if functional == "B3LYP_D3BJ": 
        INP_commands = """! """
        INP_commands += "B3LYP D3BJ"
        INP_commands += " " + basis + " "
        INP_commands += "OPT"
        INP_commands += """
%geom
MaxIter 1000000
end

%scf
MaxIter 1000000
end"""

        INP_commands += """

* xyzfile 0 1"""
        INP_commands += " " + FILENAME + ".xyz"
        INP_commands += """
%pal nprocs 20
end"""
        #make a new file for the input (NOTE: WE NEED AN EXEDPTION FOR B3LYP/G)
        inp_path = WD + "/" + FILENAME + "_" + functional + ".inp"
####################################################################################################
    elif functional == "M062X_D3BJ":
        INP_commands = """! """
        INP_commands += "M062X D3BJ"
        INP_commands += " " + basis + " "
        INP_commands += "OPT"
        INP_commands += """
%geom
MaxIter 1000000
end

%scf
MaxIter 1000000
SOSCFStart 0.00033 # Default value of orbital gradient is 0.0033. Here reduced by a factor of 10.
end"""

        INP_commands += """

* xyzfile 0 1"""
        INP_commands += " " + FILENAME + ".xyz"
        INP_commands += """
%pal nprocs 20
end"""
        inp_path = WD + "/" + FILENAME + "_" + functional + ".inp"
####################################################################################################
    elif functional == "B3LYP-gCP-D3":
        INP_commands = """! """
        INP_commands += functional + "/6-31G* "
        INP_commands += "OPT"
        INP_commands += """
%geom
MaxIter 1000000
end

%scf
MaxIter 1000000
SOSCFStart 0.00033 # Default value of orbital gradient is 0.0033. Here reduced by a factor of 10.
end"""

        INP_commands += """

* xyzfile 0 1"""
        INP_commands += " " + FILENAME + ".xyz"
        INP_commands += """
%pal nprocs 20
end"""

        inp_path = WD + "/" + FILENAME + "_" + functional + ".inp"
    else:
        INP_commands = """! """
        INP_commands += functional
        INP_commands += " " + basis + " "
        INP_commands += "OPT"
        INP_commands += """
%geom
MaxIter 1000000
end

%scf
MaxIter 1000000
SOSCFStart 0.00033 # Default value of orbital gradient is 0.0033. Here reduced by a factor of 10.
end"""

        INP_commands += """

* xyzfile 0 1"""
        INP_commands += " " + FILENAME + ".xyz"
        INP_commands += """
%pal nprocs 20
end"""
        #make a new file for the input (NOTE: WE NEED AN EXEDPTION FOR B3LYP/G)
        if functional == "B3LYP/G":
            inp_path = WD + "/" + FILENAME + "_B3LYP-G" + ".inp"
        else:
            inp_path = WD + "/" + FILENAME + "_" + functional + ".inp"
####################################################################################################
    input = open(inp_path, "w")
    #write the coordinates in it
    input.write(INP_commands)
    #Save the file
    input.close()

Make_inp(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
