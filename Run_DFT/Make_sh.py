import sys
import subprocess as sp
import re

def Make_sh(FILENAME, functional, WD):
    """ Function to make FILENAME_functional_basis.inp from FILENAME.xyz:

        FILENAME: The FILENAME for the .inp file
        the sh file will refrence, typically target.inp,
        monomer.inp, or complex.inp

        WD: The working directory path containing FILENAME.xyz
        For math path/to/current/directory
        no slash at the end
    """
    SLURM_commands = """#!/bin/bash

# Submit this script with: sbatch <this-filename>

#SBATCH --time=99:00:00   # walltime
#SBATCH --ntasks=20   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10G   # memory per CPU core, 20 recommended
#SBATCH -J """
    SLURM_commands += """\"""" + FILENAME + """\" # job name """

    SLURM_commands += """"
#SBATCH --mail-user=dmukasa@caltech.edu   # email address


# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE

module load openmpi/2.1.6

# RUN ORCA FILE
/home/dmukasa/orca/orca_4_2_1_linux_x86-64_openmpi216/orca """
    if functional == "B3LYP/G":
        SLURM_commands += FILENAME + "_" + "B3LYP-G" + ".inp > "
        SLURM_commands += FILENAME + "_" + "B3LYP-G" + ".out"
    else:
        SLURM_commands += FILENAME + "_" + functional + ".inp > "
        SLURM_commands += FILENAME + "_" + functional + ".out"


    #make a new file for the .sh
    sh_path = WD + "/" + FILENAME + ".sh"
    sh = open(sh_path, "w")
    #write the coordinates in it
    sh.write(SLURM_commands)
    #Save the file
    sh.close()

Make_sh(sys.argv[1], sys.argv[2], sys.argv[3])
