import sys
import subprocess as sp
import re


def Make_Semi_inp(FILENAME,functional, WD):
    """ Function to make FILENAME.inp from FILENAME.pdb:

        FILENAME: The afforementioned FILENAME, typically target.pdb,
        monomer.pdb, or complex.pdb

        functional: Any functional from the ORCA manual

        WD: The working directory path containing FILENAME.pdb
        For math path/to/current/directory
        no slash at the end
    """
    #####FOR OPTIMIZATION#####
    #INP_commands = """! OPT """
    #INP_commands += functional + """ """
    #INP_commands += """LOOSEOPT SLOPPYSCF NOMULLIKEN NOLOEWDIN NOMAYER XYZFILE"""

    #####FOR SINGLE POINT#####
    INP_commands = """! SP """
    INP_commands += functional + """ """
    INP_commands += """SLOPPYSCF NOMULLIKEN NOLOEWDIN NOMAYER XYZFILE"""

    INP_commands += """

* pdbfile 0 1"""
    INP_commands += """ """ + FILENAME + """.pdb\n""" 

    inp_path = WD + """/""" + FILENAME + """.inp"""

    input = open(inp_path, "w")
    #write the coordinates in it
    input.write(INP_commands)
    #Save the file
    input.close()


Make_Semi_inp(sys.argv[1], sys.argv[2], sys.argv[3])
